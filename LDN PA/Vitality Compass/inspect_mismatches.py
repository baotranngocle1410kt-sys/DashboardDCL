import pandas as pd
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

p_performance = r"C:\Users\Administrator\Desktop\AI 2026\Metor\DCL - BÁO CÁO VẬN HÀNH.xlsx"
p_hr = r"C:\Users\Administrator\Desktop\AI 2026\Metor\[ĐCL] - BÁO CÁO TUYỂN DỤNG DATA.xlsx"

df_data = pd.read_excel(p_performance, sheet_name="Data ĐCL")
df_hr = pd.read_excel(p_hr, sheet_name="Tổng hợp (T21)")

bc_col_idx = list(df_hr.columns).index('Bưu cục')
df_sub0 = df_hr.iloc[:, bc_col_idx:bc_col_idx+16].copy()
df_bc_hr = df_sub0[(df_sub0['Bưu cục'].notna()) & (df_sub0['Bưu cục'] != 'TỔNG') & (df_sub0['Tỉnh'].notna())]

def clean_bc_name(name):
    if not isinstance(name, str):
        return ""
    name = name.lower()
    name = name.replace("bưu cục", "").replace("bc", "").strip()
    name = re.sub(r'[\s\-]+', ' ', name)
    return name.strip()

print("Recruitment BC names:")
for name in sorted(df_bc_hr['Bưu cục'].unique()):
    print("  ", name)

print("\nData ĐCL BC names:")
for name in sorted(df_data['Chi tiết'].unique()):
    print("  ", name)
