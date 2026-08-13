@echo off
echo ========================================
echo   SLIME SHOOTERZ - BUILD SCRIPT
echo   Developed by MANBOY
echo ========================================
echo.

echo Building standalone executable with ALL assets embedded...
echo This will take 2-3 minutes...

py -3.12 build_exe.py

echo.
pause