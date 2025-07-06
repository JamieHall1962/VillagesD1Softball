@echo off
echo ============================================================
echo D1 Softball Stats App Launcher
echo ============================================================
echo.
echo Starting the Flask app...
echo The app will be available at: http://localhost:5000
echo Press Ctrl+C to stop the server
echo ============================================================
echo.

cd /d "%~dp0apps\drill_down"
python simple_csv_app.py

pause 