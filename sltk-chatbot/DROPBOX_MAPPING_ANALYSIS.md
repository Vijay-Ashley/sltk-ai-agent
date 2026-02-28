# 🎯 SLTK Dropbox Folder Mapping - Dynamic Detection Analysis

## 📋 Problem Statement

**Current Issue:**  
The chatbot currently uses a hardcoded dropbox folder (`/HOME/VIJAYVERMA`) which is only for POC. In production, we need to **dynamically determine the correct IFS dropbox folder** based on the uploaded Excel file or SLTK configuration.

## 🔍 Key Findings from Code Analysis

### 1. **How SLTK Determines Dropbox Path**

From `SLTKSPR.rpgle` line 509:
```rpgle
// Spreadsheet from drop box
If zgCRPG = 'SLTKDRP';
  Path = dropBoxPath(zgLOAD:zgGPDS:zgTOFF);
  fileName = %trim(zgGPDS) + '.' + zgTOFF;
```

**Key Parameters:**
- `zgLOAD` - **Load ID** (the key to finding the dropbox folder!)
- `zgGPDS` - Group Description (filename without extension)
- `zgTOFF` - Type Offset (file extension like 'xlsx')

### 2. **The `dropBoxPath()` Function**

This function takes the **Load ID** and returns the full IFS path to the dropbox folder.

**Function Signature:**
```rpgle
dropBoxPath(loadID : filename : extension) → returns IFS path
```

### 3. **SLTKLOD Table - Load Settings**

The `SLTKLOD` table stores **load settings and configurations** including the dropbox folder path for each Load ID.

**Expected Structure:**
```sql
SLTKLOD (Load Settings)
├─ Load ID (Primary Key)
├─ Dropbox Path/Folder
├─ Pre-processing Command
├─ Post-processing Command
└─ Other settings
```

## 🎯 Solution Approaches

### **Option 1: Query SLTKLOD Table** ⭐ **RECOMMENDED**

**How it works:**
1. User uploads Excel file
2. Extract or determine the **Load ID** from:
   - Filename pattern (e.g., `MODATA_upload.xlsx` → Load ID = `MODATA`)
   - First sheet name in Excel
   - User selection from dropdown
3. Query `SLTKLOD` table to get dropbox path:
   ```sql
   SELECT dropbox_path_column 
   FROM SLTKLOD 
   WHERE load_id = 'MODATA'
   ```
4. Save file to the retrieved dropbox path

**Pros:**
- ✅ Uses existing SLTK configuration
- ✅ No hardcoding needed
- ✅ Supports all SLTK objects

**Cons:**
- ❌ Need to identify correct column name in SLTKLOD
- ❌ Need to determine Load ID from Excel file

---

### **Option 2: Query SLTKOBJ Table**

**How it works:**
1. Query `SLTKOBJ` (Object Master) table
2. Get list of all available SLTK objects and their dropbox folders
3. Match Excel file to object based on:
   - Filename
   - Sheet structure
   - Column headers

**SQL Example:**
```sql
SELECT object_name, dropbox_folder 
FROM SLTKOBJ 
WHERE object_type = 'SPREADSHEET'
```

---

### **Option 3: Scan IFS Dropbox Root Folder**

**How it works:**
1. Define root SLTK dropbox folder (e.g., `/sltk/dropbox/`)
2. List all subfolders
3. Let user select target folder from dropdown
4. Save file to selected folder

**Python Example:**
```python
import os

SLTK_ROOT = '/sltk/dropbox/'
dropbox_folders = [f for f in os.listdir(SLTK_ROOT) if os.path.isdir(os.path.join(SLTK_ROOT, f))]
# Returns: ['MODATA', 'PODATA', 'INVDATA', 'VIJAYVERMA', ...]
```

**Pros:**
- ✅ Simple to implement
- ✅ No database queries needed
- ✅ User has full control

**Cons:**
- ❌ Requires user to know correct folder
- ❌ No validation

---

### **Option 4: Filename Pattern Matching**

**How it works:**
1. Define naming convention: `{LoadID}_{description}.xlsx`
2. Extract Load ID from filename
3. Map to dropbox folder

**Example:**
```
MODATA_upload_20240228.xlsx  → Load ID = MODATA → /sltk/dropbox/MODATA/
PODATA_new_orders.xlsx       → Load ID = PODATA → /sltk/dropbox/PODATA/
```

---

## 🚀 Recommended Implementation

### **Phase 1: Immediate (Use Option 3 + 4)**

```python
# In app.py

def get_dropbox_folder(filename, user_selected_load=None):
    """
    Determine dropbox folder from filename or user selection
    """
    # Option 1: User selected from dropdown
    if user_selected_load:
        return f'/sltk/dropbox/{user_selected_load}/'
    
    # Option 2: Extract from filename pattern
    # Example: MODATA_upload.xlsx → MODATA
    parts = filename.split('_')
    if len(parts) > 0:
        load_id = parts[0].upper()
        dropbox_path = f'/sltk/dropbox/{load_id}/'
        
        # Verify folder exists
        if os.path.exists(dropbox_path):
            return dropbox_path
    
    # Option 3: Fallback to default
    return '/HOME/VIJAYVERMA/'  # POC folder

# Usage in upload endpoint
@app.route('/upload/excel', methods=['POST'])
def upload_excel():
    file = request.files['excel_file']
    load_id = request.form.get('load_id')  # From dropdown
    
    dropbox_folder = get_dropbox_folder(file.filename, load_id)
    output_path = os.path.join(dropbox_folder, file.filename)
    
    # Save file
    df.to_excel(output_path, index=False)
```

