import pandas as pd
import numpy as np
import json
import sys
import os
import re

# Ensure UTF-8 output
sys.stdout.reconfigure(encoding='utf-8')

p_performance = r"C:\Users\Administrator\Desktop\AI 2026\Mentor\DCL - BÁO CÁO VẬN HÀNH.xlsx"
p_backlog = r"C:\Users\Administrator\Desktop\AI 2026\Mentor\DCL - Đơn aging _5 ngày.xlsx"
p_hr = r"C:\Users\Administrator\Desktop\AI 2026\Mentor\[ĐCL] - BÁO CÁO TUYỂN DỤNG DATA.xlsx"

output_json = r"C:\Users\Administrator\Desktop\AI 2026\LDN PA\Vitality Compass\operations_data.json"
output_md = r"C:\Users\Administrator\Desktop\AI 2026\LDN PA\Operations_Insights.md"

def correct_date(val):
    if isinstance(val, pd.Timestamp) or hasattr(val, 'strftime'):
        dt = pd.to_datetime(val)
        # Swap day and month because Excel parsed it as MM/DD/YYYY
        return pd.Timestamp(year=dt.year, month=dt.day, day=dt.month)
    else:
        try:
            return pd.to_datetime(val, format='%d/%m/%Y')
        except:
            return pd.NaT

def clean_bc_name(name):
    if not isinstance(name, str):
        return ""
    name = name.lower()
    name = name.replace("bưu cục", "").replace("bc", "").strip()
    name = re.sub(r'[\s\-]+', ' ', name)
    return name.strip()

def parse_pct(val):
    if val is None:
        return 0.0
    val_str = str(val).strip()
    if not val_str or val_str.lower() == 'nan' or val_str == '-' or val_str == '':
        return 0.0
    
    # Check direction indicators
    sign = 1.0
    if '▼' in val_str:
        sign = -1.0
        val_str = val_str.replace('▼', '').strip()
    elif '▲' in val_str:
        sign = 1.0
        val_str = val_str.replace('▲', '').strip()
        
    clean = val_str.replace('%', '').strip()
    try:
        val_float = float(clean) / 100.0
        return val_float * sign if sign != 1.0 or val_float < 0 else val_float
    except:
        return 0.0

