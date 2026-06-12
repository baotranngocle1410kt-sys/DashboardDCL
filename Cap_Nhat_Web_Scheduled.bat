@echo off
chcp 65001 > nul
cd /d "c:\Users\Administrator\Desktop\AI 2026"
echo ========================================== >> "c:\Users\Administrator\Desktop\AI 2026\schedule_log.txt"
echo Bắt đầu cập nhật tự động: %date% %time% >> "c:\Users\Administrator\Desktop\AI 2026\schedule_log.txt"
python "c:\Users\Administrator\Desktop\AI 2026\Cap_Nhat_Web.py" >> "c:\Users\Administrator\Desktop\AI 2026\schedule_log.txt" 2>&1
echo Kết thúc cập nhật tự động: %date% %time% >> "c:\Users\Administrator\Desktop\AI 2026\schedule_log.txt"
