@echo off
chcp 65001 >nul
title 招聘系统停止脚本
echo ==========================================
echo     招聘系统 - 停止服务
echo ==========================================
echo.

echo [1/2] 停止后端服务 (Python/Flask)...
tasklist | findstr python.exe >nul
if %errorlevel% == 0 (
    taskkill /F /IM python.exe >nul 2>&1
    echo     Python 进程已停止
) else (
    echo     未找到 Python 进程
)
echo.

echo [2/2] 停止前端服务 (Node/Vite)...
tasklist | findstr node.exe >nul
if %errorlevel% == 0 (
    taskkill /F /IM node.exe >nul 2>&1
    echo     Node 进程已停止
) else (
    echo     未找到 Node 进程
)
echo.

echo ==========================================
echo     所有服务已停止
echo ==========================================
pause
