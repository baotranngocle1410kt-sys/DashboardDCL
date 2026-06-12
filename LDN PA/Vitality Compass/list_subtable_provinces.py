import pandas as pd
import sys

sys.stdout.reconfigure(encoding='utf-8')

p_hr = r"C:\Users\Administrator\Desktop\AI 2026\Metor\[ĐCL] - BÁO CÁO TUYỂN DỤNG DATA.xlsx"
df = pd.read_excel(p_hr, sheet_name="Tổng hợp (T21)")

subtables = [
    ("Subtable 0 (VyLNK)", 9, 24),
    ("Subtable 1 (.1)", 50, 65),
    ("Subtable 2 (.2)", 65, 80),
    ("Subtable 3 (.3)", 80, 95),
    ("Subtable 4 (.4)", 95, 110),
    ("Subtable 5 (.5)", 110, 124)
]

for name, start, end in subtables:
    sub_df = df.iloc[:, start:end].copy()
    col_prov = sub_df.columns[1]
    col_am = sub_df.columns[2]
    unique_provs = sub_df[col_prov].dropna().unique().tolist()
    unique_ams = sub_df[col_am].dropna().unique().tolist()
    print(f"\n{name}:")
    print("  Tỉnh:", unique_provs)
    print("  AM:", unique_ams)
