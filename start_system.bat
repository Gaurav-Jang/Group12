@echo off
echo 🏥 Starting Healthcare Brain Tumor Detection System...
echo ==================================================

REM Check if MongoDB is running
tasklist /FI "IMAGENAME eq mongod.exe" 2>NUL | find /I /N "mongod.exe">NUL
if "%ERRORLEVEL%"=="1" (
    echo ❌ MongoDB is not running!
    echo 💡 Please start MongoDB first:
    echo    - Windows: net start MongoDB
    echo    - Or start MongoDB service from Services
    pause
    exit /b 1
)

echo ✅ MongoDB is running

echo 🔧 Starting Flask Backend...
cd backend

REM Install dependencies
echo 📥 Installing Python dependencies...
pip install -r requirements.txt

REM Start Flask server in background
echo 🚀 Starting Flask server on http://localhost:5000
start "Flask Backend" python app.py

cd ..

echo ⚛️  Starting React Frontend...
cd frontend

REM Install dependencies if needed
if not exist "node_modules" (
    echo 📥 Installing Node.js dependencies...
    npm install
)

REM Start React server
echo 🚀 Starting React server on http://localhost:3000
start "React Frontend" npm start

cd ..

echo.
echo 🎉 System is starting up!
echo 📍 Frontend: http://localhost:3000
echo 📍 Backend:  http://localhost:5000
echo.
echo 🔑 Login Credentials:
echo    Admin:   admin@healthcare.com / admin123
echo    Doctor:  doctor@healthcare.com / doctor123
echo    Patient: patient@healthcare.com / patient123
echo.
echo Press any key to close this window...
pause >nul