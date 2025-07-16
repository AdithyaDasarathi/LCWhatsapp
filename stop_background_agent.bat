@echo off
echo 🛑 Stopping Background LeetCode Agent
echo =====================================

echo Looking for running Python processes...

REM Kill any python.exe processes (be careful - this affects all Python processes)
tasklist | findstr python.exe
if %errorlevel% equ 0 (
    echo.
    echo Found Python processes. Stopping LeetCode agent...
    taskkill /f /im python.exe
    echo ✅ Background agent stopped.
) else (
    echo ✅ No Python processes found running.
)

echo.
echo The background scheduler has been stopped.
echo Consider using Windows Task Scheduler instead (run setup_task_scheduler.bat)
echo.
pause 