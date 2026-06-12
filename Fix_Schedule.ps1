Start-Transcript -Path "c:\Users\Administrator\Desktop\AI 2026\fix_log.txt" -Force

try {
    # 1. Stop the scheduled task
    Write-Host "Stopping scheduled task..."
    Stop-ScheduledTask -TaskName "CapNhatDashboardDCL" -ErrorAction Stop

    # 2. Kill the orphaned hanging processes
    Write-Host "Killing hanging processes..."
    $processes = @("python", "git", "git-remote-https", "git-credential-manager")
    foreach ($p in $processes) {
        Stop-Process -Name $p -Force -ErrorAction SilentlyContinue
    }

    # 3. Change the scheduled task principal to run as the logged-in user
    Write-Host "Changing task principal to baobao..."
    $principal = New-ScheduledTaskPrincipal -UserId "baobao\baobao" -LogonType Interactive
    Set-ScheduledTask -TaskName "CapNhatDashboardDCL" -Principal $principal -ErrorAction Stop

    Write-Host "SUCCESS!"
} catch {
    Write-Warning "Failed to execute: $_"
}

Stop-Transcript
