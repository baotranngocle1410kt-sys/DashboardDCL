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

print("Unique BCs in Data ĐCL:", len(df_data['Chi tiết'].unique()))
print("Unique BCs in Recruitment:", len(df_bc_hr['Bưu cục'].unique()))

matched = 0
not_matched = []
hr_names_cleaned = {clean_bc_name(name): name for name in df_bc_hr['Bưu cục'].unique()}

for name in df_data['Chi tiết'].unique():
    c_name = clean_bc_name(name)
    if c_name in hr_names_cleaned:
        matched += 1
    else:
        # Try substring match
        sub_match = None
        for hr_c, hr_orig in hr_names_cleaned.items():
            if c_name in hr_c or hr_c in c_name:
                sub_match = hr_orig
                break
        if sub_match:
            matched += 1
        else:
            not_matched.append(name)

print("Matched:", matched)
print("Not matched count:", len(not_matched))
if not_matched:
    print("Not matched list:", not_matched[:10])
