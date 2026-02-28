import React, { useEffect, useState } from 'react';
import { Upload, FileSpreadsheet, CheckCircle2, AlertTriangle, Loader2, X, Clock, TrendingUp } from 'lucide-react';
import { io, Socket } from 'socket.io-client';

// Configuration - Use environment variable or fallback to localhost
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:44001';

type UploadStatus = {
  groupId: string;
  description: string;
  status: string;
  statusText: string;
  progress: {
    total: number;
    completed: number;
    errors: number;
    processing: number;
    pending: number;
    percentage: number;
  };
  timestamp: string;
};

type ErrorDetail = {
  token: string;
  sequence: number;
  messageId: string;
  messageText: string;
  resolution: {
    issue: string;
    fix: string;
    sql: string | null;
  };
};

export default function App() {
  const [file, setFile] = useState<File | null>(null);
  const [busyUpload, setBusyUpload] = useState(false);
  const [uploadMessage, setUploadMessage] = useState<string>('');
  const [currentStatus, setCurrentStatus] = useState<UploadStatus | null>(null);
  const [errors, setErrors] = useState<ErrorDetail[]>([]);
  const [showErrors, setShowErrors] = useState(false);
  const [socket, setSocket] = useState<Socket | null>(null);
  const [health, setHealth] = useState<string>('');

  // Initialize WebSocket connection
  useEffect(() => {
    const newSocket = io(API_URL);
    
    newSocket.on('connect', () => {
      console.log('✅ Connected to SLTK Monitor');
    });

    newSocket.on('status-update', (status: UploadStatus) => {
      console.log('📊 Status update:', status);
      setCurrentStatus(status);
      setUploadMessage(`${status.statusText} - ${status.progress.percentage}% complete`);
    });

    newSocket.on('processing-complete', async (status: UploadStatus) => {
      console.log('✅ Processing complete:', status);
      setCurrentStatus(status);
      setBusyUpload(false);

      if (status.status === 'X') {
        setUploadMessage(`✅ Upload complete! ${status.progress.completed}/${status.progress.total} transactions processed`);
      } else if (status.status === 'E') {
        setUploadMessage(`⚠️ Upload completed with ${status.progress.errors} errors`);
        // Fetch error details
        await fetchErrors(status.groupId);
      }
    });

    newSocket.on('error', (error: any) => {
      console.error('❌ Socket error:', error);
      setUploadMessage(`Error: ${error.message}`);
      setBusyUpload(false);
    });

    setSocket(newSocket);

    return () => {
      newSocket.close();
    };
  }, []);

  // Check health
  useEffect(() => {
    fetch(`${API_URL}/`)
      .then(r => r.json())
      .then(j => setHealth(j.status || 'ok'))
      .catch(() => setHealth(''));
  }, []);

  const fetchErrors = async (groupId: string) => {
    try {
      const res = await fetch(`${API_URL}/api/errors/${groupId}`);
      const data = await res.json();
      if (data.success) {
        setErrors(data.data.errors);
        setShowErrors(true);
      }
    } catch (error) {
      console.error('Error fetching errors:', error);
    }
  };

  const onDrop = (ev: React.DragEvent) => {
    ev.preventDefault();
    const droppedFile = ev.dataTransfer.files[0];
    if (droppedFile && (droppedFile.name.endsWith('.xlsx') || droppedFile.name.endsWith('.xls'))) {
      setFile(droppedFile);
      setUploadMessage('');
      setCurrentStatus(null);
      setErrors([]);
      setShowErrors(false);
    } else {
      setUploadMessage('⚠️ Please upload an Excel file (.xlsx or .xls)');
    }
  };

  const doUpload = async () => {
    if (!file) return;

    setBusyUpload(true);
    setUploadMessage('📤 Uploading file to IBM i...');
    setCurrentStatus(null);
    setErrors([]);
    setShowErrors(false);

    try {
      const fd = new FormData();
      fd.append('excel_file', file);

      const res = await fetch(`${API_URL}/upload/excel`, { method: 'POST', body: fd });
      const data = await res.json();

      if (data.status === 'success') {
        setUploadMessage('✅ File uploaded! Waiting for SLTKDRP to process...');
        
        // Wait a moment for SLTKDRP to create the group
        setTimeout(async () => {
          // For now, we'll need to manually get the group ID
          // In production, you'd get this from SLTKDRP or query recent groups
          setUploadMessage('ℹ️ File uploaded. Enter Group ID to monitor, or check history.');
          setBusyUpload(false);
        }, 2000);
      } else {
        setUploadMessage(`❌ Upload failed: ${data.message}`);
        setBusyUpload(false);
      }
    } catch (error: any) {
      setUploadMessage(`❌ Error: ${error.message}`);
      setBusyUpload(false);
    }
  };

  const monitorGroup = (groupId: string) => {
    if (!socket || !groupId) return;
    
    setBusyUpload(true);
    setUploadMessage(`📡 Monitoring group ${groupId}...`);
    socket.emit('monitor', groupId);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50">
      {/* Header */}
      <div className="bg-white border-b border-gray-200 shadow-sm">
        <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <FileSpreadsheet className="w-8 h-8 text-blue-600" />
            <div>
              <h1 className="text-2xl font-bold text-gray-900">SLTK Upload Chatbot</h1>
              <p className="text-sm text-gray-500">Real-time monitoring for SLTK uploads</p>
            </div>
          </div>
          <div className="flex items-center gap-2">
            {health === 'running' && (
              <span className="flex items-center gap-2 text-sm text-green-600">
                <CheckCircle2 className="w-4 h-4" />
                Connected
              </span>
            )}
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-6 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Upload Section */}
          <div className="bg-white rounded-2xl shadow-lg p-6">
            <h2 className="text-xl font-semibold mb-4 flex items-center gap-2">
              <Upload className="w-5 h-5 text-blue-600" />
              Upload Excel File
            </h2>

            <div
              onDrop={onDrop}
              onDragOver={(e) => e.preventDefault()}
              className="border-2 border-dashed border-gray-300 rounded-xl p-8 text-center hover:border-blue-400 transition-colors cursor-pointer"
            >
              {!file ? (
                <div>
                  <FileSpreadsheet className="w-16 h-16 mx-auto text-gray-400 mb-4" />
                  <p className="text-gray-600 mb-2">Drag & drop your Excel file here</p>
                  <p className="text-sm text-gray-400">or click to browse</p>
                  <input
                    type="file"
                    accept=".xlsx,.xls"
                    onChange={(e) => e.target.files && setFile(e.target.files[0])}
                    className="hidden"
                    id="file-input"
                  />
                  <label
                    htmlFor="file-input"
                    className="inline-block mt-4 px-4 py-2 bg-blue-600 text-white rounded-lg cursor-pointer hover:bg-blue-700"
                  >
                    Browse Files
                  </label>
                </div>
              ) : (
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-3">
                    <FileSpreadsheet className="w-8 h-8 text-green-600" />
                    <span className="font-medium">{file.name}</span>
                  </div>
                  <button
                    onClick={() => setFile(null)}
                    className="p-2 hover:bg-gray-100 rounded-lg"
                  >
                    <X className="w-5 h-5" />
                  </button>
                </div>
              )}
            </div>

            <button
              onClick={doUpload}
              disabled={!file || busyUpload}
              className="w-full mt-4 px-6 py-3 bg-blue-600 text-white rounded-xl font-medium hover:bg-blue-700 disabled:bg-gray-300 disabled:cursor-not-allowed flex items-center justify-center gap-2"
            >
              {busyUpload ? (
                <>
                  <Loader2 className="w-5 h-5 animate-spin" />
                  Processing...
                </>
              ) : (
                <>
                  <Upload className="w-5 h-5" />
                  Upload to IBM i
                </>
              )}
            </button>

            {uploadMessage && (
              <div className={`mt-4 p-4 rounded-lg ${
                uploadMessage.includes('✅') ? 'bg-green-50 text-green-800' :
                uploadMessage.includes('⚠️') || uploadMessage.includes('❌') ? 'bg-red-50 text-red-800' :
                'bg-blue-50 text-blue-800'
              }`}>
                {uploadMessage}
              </div>
            )}
          </div>

          {/* Status Section */}
          <div className="bg-white rounded-2xl shadow-lg p-6">
            <h2 className="text-xl font-semibold mb-4 flex items-center gap-2">
              <TrendingUp className="w-5 h-5 text-purple-600" />
              Upload Status
            </h2>

            {currentStatus ? (
              <div className="space-y-4">
                <div className="flex items-center justify-between">
                  <span className="text-sm text-gray-600">Group ID:</span>
                  <span className="font-mono font-medium">{currentStatus.groupId}</span>
                </div>

                <div className="flex items-center justify-between">
                  <span className="text-sm text-gray-600">Status:</span>
                  <span className={`px-3 py-1 rounded-full text-sm font-medium ${
                    currentStatus.status === 'X' ? 'bg-green-100 text-green-800' :
                    currentStatus.status === 'E' ? 'bg-red-100 text-red-800' :
                    currentStatus.status === 'O' ? 'bg-blue-100 text-blue-800' :
                    'bg-gray-100 text-gray-800'
                  }`}>
                    {currentStatus.statusText}
                  </span>
                </div>

                <div>
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-sm text-gray-600">Progress:</span>
                    <span className="text-sm font-medium">{currentStatus.progress.percentage}%</span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-3">
                    <div
                      className="bg-blue-600 h-3 rounded-full transition-all duration-500"
                      style={{ width: `${currentStatus.progress.percentage}%` }}
                    />
                  </div>
                </div>

                <div className="grid grid-cols-2 gap-4 pt-4 border-t">
                  <div>
                    <p className="text-sm text-gray-600">Total</p>
                    <p className="text-2xl font-bold">{currentStatus.progress.total}</p>
                  </div>
                  <div>
                    <p className="text-sm text-gray-600">Completed</p>
                    <p className="text-2xl font-bold text-green-600">{currentStatus.progress.completed}</p>
                  </div>
                  <div>
                    <p className="text-sm text-gray-600">Processing</p>
                    <p className="text-2xl font-bold text-blue-600">{currentStatus.progress.processing}</p>
                  </div>
                  <div>
                    <p className="text-sm text-gray-600">Errors</p>
                    <p className="text-2xl font-bold text-red-600">{currentStatus.progress.errors}</p>
                  </div>
                </div>

                {currentStatus.progress.errors > 0 && (
                  <button
                    onClick={() => fetchErrors(currentStatus.groupId)}
                    className="w-full mt-4 px-4 py-2 bg-red-100 text-red-800 rounded-lg hover:bg-red-200 flex items-center justify-center gap-2"
                  >
                    <AlertTriangle className="w-4 h-4" />
                    View {currentStatus.progress.errors} Error{currentStatus.progress.errors > 1 ? 's' : ''}
                  </button>
                )}
              </div>
            ) : (
              <div className="text-center py-12 text-gray-400">
                <Clock className="w-16 h-16 mx-auto mb-4" />
                <p>No active upload</p>
                <p className="text-sm mt-2">Upload a file to start monitoring</p>
              </div>
            )}
          </div>
        </div>

        {/* Errors Modal */}
        {showErrors && errors.length > 0 && (
          <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
            <div className="bg-white rounded-2xl shadow-2xl max-w-4xl w-full max-h-[80vh] overflow-hidden">
              <div className="p-6 border-b flex items-center justify-between">
                <h3 className="text-xl font-semibold flex items-center gap-2">
                  <AlertTriangle className="w-6 h-6 text-red-600" />
                  Upload Errors ({errors.length})
                </h3>
                <button
                  onClick={() => setShowErrors(false)}
                  className="p-2 hover:bg-gray-100 rounded-lg"
                >
                  <X className="w-5 h-5" />
                </button>
              </div>
              <div className="p-6 overflow-y-auto max-h-[60vh]">
                <div className="space-y-4">
                  {errors.map((error, idx) => (
                    <div key={idx} className="border border-red-200 rounded-lg p-4 bg-red-50">
                      <div className="flex items-start gap-3">
                        <AlertTriangle className="w-5 h-5 text-red-600 mt-0.5" />
                        <div className="flex-1">
                          <p className="font-medium text-red-900">
                            Row {error.sequence}: {error.messageText || error.messageId}
                          </p>
                          <div className="mt-2 space-y-2">
                            <div className="bg-white rounded p-3">
                              <p className="text-sm font-medium text-gray-700">Issue:</p>
                              <p className="text-sm text-gray-600">{error.resolution.issue}</p>
                            </div>
                            <div className="bg-white rounded p-3">
                              <p className="text-sm font-medium text-gray-700">Fix:</p>
                              <p className="text-sm text-gray-600">{error.resolution.fix}</p>
                            </div>
                            {error.resolution.sql && (
                              <div className="bg-gray-900 rounded p-3">
                                <p className="text-sm font-medium text-gray-300 mb-1">SQL:</p>
                                <code className="text-xs text-green-400">{error.resolution.sql}</code>
                              </div>
                            )}
                          </div>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

