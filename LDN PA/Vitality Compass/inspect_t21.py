import pandas as pd
import sys

sys.stdout.reconfigure(encoding='utf-8')

p_hr = r"C:\Users\Administrator\Desktop\AI 2026\Metor\[ĐCL] - BÁO CÁO TUYỂN DỤNG DATA.xlsx"
xl = pd.ExcelFile(p_hr)

sheet_name = 'Tổng hợp (T21)'
if sheet_name in xl.sheet_names:
    print(f"=== Reading {sheet_name} ===")
    df = xl.parse(sheet_name)
    print("Shape:", df.shape)
    print("Columns:", list(df.columns))
    print("First 20 rows:")
    print(df.head(20).to_string())
else:
    print(f"Sheet {sheet_name} not found! Available sheets include:", [s for s in xl.sheet_names if 'Tổng hợp' in s])
