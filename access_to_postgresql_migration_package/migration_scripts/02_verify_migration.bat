@echo off
REM =====================================================
REM Migration Verification Script
REM Checks data integrity after migration
REM =====================================================

echo =====================================================
echo PostgreSQL Migration Verification
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
SET REPORT_FILE=..\logs\verification_report_%date:~-4,4%%date:~-10,2%%date:~-7,2%.txt

REM Create report
echo Migration Verification Report > "%REPORT_FILE%"
echo Generated: %date% %time% >> "%REPORT_FILE%"
echo ===================================== >> "%REPORT_FILE%"
echo. >> "%REPORT_FILE%"

echo Running verification checks...
echo.

REM Check 1: Database exists
echo 1. Checking database connection...
"%PGPATH%\psql" -U postgres -d %DB_NAME% -c "SELECT version();" >nul 2>&1
IF %ERRORLEVEL% EQU 0 (
    echo    [PASS] Database connection successful
    echo [PASS] Database connection successful >> "%REPORT_FILE%"
) ELSE (
    echo    [FAIL] Cannot connect to database
    echo [FAIL] Cannot connect to database >> "%REPORT_FILE%"
    pause
    exit /b 1
)

REM Check 2: Table count
echo 2. Checking table count...
"%PGPATH%\psql" -U postgres -d %DB_NAME% -t -A -c "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'public';" > temp_count.txt
SET /p TABLE_COUNT=<temp_count.txt
del temp_count.txt
IF %TABLE_COUNT% EQU 71 (
    echo    [PASS] All 71 tables created
    echo [PASS] All 71 tables created >> "%REPORT_FILE%"
) ELSE (
    echo    [WARNING] Expected 71 tables, found %TABLE_COUNT%
    echo [WARNING] Expected 71 tables, found %TABLE_COUNT% >> "%REPORT_FILE%"
)

REM Check 3: Data import
echo 3. Checking data import...
"%PGPATH%\psql" -U postgres -d %DB_NAME% -t -A -c "SELECT COALESCE(SUM(n_live_tup), 0) FROM pg_stat_user_tables WHERE schemaname = 'public';" > temp_rows.txt
SET /p ROW_COUNT=<temp_rows.txt
del temp_rows.txt
echo    Total rows imported: %ROW_COUNT%
echo Total rows imported: %ROW_COUNT% >> "%REPORT_FILE%"

REM Check 4: Main tables
echo 4. Checking main statistics tables...
echo. >> "%REPORT_FILE%"
echo Main Statistics Tables: >> "%REPORT_FILE%"
echo ----------------------- >> "%REPORT_FILE%"

"%PGPATH%\psql" -U postgres -d %DB_NAME% -t -c "SELECT 'battingstats: ' || COUNT(*) || ' rows' FROM battingstats;" >> "%REPORT_FILE%"
"%PGPATH%\psql" -U postgres -d %DB_NAME% -t -c "SELECT 'pitchingstats: ' || COUNT(*) || ' rows' FROM pitchingstats;" >> "%REPORT_FILE%"
"%PGPATH%\psql" -U postgres -d %DB_NAME% -t -c "SELECT 'fieldingstats: ' || COUNT(*) || ' rows' FROM fieldingstats;" >> "%REPORT_FILE%"
"%PGPATH%\psql" -U postgres -d %DB_NAME% -t -c "SELECT 'gamestats: ' || COUNT(*) || ' rows' FROM gamestats;" >> "%REPORT_FILE%"
"%PGPATH%\psql" -U postgres -d %DB_NAME% -t -c "SELECT 'roster: ' || COUNT(*) || ' rows' FROM roster;" >> "%REPORT_FILE%"
"%PGPATH%\psql" -U postgres -d %DB_NAME% -t -c "SELECT 'teams: ' || COUNT(*) || ' rows' FROM teams;" >> "%REPORT_FILE%"
"%PGPATH%\psql" -U postgres -d %DB_NAME% -t -c "SELECT 'people: ' || COUNT(*) || ' rows' FROM people;" >> "%REPORT_FILE%"

REM Check 5: Sample data
echo 5. Checking sample data...
echo. >> "%REPORT_FILE%"
echo Sample Data Verification: >> "%REPORT_FILE%"
echo ------------------------- >> "%REPORT_FILE%"
"%PGPATH%\psql" -U postgres -d %DB_NAME% -c "SELECT COUNT(*) as batting_records FROM battingstats WHERE teamnumber > 0;" >> "%REPORT_FILE%" 2>&1

REM Summary
echo.
echo =====================================================
echo Verification Summary
echo =====================================================
IF %ROW_COUNT% GTR 100000 (
    echo [SUCCESS] Migration verified successfully!
    echo          %ROW_COUNT% rows imported across %TABLE_COUNT% tables
    echo. >> "%REPORT_FILE%"
    echo VERIFICATION RESULT: SUCCESS >> "%REPORT_FILE%"
) ELSE (
    echo [WARNING] Migration completed with warnings.
    echo          Please check the verification report.
    echo. >> "%REPORT_FILE%"
    echo VERIFICATION RESULT: WARNING - Check data >> "%REPORT_FILE%"
)

echo.
echo Full report saved to: %REPORT_FILE%
echo.
pause