### **Phase 2: Production (Use Option 1)**

```python
def get_dropbox_from_sltklod(load_id):
    """
    Query SLTKLOD table to get dropbox path
    """
    cursor = db_connection.cursor()
    
    # TODO: Update column name after finding SLTKLOD structure
    query = """
        SELECT dropbox_path_column 
        FROM SLTKLOD 
        WHERE load_id = ?
    """
    
    cursor.execute(query, (load_id,))
    result = cursor.fetchone()
    
    if result:
        return result[0]
    else:
        raise ValueError(f"Load ID '{load_id}' not found in SLTKLOD")
```

---

## 📊 UI Changes Needed

### **Add Load ID Dropdown to Frontend**

```typescript
// In App.tsx

const [availableLoads, setAvailableLoads] = useState<string[]>([]);
const [selectedLoad, setSelectedLoad] = useState<string>('');

// Fetch available loads on mount
useEffect(() => {
  fetch(`${API_URL}/api/loads`)
    .then(r => r.json())
    .then(data => setAvailableLoads(data.loads));
}, []);

// In upload form
<select value={selectedLoad} onChange={(e) => setSelectedLoad(e.target.value)}>
  <option value="">-- Select SLTK Object --</option>
  {availableLoads.map(load => (
    <option key={load} value={load}>{load}</option>
  ))}
</select>
```

### **New API Endpoint**

```python
@app.route('/api/loads', methods=['GET'])
def get_available_loads():
    """
    Get list of available SLTK load IDs
    """
    # Option 1: From SLTKLOD table
    cursor = db_connection.cursor()
    cursor.execute("SELECT DISTINCT load_id FROM SLTKLOD ORDER BY load_id")
    loads = [row[0] for row in cursor.fetchall()]
    
    # Option 2: From IFS folders
    # loads = os.listdir('/sltk/dropbox/')
    
    return jsonify({"loads": loads})
```

---

## ✅ Implementation Status

### **COMPLETED** ✅

1. **SLTKLOD Table Structure Analyzed**
   - Confirmed: No explicit dropbox path column
   - Path is constructed as: `/sltk/dropbox/{LOAD_ID}/`

2. **Backend Updated** ✅
   - ✅ Added `/api/loads` endpoint - Returns list of available Load IDs
   - ✅ Added `get_available_loads()` - Queries SLTKLOD table
   - ✅ Added `get_dropbox_folder()` - Dynamic folder detection
   - ✅ Added `scan_dropbox_folders()` - IFS folder scanning fallback
   - ✅ Updated `/upload/excel` - Now accepts `load_id` parameter
   - ✅ Updated configuration - `DROPBOX_ROOT` and `DROPBOX_FOLDER_POC`

3. **Dynamic Detection Logic** ✅
   ```python
   Priority:
   1. If load_id provided → /sltk/dropbox/{load_id}/
   2. If filename matches {LOAD}_*.xlsx → Extract load_id
   3. Fallback → /HOME/VIJAYVERMA/ (POC folder)
   ```

### **PENDING** ⏳

4. **Update Frontend**
   - ⏳ Add Load ID dropdown to App.tsx
   - ⏳ Fetch loads from `/api/loads` on mount
   - ⏳ Pass selected `load_id` to upload endpoint

5. **Test**
   - ⏳ Upload to different dropbox folders
   - ⏳ Verify SLTKDRP processes correctly
   - ⏳ Test auto-detection from filename

---

## 🧪 Testing Guide

### **Test 1: Upload with Load ID Selection**
```bash
curl -X POST http://localhost:44001/upload/excel \
  -F "excel_file=@test.xlsx" \
  -F "load_id=DEMOITM"
```

Expected: File saved to `/sltk/dropbox/DEMOITM/test.xlsx`

### **Test 2: Upload with Filename Auto-Detection**
```bash
curl -X POST http://localhost:44001/upload/excel \
  -F "excel_file=@DEMOORD_upload.xlsx"
```

Expected: File saved to `/sltk/dropbox/DEMOORD/DEMOORD_upload.xlsx`

### **Test 3: Get Available Loads**
```bash
curl http://localhost:44001/api/loads
```

Expected Response:
```json
{
  "status": "success",
  "loads": [
    {"load_id": "DEMOITM", "description": "Demonstration Item Revision"},
    {"load_id": "DEMOORD", "description": "Demonstration Customer Order"},
    {"load_id": "DEMOSA", "description": "Demonstration Issue Sales Item (SA)"}
  ],
  "count": 3
}
```

---

## 📋 Next Steps

1. **Update Frontend UI** - Add Load ID dropdown
2. **Test Dynamic Detection** - Verify all 3 priority levels work
3. **Production Deployment** - Deploy to IBM i
4. **User Training** - Document the new Load ID selection feature