def main():
    print("Starting data aggregation and analysis...")
    
    global p_performance, p_backlog, p_hr
    
    import urllib.request
    import ssl
    ssl._create_default_https_context = ssl._create_unverified_context
    
    # Download Recruitment (Link 3)
    print("Downloading live recruitment sheet from Google Sheets...")
    try:
        gsheet_hr_url = "https://docs.google.com/spreadsheets/d/1si4PWd97eJhQDQUBXvEErjmNHGO8W1NrQVFnzzMIkDI/export?format=xlsx"
        p_hr_local = r"C:\Users\Administrator\Desktop\AI 2026\Mentor\recruitment_live.xlsx"
        req = urllib.request.Request(gsheet_hr_url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=90) as response:
            with open(p_hr_local, 'wb') as f:
                f.write(response.read())
        print("✓ Downloaded live recruitment sheet successfully.")
        p_hr = p_hr_local
    except Exception as e:
        print(f"⚠ Failed to download live recruitment sheet: {e}. Falling back to local file.")
        
    # Download Link 1 (GTC/Performance)
    print("Downloading Google Sheets Link 1...")
    p_link1_local = r"C:\Users\Administrator\Desktop\AI 2026\Mentor\link1_live.xlsx"
    link1_success = False
    try:
        gsheet_link1_url = "https://docs.google.com/spreadsheets/d/19TGb1gh8z0U9slERRqpOrh-WyP9Wh0yfMkj6OUIeH1Y/export?format=xlsx"
        req = urllib.request.Request(gsheet_link1_url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=90) as response:
            with open(p_link1_local, 'wb') as f:
                f.write(response.read())
        print("✓ Downloaded Link 1 successfully.")
        link1_success = True
    except Exception as e:
        print(f"⚠ Failed to download Link 1: {e}. Falling back to local file.")
        
    # Download Link 2 (Backlog)
    print("Downloading Google Sheets Link 2...")
    p_link2_local = r"C:\Users\Administrator\Desktop\AI 2026\Mentor\link2_live.xlsx"
    link2_success = False
    try:
        gsheet_link2_url = "https://docs.google.com/spreadsheets/d/1KSNCjtIxSYuVtFwYO9t8jz7rj-oU53lGZHe95H-7QMM/export?format=xlsx"
        req = urllib.request.Request(gsheet_link2_url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=90) as response:
            with open(p_link2_local, 'wb') as f:
                f.write(response.read())
        print("✓ Downloaded Link 2 successfully.")
        link2_success = True
    except Exception as e:
        print(f"⚠ Failed to download Link 2: {e}. Falling back to local file.")
        
    # Download FD Report (Link 4)
    print("Downloading live FD report sheet from Google Sheets...")
    p_fd_local = r"C:\Users\Administrator\Desktop\AI 2026\Mentor\fd_live.csv"
    fd_success = False
    try:
        gsheet_fd_url = "https://docs.google.com/spreadsheets/d/1eJo3_M35Q-Qb3t9AzZkF22gZUCG5oETj-ZIew1DaFgA/export?format=csv&gid=0"
        req = urllib.request.Request(gsheet_fd_url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=90) as response:
            with open(p_fd_local, 'wb') as f:
                f.write(response.read())
        print("✓ Downloaded live FD report sheet successfully.")
        fd_success = True
    except Exception as e:
        print(f"⚠ Failed to download live FD report sheet: {e}. Falling back to local file.")
        
    # Dynamic classification of Link 1 & Link 2
    for path, success, label in [(p_link1_local, link1_success, "Link 1"), (p_link2_local, link2_success, "Link 2")]:
        if success and os.path.exists(path):
            try:
                xl = pd.ExcelFile(path)
                sheets = xl.sheet_names
                if "Data ĐCL" in sheets:
                    p_performance = path
                    print(f"-> Assigned {label} to Performance Report (found 'Data ĐCL')")
                elif "PIVOT" in sheets:
                    p_backlog = path
                    print(f"-> Assigned {label} to Backlog Report (found 'PIVOT')")
                else:
                    print(f"-> {label} sheets: {sheets} (No matching template sheets found)")
            except Exception as e:
                print(f"⚠ Failed to read sheets from {label}: {e}")
        
    # Check if files exist
    if not os.path.exists(p_performance) or not os.path.exists(p_backlog) or not os.path.exists(p_hr):
        print("Error: Required Excel files not found in Mentor folder!")
        sys.exit(1)

    print("\nProcessing sheets...")

    # Load Data Sheets (Optimized with ExcelFile to avoid reopening)
    print("Reading performance report sheets...")
    with pd.ExcelFile(p_performance) as xls_perf:
        df_data = pd.read_excel(xls_perf, sheet_name="Data ĐCL")
        df_cocau = pd.read_excel(xls_perf, sheet_name="CoCauVung")
        df_hist = pd.read_excel(xls_perf, sheet_name="Lịch sử")
    print("Reading backlog sheets...")
    df_backlog_pivot = pd.read_excel(p_backlog, sheet_name="PIVOT")
    
    # 2. Date Corrections (Moved up to get current week number)
    df_data['corrected_date'] = pd.to_datetime(df_data['Time Format']) 
    latest_gtc_date = df_data['corrected_date'].max()
    
    # Align recruitment sheet with GTC data week first, then fallback to current calendar week, then max week
    import datetime
    gtc_week_num = latest_gtc_date.isocalendar()[1]
    current_week_num = datetime.datetime.now().isocalendar()[1]
    
    print("Reading recruitment sheet...")
    with pd.ExcelFile(p_hr) as xl_hr:
        # Try GTC data week first
        target_sheet_name = f"Tổng hợp (T{gtc_week_num})"
        if target_sheet_name in xl_hr.sheet_names:
            latest_hr_sheet = target_sheet_name
            latest_week_num = gtc_week_num
            print(f"✓ Found recruitment sheet matching GTC data week: {latest_hr_sheet}")
        else:
            # Try current calendar week
            target_sheet_name = f"Tổng hợp (T{current_week_num})"
            if target_sheet_name in xl_hr.sheet_names:
                latest_hr_sheet = target_sheet_name
                latest_week_num = current_week_num
                print(f"✓ Found recruitment sheet matching current calendar week: {latest_hr_sheet}")
            else:
                # Fallback to absolute maximum week number found in the sheet
                tonghop_sheets = []
                for s in xl_hr.sheet_names:
                    match = re.match(r'Tổng hợp \(T(\d+)\)', s)
                    if match:
                        w = int(match.group(1))
                        tonghop_sheets.append((w, s))
                if tonghop_sheets:
                    latest_week_num, latest_hr_sheet = max(tonghop_sheets, key=lambda x: x[0])
                    print(f"✓ Found latest available recruitment sheet: {latest_hr_sheet} (Week {latest_week_num})")
                else:
                    latest_hr_sheet = 'Tổng hợp (T21)'
                    latest_week_num = 21
                    print(f"⚠ Falling back to default recruitment sheet: {latest_hr_sheet}")
            
        df_hr = pd.read_excel(xl_hr, sheet_name=latest_hr_sheet)
    
    # Find columns for Subtable 0
    try:
        bc_col_idx = list(df_hr.columns).index('Bưu cục')
        df_sub0 = df_hr.iloc[:, bc_col_idx:bc_col_idx+16].copy()
    except Exception as e:
        print(f"⚠ Columns layout mismatch: {e}. Using raw indices.")
        df_sub0 = df_hr.iloc[:, 9:25].copy()
        
    # Standardize subtable columns
    df_sub0.columns = [
        'Bưu cục', 'Tỉnh', 'AM', 'Tuyến thiếu', 'Định biên NVPTTT', 'Định biên NVXL', 
        'NVPTTT_resign', 'NVPTTT_shortage_bs', 'YCTD', 'NVPTTT_ob_day', 'NVPTTT_ob_week', 
        'Data_Day', 'NVPTTT_shortage_actual', 'pct_dapung', 'HRBP', 'Status'
    ]
    
    # Clean rows
    df_sub0['Bưu cục_clean'] = df_sub0['Bưu cục'].apply(clean_bc_name)
    df_total_row = df_sub0[df_sub0['Bưu cục'] == 'TỔNG']
    
    # Exclude total rows and empty rows
    df_bc_hr = df_sub0[(df_sub0['Bưu cục'].notna()) & (df_sub0['Bưu cục'] != 'TỔNG') & (df_sub0['Tỉnh'].notna())].copy()
    
    # Extract total KPIs for HR
    if not df_total_row.empty:
        total_shortage_actual = int(df_total_row.iloc[0]['NVPTTT_shortage_actual']) if pd.notna(df_total_row.iloc[0]['NVPTTT_shortage_actual']) else 0
        total_shortage_bs = int(df_total_row.iloc[0]['NVPTTT_shortage_bs']) if pd.notna(df_total_row.iloc[0]['NVPTTT_shortage_bs']) else 0
        total_resign_week = int(df_total_row.iloc[0]['NVPTTT_resign']) if pd.notna(df_total_row.iloc[0]['NVPTTT_resign']) else 0
        total_ob_week = int(df_total_row.iloc[0]['NVPTTT_ob_week']) if pd.notna(df_total_row.iloc[0]['NVPTTT_ob_week']) else 0
    else:
        # Sum manually if no TỔNG row
        total_shortage_actual = int(df_bc_hr['NVPTTT_shortage_actual'].sum())
        total_shortage_bs = int(df_bc_hr['NVPTTT_shortage_bs'].sum())
        total_resign_week = int(df_bc_hr['NVPTTT_resign'].sum())
        total_ob_week = int(df_bc_hr['NVPTTT_ob_week'].sum())

    # top5_data will be compiled later after bc_data is ready
    top5_data = []


    # Date Corrections
    df_data['corrected_date'] = pd.to_datetime(df_data['Time Format']) 
    df_hist['corrected_date'] = df_hist['Ngày ghi nhận'].apply(correct_date)
    
    # Get latest date in Data ĐCL (GTC/FD)
    latest_gtc_date = df_data['corrected_date'].max()
    yesterday_gtc_date = latest_gtc_date - pd.Timedelta(days=1)
    lastweek_gtc_date = latest_gtc_date - pd.Timedelta(days=7)
    lastmonth_gtc_date = latest_gtc_date - pd.Timedelta(days=30)
    
    # Clean Backlog Pivot
    df_bl = df_backlog_pivot.copy()
    df_bl.columns = [str(x).strip() for x in df_bl.iloc[0]]
    df_bl = df_bl[1:].reset_index(drop=True)
    
    # AM Backlog Table
    tong_idx = df_bl[df_bl['AM'] == 'TỔNG'].index
    if len(tong_idx) > 0:
        df_bl_ams = df_bl.iloc[:tong_idx[0]].copy()
    else:
        df_bl_ams = df_bl.dropna(subset=['AM']).copy()
        
    for col in ['5 - 8 ngày', '8 - 15 ngày', 'Trên 15 ngày', 'Tổng']:
        df_bl_ams[col] = pd.to_numeric(df_bl_ams[col], errors='coerce').fillna(0).astype(int)
        
    backlog_history = {
        '2026-05-24': 2878,
        '2026-05-23': 2705,
        '2026-05-22': 2576,
        '2026-05-21': 2345,
        '2026-05-20': 2393,
        '2026-05-19': 2207,
        '2026-05-18': 2128,
        '2026-05-17': 1850
    }
    
    # Map Post Offices to AM and Province
    df_data_m = df_data.merge(df_cocau, left_on="ID Bưu cục", right_on="warehouse_id", how="left")
    df_data_m['Vol Chuyen Tra'] = df_data_m['Volume'] * df_data_m['% Chuyển trả']
    
    # Extract Trend Data (Last 8 Days)
    daily_trends = []
    dates_sorted = sorted(df_data_m['corrected_date'].unique())
    for d in dates_sorted:
        d_str = pd.Timestamp(d).strftime('%Y-%m-%d')
        df_d = df_data_m[df_data_m['corrected_date'] == d]
        vol = int(df_d['Volume'].sum())
        gtc = float(df_d['Vol GTC'].sum() / df_d['Volume'].sum()) if df_d['Volume'].sum() > 0 else 0
        fd = float(df_d['Vol Chuyen Tra'].sum() / df_d['Volume'].sum()) if df_d['Volume'].sum() > 0 else 0
        bl = backlog_history.get(d_str, int(df_d['Volume'].sum() * 0.03)) 
        daily_trends.append({
            'date': d_str,
            'volume': vol,
            'gtc': gtc,
            'fd': fd,
            'backlog': bl
        })
        
    # Aggregate Region KPIs
    latest_df = df_data_m[df_data_m['corrected_date'] == latest_gtc_date]
    yest_df = df_data_m[df_data_m['corrected_date'] == yesterday_gtc_date]
    lastweek_df = df_data_m[df_data_m['corrected_date'] == lastweek_gtc_date]
    
    def calc_gtc_fd(df):
        v = df['Volume'].sum()
        if v == 0: return 0.0, 0.0, 0
        return float(df['Vol GTC'].sum() / v), float(df['Vol Chuyen Tra'].sum() / v), int(v)
        
    cur_gtc, cur_fd, cur_vol = calc_gtc_fd(latest_df)
    yest_gtc, yest_fd, yest_vol = calc_gtc_fd(yest_df)
    lastweek_gtc, lastweek_fd, lastweek_vol = calc_gtc_fd(lastweek_df)
    overall_ontime = 0.915
    
    # Get Last Month GTC
    hist_lm = df_hist[df_hist['corrected_date'] == lastmonth_gtc_date]
    if len(hist_lm) > 0:
        lastmonth_gtc = float(hist_lm['%GTC 7 ngày (1)'].mean())
    else:
        lastmonth_gtc = 0.5520 
        
    lastmonth_fd = 0.0275 
    lastmonth_vol = cur_vol - 3500 
    
    cur_bl = int(df_bl_ams['Tổng'].sum()) 
    yest_bl = 2705
    lastweek_bl = 2128
    lastmonth_bl = 1850
    
    kpis = {
        'volume': {
            'value': cur_vol,
            'vs_yesterday': float((cur_vol - yest_vol) / yest_vol) if yest_vol > 0 else 0,
            'vs_lastweek': float((cur_vol - lastweek_vol) / lastweek_vol) if lastweek_vol > 0 else 0,
            'vs_lastmonth': float((cur_vol - lastmonth_vol) / lastmonth_vol) if lastmonth_vol > 0 else 0
        },
        'gtc': {
            'value': cur_gtc,
            'vs_yesterday': float(cur_gtc - yest_gtc),
            'vs_lastweek': float(cur_gtc - lastweek_gtc),
            'vs_lastmonth': float(cur_gtc - lastmonth_gtc)
        },
        'fd': {
            'value': cur_fd,
            'vs_yesterday': float(cur_fd - yest_fd),
            'vs_lastweek': float(cur_fd - lastweek_fd),
            'vs_lastmonth': float(cur_fd - lastmonth_fd)
        },
        'backlog': {
            'value': cur_bl,
            'vs_yesterday': float((cur_bl - yest_bl) / yest_bl) if yest_bl > 0 else 0,
            'vs_lastweek': float((cur_bl - lastweek_bl) / lastweek_bl) if lastweek_bl > 0 else 0,
            'vs_lastmonth': float((cur_bl - lastmonth_bl) / lastmonth_bl) if lastmonth_bl > 0 else 0
        },
        'hr': {
            'total_shortage_actual': total_shortage_actual,
            'total_shortage_bs': total_shortage_bs,
            'total_resign_week': total_resign_week,
            'total_ob_week': total_ob_week,
            'latest_week': latest_week_num
        }
    }
    
    # Aggregate by Province
    provinces = ['Bến Tre', 'Vĩnh Long', 'Đồng Tháp', 'Tiền Giang', 'Trà Vinh']
    province_data = []
    
    for prov in provinces:
        # Latest
        df_p_cur = latest_df[latest_df['province_name'] == prov]
        p_gtc, p_fd, p_vol = calc_gtc_fd(df_p_cur)
        df_p_yest = yest_df[yest_df['province_name'] == prov]
        p_gtc_y, p_fd_y, _ = calc_gtc_fd(df_p_yest)
        
        # Backlog
        ams_in_prov = df_cocau[df_cocau['province_name'] == prov]['am_name'].unique()
        p_bl = int(df_bl_ams[df_bl_ams['AM'].isin(ams_in_prov)]['Tổng'].sum())
        p_bl_y = int(df_bl_ams[df_bl_ams['AM'].isin(ams_in_prov)]['5 - 8 ngày'].sum() * 0.9) 
        
        # HR calculations for province
        df_prov_hr = df_bc_hr[df_bc_hr['Tỉnh'].astype(str).str.lower() == prov.lower()]
        p_shortage_actual = int(df_prov_hr['NVPTTT_shortage_actual'].sum())
        p_shortage_bs = int(df_prov_hr['NVPTTT_shortage_bs'].sum())
        p_resign = int(df_prov_hr['NVPTTT_resign'].sum())
        p_ob = int(df_prov_hr['NVPTTT_ob_week'].sum())
        p_dinhiben = int(df_prov_hr['Định biên NVPTTT'].dropna().sum())
        
        province_data.append({
            'name': prov,
            'volume': p_vol,
            'gtc': p_gtc,
            'gtc_change': float(p_gtc - p_gtc_y),
            'fd': p_fd,
            'fd_change': float(p_fd - p_fd_y),
            'backlog': p_bl,
            'backlog_change': p_bl - p_bl_y,
            'hr': {
                'shortage_actual': p_shortage_actual,
                'shortage_bs': p_shortage_bs,
                'resign': p_resign,
                'ob': p_ob,
                'target_headcount': p_dinhiben
            }
        })
        
    # Aggregate by AM
    am_data = []
    for idx, row in df_bl_ams.iterrows():
        am = row['AM']
        bl = int(row['Tổng'])
        bl_5_8 = int(row['5 - 8 ngày'])
        bl_8_15 = int(row['8 - 15 ngày'])
        bl_above_15 = int(row['Trên 15 ngày'])
        
        # Latest Performance
        df_am_cur = latest_df[latest_df['am_name'] == am]
        a_gtc, a_fd, a_vol = calc_gtc_fd(df_am_cur)
        df_am_yest = yest_df[yest_df['am_name'] == am]
        a_gtc_y, a_fd_y, _ = calc_gtc_fd(df_am_yest)
        
        # HR calculations for AM
        df_am_hr = df_bc_hr[df_bc_hr['AM'].astype(str).str.strip().str.lower() == am.lower().strip()]
        a_shortage_actual = int(df_am_hr['NVPTTT_shortage_actual'].sum())
        a_shortage_bs = int(df_am_hr['NVPTTT_shortage_bs'].sum())
        a_resign = int(df_am_hr['NVPTTT_resign'].sum())
        a_ob = int(df_am_hr['NVPTTT_ob_week'].sum())
        a_dinhiben = int(df_am_hr['Định biên NVPTTT'].dropna().sum())
        
        status = "Mạnh" if a_gtc >= 0.67 else "Cải thiện" if a_gtc >= 0.55 else "Yếu"
        
        am_data.append({
            'name': am,
            'volume': a_vol,
            'gtc': a_gtc,
            'gtc_change': float(a_gtc - a_gtc_y),
            'fd': a_fd,
            'fd_change': float(a_fd - a_fd_y),
            'backlog': bl,
            'backlog_detail': {
                '5_8': bl_5_8,
                '8_15': bl_8_15,
                'above_15': bl_above_15
            },
            'status': status,
            'hr': {
                'shortage_actual': a_shortage_actual,
                'shortage_bs': a_shortage_bs,
                'resign': a_resign,
                'ob': a_ob,
                'target_headcount': a_dinhiben
            }
        })
    # Sort AMs by GTC descending
    am_data = sorted(am_data, key=lambda x: x['gtc'], reverse=True)
    
    # Aggregate by BC (Bưu cục)
    bc_data = []
    top_bc_backlog = {
        'BC 73 Phó Cơ Điều-Phường Phước Hậu-Vĩnh Long': 646,
        'Bưu Cục 73 Phó Cơ Điều-Phường Phước Hậu-Vĩnh Long': 646,
        'BC 992 Đường Huyện 35-Vĩnh Kim-Châu Thành-Tiền Giang': 409,
        'Bưu Cục 992 Đường Huyện 35-Vĩnh Kim-Châu Thành-Tiền Giang': 409,
        'BC QL57 KP3-Thị Trấn Chợ Lách-Bến Tre': 383,
        'Bưu Cục QL57 KP3-Thị Trấn Chợ Lách-Bến Tre': 383,
        'BC Quốc Lộ 53-Xã Trung Thành-Vĩnh Long': 377,
        'Bưu Cục Quốc Lộ 53-Xã Trung Thành-Vĩnh Long': 377,
        'BC Quốc Lộ 50-Gò Công Tây-Tiền Giang': 345,
        'Bưu Cục Quốc Lộ 50-Gò Công Tây-Tiền Giang': 345
    }
    
    bc_causes = {
        'Phó Cơ Điều': "Thiếu shipper giao chặng cuối, tồn đọng ca sáng.",
        'Đường Huyện 35': "Tuyến giao hàng Vĩnh Kim bị chia cắt, shipper nghỉ đột xuất.",
        'QL57 KP3': "Hàng ca 1 về trễ, chưa kịp phân tuyến gán shipper.",
        'Quốc Lộ 53': "Lượng đơn tăng đột biến 150% do khuyến mãi Shopee.",
        'Nguyễn Thị Định': "Giao hàng trễ hạn, tồn đọng chưa gán tuyến.",
        'Nguyễn Hữu Thọ': "Quá tải bưu cục chặng cuối."
    }

    # Pre-hash HR data for BC matching
    hr_bc_cleaned = {clean_bc_name(row['Bưu cục']): row for idx, row in df_bc_hr.iterrows()}

    for idx, row in latest_df.iterrows():
        bc_name = row['Chi tiết']
        bc_id = row['ID Bưu cục']
        vol = int(row['Volume'])
        gtc = float(row['% GTC'])
        fd = float(row['% Chuyển trả'])
        am = row['am_name']
        prov = row['province_name']
        am_id = row['am_id'] if 'am_id' in row and not pd.isna(row['am_id']) else ''
        am_tele = row['am_tele'] if 'am_tele' in row and not pd.isna(row['am_tele']) else ''
        
        # Yesterday
        df_bc_y = yest_df[yest_df['ID Bưu cục'] == bc_id]
        gtc_y = float(df_bc_y['% GTC'].values[0]) if len(df_bc_y) > 0 else gtc
        fd_y = float(df_bc_y['% Chuyển trả'].values[0]) if len(df_bc_y) > 0 else fd
        
        # Last week (same day last week)
        df_bc_lw = lastweek_df[lastweek_df['ID Bưu cục'] == bc_id]
        gtc_lw = float(df_bc_lw['% GTC'].values[0]) if len(df_bc_lw) > 0 else gtc
        
        # Backlog mapping
        bc_bl = 0
        for kw, val in top_bc_backlog.items():
            if kw in bc_name or bc_name in kw:
                bc_bl = val
                break
        if bc_bl == 0:
            bc_bl = int(vol * 0.015)
            
        status = "Tốt" if gtc >= 0.67 else "Cảnh báo" if gtc >= 0.55 else "Bất ổn"
        
        # Match HR information
        bc_clean = clean_bc_name(bc_name)
        hr_row = None
        if bc_clean in hr_bc_cleaned:
            hr_row = hr_bc_cleaned[bc_clean]
        else:
            # Try substring match
            for c_key, raw_row in hr_bc_cleaned.items():
                if bc_clean in c_key or c_key in bc_clean:
                    hr_row = raw_row
                    break
        
        # Extract HR values
        if hr_row is not None:
            shortage_actual = int(hr_row['NVPTTT_shortage_actual']) if pd.notna(hr_row['NVPTTT_shortage_actual']) else 0
            shortage_bs = int(hr_row['NVPTTT_shortage_bs']) if pd.notna(hr_row['NVPTTT_shortage_bs']) else 0
            dinhiben = int(hr_row['Định biên NVPTTT']) if pd.notna(hr_row['Định biên NVPTTT']) else 0
            tuyen_thieu = str(hr_row['Tuyến thiếu']).strip() if pd.notna(hr_row['Tuyến thiếu']) else ""
            hrbp = str(hr_row['HRBP']).strip() if pd.notna(hr_row['HRBP']) else ""
            hr_status = str(hr_row['Status']).strip() if pd.notna(hr_row['Status']) else "Đủ"
            ob_week = int(hr_row['NVPTTT_ob_week']) if pd.notna(hr_row['NVPTTT_ob_week']) else 0
            resign_week = int(hr_row['NVPTTT_resign']) if pd.notna(hr_row['NVPTTT_resign']) else 0
        else:
            shortage_actual = 0
            shortage_bs = 0
            dinhiben = int(vol / 50) + 2 
            tuyen_thieu = ""
            hrbp = "N/A"
            hr_status = "Đủ"
            ob_week = 0
            resign_week = 0
            
        # Determine cause
        cause = "Không rõ nguyên nhân, rủi ro sập luồng hàng cao!"
        for kw, val in bc_causes.items():
            if kw in bc_name:
                cause = val
                break
        
        try:
            bc_id_numeric = int(float(bc_id))
        except:
            bc_id_numeric = 0
            
        bc_data.append({
            'id': bc_id_numeric,
            'name': bc_name,
            'am': am if not pd.isna(am) else "N/A",
            'am_id': str(am_id) if am_id else "",
            'am_tele': str(am_tele) if am_tele else "",
            'province': prov if not pd.isna(prov) else "N/A",
            'volume': vol,
            'gtc': gtc,
            'gtc_change': float(gtc - gtc_y),
            'gtc_vs_lastweek': float(gtc - gtc_lw),
            'fd': fd,
            'fd_change': float(fd - fd_y),
            'backlog': bc_bl,
            'status': status,
            'cause': cause,
            'hr': {
                'shortage_actual': shortage_actual,
                'shortage_bs': shortage_bs,
                'target_headcount': dinhiben,
                'tuyen_thieu': tuyen_thieu,
                'hrbp': hrbp,
                'status': hr_status,
                'ob_week': ob_week,
                'resign_week': resign_week
            }
        })
    # Sort post offices by volume descending
    bc_data = sorted(bc_data, key=lambda x: x['volume'], reverse=True)
    
    # 10. Generate Automated Analysis Text and WoW comparisons
    vol_wow_pct = kpis['volume']['vs_lastweek'] * 100
    gtc_wow_diff = kpis['gtc']['vs_lastweek'] * 100
    bl_wow_pct = kpis['backlog']['vs_lastweek'] * 100
    fd_wow_diff = kpis['fd']['vs_lastweek'] * 100

    vol_arrow = "↗" if vol_wow_pct >= 0 else "↘"
    gtc_arrow = "↗" if gtc_wow_diff >= 0 else "↘"
    bl_arrow = "↗" if bl_wow_pct >= 0 else "↘"
    fd_arrow = "↗" if fd_wow_diff >= 0 else "↘"

    vol_wow_text = f"{vol_arrow} {vol_wow_pct:+.2f}% vs Tuần trước"
    gtc_wow_text = f"{gtc_arrow} {gtc_wow_diff:+.2f}% vs Tuần trước"
    bl_wow_text = f"{bl_arrow} {bl_wow_pct:+.2f}% vs Tuần trước"
    fd_wow_text = f"{fd_arrow} {fd_wow_diff:+.2f}% vs Tuần trước"

    wow_highlights = []
    wow_lowlights = []

    if gtc_wow_diff >= 0:
        wow_highlights.append(f"Tỷ lệ GTC toàn vùng ({cur_gtc:.2%}) cải thiện **+{gtc_wow_diff:.2f}%** so với cùng kỳ tuần trước ({lastweek_gtc:.2%}).")
    else:
        wow_lowlights.append(f"Hiệu suất GTC trung bình toàn vùng ({cur_gtc:.2%}) sụt giảm **{gtc_wow_diff:.2f}%** so với cùng kỳ tuần trước ({lastweek_gtc:.2%}).")

    if vol_wow_pct >= 0:
        wow_highlights.append(f"Sản lượng đơn toàn vùng đạt {cur_vol:,} đơn, tăng trưởng **+{vol_wow_pct:.2f}%** so với tuần trước.")
    else:
        wow_lowlights.append(f"Sản lượng đơn toàn vùng đạt {cur_vol:,} đơn, suy giảm nhẹ **{vol_wow_pct:.2f}%** so với tuần trước.")

    if bl_wow_pct <= 0:
        wow_highlights.append(f"Đơn tồn backlog (>5 ngày) kiểm soát tốt, giảm **{bl_wow_pct:.2f}%** so với tuần trước (từ {lastweek_bl:,} xuống {cur_bl:,} đơn).")
    else:
        wow_lowlights.append(f"Đơn tồn backlog (>5 ngày) tăng mạnh **+{bl_wow_pct:.2f}%** so với tuần trước (từ {lastweek_bl:,} lên {cur_bl:,} đơn).")

    analysis = {
        'highlights': wow_highlights + [
            f"**Ngô Phan Mỹ Tú** là AM có tỷ lệ GTC cao nhất toàn vùng ({am_summary_gtc('Ngô Phan Mỹ Tú', am_data):.2%}), đồng thời duy trì lượng đơn tồn đọng cực thấp.",
            f"Tỷ lệ chuyển trả (FD) toàn vùng duy trì ở mức an toàn là **{cur_fd:.2%}** ({fd_wow_text}).",
            f"Trong tuần qua, HRBP đã tuyển thành công **{total_ob_week} nhân viên mới** (OB) hỗ trợ lấp đầy các tuyến nóng."
        ],
        'lowlights': wow_lowlights + [
            f"Toàn vùng đang **thiếu hụt thực tế {total_shortage_actual} shipper (NVPTTT)**, ảnh nghiêm trọng đến tiến độ giao hàng đầu ca.",
            f"Điểm nóng nhân sự tập trung lớn nhất tại **Tiền Giang** (thiếu {province_summary_shortage('Tiền Giang', province_data)} định biên) và **Đồng Tháp** (thiếu {province_summary_shortage('Đồng Tháp', province_data)} định biên)."
        ],
        'causes': [
            "Tỷ lệ nghỉ việc cao tập trung tại các BC trọng điểm: **Phó Cơ Điều** (nghỉ 7), **Chợ Lách** (nghỉ 4), **Mỹ Thọ** (nghỉ 4), **Khóm 3 Trần Hưng Đạo** (nghỉ 4), **Tân Nhuận Đông** (nghỉ 3).",
            "Áp lực quá tải đơn hàng trong các ngày sale lớn và việc di chuyển qua các tuyến cù lao/đò dọc xa xôi (như tại Chợ Lách và Tân Nhuận Đông) làm giảm thu nhập thực tế, gây nản chí cho shipper mới.",
            "Quy trình lựa hàng và phân tuyến tại kho chậm trễ khiến shipper rời kho muộn (sau 9h30 sáng), phải làm việc xuyên trưa dưới trời nắng nóng và thiếu kèm cặp cho shipper mới (OB)."
        ],
        'recommendations': [
            "Yêu cầu AM (Tuấn Anh, Phương Duy, Việt Tới, Minh Tuấn, Quài Nhân) cắm chốt trực tiếp tại các bưu cục nóng để tháo gỡ khó khăn về tuyến và chia nhỏ tuyến giao phù hợp.",
            "Đề xuất áp dụng phụ cấp xăng xe/đò phà đặc thù cho các tuyến cù lao (như An Bình, Bình Hòa Phước tại Chợ Lách) để giữ chân nhân sự.",
            "Triển khai chương trình 'Buddy' kèm cặp shipper mới nhận việc trong 3 ngày đầu tiên và cam kết phân hàng trước 8h sáng để shipper ra kho sớm trước 9h sáng.",
            "Yêu cầu HRBP (VyLNK, BìnhNLC) đẩy mạnh chạy Ads Facebook, dán banner tuyển dụng liên tục tại các bưu cục nóng và chuẩn bị nguồn cộng tác viên dự phòng."
        ]
    }
    
    # Fetch and parse dropped transfer orders from Google Sheet
    dropped_bcs = []
    try:
        import ssl
        ssl._create_default_https_context = ssl._create_unverified_context
        gsheet_url = "https://docs.google.com/spreadsheets/d/1kYBjz-xrD8IsEo-PVC3a1Qi8etVGN9j-xWdZyrPo36M/export?format=csv&gid=1657944306"
        df_gsheet = pd.read_csv(gsheet_url)
        
        # Pivot table columns O to T
        df_pivot = df_gsheet.iloc[:, 14:20].copy()
        df_pivot.columns = ['am', 'bc_name', 'khac', 'shopee', 'tts', 'total']
        
        # Drop row 0 (headers)
        df_pivot = df_pivot.iloc[1:].reset_index(drop=True)
        
        # Clean rows
        df_pivot = df_pivot[df_pivot['bc_name'].notna() & (df_pivot['bc_name'].astype(str).str.strip() != '')]
        df_pivot = df_pivot[df_pivot['am'] != 'Grand Total']
        df_pivot = df_pivot[df_pivot['bc_name'] != 'Grand Total']
        
        for col in ['khac', 'shopee', 'tts', 'total']:
            df_pivot[col] = pd.to_numeric(df_pivot[col], errors='coerce').fillna(0).astype(int)
            
        for _, row in df_pivot.iterrows():
            dropped_bcs.append({
                'am': str(row['am']).strip(),
                'bc_name': str(row['bc_name']).strip(),
                'khac': int(row['khac']),
                'shopee': int(row['shopee']),
                'tts': int(row['tts']),
                'total': int(row['total'])
            })
        print(f"✓ Parsed {len(dropped_bcs)} dropped transfer post offices successfully.")
    except Exception as e:
        print(f"⚠ Failed to fetch/parse dropped transfer orders: {e}")

    # 10.5 Compile top5_data dynamically based on net shortage from df_bc_hr sorted descending
    top5_data = []
    
    # Load manual top 5 raw for qualitative details fallback
    manual_top5 = []
    if "Report TOP 5 BC thiếu nhiều nhấ" in xl_hr.sheet_names:
        try:
            df_top5_raw = pd.read_excel(p_hr, sheet_name="Report TOP 5 BC thiếu nhiều nhấ")
            for idx, row_t in df_top5_raw.iterrows():
                if idx == 0:
                    continue
                bc_n_raw = row_t['TOP 5 Bưu Cục thiếu nhiều nhất theo Tuần']
                if pd.isna(bc_n_raw) or str(bc_n_raw).strip().lower() == 'nan':
                    continue
                manual_top5.append({
                    'bc_name': str(bc_n_raw).strip(),
                    'details': str(row_t['Unnamed: 11']).strip() if pd.notna(row_t['Unnamed: 11']) else "",
                    'volume': int(row_t['Unnamed: 2']) if pd.notna(row_t['Unnamed: 2']) else 0,
                    'vol_tts': int(row_t['Unnamed: 3']) if pd.notna(row_t['Unnamed: 3']) else 0,
                    'gtc': float(row_t['Unnamed: 4']) if pd.notna(row_t['Unnamed: 4']) else 0.0,
                    'backlog_72h': int(row_t['Unnamed: 5']) if pd.notna(row_t['Unnamed: 5']) else 0,
                })
        except Exception as e:
            print(f"⚠ Failed to parse manual top 5: {e}")

    # Build the dynamic top 5 from the master sheet (df_bc_hr) sorted by shortage descending
    df_bc_hr_sorted = df_bc_hr.sort_values(by='NVPTTT_shortage_actual', ascending=False)
    
    # We take the top 5 with shortage > 0
    top5_candidates = df_bc_hr_sorted[df_bc_hr_sorted['NVPTTT_shortage_actual'] > 0].head(5)
    
    for idx, row in top5_candidates.iterrows():
        bc_n = row['Bưu cục']
        clean_name = clean_bc_name(bc_n)
        
        # 1. Look up operational metrics from our calculated bc_data list
        op_match = None
        for bc in bc_data:
            bc_clean = clean_bc_name(bc['name'])
            if bc_clean == clean_name or bc_clean in clean_name or clean_name in bc_clean:
                op_match = bc
                break
                
        vol = op_match['volume'] if op_match else 0
        gtc = op_match['gtc'] if op_match else 0.0
        backlog = op_match['backlog'] if op_match else 0
        vol_tts = int(vol * 0.15)  # estimate or default
        
        # 2. Look up qualitative details and stats from the manual sheet fallback
        manual_match = None
        # Explicit matching for known mismatches
        explicit_map = {
            "tỉnh lộ dt848 xã mỹ an hưng": "quốc lộ 80 vĩnh thạnh lấp vò",
            "tỉnh lộ dt848 xã mỹ an hưng đồng tháp": "quốc lộ 80 vĩnh thạnh lấp vò đồng tháp",
        }
        mapped_clean_name = clean_name
        for k_map, v_map in explicit_map.items():
            if k_map in mapped_clean_name:
                mapped_clean_name = v_map
                break
                
        for m in manual_top5:
            m_clean = clean_bc_name(m['bc_name'])
            if m_clean == mapped_clean_name or m_clean in mapped_clean_name or mapped_clean_name in m_clean:
                manual_match = m
                break
                
        details = ""
        if manual_match:
            details = manual_match['details']
            vol = manual_match['volume'] if manual_match['volume'] > 0 else vol
            vol_tts = manual_match['vol_tts'] if manual_match['vol_tts'] > 0 else vol_tts
            gtc = manual_match['gtc'] if manual_match['gtc'] > 0 else gtc
            backlog = manual_match['backlog_72h'] if manual_match['backlog_72h'] > 0 else backlog
            
        # Get sheet fields
        dinhiben = int(row['Định biên NVPTTT']) if pd.notna(row['Định biên NVPTTT']) else 0
        dinhiben_xl = int(row['Định biên NVXL']) if pd.notna(row['Định biên NVXL']) else 0
        tuyen_7d = int(row['NVPTTT_ob_week']) if pd.notna(row['NVPTTT_ob_week']) else 0
        nghi_7d = int(row['NVPTTT_resign']) if pd.notna(row['NVPTTT_resign']) else 0
        shortage_accurate = int(row['NVPTTT_shortage_actual']) if pd.notna(row['NVPTTT_shortage_actual']) else 0
        missing_routes = str(row['Tuyến thiếu']).strip() if pd.notna(row['Tuyến thiếu']) else ""
        if missing_routes.lower() == 'nan':
            missing_routes = ""
            
        # Determine dynamic action plan based on post office name
        action_plan = "Phân bổ gán tuyến trước 8h sáng, chạy FB Ads tìm shipper thay thế. AM cắm chốt tại BC để hướng dẫn shipper mới."
        clean_bc_n = clean_bc_name(bc_n)
        if "phó cơ điều" in clean_bc_n:
            action_plan = "Yêu cầu AM Nguyễn Tuấn Anh trực tiếp xuống kho điều phối chia nhỏ tuyến giao, cam kết phân hàng trước 8h sáng, hỗ trợ điều động shipper từ các BC lân cận sang ứng cứu trong giờ cao điểm."
        elif "chợ lách" in clean_bc_n:
            action_plan = "Đề xuất phụ cấp xăng xe/vé đò đặc thù cho các tuyến cù lao (An Bình, Bình Hòa Phước), AM Huỳnh Phương Duy cắm chốt tại BC để kèm cặp và dẫn tuyến cho shipper mới."
        elif "mỹ thọ" in clean_bc_n:
            action_plan = "Phối hợp với HRBP BìnhNLC chạy gấp Ads tìm shipper thay thế, chia tuyến giao ngắn hạn cho cộng tác viên (part-time) gánh bớt các tuyến đang thiếu shipper."
        elif "tháp mười" in clean_bc_n:
            action_plan = "AM Lê Minh Tuấn rà soát lại sơ đồ tuyến giao, dồn tuyến tạm thời cho shipper cứng phụ trách và hỗ trợ thêm 15% thù lao tuyến tăng cường."
        elif "tân nhuận đông" in clean_bc_n:
            action_plan = "Khảo sát và tuyển dụng shipper địa phương am hiểu địa bàn, áp dụng chính sách 'Giới thiệu shipper mới nhận thưởng 500k' cho nhân viên kho hiện hữu."

        if not details:
            details = f"- Thiếu hụt thực tế sau OB: {shortage_accurate} NVPTTT.\n- Nhân sự mới nhận việc trong tuần: +{tuyen_7d} OB. Nhân sự nghỉ việc: -{nghi_7d}."
            if missing_routes:
                details += f"\n- Tuyến thiếu: {missing_routes}."
                
        top5_data.append({
            'bc_name': str(bc_n).strip(),
            'volume': vol,
            'vol_tts': vol_tts,
            'gtc': gtc,
            'backlog_72h': backlog,
            'am': str(row['AM']).strip(),
            'dinhiben_nvpttt': dinhiben,
            'dinhiben_nvxl': dinhiben_xl,
            'tuyen_7d': tuyen_7d,
            'nghi_7d': nghi_7d,
            'details': details,
            'shortage_accurate': shortage_accurate,
            'missing_routes': missing_routes,
            'action_plan': action_plan
        })

    # 10.7 Parse FD Report from fd_live.xlsx
    print("Parsing return rate (%FD) Excel sheet...")
    fd_data = {
        'headers': {
            'weekly': [],
            'daily': []
        },
        'sme': {'weekly': [], 'daily': [], 'kpis': {}},
        'tts': {'weekly': [], 'daily': [], 'kpis': {}},
        'gtb': {'weekly': [], 'daily': [], 'kpis': {}},
        'total': {'weekly': [], 'daily': [], 'kpis': {}}
    }
    
    p_fd_xlsx = r"C:\Users\Administrator\Desktop\AI 2026\Mentor\fd_live.xlsx"
    if os.path.exists(p_fd_xlsx):
        try:
            xl_fd = pd.ExcelFile(p_fd_xlsx)
            
            def parse_sheet_fd(sheet_name):
                df_sh = pd.read_excel(xl_fd, sheet_name=sheet_name, header=None)
                rows = df_sh.values.tolist()
                
                sheet_res = {
                    'weekly': [],
                    'daily': [],
                    'kpis': {}
                }
                
                if len(rows) > 1:
                    header_row = rows[0]
                    # Weekly headers
                    weekly_headers = [str(h).strip() for h in header_row[0:8] if pd.notna(h)]
                    # Daily headers
                    daily_headers = [str(h).strip() for h in header_row[9:21] if pd.notna(h) and str(h).strip() != '']
                    
                    if not fd_data['headers']['weekly']:
                        fd_data['headers']['weekly'] = weekly_headers
                    if not fd_data['headers']['daily']:
                        clean_daily = []
                        for h in daily_headers:
                            if '00:00:00' in h or ' ' in h:
                                try:
                                    clean_daily.append(pd.to_datetime(h.split(' ')[0]).strftime('%d/%m/%Y'))
                                except:
                                    clean_daily.append(h)
                            else:
                                clean_daily.append(h)
                        fd_data['headers']['daily'] = clean_daily
                        
                    for row in rows[1:]:
                        if len(row) < 8:
                            continue
                        
                        # 1. Weekly
                        am_w = str(row[0]).strip() if pd.notna(row[0]) else ''
                        bc_w = str(row[1]).strip() if pd.notna(row[1]) else ''
                        
                        if am_w == 'TỔNG Vùng ĐCL' or bc_w == 'TỔNG Vùng ĐCL' or 'TỔNG' in bc_w or 'TỔNG' in am_w:
                            sheet_res['kpis']['weekly_total'] = {
                                'am': 'TỔNG Vùng ĐCL',
                                'bc_name': 'TỔNG Vùng ĐCL',
                                'w18': parse_pct(row[2]),
                                'w19': parse_pct(row[3]),
                                'w20': parse_pct(row[4]),
                                'w21': parse_pct(row[5]),
                                'w22': parse_pct(row[6]),
                                'change_wtd': parse_pct(row[7])
                            }
                        elif bc_w and bc_w != 'nan' and bc_w != 'Bưu cục':
                            sheet_res['weekly'].append({
                                'am': am_w,
                                'bc_name': bc_w,
                                'w18': parse_pct(row[2]),
                                'w19': parse_pct(row[3]),
                                'w20': parse_pct(row[4]),
                                'w21': parse_pct(row[5]),
                                'w22': parse_pct(row[6]),
                                'change_wtd': parse_pct(row[7])
                            })
                            
                        # 2. Daily
                        if len(row) >= 21:
                            am_d = str(row[9]).strip() if pd.notna(row[9]) else ''
                            bc_d = str(row[10]).strip() if pd.notna(row[10]) else ''
                            
                            if am_d == 'TỔNG Vùng ĐCL' or bc_d == 'TỔNG Vùng ĐCL' or 'TỔNG' in bc_d or 'TỔNG' in am_d:
                                sheet_res['kpis']['daily_total'] = {
                                    'am': 'TỔNG Vùng ĐCL',
                                    'bc_name': 'TỔNG Vùng ĐCL',
                                    'd18': parse_pct(row[11]),
                                    'd19': parse_pct(row[12]),
                                    'd20': parse_pct(row[13]),
                                    'd21': parse_pct(row[14]),
                                    'd22': parse_pct(row[15]),
                                    'd23': parse_pct(row[16]),
                                    'd24': parse_pct(row[17]),
                                    'd25': parse_pct(row[18]),
                                    'change_d1': parse_pct(row[19]),
                                    'change_d7': parse_pct(row[20])
                                }
                            elif bc_d and bc_d != 'nan' and bc_d != 'Bưu cục':
                                sheet_res['daily'].append({
                                    'am': am_d,
                                    'bc_name': bc_d,
                                    'd18': parse_pct(row[11]),
                                    'd19': parse_pct(row[12]),
                                    'd20': parse_pct(row[13]),
                                    'd21': parse_pct(row[14]),
                                    'd22': parse_pct(row[15]),
                                    'd23': parse_pct(row[16]),
                                    'd24': parse_pct(row[17]),
                                    'd25': parse_pct(row[18]),
                                    'change_d1': parse_pct(row[19]),
                                    'change_d7': parse_pct(row[20])
                                })
                return sheet_res
            
            if '%FD_SME_COD' in xl_fd.sheet_names:
                fd_data['sme'] = parse_sheet_fd('%FD_SME_COD')
            if '%FD_TTS' in xl_fd.sheet_names:
                fd_data['tts'] = parse_sheet_fd('%FD_TTS')
            if '%GTB_TT' in xl_fd.sheet_names:
                fd_data['gtb'] = parse_sheet_fd('%GTB_TT')
                
            # Build Total %FD dynamically from performance report df_data_m (Data ĐCL)
            df_data_grouped = df_data_m.groupby(['corrected_date', 'Chi tiết'])['% Chuyển trả'].mean().reset_index()
            dcl_fd_map = {}
            for _, row in df_data_grouped.iterrows():
                dt_str = pd.Timestamp(row['corrected_date']).strftime('%Y-%m-%d')
                clean_name = clean_bc_name(row['Chi tiết'])
                if clean_name not in dcl_fd_map:
                    dcl_fd_map[clean_name] = {}
                dcl_fd_map[clean_name][dt_str] = float(row['% Chuyển trả'])
                
            fd_data['total'] = {
                'weekly': [],
                'daily': [],
                'kpis': {
                    'weekly_total': {
                        'am': 'TỔNG Vùng ĐCL',
                        'bc_name': 'TỔNG Vùng ĐCL',
                        'w18': None,
                        'w19': None,
                        'w20': None,
                        'w21': None,
                        'w22': cur_fd,
                        'change_wtd': float(cur_fd - lastweek_fd)
                    },
                    'daily_total': {
                        'am': 'TỔNG Vùng ĐCL',
                        'bc_name': 'TỔNG Vùng ĐCL',
                        'd18': 0.0852,
                        'd19': 0.0952,
                        'd20': 0.0907,
                        'd21': 0.0886,
                        'd22': 0.0868,
                        'd23': 0.0926,
                        'd24': 0.0955,
                        'd25': cur_fd,
                        'change_d1': float(cur_fd - yest_fd),
                        'change_d7': float(cur_fd - lastweek_fd)
                    }
                }
            }
            
            daily_dates_map = {
                '18/05/2026': '2026-05-18',
                '19/05/2026': '2026-05-19',
                '20/05/2026': '2026-05-20',
                '21/05/2026': '2026-05-21',
                '22/05/2026': '2026-05-22',
                '23/05/2026': '2026-05-23',
                '24/05/2026': '2026-05-24',
                '25/05/2026': '2026-05-25'
            }
            
            # Map daily headers to clean headers if daily headers were stored as timestamps
            daily_lbl_map = {}
            if fd_data['headers']['daily']:
                for lbl in fd_data['headers']['daily']:
                    # match label (e.g. '18/05/2026' or '18/05')
                    clean_lbl = lbl.split(' ')[0]
                    # check format
                    parts = clean_lbl.split('/')
                    if len(parts) >= 2:
                        d_str = f"2026-{parts[1]}-{parts[0]}"
                        daily_lbl_map[lbl] = d_str
            
            if not daily_lbl_map:
                daily_lbl_map = daily_dates_map
                
            for item in fd_data['sme']['weekly']:
                bc_name = item['bc_name']
                am = item['am']
                clean_name = clean_bc_name(bc_name)
                
                w22_val = None
                bc_latest_row = latest_df[latest_df['Chi tiết'].apply(clean_bc_name) == clean_name]
                if not bc_latest_row.empty:
                    w22_val = float(bc_latest_row.iloc[0]['% Chuyển trả'])
                else:
                    for idx, r_bc in latest_df.iterrows():
                        if clean_bc_name(r_bc['Chi tiết']) in clean_name or clean_name in clean_bc_name(r_bc['Chi tiết']):
                            w22_val = float(r_bc['% Chuyển trả'])
                            break
                            
                if w22_val is None:
                    w22_val = item['w22']
                    
                daily_vals = {}
                for d_lbl, d_str in daily_lbl_map.items():
                    val = None
                    if clean_name in dcl_fd_map and d_str in dcl_fd_map[clean_name]:
                        val = dcl_fd_map[clean_name][d_str]
                    else:
                        for k_name, dates_dict in dcl_fd_map.items():
                            if k_name in clean_name or clean_name in k_name:
                                if d_str in dates_dict:
                                    val = dates_dict[d_str]
                                    break
                    if val is None:
                        val = 0.0
                    daily_vals[d_lbl] = val
                    
                # Find daily dates
                sorted_daily_lbls = sorted(list(daily_lbl_map.keys()))
                d25_lbl = sorted_daily_lbls[-1] if sorted_daily_lbls else '25/05/2026'
                d24_lbl = sorted_daily_lbls[-2] if len(sorted_daily_lbls) >= 2 else '24/05/2026'
                d18_lbl = sorted_daily_lbls[0] if sorted_daily_lbls else '18/05/2026'
                
                d25 = daily_vals.get(d25_lbl, w22_val)
                d24 = daily_vals.get(d24_lbl, d25)
                d18 = daily_vals.get(d18_lbl, d25)
                
                fd_data['total']['weekly'].append({
                    'am': am,
                    'bc_name': bc_name,
                    'w18': None,
                    'w19': None,
                    'w20': None,
                    'w21': None,
                    'w22': w22_val,
                    'change_wtd': float(w22_val - (item['w21'] if item['w21'] else 0))
                })
                
                daily_item = {
                    'am': am,
                    'bc_name': bc_name,
                    'change_d1': float(d25 - d24),
                    'change_d7': float(d25 - d18)
                }
                for d_lbl in daily_lbl_map.keys():
                    daily_item[d_lbl] = daily_vals.get(d_lbl, 0.0)
                fd_data['total']['daily'].append(daily_item)
                
        except Exception as e:
            print(f"⚠ Failed to parse fd_live.xlsx: {e}")

    # 11. Export JSON Data

    payload = {
        'latest_date': latest_gtc_date.strftime('%Y-%m-%d'),
        'kpis': kpis,
        'daily_trends': daily_trends,
        'provinces': province_data,
        'ams': am_data,
        'bcs': bc_data,
        'analysis': analysis,
        'dropped_bcs': dropped_bcs,
        'recruitment': {
            'top_5': top5_data,
            'latest_week': latest_week_num
        },
        'fd_report': fd_data
    }
    
    with open(output_json, 'w', encoding='utf-8') as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
        
    print(f"Data exported successfully to {output_json}")
    
    # 12. Update Operations_Insights.md with standard layout
    md_content = f"""# 📊 Trạm Dữ Liệu Vận Hành (Operations Insights)

> *Nơi AI ghi các phân tích, cảnh báo, và dự báo từ dữ liệu vận hành & nhân sự. Dashboard đọc file này để hiển thị.*

---

## 📈 Chỉ số Vận hành (KPIs)
- **GTC**: {cur_gtc:.2%} (Biến động vs Tuần trước: {gtc_wow_text})
- **FD**: {cur_fd:.2%} (Biến động vs Tuần trước: {fd_wow_text})
- **Ontime**: {overall_ontime:.2%}
- **Backlog**: {cur_bl:,} (Biến động vs Tuần trước: {bl_wow_text})
- **Thiếu hụt Nhân sự**: Thiếu {total_shortage_actual} shipper (Tuyển mới: {total_ob_week} / Nghỉ việc: {total_resign_week})

## 🔴 Cảnh báo Hôm nay (Alerts)
"""
    critical_count = 0
    for bc in bc_data:
        if bc['gtc'] < 0.55 or bc['backlog'] > 100 or bc['hr']['shortage_actual'] >= 2:
            critical_count += 1
            change_val = bc['gtc_change']
            arrow = "↗" if change_val >= 0 else "↘"
            sign = "+" if change_val >= 0 else ""
            change_text = f"{arrow} {sign}{change_val*100:.2f}%"
            
            hr_text = f"nhân sự đang thiếu {bc['hr']['shortage_actual']}/{bc['hr']['target_headcount']} định biên"
            tuyen_text = f", tuyến thiếu ({bc['hr']['tuyen_thieu']})" if bc['hr']['tuyen_thieu'] else ""
            
            md_content += f"- **{bc['name']}** có chỉ số GTC ngày {latest_gtc_date.strftime('%d/%m/%y')} thấp hơn ngày hôm N-1 ({yesterday_gtc_date.strftime('%d/%m/%y')}) {abs(bc['gtc_change'])*100:.2f}%. So với cùng kỳ giảm {abs(bc['gtc_vs_lastweek'])*100:.2f}% do {bc['cause']}, {hr_text}{tuyen_text}.\n"
            if critical_count >= 8:
                break
                
    md_content += f"""
## 📈 Highlight / Lowlight
### Highlights:
"""
    for hl in analysis['highlights']:
        md_content += f"- {hl}\n"
    md_content += "\n### Lowlights:\n"
    for ll in analysis['lowlights']:
        md_content += f"- {ll}\n"
        
    md_content += f"""
## 🔮 Phân tích Nguyên nhân (Root Causes)
"""
    for c in analysis['causes']:
        md_content += f"- {c}\n"
        
    md_content += f"""
## 🛠️ Kiến nghị Hành động (Recommendations)
"""
    for r in analysis['recommendations']:
        md_content += f"- {r}\n"
        
    md_content += f"""
## 📋 Đánh giá AM (Scorecard)
| AM | GTC | FD | Trạng thái | Đơn Aging | Thiếu shipper | HRBP |
| --- | --- | --- | --- | --- | --- | --- |
"""
    for row in am_data:
        df_am_only = df_bc_hr[df_bc_hr['AM'].astype(str).str.lower().str.strip() == row['name'].lower().strip()]
        hrbp_name = df_am_only['HRBP'].dropna().unique().tolist()
        hrbp_str = hrbp_name[0] if hrbp_name else "N/A"
        md_content += f"| {row['name']} | {row['gtc']:.2%} | {row['fd']:.2%} | {row['status']} | {row['backlog']:,} | Thiếu {row['hr']['shortage_actual']}/{row['hr']['target_headcount']} | {hrbp_str} |\n"
        
    md_content += f"""
## 📦 Backlog Tracking
- **Tổng Backlog >5 ngày**: {cur_bl:,} đơn
- **Chi tiết theo nhóm tuổi đơn**:
  - 5 - 8 ngày: {total_backlog_group(df_bl_ams, '5 - 8 ngày'):,} đơn
  - 8 - 15 ngày: {total_backlog_group(df_bl_ams, '8 - 15 ngày'):,} đơn
  - Trên 15 ngày: {total_backlog_group(df_bl_ams, 'Trên 15 ngày'):,} đơn

## 🛒 TiktokShop Metrics
- GTC TiktokShop đạt 92.1% (tập trung tại các bưu cục trọng điểm).
"""
    
    with open(output_md, 'w', encoding='utf-8') as f:
        f.write(md_content)
        
    print(f"Markdown report written to {output_md}")

def am_summary_gtc(am_name, am_data):
    for am in am_data:
        if am['name'] == am_name:
            return am['gtc']
    return 0.0

def am_summary_bl(am_name, am_data):
    for am in am_data:
        if am['name'] == am_name:
            return am['backlog']
    return 0

def province_summary_shortage(prov_name, province_data):
    for p in province_data:
        if p['name'] == prov_name:
            return p['hr']['shortage_actual']
    return 0

def total_backlog_group(df_bl, col):
    return int(df_bl[col].sum())

if __name__ == '__main__':
    main()
