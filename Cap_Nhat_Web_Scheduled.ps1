Set-Location "c:\Users\Administrator\Desktop\AI 2026"
$dateStr = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
"==========================================" | Out-File -Append -FilePath "c:\Users\Administrator\Desktop\AI 2026\schedule_log.txt" -Encoding utf8
"Bắt đầu cập nhật tự động: $dateStr" | Out-File -Append -FilePath "c:\Users\Administrator\Desktop\AI 2026\schedule_log.txt" -Encoding utf8
# Đảm bảo Git tin cậy thư mục làm việc khi chạy dưới tài khoản SYSTEM
& "C:\Program Files\Git\cmd\git.exe" config --global --add safe.directory 'C:/Users/Administrator/Desktop/AI 2026' 2>&1 | Out-File -Append -FilePath "c:\Users\Administrator\Desktop\AI 2026\schedule_log.txt" -Encoding utf8

# Cấu hình môi trường cho Playwright và Chrome khi chạy dưới tài khoản SYSTEM
$env:PLAYWRIGHT_BROWSERS_PATH = "C:\Users\Administrator\AppData\Local\ms-playwright"
$env:USERPROFILE = "C:\Users\Administrator"

& "C:\Users\Administrator\AppData\Local\Programs\Python\Python314\python.exe" "c:\Users\Administrator\Desktop\AI 2026\Cap_Nhat_Web.py" *>&1 | Out-File -Append -FilePath "c:\Users\Administrator\Desktop\AI 2026\schedule_log.txt" -Encoding utf8
$dateStr = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
"Kết thúc cập nhật tự động: $dateStr" | Out-File -Append -FilePath "c:\Users\Administrator\Desktop\AI 2026\schedule_log.txt" -Encoding utf8

