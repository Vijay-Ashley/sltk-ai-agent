# SLTK Upload Chatbot - Backend API

Flask API for monitoring SLTK uploads on IBM i with real-time WebSocket updates.

## Features

✅ **File Upload** - Upload Excel files to IFS folder  
✅ **Real-Time Monitoring** - WebSocket-based live status updates  
✅ **Error Retrieval** - Get detailed errors with resolution guidance  
✅ **Upload History** - Query past uploads with filtering  
✅ **Progress Tracking** - Track transaction processing percentage  

## Installation on IBM i

### 1. Install Python Packages

```bash
# Using pip
pip install -r requirements.txt

# Or install individually
pip install Flask Flask-CORS Flask-SocketIO pandas openpyxl pyodbc
```

### 2. Configure Database Connection

Edit `app.py` line 51-57:

```python
connection_string = (
    "DRIVER={IBM i Access ODBC Driver};"
    "SYSTEM=localhost;"  # Your IBM i system name
    "DATABASE=ACTLIBDB;"
    "UID=your_user;"     # Your IBM i user
    "PWD=your_password;" # Your IBM i password
)
```

### 3. Configure Dropbox Folder

Edit `app.py` line 35:

```python
DROPBOX_FOLDER = '/HOME/VIJAYVERMA'  # Your IFS folder path
```

## Running the Server

```bash
# Start the server
python app.py

# Server will start on port 44001
# Access at: http://your-ibmi-ip:44001
```

## API Endpoints

### REST API

#### Health Check
```http
GET /
```

#### Upload Excel File
```http
POST /upload/excel
Content-Type: multipart/form-data

Body: excel_file=<file>
```

#### Get Status
```http
GET /api/status/<groupId>
```

**Response:**
```json
{
  "success": true,
  "data": {
    "groupId": "GRP0001234",
    "status": "O",
    "statusText": "Processing",
    "progress": {
      "total": 50,
      "completed": 25,
      "percentage": 50
    }
  }
}
```

#### Get Errors
```http
GET /api/errors/<groupId>
```

#### Get History
```http
GET /api/history?user=JSMITH&status=X&limit=20
```

### WebSocket API

```javascript
// Connect
const socket = io('http://your-ibmi-ip:44001');

// Monitor group
socket.emit('monitor', 'GRP0001234');

// Listen for updates
socket.on('status-update', (status) => {
  console.log('Status:', status);
});

socket.on('processing-complete', (status) => {
  console.log('Complete:', status);
});

// Stop monitoring
socket.emit('stop-monitor', 'GRP0001234');
```

## Status Codes

| Code | Status | Description |
|------|--------|-------------|
| P | Preparing | Spreadsheet being parsed |
| R | Ready | Ready to process |
| O | Processing | Transactions being processed |
| X | Success | All transactions completed |
| E | Error | Errors occurred |
| C | Cancelled | Upload cancelled |

## Troubleshooting

### Database Connection Error

```
ERROR: Database connection failed
```

**Fix:** Update connection string with correct credentials

### Permission Denied on IFS Folder

```
ERROR: Permission denied: Cannot access /HOME/VIJAYVERMA
```

**Fix:** Create folder and set permissions:
```bash
mkdir /HOME/VIJAYVERMA
chmod 777 /HOME/VIJAYVERMA
```

### Port Already in Use

```
ERROR: Address already in use
```

**Fix:** Change PORT in app.py or kill existing process

## License

ISC - Ashley Furniture Industries, Inc.

