import pandas as pd
import os
import sys

# Ensure UTF-8 output
sys.stdout.reconfigure(encoding='utf-8')

files = [
    r"C:\Users\Administrator\Desktop\AI 2026\Metor\DCL - BÁO CÁO VẬN HÀNH.xlsx",
    r"C:\Users\Administrator\Desktop\AI 2026\Metor\DCL - Đơn aging _5 ngày.xlsx",
    r"C:\Users\Administrator\Desktop\AI 2026\Data Vận hành\Data Vận hành.xlsx"
]

for f in files:
    if not os.path.exists(f):
        print(f"File not found: {f}")
        continue
    print(f"\n=== Searching in: {os.path.basename(f)} ===")
    try:
        xl = pd.ExcelFile(f)
        for sheet in xl.sheet_names:
            df = xl.parse(sheet)
            # Find occurrences of 13.42 or 28.04 or 14.12 or 25.18 or 30.21
            for col in df.columns:
                matches = df[df[col].astype(str).str.contains('13.42|28.04|14.12|25.18|30.21', case=False, na=False)]
                if not matches.empty:
                    print(f"  [GTC Match] Sheet: '{sheet}', Col: '{col}'")
                    print(matches[[col] + [c for c in df.columns if c != col][:3]].head(5))
                    
                matches_bl = df[df[col].astype(str).str.contains('^41$|^9$', na=False)]
                if not matches_bl.empty:
                    for idx, row in matches_bl.iterrows():
                        row_str = " | ".join(row.astype(str))
                        if 'Phó Cơ Điều' in row_str or 'Đường Huyện 35' in row_str or 'Chợ Lách' in row_str or 'Nguyễn Thị Định' in row_str:
                            print(f"  [Backlog Match] Sheet: '{sheet}', Row {idx}: {row_str}")
    except Exception as e:
        print(f"Error in {os.path.basename(f)}: {e}")
