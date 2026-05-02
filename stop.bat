@echo off
chcp 65001 >nul
title 招聘系统停止脚本
echo ==========================================
echo     招聘系统 - 停止服务
echo ==========================================
echo.

echo [1/2] 停止后端服务 (Flask)...
tasklist | findstr python.exe >nul
if %errorlevel% == 0 (
    taskkill /F /IM python.exe >nul 2>&1
    echo     后端服务已停止 (端口 5000)
) else (
    echo     未找到后端服务
)
echo.

echo [2/2] 停止前端服务 (Web + 小程序 H5)...
tasklist | findstr node.exe >nul
if %errorlevel% == 0 (
    taskkill /F /IM node.exe >nul 2>&1
    echo     前端服务已停止 (端口 5173 和 5174)
) else (
    echo     未找到前端服务
)
echo.

echo ==========================================
echo     所有服务已停止
echo ==========================================
echo.
echo 说明:
echo   - Python 进程: 后端服务
echo   - Node 进程: 前端 Web 页面 + 小程序 H5 页面
echo.
pause
