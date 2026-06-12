import pandas as pd
import sys

sys.stdout.reconfigure(encoding='utf-8')

p_hr = r"C:\Users\Administrator\Desktop\AI 2026\Metor\[ĐCL] - BÁO CÁO TUYỂN DỤNG DATA.xlsx"
df = pd.read_excel(p_hr, sheet_name="Tổng hợp (T21)")

# Subtable 0 is cols 9 to 24 (inclusive)
sub_df = df.iloc[:, 9:25].copy()
print("Subtable 0 Columns:")
print(list(sub_df.columns))

print("\nFirst 15 rows of Subtable 0:")
# Row 0 is the headers or summary row, let's see:
for idx, row in sub_df.head(15).iterrows():
    print(f"Row {idx}: {row.to_dict()}")
