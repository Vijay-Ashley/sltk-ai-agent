@echo off
REM SLTK Chatbot Frontend - Windows Start Script
REM This script starts the React frontend on port 8001

echo ========================================
echo   SLTK Chatbot Frontend
echo   Starting on port 8001...
echo ========================================
echo.

REM Check if .env file exists
if not exist .env (
    echo ERROR: .env file not found!
    echo.
    echo Please create .env file with:
    echo VITE_API_URL=http://your-ibmi-hostname:44001
    echo.
    pause
    exit /b 1
)

REM Check if node_modules exists
if not exist node_modules (
    echo Installing dependencies...
    call npm install
    if errorlevel 1 (
        echo ERROR: npm install failed!
        pause
        exit /b 1
    )
)

REM Start the development server
echo.
echo Starting Vite development server...
echo Access the UI at: http://localhost:8001
echo Or from network: http://ae1dcvpap23919:8001
echo.
echo Press Ctrl+C to stop the server
echo.

call npm run dev

