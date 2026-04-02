# 招聘系统 - PowerShell 停止脚本
# 使用: .\stop.ps1

$ErrorActionPreference = "SilentlyContinue"
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "    招聘系统 - 停止服务" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

# 停止 Python 进程 (后端)
Write-Host "[1/2] 停止后端服务 (Python/Flask)..." -ForegroundColor Yellow
$PythonProcesses = Get-Process -Name "python" -ErrorAction SilentlyContinue
if ($PythonProcesses) {
    $PythonProcesses | Stop-Process -Force
    Write-Host "    Python 进程已停止 ($($PythonProcesses.Count) 个)" -ForegroundColor Green
} else {
    Write-Host "    未找到 Python 进程" -ForegroundColor Gray
}
Write-Host ""

# 停止 Node 进程 (前端)
Write-Host "[2/2] 停止前端服务 (Node/Vite)..." -ForegroundColor Yellow
$NodeProcesses = Get-Process -Name "node" -ErrorAction SilentlyContinue
if ($NodeProcesses) {
    $NodeProcesses | Stop-Process -Force
    Write-Host "    Node 进程已停止 ($($NodeProcesses.Count) 个)" -ForegroundColor Green
} else {
    Write-Host "    未找到 Node 进程" -ForegroundColor Gray
}
Write-Host ""

# 额外检查端口是否释放
$Ports = @(5000, 5173)
foreach ($Port in $Ports) {
    $connection = Get-NetTCPConnection -LocalPort $Port -State Listen -ErrorAction SilentlyContinue
    if ($connection) {
        $process = Get-Process -Id $connection.OwningProcess -ErrorAction SilentlyContinue
        if ($process) {
            Stop-Process -Id $process.Id -Force
            Write-Host "    已释放端口 $Port" -ForegroundColor Green
        }
    }
}

Write-Host ""
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "    所有服务已停止" -ForegroundColor Green
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

Read-Host "按 Enter 键继续"
