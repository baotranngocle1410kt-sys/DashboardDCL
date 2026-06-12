import pandas as pd
import sys

sys.stdout.reconfigure(encoding='utf-8')

p_hr = r"C:\Users\Administrator\Desktop\AI 2026\Metor\[ĐCL] - BÁO CÁO TUYỂN DỤNG DATA.xlsx"
df = pd.read_excel(p_hr, sheet_name="Tổng hợp (T21)")

print("Total columns:", len(df.columns))

# Let's group columns that are not completely empty
# We see repeated groups of columns like:
# Group 0: Bưu cục (col 9), Tỉnh (col 10), AM (col 11), Tuyến thiếu (col 12), Định biên NVPTTT (col 13), Định biên NVXL (col 14)...
# Group 1: Bưu cục.1 (col 50), Tỉnh.1, AM.1, ...
# Group 2: Bưu cục.2 (col 65), Tỉnh.2, AM.2, ...

# Let's print out the column names and non-null counts for groups of columns
for i in range(0, len(df.columns), 15):
    sub_cols = df.columns[i:i+15]
    print(f"\n--- Columns {i} to {min(i+15, len(df.columns))} ---")
    for col in sub_cols:
        non_null = df[col].notna().sum()
        print(f"  {col} (non-null: {non_null})")
