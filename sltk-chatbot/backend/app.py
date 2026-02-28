"""
SLTK Upload Chatbot - Flask API (Runs on IBM i)
Real-time monitoring for SLTK upload groups
"""

import os
import sys
import time
from datetime import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO, emit, join_room, leave_room
import threading

# Check if pandas is available (optional - for Excel processing)
PANDAS_AVAILABLE = False
try:
    import pandas as pd
    PANDAS_AVAILABLE = True
    print("✅ SUCCESS: Pandas imported successfully")
except ImportError as e:
    print(f"⚠️  WARNING: pandas not available: {e}")
    print("   Excel upload feature will be limited")
    print("   To install: yum install python313-pandas")
    # Try openpyxl as fallback
    try:
        from openpyxl import load_workbook, Workbook
        print("✅ Using openpyxl as fallback for Excel processing")
    except ImportError:
        print("⚠️  openpyxl also not available")

# Check if pyodbc is available for DB2 access (optional - for database features)
PYODBC_AVAILABLE = False
try:
    import pyodbc
    PYODBC_AVAILABLE = True
    print("✅ SUCCESS: pyodbc imported successfully")
except ImportError as e:
    print(f"⚠️  WARNING: pyodbc not available: {e}")
    print("   Database features will be disabled")
    print("   To install: yum install python313-pyodbc")
    print("   App will run in limited mode without database access")

# --- Configuration ---
DROPBOX_ROOT = '/sltk/dropbox'  # Root SLTK dropbox folder
DROPBOX_FOLDER_POC = '/HOME/VIJAYVERMA'  # POC folder (fallback)
SLTK_LIBRARY = 'ASHLEY'  # SLTK library
HOST_IP = '0.0.0.0'  # Network access
PORT = 44001  # IBM i API port
POLL_INTERVAL = 2  # Poll every 2 seconds

# --- Initialize Flask App ---
app = Flask(__name__)
app.config['SECRET_KEY'] = 'sltk-secret-key-change-in-production'
CORS(app, resources={r"/*": {"origins": "*"}})
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')

# --- Database Connection ---
db_connection = None
active_monitors = {}  # groupId -> thread

def get_db_connection():
    """Get IBM i DB2 connection"""
    global db_connection

    if not PYODBC_AVAILABLE:
        raise RuntimeError("pyodbc is not available - database features are disabled")

    if db_connection is None:
        try:
            # IBM i ODBC connection string
            connection_string = (
                "DRIVER={IBM i Access ODBC Driver};"
                "SYSTEM=localhost;"  # Change if needed
                "DATABASE=ASHLEY;"
                "UID=VIJAYVERMA;"  # Change to your user
                "PWD=COSTARIC1;"  # Change to your password
            )
            db_connection = pyodbc.connect(connection_string)
            print("✅ SUCCESS: Database connection established")
        except Exception as e:
            print(f"❌ ERROR: Database connection failed: {e}")
            raise
    return db_connection

