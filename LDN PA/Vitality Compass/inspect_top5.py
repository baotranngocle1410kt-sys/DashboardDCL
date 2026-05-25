import pandas as pd
import sys

sys.stdout.reconfigure(encoding='utf-8')

p_hr = r"C:\Users\Administrator\Desktop\AI 2026\Metor\[ĐCL] - BÁO CÁO TUYỂN DỤNG DATA.xlsx"
df = pd.read_excel(p_hr, sheet_name="Report TOP 5 BC thiếu nhiều nhấ")

print("Columns:", list(df.columns))
print("Data rows:")
for idx, row in df.iterrows():
    print(f"\nRow {idx}:")
    for col in df.columns:
        print(f"  {col}: {row[col]}")
