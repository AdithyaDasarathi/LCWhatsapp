@echo off
echo 🤖 LeetCode WhatsApp Agent
echo ========================

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH
    echo Please install Python 3.7+ from https://python.org
    pause
    exit /b 1
)

REM Check if .env file exists
if not exist .env (
    echo ⚠️  No .env file found
    echo Please run setup.py first to configure the agent
    echo.
    echo Running setup now...
    python setup.py
    if errorlevel 1 (
        echo ❌ Setup failed
        pause
        exit /b 1
    )
)

REM Show menu
echo.
echo What would you like to do?
echo 1. Start daily agent (background - requires keeping open)
echo 2. Setup Windows Task Scheduler (recommended - runs automatically)
echo 3. Send problems now (once)
echo 4. Test setup
echo 5. View statistics
echo 6. Stop background agent
echo 7. Fetch problems manually
echo 8. Exit
echo.

set /p choice="Enter your choice (1-8): "

if "%choice%"=="1" (
    echo Starting daily agent in background...
    echo NOTE: Keep this window open for scheduling to work
    python leetcode_agent.py
) else if "%choice%"=="2" (
    echo Setting up Windows Task Scheduler...
    call setup_task_scheduler.bat
) else if "%choice%"=="3" (
    echo Sending problems now...
    python leetcode_agent.py --once
) else if "%choice%"=="4" (
    echo Testing setup...
    python leetcode_agent.py --test
) else if "%choice%"=="5" (
    echo Getting statistics...
    python leetcode_agent.py --stats
) else if "%choice%"=="6" (
    echo Stopping background agent...
    call stop_background_agent.bat
) else if "%choice%"=="7" (
    echo Fetching problems...
    python leetcode_agent.py --fetch
) else if "%choice%"=="8" (
    echo Goodbye! 👋
    exit /b 0
) else (
    echo Invalid choice. Please try again.
)

echo.
pause 