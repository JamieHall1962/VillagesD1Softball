@echo off
REM =====================================================
REM Access to PostgreSQL Database Migration Script
REM Version: 1.0
REM =====================================================

echo =====================================================
echo Access to PostgreSQL Migration Tool
echo Version 1.0
echo =====================================================
echo.

REM Configuration
SET PGPATH=C:\Program Files\PostgreSQL\14\bin
IF NOT EXIST "%PGPATH%" SET PGPATH=C:\Program Files\PostgreSQL\13\bin
IF NOT EXIST "%PGPATH%" SET PGPATH=C:\Program Files\PostgreSQL\12\bin
IF NOT EXIST "%PGPATH%" SET PGPATH=C:\Program Files\PostgreSQL\11\bin
IF NOT EXIST "%PGPATH%" SET PGPATH=C:\Program Files\PostgreSQL\10\bin

SET PATH=%PGPATH%;%PATH%
SET DB_NAME=apssb_db
SET SCHEMA_FILE=..\database_files\schema.sql
SET IMPORT_FILE=..\database_files\import_data.sql
SET LOG_FILE=..\logs\migration_%date:~-4,4%%date:~-10,2%%date:~-7,2%_%time:~0,2%%time:~3,2%.log

REM Create logs directory
IF NOT EXIST ..\logs mkdir ..\logs

REM Start logging
echo Migration started at %date% %time% > "%LOG_FILE%"
echo. >> "%LOG_FILE%"

REM Check PostgreSQL installation
echo Checking PostgreSQL installation...
IF NOT EXIST "%PGPATH%\psql.exe" (
    echo ERROR: PostgreSQL not found in standard locations!
    echo Please install PostgreSQL or update PGPATH in this script.
    echo. >> "%LOG_FILE%"
    echo ERROR: PostgreSQL not found >> "%LOG_FILE%"
    pause
    exit /b 1
)

echo PostgreSQL found at: %PGPATH%
echo PostgreSQL found at: %PGPATH% >> "%LOG_FILE%"

REM Step 1: Drop existing database
echo.
echo Step 1: Preparing database...
echo Step 1: Preparing database... >> "%LOG_FILE%"
"%PGPATH%\psql" -U postgres -c "SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname = '%DB_NAME%' AND pid <> pg_backend_pid();" >> "%LOG_FILE%" 2>&1
"%PGPATH%\dropdb" -U postgres %DB_NAME% >> "%LOG_FILE%" 2>&1

REM Step 2: Create new database
echo Step 2: Creating database '%DB_NAME%'...
echo Step 2: Creating database '%DB_NAME%'... >> "%LOG_FILE%"
"%PGPATH%\createdb" -U postgres %DB_NAME% >> "%LOG_FILE%" 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo ERROR: Failed to create database. Check log file.
    echo See log file: %LOG_FILE%
    pause
    exit /b 1
)

REM Step 3: Import schema
echo Step 3: Creating database structure...
echo Step 3: Creating database structure... >> "%LOG_FILE%"
"%PGPATH%\psql" -U postgres -d %DB_NAME% -f "%SCHEMA_FILE%" >> "%LOG_FILE%" 2>&1

REM Step 4: Import data
echo Step 4: Importing data (this may take a few minutes)...
echo Step 4: Importing data... >> "%LOG_FILE%"
cd ..\database_files
"%PGPATH%\psql" -U postgres -d %DB_NAME% -f "import_data.sql" >> "..\logs\import_details.log" 2>&1
cd ..\migration_scripts

REM Step 5: Verify migration
echo Step 5: Verifying migration...
echo Step 5: Verifying migration... >> "%LOG_FILE%"
echo. >> "%LOG_FILE%"
"%PGPATH%\psql" -U postgres -d %DB_NAME% -t -c "SELECT 'Tables created: ' || COUNT(*) FROM information_schema.tables WHERE table_schema = 'public';" >> "%LOG_FILE%" 2>&1
"%PGPATH%\psql" -U postgres -d %DB_NAME% -t -c "SELECT 'Total rows imported: ' || SUM(n_live_tup) FROM pg_stat_user_tables WHERE schemaname = 'public';" >> "%LOG_FILE%" 2>&1

REM Display summary
echo.
echo =====================================================
echo Migration Complete!
echo =====================================================
"%PGPATH%\psql" -U postgres -d %DB_NAME% -t -c "SELECT 'Tables created: ' || COUNT(*) FROM information_schema.tables WHERE table_schema = 'public';"
"%PGPATH%\psql" -U postgres -d %DB_NAME% -t -c "SELECT 'Total rows imported: ' || SUM(n_live_tup) FROM pg_stat_user_tables WHERE schemaname = 'public';"
echo.
echo Database: %DB_NAME%
echo Host: localhost
echo Port: 5432
echo Username: postgres
echo.
echo Log files saved in: ..\logs\
echo.
echo Migration completed at %date% %time% >> "%LOG_FILE%"
pause