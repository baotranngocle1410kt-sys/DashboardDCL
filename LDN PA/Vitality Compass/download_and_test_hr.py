import pandas as pd
import urllib.request
import urllib.error
import sys
import os

# Ensure UTF-8 output
sys.stdout.reconfigure(encoding='utf-8')

URL_HR = "https://docs.google.com/spreadsheets/d/1si4PWd97eJhQDQUBXvEErjmNHGO8W1NrQVFnzzMIkDI/export?format=xlsx"
p_hr = r"C:\Users\Administrator\Desktop\AI 2026\Metor\[ĐCL] - BÁO CÁO TUYỂN DỤNG DATA.xlsx"

print("Downloading HR sheet...")
try:
    req = urllib.request.Request(URL_HR, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=10) as response:
        with open(p_hr, 'wb') as f:
            f.write(response.read())
    print("✓ Success download.")
except Exception as e:
    print("Failed to download:", e)

# Test read
if os.path.exists(p_hr):
    print("File size:", os.path.getsize(p_hr))
    xl = pd.ExcelFile(p_hr)
    print("Sheets:", xl.sheet_names)
