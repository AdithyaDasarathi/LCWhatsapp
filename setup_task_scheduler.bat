@echo off
echo 🕘 Setting up Windows Task Scheduler for LeetCode Agent
echo ================================================

REM Get current directory
set CURRENT_DIR=%~dp0
set PYTHON_SCRIPT=%CURRENT_DIR%leetcode_agent.py

echo.
echo Creating daily task in Windows Task Scheduler...
echo Script location: %PYTHON_SCRIPT%
echo.

REM Create the scheduled task
schtasks /create /tn "LeetCode Daily Problems" /tr "python \"%PYTHON_SCRIPT%\" --once" /sc daily /st 09:00 /f

if %errorlevel% equ 0 (
    echo ✅ Task created successfully!
    echo.
    echo Your LeetCode problems will now be sent daily at 9:00 AM
    echo even when your computer restarts or the script isn't running.
    echo.
    echo To view/modify the task:
    echo 1. Open Task Scheduler (taskschd.msc)
    echo 2. Look for "LeetCode Daily Problems"
    echo.
    echo To delete the task later:
    echo schtasks /delete /tn "LeetCode Daily Problems" /f
) else (
    echo ❌ Failed to create task. You may need to run as Administrator.
    echo Right-click this file and select "Run as administrator"
)

echo.
pause 