# 招聘系统 - PowerShell 启动脚本
# 使用: .\start.ps1

$ErrorActionPreference = "SilentlyContinue"
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "    招聘系统 - 一键启动脚本" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

# 获取脚本所在目录
$ScriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $ScriptPath

# 检查端口占用的函数
function Test-PortInUse {
    param([int]$Port)
    $connection = Get-NetTCPConnection -LocalPort $Port -State Listen -ErrorAction SilentlyContinue
    return $connection -ne $null
}

function Stop-ProcessOnPort {
    param([int]$Port)
    $connection = Get-NetTCPConnection -LocalPort $Port -State Listen -ErrorAction SilentlyContinue
    if ($connection) {
        $process = Get-Process -Id $connection.OwningProcess -ErrorAction SilentlyContinue
        if ($process) {
            Stop-Process -Id $process.Id -Force
            Write-Host "    已关闭占用端口 $Port 的进程" -ForegroundColor Yellow
        }
    }
}

# 检查并清理端口
Write-Host "[1/4] 检查端口 5000 (后端)..." -ForegroundColor Green
if (Test-PortInUse -Port 5000) {
    Stop-ProcessOnPort -Port 5000
}
Write-Host "    端口 5000 可用" -ForegroundColor Gray
Write-Host ""

Write-Host "[2/4] 检查端口 5173 (前端)..." -ForegroundColor Green
if (Test-PortInUse -Port 5173) {
    Stop-ProcessOnPort -Port 5173
}
Write-Host "    端口 5173 可用" -ForegroundColor Gray
Write-Host ""

# 启动后端
Write-Host "[3/4] 启动后端服务 (Flask)..." -ForegroundColor Green
$BackendPath = Join-Path $ScriptPath "backend"
$BackendCmd = "cd `"$BackendPath`"; .\venv\Scripts\python -c `"from app import create_app; app = create_app(); app.run(debug=False, port=5000, threaded=True)`""
Start-Process "cmd.exe" -ArgumentList "/k", $BackendCmd -WindowStyle Normal
Write-Host "    后端启动中... http://localhost:5000" -ForegroundColor Gray
Start-Sleep -Seconds 2
Write-Host ""

# 启动前端
Write-Host "[4/4] 启动前端服务 (Vue)..." -ForegroundColor Green
$FrontendPath = Join-Path $ScriptPath "frontend"
$FrontendCmd = "cd `"$FrontendPath`"; npm run dev"
Start-Process "cmd.exe" -ArgumentList "/k", $FrontendCmd -WindowStyle Normal
Write-Host "    前端启动中... http://localhost:5173" -ForegroundColor Gray
Write-Host ""

# 等待服务启动
Write-Host "等待服务启动..." -ForegroundColor Yellow
$MaxWait = 30
$Waited = 0
$BackendReady = $false
$FrontendReady = $false

while ($Waited -lt $MaxWait) {
    Start-Sleep -Seconds 1
    $Waited++
    
    # 检查后端的
    if (-not $BackendReady) {
        try {
            $response = Invoke-RestMethod -Uri "http://localhost:5000/api/health" -Method GET -TimeoutSec 2 -ErrorAction Stop
            $BackendReady = $true
            Write-Host "    后端服务已就绪" -ForegroundColor Green
        } catch {}
    }
    
    # 检查前端
    if (-not $FrontendReady) {
        try {
            $response = Invoke-WebRequest -Uri "http://localhost:5173" -Method GET -TimeoutSec 2 -ErrorAction Stop
            if ($response.StatusCode -eq 200) {
                $FrontendReady = $true
                Write-Host "    前端服务已就绪" -ForegroundColor Green
            }
        } catch {}
    }
    
    if ($BackendReady -and $FrontendReady) {
        break
    }
}

Write-Host ""
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "    服务启动完成！" -ForegroundColor Green
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "访问地址:" -ForegroundColor Yellow
Write-Host "  - 前端页面: http://localhost:5173" -ForegroundColor White
Write-Host "  - 后端API:  http://localhost:5000" -ForegroundColor White
Write-Host "  - API测试:  http://localhost:5000/api/health" -ForegroundColor White
Write-Host ""
Write-Host "停止服务:" -ForegroundColor Yellow
Write-Host "  - 运行 .\stop.ps1" -ForegroundColor White
Write-Host "  - 或关闭后端和前端的命令行窗口" -ForegroundColor White
Write-Host ""

Read-Host "按 Enter 键继续"
