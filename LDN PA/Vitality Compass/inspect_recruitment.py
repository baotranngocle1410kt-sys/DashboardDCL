import pandas as pd
import os
import sys

# Ensure UTF-8 output
sys.stdout.reconfigure(encoding='utf-8')

f_path = r"C:\Users\Administrator\Desktop\AI 2026\Metor\[ĐCL] - BÁO CÁO TUYỂN DỤNG DATA.xlsx"
if not os.path.exists(f_path):
    print("File not found:", f_path)
    sys.exit(1)

print("Reading sheet names...")
try:
    xl = pd.ExcelFile(f_path)
    print("Sheets in file:", xl.sheet_names)
    for name in xl.sheet_names:
        print(f"\n--- Sheet: {name} ---")
        df = xl.parse(name, nrows=10)
        print("Columns:", list(df.columns))
        print("First 5 rows:")
        print(df.head(5).to_string())
except Exception as e:
    print("Error:", e)
