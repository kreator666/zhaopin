@echo off
chcp 65001 >nul
title 招聘系统启动脚本
echo ==========================================
echo     招聘系统 - 一键启动脚本
echo ==========================================
echo.

:: 检查端口占用
echo [1/5] 检查端口 5000 (后端)...
netstat -ano | findstr :5000 >nul
if %errorlevel% == 0 (
    echo     端口 5000 已被占用，尝试关闭旧进程...
    for /f "tokens=5" %%a in ('netstat -ano ^| findstr :5000') do (
        taskkill /F /PID %%a >nul 2>&1
    )
)
echo     端口 5000 可用
echo.

echo [2/5] 检查端口 5173 (前端 Web)...
netstat -ano | findstr :5173 >nul
if %errorlevel% == 0 (
    echo     端口 5173 已被占用，尝试关闭旧进程...
    for /f "tokens=5" %%a in ('netstat -ano ^| findstr :5173') do (
        taskkill /F /PID %%a >nul 2>&1
    )
)
echo     端口 5173 可用
echo.

echo [3/5] 检查端口 5174 (小程序 H5)...
netstat -ano | findstr :5174 >nul
if %errorlevel% == 0 (
    echo     端口 5174 已被占用，尝试关闭旧进程...
    for /f "tokens=5" %%a in ('netstat -ano ^| findstr :5174') do (
        taskkill /F /PID %%a >nul 2>&1
    )
)
echo     端口 5174 可用
echo.

:: 启动后端
echo [4/5] 启动后端服务 (Flask)...
cd /d "%~dp0backend"
start "招聘系统-后端" cmd /k "venv\Scripts\python -c "from app import create_app; app = create_app(); app.run(debug=False, port=5000, threaded=True)""
echo     后端启动中... http://localhost:5000
timeout /t 2 >nul
echo.

:: 启动前端 Web
echo [5/5] 启动前端服务...
cd /d "%~dp0frontend"
start "招聘系统-前端(Web)" cmd /k "npm run dev"
echo     前端 Web 启动中... http://localhost:5173

:: 启动小程序 H5（检查 miniprogram 目录是否存在）
cd /d "%~dp0"
if exist "miniprogram\package.json" (
    echo     小程序项目存在，正在启动...
    cd /d "%~dp0miniprogram"
    start "招聘系统-小程序(H5)" cmd /k "npm run dev:h5"
    echo     小程序 H5 启动中... http://localhost:5174
) else (
    echo     小程序项目不存在，跳过启动
)
echo.

echo ==========================================
echo     服务启动完成！
echo ==========================================
echo.
echo 访问地址:
echo   - Web 前端页面:   http://localhost:5173
echo   - 小程序 H5 页面:  http://localhost:5174
echo   - 后端API:        http://localhost:5000
echo   - API测试:        http://localhost:5000/api/health
echo.
echo 停止服务:
echo   - 运行 stop.bat
echo   - 或关闭各命令行窗口
echo.
pause
