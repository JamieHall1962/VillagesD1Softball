@echo off
REM === D1 Softball Automated Update Script ===
REM 1. Backup SQLite database (disabled for now)
REM set DBFILE=your_database.sqlite
REM set BACKUPDIR=backups
REM if not exist %BACKUPDIR% mkdir %BACKUPDIR%
REM set BACKUPFILE=%BACKUPDIR%\%DBFILE%_%date:~10,4%-%date:~4,2%-%date:~7,2%_%time:~0,2%-%time:~3,2%-%time:~6,2%.sqlite
REM copy /Y %DBFILE% %BACKUPFILE%

REM 2. Add all changes to git
git add -A

REM 3. Commit with timestamp
set msg=Auto-update %date% %time%
git commit -m "%msg%"

REM 4. Push to GitHub
git push origin main

REM 5. Notify user
@echo All changes pushed to GitHub. Render.com will redeploy automatically.
pause 