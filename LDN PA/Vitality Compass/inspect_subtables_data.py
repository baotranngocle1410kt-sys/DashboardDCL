import pandas as pd
import sys

sys.stdout.reconfigure(encoding='utf-8')

p_hr = r"C:\Users\Administrator\Desktop\AI 2026\Metor\[ĐCL] - BÁO CÁO TUYỂN DỤNG DATA.xlsx"
df = pd.read_excel(p_hr, sheet_name="Tổng hợp (T21)")

print("Header row 0:")
print(df.iloc[0].to_dict())

# Let's inspect sub-tables by columns and see what values are in Bưu cục and Tỉnh
subtables = [
    ("", 9, 24),
    (".1", 50, 65),
    (".2", 65, 80),
    (".3", 80, 95),
    (".4", 95, 110),
    (".5", 110, 124)
]

for name, start, end in subtables:
    print(f"\n=================== Subtable {name} (cols {start} to {end}) ===================")
    sub_df = df.iloc[:, start:end].copy()
    # Rename columns to their actual values in row 0 if row 0 has headers, or just print
    print("Cols:", list(sub_df.columns))
    # Print first 5 non-null rows
    valid_rows = sub_df[sub_df.iloc[:, 0].notna()]
    print(f"Number of non-null rows: {len(valid_rows)}")
    print(valid_rows.head(5).to_string())
