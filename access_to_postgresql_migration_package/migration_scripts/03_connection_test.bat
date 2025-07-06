@echo off
REM =====================================================
REM Database Connection Test
REM Tests PostgreSQL connection and provides examples
REM =====================================================

echo =====================================================
echo PostgreSQL Connection Test
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

echo Connection Details:
echo -------------------
echo Host: localhost
echo Port: 5432
echo Database: %DB_NAME%
echo Username: postgres
echo.

REM Test connection
echo Testing connection...
"%PGPATH%\psql" -U postgres -d %DB_NAME% -c "SELECT 'Connection successful!' as status;" 2>nul
IF %ERRORLEVEL% EQU 0 (
    echo.
    echo [SUCCESS] Database connection working!
    echo.
    
    REM Show sample query
    echo Running sample query...
    echo.
    echo Top 5 batters by games played:
    echo -------------------------------
    "%PGPATH%\psql" -U postgres -d %DB_NAME% -c "SELECT playernumber, COUNT(*) as games_played FROM battingstats GROUP BY playernumber ORDER BY games_played DESC LIMIT 5;"
) ELSE (
    echo.
    echo [ERROR] Connection failed!
    echo.
    echo Possible issues:
    echo - PostgreSQL service not running
    echo - Database not created (run 01_run_migration.bat first)
    echo - Incorrect password
    echo - PostgreSQL not installed
)

echo.
echo Connection String Examples:
echo ---------------------------
echo.
echo JDBC:
echo jdbc:postgresql://localhost:5432/%DB_NAME%
echo.
echo ODBC:
echo Driver={PostgreSQL};Server=localhost;Port=5432;Database=%DB_NAME%;Uid=postgres;Pwd=yourpassword;
echo.
echo Python (psycopg2):
echo postgresql://postgres:yourpassword@localhost:5432/%DB_NAME%
echo.
echo .NET:
echo Server=localhost;Port=5432;Database=%DB_NAME%;User Id=postgres;Password=yourpassword;
echo.
pause