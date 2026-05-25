import pandas as pd
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

f2 = r"C:\Users\Administrator\Desktop\AI 2026\Metor\DCL - Đơn aging _5 ngày.xlsx"

try:
    xl = pd.ExcelFile(f2)
    # Read first sheet
    df_raw = xl.parse('Đơn GIAO aging >5 ngày')
    print("=== Raw Backlog Sheet Info ===")
    print("Shape:", df_raw.shape)
    print("Columns:", list(df_raw.columns))
    print("First 5 rows:\n", df_raw.head(5).to_string())
    
    # Read pivot sheet
    df_pivot = xl.parse('PIVOT')
    print("\n=== PIVOT Sheet Info ===")
    print("Shape:", df_pivot.shape)
    print("First 25 rows:\n", df_pivot.head(25).to_string())
    
except Exception as e:
    print("Error:", e)
