import pandas as pd
import sys
import os

sys.stdout.reconfigure(encoding='utf-8')

p_performance = r"C:\Users\Administrator\Desktop\AI 2026\Metor\DCL - BÁO CÁO VẬN HÀNH.xlsx"
df_data = pd.read_excel(p_performance, sheet_name="Data ĐCL")

# Let's filter for post offices
keywords = ['Phó Cơ Điều', 'Đường Huyện 35', 'Chợ Lách', 'Nguyễn Thị Định', 'Long Hồ', 'Trung Thành']
print("=== Columns ===")
print(list(df_data.columns))

print("\n=== Data Rows ===")
# We want to see unique Time / Time Format values
print("Unique Dates:", df_data['Time Format'].unique())

for kw in keywords:
    matches = df_data[df_data['Chi tiết'].astype(str).str.contains(kw, case=False, na=False)]
    if not matches.empty:
        print(f"\nMatches for keyword '{kw}':")
        print(matches[['Time Format', 'Chi tiết', 'Volume', '% GTC', '% Chuyển trả']].to_string())
