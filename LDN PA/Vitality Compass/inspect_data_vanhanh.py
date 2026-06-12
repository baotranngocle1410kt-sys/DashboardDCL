import pandas as pd
import sys
import os
import glob

# Ensure UTF-8 output
sys.stdout.reconfigure(encoding='utf-8')

# Dynamic search for all .xlsx files in the workspace
workspace_dir = r"C:\Users\Administrator\Desktop\AI 2026"
xlsx_files = []
for root, dirs, files in os.walk(workspace_dir):
    for f in files:
        if f.endswith('.xlsx') and not f.startswith('~$'):
            xlsx_files.append(os.path.join(root, f))

print("Found Excel files:", xlsx_files)

keywords = ['Phó Cơ Điều', 'Đường Huyện 35', 'Chợ Lách', 'Nguyễn Thị Định', 'Long Hồ', 'Trung Thành']

for f in xlsx_files:
    print(f"\n=== File: {os.path.basename(f)} ===")
    try:
        xl = pd.ExcelFile(f)
        for sheet in xl.sheet_names:
            print(f"  Sheet: {sheet}")
            df = xl.parse(sheet, nrows=50) # only read first 50 rows to be fast
            for kw in keywords:
                # search row by row
                for idx, row in df.iterrows():
                    row_str = " | ".join(row.astype(str))
                    if kw in row_str:
                        print(f"    Match [{kw}] in Sheet '{sheet}' Row {idx}: {row_str}")
    except Exception as e:
        print(f"    Error reading {os.path.basename(f)}: {e}")