def query_db(sql, params=None):
    """Execute SQL query and return results"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        if params:
            cursor.execute(sql, params)
        else:
            cursor.execute(sql)
        
        # Get column names
        columns = [column[0] for column in cursor.description]
        
        # Fetch all rows
        rows = cursor.fetchall()
        
        # Convert to list of dicts
        results = []
        for row in rows:
            results.append(dict(zip(columns, row)))
        
        cursor.close()
        return results
    except Exception as e:
        print(f"ERROR: Query failed: {e}")
        raise

# --- SLTK Dropbox Helper Functions ---

def get_available_loads():
    """
    Get list of available SLTK Load IDs from SLTKLOD table
    """
    try:
        cursor = get_db_connection().cursor()
        query = f"SELECT ZFLOAD, ZFLDTX FROM {SLTK_LIBRARY}.SLTKLOD WHERE ZFAVST = '0' ORDER BY ZFLOAD"
        cursor.execute(query)

        loads = []
        for row in cursor.fetchall():
            loads.append({
                "load_id": row[0].strip(),
                "description": row[1].strip()
            })

        cursor.close()
        return loads
    except Exception as e:
        print(f"ERROR: Failed to get loads: {e}")
        return []

def get_dropbox_folder(load_id=None, filename=None):
    """
    Dynamically determine dropbox folder based on Load ID or filename

    Priority:
    1. If load_id provided, use /sltk/dropbox/{load_id}/
    2. If filename matches pattern {LOAD}_*.xlsx, extract load_id
    3. Fallback to POC folder
    """
    # Option 1: Load ID provided explicitly
    if load_id:
        dropbox_path = os.path.join(DROPBOX_ROOT, load_id.strip().upper())
        if os.path.exists(dropbox_path):
            return dropbox_path
        else:
            print(f"WARNING: Dropbox folder not found: {dropbox_path}")
            # Try to create it
            try:
                os.makedirs(dropbox_path, exist_ok=True)
                print(f"SUCCESS: Created dropbox folder: {dropbox_path}")
                return dropbox_path
            except Exception as e:
                print(f"ERROR: Cannot create dropbox folder: {e}")

    # Option 2: Extract Load ID from filename pattern
    if filename:
        # Try pattern: LOADID_description.xlsx
        parts = filename.split('_')
        if len(parts) > 0:
            potential_load = parts[0].upper()
            dropbox_path = os.path.join(DROPBOX_ROOT, potential_load)
            if os.path.exists(dropbox_path):
                print(f"INFO: Detected Load ID '{potential_load}' from filename")
                return dropbox_path

    # Option 3: Fallback to POC folder
    print(f"INFO: Using POC dropbox folder: {DROPBOX_FOLDER_POC}")
    return DROPBOX_FOLDER_POC

def scan_dropbox_folders():
    """
    Scan IFS root dropbox folder and return list of available folders
    """
    try:
        if os.path.exists(DROPBOX_ROOT):
            folders = [f for f in os.listdir(DROPBOX_ROOT)
                      if os.path.isdir(os.path.join(DROPBOX_ROOT, f))]
            return sorted(folders)
        else:
            print(f"WARNING: Dropbox root not found: {DROPBOX_ROOT}")
            return []
    except Exception as e:
        print(f"ERROR: Cannot scan dropbox folders: {e}")
        return []

# --- Helper Functions ---
def get_status_text(status):
    """Convert status code to human-readable text"""
    status_map = {
        'P': 'Preparing',
        'R': 'Ready',
        'O': 'Processing',
        'X': 'Success',
        'E': 'Error',
        'C': 'Cancelled',
        'V': 'Validation Error'
    }
    return status_map.get(status.strip(), 'Unknown')

def get_group_status(group_id):
    """Get current status of a SLTK group"""
    try:
        # Get group information
        group_query = f"""
            SELECT 
                ZGGPID as groupId,
                ZGGPDS as description,
                ZGGPST as status,
                ZGCHDT as changeDate,
                ZGCHTM as changeTime,
                ZGUSER as user
            FROM {SLTK_LIBRARY}.SLTKGRP
            WHERE ZGGPID = ?
        """
        
        group_result = query_db(group_query, [group_id])
        
        if not group_result:
            return None
        
        group = group_result[0]
        
        # Get transaction counts
        progress_query = f"""
            SELECT 
                COUNT(*) as total,
                SUM(CASE WHEN ZTSYST = 'X' THEN 1 ELSE 0 END) as completed,
                SUM(CASE WHEN ZTSYST = 'E' THEN 1 ELSE 0 END) as errors,
                SUM(CASE WHEN ZTSYST = 'O' THEN 1 ELSE 0 END) as processing,
                SUM(CASE WHEN ZTSYST = 'P' THEN 1 ELSE 0 END) as pending
            FROM {SLTK_LIBRARY}.SLTKTRN
            WHERE ZTGPID = ?
        """
        
        progress_result = query_db(progress_query, [group_id])
        progress = progress_result[0] if progress_result else {}
        
        total = progress.get('total', 0) or 0
        completed = progress.get('completed', 0) or 0
        percentage = round((completed / total) * 100) if total > 0 else 0
        
        return {
            'groupId': group['groupId'].strip(),
            'description': group['description'].strip(),
            'status': group['status'].strip(),
            'statusText': get_status_text(group['status']),
            'changeDate': group['changeDate'],
            'changeTime': group['changeTime'],
            'user': group['user'].strip(),
            'progress': {
                'total': total,
                'completed': completed,
                'errors': progress.get('errors', 0) or 0,
                'processing': progress.get('processing', 0) or 0,
                'pending': progress.get('pending', 0) or 0,
                'percentage': percentage
            },
            'timestamp': datetime.now().isoformat()
        }
    except Exception as e:
        print(f"ERROR: get_group_status failed: {e}")
        raise

def get_errors(group_id):
    """Get errors for a SLTK group"""
    try:
        errors_query = f"""
            SELECT
                t.ZTTKEN as token,
                t.ZTSEQ as sequence,
                t.ZTSYST as status,
                e.ZTMSGF as messageFile,
                e.ZTMSGI as messageId,
                e.ZTMSGD as messageData,
                e.ZTMSGT as messageText
            FROM {SLTK_LIBRARY}.SLTKTRN t
            LEFT JOIN {SLTK_LIBRARY}.SLTKERR e ON t.ZTTKEN = e.ZTTKEN
            WHERE t.ZTGPID = ? AND t.ZTSYST = 'E'
            ORDER BY t.ZTSEQ
        """

        errors = query_db(errors_query, [group_id])

        # Format errors with resolution guidance
        formatted_errors = []
        for err in errors:
            msg_id = err.get('messageId', '').strip() if err.get('messageId') else None
            formatted_errors.append({
                'token': err['token'].strip(),
                'sequence': err['sequence'],
                'status': err['status'].strip(),
                'messageFile': err.get('messageFile', '').strip() if err.get('messageFile') else None,
                'messageId': msg_id,
                'messageData': err.get('messageData', '').strip() if err.get('messageData') else None,
                'messageText': err.get('messageText', '').strip() if err.get('messageText') else None,
                'resolution': get_error_resolution(msg_id)
            })

        return formatted_errors
    except Exception as e:
        print(f"ERROR: get_errors failed: {e}")
        raise

def get_error_resolution(message_id):
    """Get resolution guidance for error codes"""
    resolutions = {
        'XML0021': {
            'issue': 'Object not found',
            'fix': 'Check object name spelling in spreadsheet. Verify object exists in SLTKOBJ table.',
            'sql': 'SELECT * FROM SLTKOBJ WHERE ZONAME = \'<object_name>\''
        },
        'XML0141': {
            'issue': 'Profile handle error',
            'fix': 'Verify user profile exists and has proper authority. Contact system administrator.',
            'sql': None
        },
        'XML0161': {
            'issue': 'No transactions found in spreadsheet',
            'fix': 'Check that spreadsheet has data rows. Verify worksheet name matches configuration.',
            'sql': 'SELECT * FROM SLTKSNU WHERE Z8LOAD = \'<load_name>\''
        },
        'XML0162': {
            'issue': 'Worksheet not found',
            'fix': 'Verify worksheet name in spreadsheet matches SLTKSNU configuration.',
            'sql': 'SELECT * FROM SLTKSNU WHERE Z8LOAD = \'<load_name>\''
        },
        'XML0163': {
            'issue': 'Worksheet processed (informational)',
            'fix': 'No action needed - this is an informational message.',
            'sql': None
        }
    }

    return resolutions.get(message_id, {
        'issue': 'Unknown error',
        'fix': 'Review error message and contact support if needed.',
        'sql': None
    })

# --- API Endpoints ---

@app.route('/', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "running",
        "message": "SLTK Monitor API is operational",
        "timestamp": datetime.now().isoformat(),
        "endpoints": [
            "/",
            "/api/loads",
            "/upload/excel",
            "/api/status/<groupId>",
            "/api/errors/<groupId>",
            "/api/history"
        ]
    }), 200

@app.route('/api/loads', methods=['GET'])
def get_loads():
    """Get list of available SLTK Load IDs"""
    try:
        # Try to get from SLTKLOD table
        loads = get_available_loads()

        # If database query fails, try scanning IFS folders
        if not loads:
            folders = scan_dropbox_folders()
            loads = [{"load_id": f, "description": f"Dropbox folder: {f}"} for f in folders]

        return jsonify({
            "status": "success",
            "loads": loads,
            "count": len(loads)
        }), 200
    except Exception as e:
        print(f"ERROR: Failed to get loads: {e}")
        return jsonify({
            "status": "error",
            "message": str(e),
            "loads": []
        }), 500

@app.route('/upload/excel', methods=['POST'])
def upload_excel_file():
    """Upload Excel file to IFS folder for SLTK processing"""
    try:
        if 'excel_file' not in request.files:
            return jsonify({"status": "error", "message": "No file part found in request"}), 400

        file = request.files['excel_file']

        if file.filename == '':
            return jsonify({"status": "error", "message": "No file selected for uploading"}), 400

        # Get Load ID from request (optional)
        load_id = request.form.get('load_id', None)

        # Dynamically determine dropbox folder
        dropbox_folder = get_dropbox_folder(load_id=load_id, filename=file.filename)

        print(f"INFO: Using dropbox folder: {dropbox_folder}")
        print(f"INFO: Load ID: {load_id if load_id else 'Auto-detected from filename'}")

        # Create folder if needed
        try:
            os.makedirs(dropbox_folder, exist_ok=True)
            print(f"SUCCESS: Directory verified: {dropbox_folder}")
        except Exception as folder_error:
            return jsonify({"status": "error", "message": f"Cannot create folder: {folder_error}"}), 500

        # Save file to IFS folder
        output_path = os.path.join(dropbox_folder, file.filename)

        if PANDAS_AVAILABLE:
            # Use pandas to read and add timestamp
            df = pd.read_excel(file.stream, engine='openpyxl')
            df['IBMi_Process_Timestamp'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            df.to_excel(output_path, index=False, engine='openpyxl')
            print(f"✅ SUCCESS: File processed with pandas and saved to {output_path}")
        else:
            # Fallback: Just save the file as-is
            file.save(output_path)
            print(f"✅ SUCCESS: File saved to {output_path} (without pandas processing)")
            print(f"⚠️  WARNING: Timestamp column not added (pandas not available)")

        print(f"INFO: SLTKDRP will process this file automatically")

        return jsonify({
            "status": "success",
            "message": f"File '{file.filename}' uploaded successfully. SLTKDRP will process it automatically.",
            "server_path": output_path,
            "next_steps": "Monitor the upload using /api/status/<groupId> endpoint"
        }), 200

    except Exception as e:
        print(f"ERROR: upload_excel_file failed: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/status/<group_id>', methods=['GET'])
def get_status(group_id):
    """Get current status of a SLTK group"""
    try:
        if not PYODBC_AVAILABLE:
            return jsonify({
                "success": False,
                "error": "Database not available",
                "message": "pyodbc is not installed - database features are disabled"
            }), 503

        status = get_group_status(group_id)

        if not status:
            return jsonify({
                "success": False,
                "error": "Group not found",
                "message": f"Group {group_id} does not exist"
            }), 404

        return jsonify({
            "success": True,
            "data": status
        }), 200
    except Exception as e:
        print(f"ERROR: get_status endpoint failed: {e}")
        return jsonify({
            "success": False,
            "error": "Internal server error",
            "message": str(e)
        }), 500

@app.route('/api/errors/<group_id>', methods=['GET'])
def get_errors_endpoint(group_id):
    """Get errors for a SLTK group"""
    try:
        if not PYODBC_AVAILABLE:
            return jsonify({
                "success": False,
                "error": "Database not available",
                "message": "pyodbc is not installed - database features are disabled"
            }), 503

        errors = get_errors(group_id)

        return jsonify({
            "success": True,
            "data": {
                "groupId": group_id,
                "errorCount": len(errors),
                "errors": errors
            }
        }), 200
    except Exception as e:
        print(f"ERROR: get_errors endpoint failed: {e}")
        return jsonify({
            "success": False,
            "error": "Internal server error",
            "message": str(e)
        }), 500

@app.route('/api/history', methods=['GET'])
def get_history():
    """Get SLTK upload history"""
    try:
        if not PYODBC_AVAILABLE:
            return jsonify({
                "success": False,
                "error": "Database not available",
                "message": "pyodbc is not installed - database features are disabled"
            }), 503

        user = request.args.get('user')
        status = request.args.get('status')
        from_date = request.args.get('fromDate')
        to_date = request.args.get('toDate')
        limit = int(request.args.get('limit', 50))

        # Build query
        where_conditions = []
        params = []

        if user:
            where_conditions.append('ZGUSER = ?')
            params.append(user)

        if status:
            where_conditions.append('ZGGPST = ?')
            params.append(status)

        if from_date:
            where_conditions.append('ZGCHDT >= ?')
            params.append(int(from_date))

        if to_date:
            where_conditions.append('ZGCHDT <= ?')
            params.append(int(to_date))

        where_clause = 'WHERE ' + ' AND '.join(where_conditions) if where_conditions else ''

        history_query = f"""
            SELECT
                ZGGPID as groupId,
                ZGGPDS as description,
                ZGGPST as status,
                ZGCHDT as changeDate,
                ZGCHTM as changeTime,
                ZGUSER as user
            FROM {SLTK_LIBRARY}.SLTKGRP
            {where_clause}
            ORDER BY ZGCHDT DESC, ZGCHTM DESC
            FETCH FIRST {limit} ROWS ONLY
        """

        history = query_db(history_query, params if params else None)

        # Format results
        formatted_history = []
        for record in history:
            formatted_history.append({
                'groupId': record['groupId'].strip(),
                'description': record['description'].strip(),
                'status': record['status'].strip(),
                'statusText': get_status_text(record['status']),
                'changeDate': record['changeDate'],
                'changeTime': record['changeTime'],
                'user': record['user'].strip()
            })

        return jsonify({
            "success": True,
            "data": {
                "count": len(formatted_history),
                "history": formatted_history
            }
        }), 200
    except Exception as e:
        print(f"ERROR: get_history endpoint failed: {e}")
        return jsonify({
            "success": False,
            "error": "Internal server error",
            "message": str(e)
        }), 500

# --- WebSocket Events ---

def monitor_group(group_id):
    """Background thread to monitor a SLTK group"""
    print(f"INFO: Starting monitor for group {group_id}")
    last_status = None

    while group_id in active_monitors:
        try:
            status = get_group_status(group_id)

            if not status:
                socketio.emit('error', {
                    'groupId': group_id,
                    'message': 'Group not found'
                }, room=group_id)
                break

            # Emit update if status changed
            status_changed = (
                not last_status or
                last_status['status'] != status['status'] or
                last_status['progress']['percentage'] != status['progress']['percentage']
            )

            if status_changed:
                socketio.emit('status-update', status, room=group_id)
                print(f"INFO: Status update emitted for {group_id}: {status['statusText']} - {status['progress']['percentage']}%")

            # Stop monitoring if complete or error
            if status['status'] in ['X', 'E', 'C']:
                print(f"INFO: Group {group_id} finished with status {status['status']}")
                socketio.emit('processing-complete', status, room=group_id)
                break

            last_status = status
            time.sleep(POLL_INTERVAL)

        except Exception as e:
            print(f"ERROR: Monitor thread error for {group_id}: {e}")
            socketio.emit('error', {
                'groupId': group_id,
                'message': 'Monitoring error',
                'error': str(e)
            }, room=group_id)
            break

    # Cleanup
    if group_id in active_monitors:
        del active_monitors[group_id]
    print(f"INFO: Stopped monitoring group {group_id}")

@socketio.on('connect')
def handle_connect():
    """Handle client connection"""
    print(f"INFO: Client connected: {request.sid}")
    emit('connected', {'message': 'Connected to SLTK Monitor'})

@socketio.on('disconnect')
def handle_disconnect():
    """Handle client disconnection"""
    print(f"INFO: Client disconnected: {request.sid}")

@socketio.on('monitor')
def handle_monitor(group_id):
    """Start monitoring a SLTK group"""
    print(f"INFO: Client {request.sid} requested monitoring for group {group_id}")

    # Join room for this group
    join_room(group_id)

    # Send initial status
    try:
        status = get_group_status(group_id)
        if status:
            emit('status-update', status)
        else:
            emit('error', {'message': f'Group {group_id} not found'})
            return
    except Exception as e:
        emit('error', {'message': f'Error getting status: {str(e)}'})
        return

    # Start monitoring thread if not already running
    if group_id not in active_monitors:
        monitor_thread = threading.Thread(target=monitor_group, args=(group_id,), daemon=True)
        active_monitors[group_id] = monitor_thread
        monitor_thread.start()
        print(f"INFO: Started monitoring thread for group {group_id}")
    else:
        print(f"INFO: Already monitoring group {group_id}")

@socketio.on('stop-monitor')
def handle_stop_monitor(group_id):
    """Stop monitoring a SLTK group"""
    print(f"INFO: Client {request.sid} stopped monitoring group {group_id}")
    leave_room(group_id)

# --- Start the Server ---
if __name__ == '__main__':
    print(f"\n{'='*60}")
    print(f"  SLTK Upload Chatbot - Flask API")
    print(f"{'='*60}")
    print(f"  Port: {PORT}")
    print(f"  Dropbox Root: {DROPBOX_ROOT}")
    print(f"  POC Folder: {DROPBOX_FOLDER_POC}")
    print(f"  SLTK Library: {SLTK_LIBRARY}")
    print(f"{'='*60}\n")
    print(f"  Endpoints:")
    print(f"    Health check:  http://localhost:{PORT}/")
    print(f"    Get Loads:     GET  http://localhost:{PORT}/api/loads")
    print(f"    Upload:        POST http://localhost:{PORT}/upload/excel")
    print(f"    Status:        GET  http://localhost:{PORT}/api/status/<groupId>")
    print(f"    Errors:        GET  http://localhost:{PORT}/api/errors/<groupId>")
    print(f"    History:       GET  http://localhost:{PORT}/api/history")
    print(f"    WebSocket:     ws://localhost:{PORT}/socket.io/")
    print(f"{'='*60}\n")

    # Test folder creation at startup
    try:
        os.makedirs(DROPBOX_FOLDER_POC, exist_ok=True)
        print(f"✅ POC dropbox folder verified: {DROPBOX_FOLDER_POC}")
    except Exception as e:
        print(f"⚠️  WARNING: Cannot create POC dropbox folder: {e}")

    # Test database connection
    if PYODBC_AVAILABLE:
        try:
            get_db_connection()
            print(f"✅ Database connection successful")
        except Exception as e:
            print(f"⚠️  WARNING: Database connection failed: {e}")
            print(f"   Update connection string in get_db_connection()")
    else:
        print(f"⚠️  WARNING: pyodbc not available - database features disabled")
        print(f"   Install with: yum install python313-pyodbc")

    print(f"\n🚀 Starting server...\n")

    try:
        socketio.run(app, host=HOST_IP, port=PORT, debug=True, allow_unsafe_werkzeug=True)
    except Exception as e:
        print(f"ERROR: Error starting Flask server: {e}")
        input("Press Enter to exit...")

