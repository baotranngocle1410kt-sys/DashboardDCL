import pandas as pd
import os
import sys

# Ensure UTF-8 output
sys.stdout.reconfigure(encoding='utf-8')

f_path = r"C:\Users\Administrator\Desktop\AI 2026\Metor\[ĐCL] - BÁO CÁO TUYỂN DỤNG DATA.xlsx"

try:
    xl = pd.ExcelFile(f_path)
    sheets = ['Báo cáo tỉnh nóng', 'Report TOP 5 BC thiếu nhiều nhấ', 'Intern theo tỉnh', 'Cơ cấu Vùng', 'Cơ cấu Intern']
    for s in sheets:
        if s in xl.sheet_names:
            print(f"\n=================== Sheet: {s} ===================")
            df = xl.parse(s)
            print(f"Shape: {df.shape}")
            print("Columns:")
            print(df.columns.tolist()[:10])
            print("First 15 rows:")
            print(df.head(15).to_string())
        else:
            print(f"\nSheet '{s}' NOT found in Excel!")
except Exception as e:
    print("Error:", e)
