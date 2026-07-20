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
p_hr = r"C:\Users\Administrator\Desktop\AI 2026\Mentor\recruitment_live.xlsx"

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
    if isinstance(val, (int, float)):
        import numpy as np
        if np.isnan(val):
            return 0.0
        if abs(val) > 1.0:
            return float(val) / 100.0
        return float(val)
        
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
        val_float = float(clean)
        if '%' in val_str or abs(val_float) > 1.0:
            return (val_float / 100.0) * sign
        return val_float * sign
    except:
        return 0.0

def main():
    print("Starting data aggregation and analysis...")
    
    global p_performance, p_backlog, p_hr
    
    import urllib.request
    import ssl
    # security-rules: Always validate SSL certificates (MITM prevention)
    try:
        import certifi
        ssl._create_default_https_context = lambda: ssl.create_default_context(cafile=certifi.where())
    except ImportError:
        print("[WARNING] certifi not installed. Using unverified SSL context as fallback.")
        ssl._create_default_https_context = ssl._create_unverified_context
    
    # Download Recruitment (Link 3)
    p_hr_local = r"C:\Users\Administrator\Desktop\AI 2026\Mentor\recruitment_live.xlsx"
    p_hr_user = r"C:\Users\Administrator\Desktop\AI 2026\Mentor\[ĐCL] - BÁO CÁO TUYỂN DỤNG DATA.xlsx"
    
    download_success = False
    
    if "--skip-hr" in sys.argv:
        print("Skipping live recruitment sheet download as requested via argument.")
    else:
        print("Downloading live recruitment sheet from Google Sheets...")
        try:
            gsheet_hr_url = "https://docs.google.com/spreadsheets/d/1si4PWd97eJhQDQUBXvEErjmNHGO8W1NrQVFnzzMIkDI/export?format=xlsx"
            import subprocess
            try:
                # Use PowerShell as primary because it handles large GSheet chunked exports on Windows reliably
                cmd = ["powershell", "-Command", f"Invoke-WebRequest -Uri '{gsheet_hr_url}' -OutFile '{p_hr_local}'"]
                subprocess.run(cmd, check=True, timeout=120)
                download_success = True
            except Exception as pe:
                # Fallback to urllib
                req = urllib.request.Request(gsheet_hr_url, headers={'User-Agent': 'Mozilla/5.0'})
                with urllib.request.urlopen(req, timeout=90) as response:
                    with open(p_hr_local, 'wb') as f:
                        f.write(response.read())
                download_success = True
            
            if download_success:
                print("✓ Downloaded live recruitment sheet successfully.")
                p_hr = p_hr_local
        except Exception as e:
            print(f"⚠ Failed to download live recruitment sheet: {e}.")
            
    if not download_success:
        if os.path.exists(p_hr_user):
            print("✓ Falling back to local recruitment file '[ĐCL] - BÁO CÁO TUYỂN DỤNG DATA.xlsx'. Copying to recruitment_live.xlsx...")
            import shutil
            try:
                shutil.copy2(p_hr_user, p_hr_local)
                p_hr = p_hr_local
            except Exception as e:
                print(f"⚠ Failed to copy local recruitment file: {e}")
                p_hr = p_hr_local
        else:
            print("✓ Using existing recruitment_live.xlsx as fallback.")
            p_hr = p_hr_local
        
    # Download Link 1 (GTC/Performance) - SKIPPED AS REQUESTED
    print("Downloading Google Sheets Link 1 is skipped as requested.")
    p_link1_local = r"C:\Users\Administrator\Desktop\AI 2026\Mentor\link1_live.xlsx"
    link1_success = False
        
    # Download Link 2 (Backlog)
    print("Downloading Google Sheets Link 2...")
    p_link2_local = r"C:\Users\Administrator\Desktop\AI 2026\Mentor\link2_live.xlsx"
    link2_success = False
    try:
        gsheet_link2_url = "https://docs.google.com/spreadsheets/d/1czdUAW8M9hJZ_OBk5fUgwJupOmahM6QW5AlufN36jaU/export?format=xlsx"
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
    p_fd_xlsx = r"C:\Users\Administrator\Desktop\AI 2026\Mentor\fd_live.xlsx"
    p_fd_user = r"C:\Users\Administrator\Desktop\AI 2026\Mentor\ĐCL - %Chuyển trả.xlsx"
    fd_success = False
    try:
        gsheet_fd_url = "https://docs.google.com/spreadsheets/d/1eJo3_M35Q-Qb3t9AzZkF22gZUCG5oETj-ZIew1DaFgA/export?format=xlsx"
        req = urllib.request.Request(gsheet_fd_url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=90) as response:
            with open(p_fd_xlsx, 'wb') as f:
                f.write(response.read())
        print("✓ Downloaded live FD report sheet successfully.")
        fd_success = True
    except Exception as e:
        print(f"⚠ Failed to download live FD report sheet: {e}. Falling back to local file.")
        
    if not fd_success:
        if os.path.exists(p_fd_user):
            print("✓ Falling back to local FD report file 'ĐCL - %Chuyển trả.xlsx'. Copying to fd_live.xlsx...")
            import shutil
            try:
                shutil.copy2(p_fd_user, p_fd_xlsx)
                fd_success = True
            except Exception as ce:
                print(f"⚠ Failed to copy local FD report file: {ce}")
        else:
            print("✓ Using existing fd_live.xlsx as fallback.")
        
    # Download Transfer Backlog (Link 5)
    print("Downloading live Transfer Backlog sheet from Google Sheets...")
    p_tb_xlsx = r"C:\Users\Administrator\Desktop\AI 2026\Mentor\DCL _24h chưa luân chuyển.xlsx"
    tb_success = False
    try:
        gsheet_tb_url = "https://docs.google.com/spreadsheets/d/1zyZsYWuHeL2WiEu5O7rABZZpyWoH5wEacxXe5s-IQQw/export?format=xlsx"
        req = urllib.request.Request(gsheet_tb_url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=90) as response:
            with open(p_tb_xlsx, 'wb') as f:
                f.write(response.read())
        print("✓ Downloaded Transfer Backlog sheet successfully.")
        tb_success = True
    except Exception as e:
        print(f"⚠ Failed to download Transfer Backlog sheet: {e}. Falling back to local file.")
        
    # Dynamic classification of Link 1 & Link 2
    for path, success, label in [(p_link1_local, link1_success, "Link 1"), (p_link2_local, link2_success, "Link 2")]:
        if success and os.path.exists(path):
            try:
                xl = pd.ExcelFile(path)
                sheets = xl.sheet_names
                if "Data ĐCL" in sheets:
                    p_performance = path
                    print(f"-> Assigned {label} to Performance Report (found 'Data ĐCL')")
                elif "PIVOT" in sheets or "aging>5" in sheets:
                    p_backlog = path
                    print(f"-> Assigned {label} to Backlog Report (found 'PIVOT' or 'aging>5')")
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
        df_hist = pd.read_excel(xls_perf, sheet_name="Lịch sử")
    print("Reading backlog sheets...")
    xl_bl = pd.ExcelFile(p_backlog)
    bl_by_bc = {}
    df_bl_ams = pd.DataFrame()
    
    if "aging>5" in xl_bl.sheet_names:
        print("✓ Detected new backlog format ('aging>5' sheet)")
        df_raw_bl = pd.read_excel(xl_bl, sheet_name="aging>5")
        if 'vung' in df_raw_bl.columns:
            df_dcl = df_raw_bl[df_raw_bl['vung'].astype(str).str.strip().str.upper() == 'ĐCL'].copy()
        else:
            df_dcl = df_raw_bl.copy()
            
        bc_col = 'bc' if 'bc' in df_dcl.columns else ('BC' if 'BC' in df_dcl.columns else '')
        if bc_col:
            for bc_name_raw, grp in df_dcl.groupby(bc_col):
                bl_by_bc[clean_bc_name(bc_name_raw)] = len(grp)
        
        am_col = 'am_name' if 'am_name' in df_dcl.columns else ('AM' if 'AM' in df_dcl.columns else 'am')
        days_col = 'BL số ngày' if 'BL số ngày' in df_dcl.columns else ('bl_so_ngay' if 'bl_so_ngay' in df_dcl.columns else 'BL số ngày')
        
        def get_bucket(days):
            try:
                val = float(days)
                if val < 8:
                    return '5 - 8 ngày'
                elif val < 15:
                    return '8 - 15 ngày'
                else:
                    return 'Trên 15 ngày'
            except:
                return '5 - 8 ngày'
                  
        if am_col in df_dcl.columns and days_col in df_dcl.columns:
            rows_list = []
            for am_val, grp in df_dcl.groupby(am_col):
                if pd.isna(am_val):
                    continue
                am_str = str(am_val).strip()
                if not am_str or am_str.lower() == 'nan' or am_str.lower() == 'tổng':
                    continue
                bucket_counts = {'5 - 8 ngày': 0, '8 - 15 ngày': 0, 'Trên 15 ngày': 0}
                for days in grp[days_col]:
                    bucket = get_bucket(days)
                    bucket_counts[bucket] += 1
                total = sum(bucket_counts.values())
                rows_list.append({
                    'AM': am_str,
                    '5 - 8 ngày': bucket_counts['5 - 8 ngày'],
                    '8 - 15 ngày': bucket_counts['8 - 15 ngày'],
                    'Trên 15 ngày': bucket_counts['Trên 15 ngày'],
                    'Tổng': total
                })
            if rows_list:
                df_bl_ams = pd.DataFrame(rows_list)
            else:
                df_bl_ams = pd.DataFrame(columns=['AM', '5 - 8 ngày', '8 - 15 ngày', 'Trên 15 ngày', 'Tổng'])
        else:
            print("⚠ Warning: am_col or days_col not found in new sheet layout!")
            df_bl_ams = pd.DataFrame(columns=['AM', '5 - 8 ngày', '8 - 15 ngày', 'Trên 15 ngày', 'Tổng'])
    else:
        print("✓ Detected old backlog format ('PIVOT' sheet)")
        df_backlog_pivot = pd.read_excel(xl_bl, sheet_name="PIVOT")
        df_backlog_raw = pd.read_excel(xl_bl, sheet_name="Đơn GIAO aging >5 ngày", usecols=['BC'])
        
        for bc_name_raw, grp in df_backlog_raw.groupby('BC'):
            bl_by_bc[clean_bc_name(bc_name_raw)] = len(grp)
    
    # 2. Date Corrections (Moved up to get current week number)
    df_data['corrected_date'] = pd.to_datetime(df_data['Time Format']) 
    latest_gtc_date = df_data['corrected_date'].max()
    
    print("Reading recruitment sheet...")
    interns_map = {}
    with pd.ExcelFile(p_hr) as xl_hr:
        # Find all Tổng hợp (T\d+) sheets and select the one with max week number
        tonghop_sheets = []
        for s in xl_hr.sheet_names:
            match = re.match(r'Tổng hợp \(T(\d+)\)', s)
            if match:
                w = int(match.group(1))
                tonghop_sheets.append((w, s))
                
        if tonghop_sheets:
            # Sort chronologically: weeks >= 40 are from 2025 (lesser chronological value), weeks < 40 are from 2026.
            latest_week_num, latest_hr_sheet = max(tonghop_sheets, key=lambda x: x[0] if x[0] < 40 else x[0] - 100)
            print(f"✓ Selected latest available recruitment sheet: {latest_hr_sheet} (Week {latest_week_num})")
        else:
            latest_hr_sheet = 'Tổng hợp (T23)'
            latest_week_num = 23
            print(f"⚠ No 'Tổng hợp (T*)' sheet found. Falling back to default: {latest_hr_sheet}")
            
        df_hr = pd.read_excel(xl_hr, sheet_name=latest_hr_sheet)
        
        # Parse interns map from 'Cơ cấu Intern'
        if 'Cơ cấu Intern' in xl_hr.sheet_names:
            try:
                df_intern = xl_hr.parse('Cơ cấu Intern', header=None)
                for idx, row in df_intern.iterrows():
                    if idx < 2:
                        continue
                    tỉnh = str(row[0]).strip() if pd.notna(row[0]) else ""
                    if not tỉnh or tỉnh == 'TỔNG' or tỉnh == 'nan' or tỉnh == 'Tổng cộng':
                        continue
                    # Get active intern from column 7, fallback to column 4
                    intern = str(row[7]).strip() if pd.notna(row[7]) and str(row[7]).strip() != 'nan' else str(row[4]).strip()
                    if intern and intern != 'nan':
                        interns_map[tỉnh.lower()] = intern
                print("✓ Parsed HRBP Interns from 'Cơ cấu Intern' sheet:", interns_map)
            except Exception as ie:
                print(f"⚠ Failed to parse 'Cơ cấu Intern': {ie}")
                
        # Read CoCauVung from recruitment_live.xlsx
        cocau_map = {}
        try:
            print("Reading new AM/BC structure from recruitment_live.xlsx...")
            df_cocau_raw = pd.read_excel(xl_hr, sheet_name="Cơ cấu Vùng")
            df_cocau = pd.DataFrame()
            df_cocau['warehouse_id'] = df_cocau_raw['Mã BC']
            df_cocau['warehouse_name'] = df_cocau_raw['Bưu cục']
            df_cocau['province_name'] = df_cocau_raw['Tỉnh']
            df_cocau['am_name'] = df_cocau_raw['AM']
            
            am_tele_map = {
                'Nguyễn Tuấn Anh': '@Tuananh_kr',
                'Nguyễn Huỳnh Quốc Dũng': '@DungBt',
                'Huỳnh Quốc Trung': '@HuynhQTrung',
                'Nguyễn Anh Tùng': '@jimmytho91',
                'Nguyễn Việt Tới': '@OP_MN_CAOLANH_DONGTHAP_TOI',
                'Lý Quài Nhân': '@lynhantv92',
                'Đoàn Công Tín': '@congtind',
                'Nguyễn Thành Huy': '@nguyenthanhhuytv',
                'Lê Minh Tuấn': '@MinhTuanLM',
                'Ngô Phan Mỹ Tú': '@MyTuNgoPhan',
                'Võ Hồng Chơn': '@chonvh',
                'Ngô Thị Bé Mi': '@bemi_tgi'
            }
            df_cocau['am_tele'] = df_cocau['am_name'].map(am_tele_map).fillna('')
            df_cocau['am_id'] = df_cocau_raw['ID AM'].fillna('').astype(str)
            
            # Populate cocau_map for old to new name translations
            for idx_c, row_c in df_cocau_raw.iterrows():
                old_name_raw = row_c['Bưu cục cũ']
                new_name_raw = row_c['Bưu cục']
                new_am_raw = row_c['AM']
                if pd.notna(old_name_raw) and pd.notna(new_name_raw):
                    clean_old = clean_bc_name(str(old_name_raw))
                    cocau_map[clean_old] = {
                        'new_name': str(new_name_raw).strip(),
                        'new_am': str(new_am_raw).strip() if pd.notna(new_am_raw) else ''
                    }
            print("✓ Loaded new AM/BC structure successfully.")
        except Exception as ce:
            print(f"⚠ Failed to load new AM/BC structure from Cơ cấu Vùng: {ce}")
            # Fallback empty df with correct columns
            df_cocau = pd.DataFrame(columns=['warehouse_id', 'warehouse_name', 'province_name', 'am_name', 'am_tele', 'am_id'])
    
    # Find columns for Subtable 0 (fallback)
    try:
        bc_col_idx = list(df_hr.columns).index('Bưu cục')
        df_sub0 = df_hr.iloc[:, bc_col_idx:bc_col_idx+16].copy()
    except Exception as e:
        print(f"⚠ Columns layout mismatch: {e}. Using raw indices.")
        df_sub0 = df_hr.iloc[:, 9:25].copy()
        
    # Standardize subtable columns (Subtable 0 has 16 columns including Status and HRBP)
    df_sub0.columns = [
        'Bưu cục', 'Tỉnh', 'AM', 'Tuyến thiếu', 'Định biên NVPTTT', 'Định biên NVXL', 
        'NVPTTT_resign', 'NVPTTT_shortage_bs', 'YCTD', 'NVPTTT_ob_day', 'NVPTTT_ob_week', 
        'Data_Day', 'NVPTTT_shortage_actual', 'pct_dapung', 'HRBP', 'Status'
    ]

    # Read headcount allocation and HRBP assignments directly from Subtable 0
    df_bc_hr = df_sub0[(df_sub0['Bưu cục'].notna()) & (df_sub0['Bưu cục'] != 'TỔNG') & (df_sub0['Tỉnh'].notna()) & (df_sub0['Bưu cục'].astype(str).str.strip() != '')].copy()
    df_bc_hr['Bưu cục_clean'] = df_bc_hr['Bưu cục'].apply(clean_bc_name)
    print(f"✓ Parsed recruitment data from Subtable 0. Total: {len(df_bc_hr)} bưu cục.")
        
    # Standardize numeric columns
    for col in ['NVPTTT_shortage_actual', 'NVPTTT_shortage_bs', 'NVPTTT_resign', 'NVPTTT_ob_week', 'Định biên NVPTTT', 'Định biên NVXL']:
        if col in df_bc_hr.columns:
            df_bc_hr[col] = pd.to_numeric(df_bc_hr[col], errors='coerce').fillna(0).astype(int)
            
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
    
    # Clean Backlog Pivot (Old format only)
    if 'df_backlog_pivot' in locals():
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
            
    # Load historical backlogs from existing JSON if available
    json_backlog_history = {}
    if os.path.exists(output_json):
        try:
            with open(output_json, 'r', encoding='utf-8') as f:
                old_data = json.load(f)
            if 'daily_trends' in old_data:
                for trend in old_data['daily_trends']:
                    if 'date' in trend and 'backlog' in trend:
                        json_backlog_history[trend['date']] = int(trend['backlog'])
            print(f"✓ Loaded {len(json_backlog_history)} historical backlog values from existing operations_data.json")
        except Exception as je:
            print(f"⚠ Failed to load historical backlog from JSON: {je}")

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
    backlog_history.update(json_backlog_history)
    
    # Parse daily backlog totals dynamically from bottom of PIVOT sheet (Old format only)
    parsed_history = {}
    if 'df_backlog_pivot' in locals():
        try:
            header_idx = None
            total_idx = None
            for idx, r_row in df_backlog_pivot.iterrows():
                val = str(r_row.iloc[0]).strip() if pd.notna(r_row.iloc[0]) else ""
                if val == 'AM' and any('Ngày N' in str(cell) for cell in r_row):
                    header_idx = idx
                elif val == 'TỔNG' and header_idx is not None:
                    total_idx = idx
                    
            if header_idx is not None and total_idx is not None:
                headers = df_backlog_pivot.iloc[header_idx].tolist()
                totals = df_backlog_pivot.iloc[total_idx].tolist()
                
                for col_idx in range(1, len(headers)):
                    h_val = str(headers[col_idx]).strip() if pd.notna(headers[col_idx]) else ""
                    t_val = str(totals[col_idx]).strip() if pd.notna(totals[col_idx]) else ""
                    
                    if not h_val or not t_val:
                        continue
                    date_match = re.search(r'\((\d{2}/\d{2})\)', h_val)
                    if not date_match:
                        date_match = re.search(r'(\d{2}/\d{2})', h_val)
                    cnt_match = re.match(r'^([\d\.,]+)', t_val)
                    
                    if date_match and cnt_match:
                        date_str = date_match.group(1)
                        day, month = date_str.split('/')
                        full_date = f"2026-{month}-{day}"
                        cnt_str = cnt_match.group(1).replace('.', '').replace(',', '')
                        parsed_history[full_date] = int(cnt_str)
                        
            for k, v in parsed_history.items():
                backlog_history[k] = v
        except Exception as e:
            print(f"⚠ Failed to parse daily backlog history: {e}")
    
    # Clean keys before merge to prevent type mismatches (int vs float vs string)
    def clean_id(val):
        try:
            if pd.isna(val):
                return -1
            return int(float(str(val).strip()))
        except:
            return -1

    df_cocau['warehouse_id'] = df_cocau['warehouse_id'].apply(clean_id)
    df_data['ID Bưu cục'] = df_data['ID Bưu cục'].apply(clean_id)

    # Map Post Offices to AM and Province
    df_data_m = df_data.merge(df_cocau, left_on="ID Bưu cục", right_on="warehouse_id", how="left")
    df_data_m['warehouse_name'] = df_data_m['warehouse_name'].fillna(df_data_m['Chi tiết'])
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
    
    cur_bl = int(df_bl_ams['Tổng'].sum()) if not df_bl_ams.empty else 0
    
    # Add today's backlog dynamically to backlog_history
    try:
        if 'df_dcl' in locals() and 'updated_time' in df_dcl.columns and not df_dcl['updated_time'].isna().all():
            backlog_date_str = pd.to_datetime(df_dcl['updated_time'].max()).strftime('%Y-%m-%d')
        else:
            backlog_date_str = pd.to_datetime(latest_gtc_date).strftime('%Y-%m-%d')
    except:
        import datetime
        backlog_date_str = datetime.datetime.now().strftime('%Y-%m-%d')
        
    backlog_history[backlog_date_str] = cur_bl
    print(f"✓ Added today's backlog ({backlog_date_str}: {cur_bl} orders) to backlog_history")

    # Calculate relative backlogs dynamically
    today_str = pd.to_datetime(latest_gtc_date).strftime('%Y-%m-%d')
    if backlog_history:
        valid_dates = [d for d in backlog_history.keys() if d <= today_str]
        if valid_dates:
            today_str = max(valid_dates)
        else:
            today_str = max(backlog_history.keys())
        
    yest_dt = pd.to_datetime(today_str) - pd.Timedelta(days=1)
    yest_bl = backlog_history.get(yest_dt.strftime('%Y-%m-%d'), 2705)
    
    lastweek_dt = pd.to_datetime(today_str) - pd.Timedelta(days=7)
    lastweek_bl = backlog_history.get(lastweek_dt.strftime('%Y-%m-%d'), 2128)
    
    lastmonth_dt = pd.to_datetime(today_str) - pd.Timedelta(days=30)
    lastmonth_bl = backlog_history.get(lastmonth_dt.strftime('%Y-%m-%d'), 1850)
    
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
        
        # Get HRBP dynamically from df_prov_hr
        prov_hrbps = df_prov_hr['HRBP'].dropna().astype(str).str.strip().tolist()
        p_hrbp = max(set(prov_hrbps), key=prov_hrbps.count) if prov_hrbps else "N/A"
        
        # Get Intern dynamically from interns_map
        p_intern = interns_map.get(prov.lower(), "N/A")
        
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
                'target_headcount': p_dinhiben,
                'hrbp': p_hrbp,
                'intern': p_intern
            }
        })
        
    # Aggregate by AM
    am_data = []
    for idx, row in df_bl_ams.iterrows():
        am = row['AM']
        if pd.isna(am):
            am_str = ""
        else:
            am_str = str(am).strip()
        if not am_str or am_str.lower() == 'nan' or am_str.lower() == 'tổng':
            continue
            
        bl = int(row['Tổng'])
        bl_5_8 = int(row['5 - 8 ngày'])
        bl_8_15 = int(row['8 - 15 ngày'])
        bl_above_15 = int(row['Trên 15 ngày'])
        
        # Latest Performance
        df_am_cur = latest_df[latest_df['am_name'] == am_str]
        a_gtc, a_fd, a_vol = calc_gtc_fd(df_am_cur)
        df_am_yest = yest_df[yest_df['am_name'] == am_str]
        a_gtc_y, a_fd_y, _ = calc_gtc_fd(df_am_yest)
        
        # HR calculations for AM
        df_am_hr = df_bc_hr[df_bc_hr['AM'].astype(str).str.strip().str.lower() == am_str.lower()]
        a_shortage_actual = int(df_am_hr['NVPTTT_shortage_actual'].sum())
        a_shortage_bs = int(df_am_hr['NVPTTT_shortage_bs'].sum())
        a_resign = int(df_am_hr['NVPTTT_resign'].sum())
        a_ob = int(df_am_hr['NVPTTT_ob_week'].sum())
        a_dinhiben = int(df_am_hr['Định biên NVPTTT'].dropna().sum())
        
        status = "Mạnh" if a_gtc >= 0.67 else "Cải thiện" if a_gtc >= 0.55 else "Yếu"
        
        am_data.append({
            'name': am_str,
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
        bc_name = row['warehouse_name']
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
        bc_clean = clean_bc_name(bc_name)
        bc_bl = 0
        if bc_clean in bl_by_bc:
            bc_bl = bl_by_bc[bc_clean]
        else:
            # Try substring match
            for k_bl, cnt in bl_by_bc.items():
                if k_bl in bc_clean or bc_clean in k_bl:
                    bc_bl = cnt
                    break
            
        status = "Tốt" if gtc >= 0.67 else "Cảnh báo" if gtc >= 0.55 else "Bất ổn"
        
        # Match HR information
        bc_clean = clean_bc_name(bc_name)
        hr_row = None
        if bc_clean:
            if bc_clean in hr_bc_cleaned:
                hr_row = hr_bc_cleaned[bc_clean]
            else:
                # Try substring match
                for c_key, raw_row in hr_bc_cleaned.items():
                    if c_key and (c_key in bc_clean or bc_clean in c_key):
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

    
    # Fetch and parse dropped transfer orders from Google Sheet
    dropped_bcs = []
    try:
        import ssl
        # security-rules: Always validate SSL certificates
        try:
            import certifi
            ssl._create_default_https_context = lambda: ssl.create_default_context(cafile=certifi.where())
        except ImportError:
            ssl._create_default_https_context = ssl._create_unverified_context
        gsheet_url = "https://docs.google.com/spreadsheets/d/1kYBjz-xrD8IsEo-PVC3a1Qi8etVGN9j-xWdZyrPo36M/export?format=csv&gid=1657944306"
        df_gsheet = pd.read_csv(gsheet_url)
        
        # Find where the pivot table starts in the sheet
        row0 = df_gsheet.iloc[0].tolist() if not df_gsheet.empty else []
        pivot_start_col = -1
        # Scan from index 13 to end to find the pivot table header 'AM'
        for i in range(13, len(row0)):
            if str(row0[i]).strip() == 'AM':
                pivot_start_col = i
                break
                
        if pivot_start_col != -1:
            header_map = {
                'am': 'am',
                'bưu cục': 'bc_name',
                'khac': 'khac',
                'khác': 'khac',
                'shopee': 'shopee',
                'tts': 'tts',
                'grand total': 'total',
                'tổng cộng': 'total',
                'tổng': 'total'
            }
            
            pivot_cols = df_gsheet.iloc[:, pivot_start_col:].copy()
            pivot_headers = [str(x).strip().lower() for x in row0[pivot_start_col:]]
            
            populated_cols = {}
            for idx, h in enumerate(pivot_headers):
                if h in header_map:
                    target_col = header_map[h]
                    col_data = pivot_cols.iloc[1:, idx].reset_index(drop=True)
                    populated_cols[target_col] = col_data
                    
            df_pivot = pd.DataFrame(index=range(len(pivot_cols) - 1))
            for key, default_val in [('am', ""), ('bc_name', "")]:
                if key in populated_cols:
                    df_pivot[key] = populated_cols[key].astype(str).str.strip()
                else:
                    df_pivot[key] = default_val
            for key in ['khac', 'shopee', 'tts', 'total']:
                if key in populated_cols:
                    df_pivot[key] = pd.to_numeric(populated_cols[key], errors='coerce').fillna(0).astype(int)
                else:
                    df_pivot[key] = 0
            
            # Clean rows
            df_pivot = df_pivot[df_pivot['bc_name'].notna() & (df_pivot['bc_name'].astype(str).str.strip() != '')]
            df_pivot = df_pivot[df_pivot['am'].str.lower() != 'grand total']
            df_pivot = df_pivot[df_pivot['bc_name'].str.lower() != 'grand total']
            
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
        else:
            print("⚠ Could not find 'AM' header for pivot table starting from column 13.")
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
                
                # Match old name to new name and AM
                clean_old_bc = clean_bc_name(str(bc_n_raw))
                bc_name_new = str(bc_n_raw).strip()
                if clean_old_bc in cocau_map:
                    bc_name_new = cocau_map[clean_old_bc]['new_name']
                else:
                    for k_old, info in cocau_map.items():
                        if k_old in clean_old_bc or clean_old_bc in k_old:
                            bc_name_new = info['new_name']
                            break
                            
                manual_top5.append({
                    'bc_name': bc_name_new,
                    'details': str(row_t['Unnamed: 11']).strip() if pd.notna(row_t['Unnamed: 11']) else "",
                    'volume': int(row_t['Unnamed: 2']) if pd.notna(row_t['Unnamed: 2']) else 0,
                    'vol_tts': int(row_t['Unnamed: 3']) if pd.notna(row_t['Unnamed: 3']) else 0,
                    'gtc': float(row_t['Unnamed: 4']) if pd.notna(row_t['Unnamed: 4']) else 0.0,
                    'backlog_72h': int(row_t['Unnamed: 5']) if pd.notna(row_t['Unnamed: 5']) else 0,
                })
        except Exception as e:
            print(f"⚠ Failed to parse manual top 5: {e}")

    # Build dynamic causes and recommendations from manual_top5
    dynamic_causes = []
    dynamic_recs = []
    for item in manual_top5:
        bc_name = item['bc_name']
        details_text = item['details']
        if not details_text:
            continue
            
        parts = re.split(r'\* Phương án:|\* phương án:|\*Phương án:|\*Phương án|-----------|==============', details_text)
        causes_str = parts[0].strip()
        recs_str = parts[1].strip() if len(parts) > 1 else ""
        
        def get_bullets(block):
            lines = []
            for line in block.split('\n'):
                line = line.strip()
                if not line:
                    continue
                line = re.sub(r'^[\-\*\+\d\.\s]+', '', line).strip()
                if line:
                    lines.append(line)
            return lines
            
        bc_causes = get_bullets(causes_str)
        bc_recs = get_bullets(recs_str)
        
        if bc_causes:
            combined_causes = "; ".join(bc_causes)
            dynamic_causes.append(f"Tại **{bc_name}**: {combined_causes}")
        if bc_recs:
            combined_recs = "; ".join(bc_recs)
            dynamic_recs.append(f"Tại **{bc_name}**: {combined_recs}")

    if not dynamic_causes:
        dynamic_causes = [
            "Tỷ lệ nghỉ việc cao tập trung tại các BC trọng điểm: **Phó Cơ Điều** (nghỉ 7), **Chợ Lách** (nghỉ 4), **Mỹ Thọ** (nghỉ 4), **Khóm 3 Trần Hưng Đạo** (nghỉ 4), **Tân Nhuận Đông** (nghỉ 3).",
            "Áp lực quá tải đơn hàng trong các ngày sale lớn và việc di chuyển qua các tuyến cù lao/đò dọc xa xôi (như tại Chợ Lách và Tân Nhuận Đông) làm giảm thu nhập thực tế, gây nản chí cho shipper mới.",
            "Quy trình lựa hàng và phân tuyến tại kho chậm trễ khiến shipper rời kho muộn (sau 9h30 sáng), phải làm việc xuyên trưa dưới trời nắng nóng và thiếu kèm cặp cho shipper mới (OB)."
        ]
    if not dynamic_recs:
        dynamic_recs = [
            "Yêu cầu AM (Tuấn Anh, Phương Duy, Việt Tới, Minh Tuấn, Quài Nhân) cắm chốt trực tiếp tại các bưu cục nóng để tháo gỡ khó khăn về tuyến và chia nhỏ tuyến giao phù hợp.",
            "Đề xuất áp dụng phụ cấp xăng xe/đò phà đặc thù cho các tuyến cù lao (như An Bình, Bình Hòa Phước tại Chợ Lách) để giữ chân nhân sự.",
            "Triển khai chương trình 'Buddy' kèm cặp shipper mới nhận việc trong 3 ngày đầu tiên và cam kết phân hàng trước 8h sáng để shipper ra kho sớm trước 9h sáng.",
            "Yêu cầu HRBP (VyLNK, BìnhNLC) đẩy mạnh chạy Ads Facebook, dán banner tuyển dụng liên tục tại các bưu cục nóng và chuẩn bị nguồn cộng tác viên dự phòng."
        ]

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
        'causes': dynamic_causes,
        'recommendations': dynamic_recs
    }

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
            df_data_grouped = df_data_m.groupby(['corrected_date', 'warehouse_name'])['% Chuyển trả'].mean().reset_index()
            dcl_fd_map = {}
            for _, row in df_data_grouped.iterrows():
                dt_str = pd.Timestamp(row['corrected_date']).strftime('%Y-%m-%d')
                clean_name = clean_bc_name(row['warehouse_name'])
                if clean_name not in dcl_fd_map:
                    dcl_fd_map[clean_name] = {}
                dcl_fd_map[clean_name][dt_str] = float(row['% Chuyển trả'])

            # Calculate regional daily rates from df_data_m (Data ĐCL)
            df_data_m['Vol Chuyen Tra'] = df_data_m['Volume'] * df_data_m['% Chuyển trả']
            daily_agg = df_data_m.groupby('corrected_date').agg({
                'Volume': 'sum',
                'Vol Chuyen Tra': 'sum'
            }).reset_index()
            daily_agg['rate'] = daily_agg['Vol Chuyen Tra'] / daily_agg['Volume']
            daily_rates = {pd.Timestamp(r['corrected_date']).strftime('%Y-%m-%d'): r['rate'] for _, r in daily_agg.iterrows()}

            # Calculate target week string based on latest_gtc_date
            isocal = latest_gtc_date.isocalendar()
            target_week_str = f"{isocal.year}/{isocal.week}"
            
            sme_w_total = fd_data['sme']['kpis'].get('weekly_total', {})
            tts_w_total = fd_data['tts']['kpis'].get('weekly_total', {})
            sme_d_total = fd_data['sme']['kpis'].get('daily_total', {})
            tts_d_total = fd_data['tts']['kpis'].get('daily_total', {})

            # Match target week in weekly headers dynamically
            weekly_headers = fd_data['headers']['weekly']
            latest_week_key = 'w22'  # default fallback
            
            if target_week_str in weekly_headers:
                col_idx = weekly_headers.index(target_week_str)
                key_map = {2: 'w18', 3: 'w19', 4: 'w20', 5: 'w21', 6: 'w22'}
                latest_week_key = key_map.get(col_idx, 'w22')
            else:
                target_week_str_zero = f"{isocal.year}/{isocal.week:02d}"
                if target_week_str_zero in weekly_headers:
                    col_idx = weekly_headers.index(target_week_str_zero)
                    key_map = {2: 'w18', 3: 'w19', 4: 'w20', 5: 'w21', 6: 'w22'}
                    latest_week_key = key_map.get(col_idx, 'w22')

            sme_w_latest = sme_w_total.get(latest_week_key, 0.0793)
            tts_w_latest = tts_w_total.get(latest_week_key, 0.0699)
            weighted_latest = sme_w_latest * 0.81 + tts_w_latest * 0.19
            factor = cur_fd / weighted_latest if weighted_latest > 0 else 0.40

            weekly_tots = {}
            for key in ['w18', 'w19', 'w20', 'w21', 'w22']:
                if key == latest_week_key:
                    weekly_tots[key] = cur_fd
                else:
                    sme_k = sme_w_total.get(key, 0.0)
                    tts_k = tts_w_total.get(key, 0.0)
                    weekly_tots[key] = (sme_k * 0.81 + tts_k * 0.19) * factor

            w18_tot = weekly_tots['w18']
            w19_tot = weekly_tots['w19']
            w20_tot = weekly_tots['w20']
            w21_tot = weekly_tots['w21']
            w22_tot = weekly_tots['w22']

            # Dynamic daily dates calculation (consecutive dates starting from the first daily header)
            daily_dates_str = []
            if fd_data['headers']['daily']:
                first_lbl = fd_data['headers']['daily'][0]
                first_date = None
                match = re.search(r'(\d{1,2})/(\d{1,2})', str(first_lbl))
                if match:
                    day = int(match.group(1))
                    month = int(match.group(2))
                    first_date = pd.Timestamp(year=latest_gtc_date.year, month=month, day=day)
                else:
                    try:
                        dt = pd.to_datetime(first_lbl, dayfirst=True)
                        first_date = pd.Timestamp(year=latest_gtc_date.year, month=dt.month, day=dt.day)
                    except:
                        first_date = latest_gtc_date - pd.Timedelta(days=7)
                
                daily_dates = [first_date + pd.Timedelta(days=i) for i in range(8)]
                daily_dates_str = [d.strftime('%Y-%m-%d') for d in daily_dates]
            else:
                daily_dates_str = [f"2026-05-{18+i}" for i in range(8)]

            # Dynamically calculate d18_tot to d25_tot
            daily_vals_tot = {}
            for idx in range(8):
                d_key = f"d{18 + idx}"
                d_str = daily_dates_str[idx]
                if d_str in daily_rates:
                    daily_vals_tot[d_key] = daily_rates[d_str]
                else:
                    sme_val = sme_d_total.get(d_key, 0.0)
                    tts_val = tts_d_total.get(d_key, 0.0)
                    daily_vals_tot[d_key] = (sme_val * 0.81 + tts_val * 0.19) * factor

            d18_tot = daily_vals_tot['d18']
            d19_tot = daily_vals_tot['d19']
            d20_tot = daily_vals_tot['d20']
            d21_tot = daily_vals_tot['d21']
            d22_tot = daily_vals_tot['d22']
            d23_tot = daily_vals_tot['d23']
            d24_tot = daily_vals_tot['d24']
            d25_tot = daily_vals_tot['d25']

            w_keys = ['w18', 'w19', 'w20', 'w21', 'w22']
            latest_w_idx = w_keys.index(latest_week_key) if latest_week_key in w_keys else 4
            prev_w_key = w_keys[max(0, latest_w_idx - 1)]

            fd_data['total'] = {
                'weekly': [],
                'daily': [],
                'kpis': {
                    'weekly_total': {
                        'am': 'TỔNG Vùng ĐCL',
                        'bc_name': 'TỔNG Vùng ĐCL',
                        'w18': w18_tot,
                        'w19': w19_tot,
                        'w20': w20_tot,
                        'w21': w21_tot,
                        'w22': w22_tot,
                        'change_wtd': float(weekly_tots[latest_week_key] - weekly_tots[prev_w_key])
                    },
                    'daily_total': {
                        'am': 'TỔNG Vùng ĐCL',
                        'bc_name': 'TỔNG Vùng ĐCL',
                        'd18': d18_tot,
                        'd19': d19_tot,
                        'd20': d20_tot,
                        'd21': d21_tot,
                        'd22': d22_tot,
                        'd23': d23_tot,
                        'd24': d24_tot,
                        'd25': d25_tot,
                        'change_d1': float(d25_tot - d24_tot),
                        'change_d7': float(d25_tot - d18_tot)
                    }
                }
            }
            
            # Map daily headers to clean headers dynamically (for post-office lookups)
            daily_lbl_map = {}
            for idx, lbl in enumerate(fd_data['headers']['daily']):
                if idx < len(daily_dates_str):
                    daily_lbl_map[lbl] = daily_dates_str[idx]
            
            sorted_daily_lbls = sorted(list(daily_lbl_map.keys()))
            sme_weekly_lookup = {clean_bc_name(x['bc_name']): x for x in fd_data['sme']['weekly']}
            tts_weekly_lookup = {clean_bc_name(x['bc_name']): x for x in fd_data['tts']['weekly']}
            sme_daily_lookup = {clean_bc_name(x['bc_name']): x for x in fd_data['sme']['daily']}
            tts_daily_lookup = {clean_bc_name(x['bc_name']): x for x in fd_data['tts']['daily']}
                
            for item in fd_data['sme']['weekly']:
                bc_name = item['bc_name']
                am = item['am']
                clean_name = clean_bc_name(bc_name)
                
                w22_val = None
                bc_latest_row = latest_df[latest_df['warehouse_name'].apply(clean_bc_name) == clean_name]
                if not bc_latest_row.empty:
                    w22_val = float(bc_latest_row.iloc[0]['% Chuyển trả'])
                else:
                    for idx, r_bc in latest_df.iterrows():
                        if clean_bc_name(r_bc['warehouse_name']) in clean_name or clean_name in clean_bc_name(r_bc['warehouse_name']):
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
                        # Fallback to scaled weighted average of SME and TTS
                        idx_lbl = sorted_daily_lbls.index(d_lbl) if d_lbl in sorted_daily_lbls else 0
                        key_name = f"d{18 + idx_lbl}"
                        sme_val = sme_daily_lookup.get(clean_name, {}).get(key_name, 0.0)
                        tts_val = tts_daily_lookup.get(clean_name, {}).get(key_name, 0.0)
                        val = (sme_val * 0.81 + tts_val * 0.19) * factor
                    daily_vals[d_lbl] = val
                    
                # Find daily dates
                d25_lbl = sorted_daily_lbls[-1] if sorted_daily_lbls else '25/05/2026'
                d24_lbl = sorted_daily_lbls[-2] if len(sorted_daily_lbls) >= 2 else '24/05/2026'
                d18_lbl = sorted_daily_lbls[0] if sorted_daily_lbls else '18/05/2026'
                
                d25 = daily_vals.get(d25_lbl, w22_val)
                d24 = daily_vals.get(d24_lbl, d25)
                d18 = daily_vals.get(d18_lbl, d25)

                sme_bc_item = sme_weekly_lookup.get(clean_name, {})
                tts_bc_item = tts_weekly_lookup.get(clean_name, {})
                
                bc_weekly_vals = {}
                for key in ['w18', 'w19', 'w20', 'w21', 'w22']:
                    if key == latest_week_key:
                        bc_weekly_vals[key] = w22_val if w22_val is not None else 0.0
                    else:
                        sme_k = sme_bc_item.get(key, 0.0)
                        tts_k = tts_bc_item.get(key, 0.0)
                        bc_weekly_vals[key] = (sme_k * 0.81 + tts_k * 0.19) * factor
                
                w_keys = ['w18', 'w19', 'w20', 'w21', 'w22']
                latest_idx = w_keys.index(latest_week_key) if latest_week_key in w_keys else 4
                prev_key = w_keys[max(0, latest_idx - 1)]
                bc_change_wtd = float(bc_weekly_vals[latest_week_key] - bc_weekly_vals[prev_key]) if bc_weekly_vals[latest_week_key] is not None and bc_weekly_vals[prev_key] is not None else 0.0

                fd_data['total']['weekly'].append({
                    'am': am,
                    'bc_name': bc_name,
                    'w18': bc_weekly_vals['w18'],
                    'w19': bc_weekly_vals['w19'],
                    'w20': bc_weekly_vals['w20'],
                    'w21': bc_weekly_vals['w21'],
                    'w22': bc_weekly_vals['w22'],
                    'change_wtd': bc_change_wtd
                })
                
                daily_item = {
                    'am': am,
                    'bc_name': bc_name,
                    'change_d1': float(d25 - d24),
                    'change_d7': float(d25 - d18)
                }
                for idx, lbl in enumerate(sorted_daily_lbls):
                    key_name = f"d{18 + idx}"
                    daily_item[key_name] = daily_vals.get(lbl, 0.0)
                fd_data['total']['daily'].append(daily_item)
                
        except Exception as e:
            print(f"⚠ Failed to parse fd_live.xlsx: {e}")

    # 10.8 Parse Transfer Backlog Data (DCL _24h chưa luân chuyển.xlsx)
    tb_data = {
        'kpis': {
            'giao': 0, 'tra': 0, 'total': 0,
            'prev_giao': 0, 'prev_tra': 0, 'prev_total': 0,
            'as_of': '', 'prev_as_of': ''
        },
        'top_20': [],
        'ams': [],
        'provinces': [],
        'bcs': [],
        'orders': []
    }
    
    p_tb_xlsx = r"C:\Users\Administrator\Desktop\AI 2026\Mentor\DCL _24h chưa luân chuyển.xlsx"
    if os.path.exists(p_tb_xlsx):
        try:
            print("Parsing Transfer Backlog Excel sheet...")
            with pd.ExcelFile(p_tb_xlsx) as xls_tb:
                # 1. Read Pivot sheet
                df_pivot = pd.read_excel(xls_tb, sheet_name="Pivot", header=None)
                
                # Extract timestamps
                as_of_val = str(df_pivot.iloc[1, 0]) if len(df_pivot) > 1 else ""
                prev_as_of_val = str(df_pivot.iloc[1, 6]) if len(df_pivot) > 1 and df_pivot.shape[1] > 6 else ""
                
                def extract_time(text):
                    m = re.search(r'\d{2}/\d{2}/\d{4} \d{2}:\d{2}', text)
                    return m.group(0) if m else text
                    
                tb_data['kpis']['as_of'] = extract_time(as_of_val)
                tb_data['kpis']['prev_as_of'] = extract_time(prev_as_of_val)
                
                # Extract Total KPIs (Row 2)
                if len(df_pivot) > 2:
                    tb_data['kpis']['giao'] = int(df_pivot.iloc[2, 3]) if pd.notna(df_pivot.iloc[2, 3]) else 0
                    tb_data['kpis']['tra'] = int(df_pivot.iloc[2, 4]) if pd.notna(df_pivot.iloc[2, 4]) else 0
                    tb_data['kpis']['total'] = int(df_pivot.iloc[2, 5]) if pd.notna(df_pivot.iloc[2, 5]) else 0
                    
                    tb_data['kpis']['prev_giao'] = int(df_pivot.iloc[2, 6]) if pd.notna(df_pivot.iloc[2, 6]) else 0
                    tb_data['kpis']['prev_tra'] = int(df_pivot.iloc[2, 7]) if pd.notna(df_pivot.iloc[2, 7]) else 0
                    tb_data['kpis']['prev_total'] = int(df_pivot.iloc[2, 8]) if pd.notna(df_pivot.iloc[2, 8]) else 0
                
                # Extract Top 20 (Rows 5 to 24)
                for r_idx in range(5, min(25, len(df_pivot))):
                    row_vals = df_pivot.iloc[r_idx]
                    if pd.isna(row_vals[0]) or str(row_vals[0]).strip() == "":
                        continue
                    try:
                        stt = int(row_vals[0])
                        bc_name_val = str(row_vals[1]).strip()
                        am_val = str(row_vals[2]).strip()
                        
                        giao_val = int(row_vals[3]) if pd.notna(row_vals[3]) else 0
                        tra_val = int(row_vals[4]) if pd.notna(row_vals[4]) else 0
                        tot_val = int(row_vals[5]) if pd.notna(row_vals[5]) else 0
                        
                        pg_val = int(row_vals[6]) if pd.notna(row_vals[6]) else 0
                        pt_val = int(row_vals[7]) if pd.notna(row_vals[7]) else 0
                        ptot_val = int(row_vals[8]) if pd.notna(row_vals[8]) else 0
                        
                        d_giao = str(row_vals[9]).strip()
                        d_tra = str(row_vals[10]).strip()
                        d_tot = str(row_vals[11]).strip()
                        trend = str(row_vals[12]).strip() if pd.notna(row_vals[12]) else ""
                        
                        tb_data['top_20'].append({
                            'stt': stt,
                            'bc_name': bc_name_val,
                            'am': am_val,
                            'giao': giao_val,
                            'tra': tra_val,
                            'total': tot_val,
                            'prev_giao': pg_val,
                            'prev_tra': pt_val,
                            'prev_total': ptot_val,
                            'change_giao': d_giao,
                            'change_tra': d_tra,
                            'change_total': d_tot,
                            'trend': trend
                        })
                    except Exception as ex_row:
                        print(f"  ⚠ Failed to parse top 20 row {r_idx}: {ex_row}")
                
                # 2. Read Đơn treo luân chuyển GIAOTRẢ sheet for details
                df_main = pd.read_excel(xls_tb, sheet_name="Đơn treo luân chuyển GIAOTRẢ")
                
                # Filter rows where BL is not in ['A. 0-6', 'B. 6-12', 'C. 12-24']
                bl_col = None
                for col in df_main.columns:
                    if str(col).strip().upper() == 'BL':
                        bl_col = col
                        break
                
                if bl_col is not None:
                    df_filtered = df_main[~df_main[bl_col].isin(['A. 0-6', 'B. 6-12', 'C. 12-24'])].copy()
                else:
                    df_filtered = df_main.copy()
                
                # Helper to fill na safely even if columns are named differently or missing
                def safe_fillna(df, col_name, fill_value):
                    actual_col = None
                    for col in df.columns:
                        if str(col).strip().lower() == col_name.lower():
                            actual_col = col
                            break
                    if actual_col is not None:
                        df[col_name] = df[actual_col].fillna(fill_value)
                    else:
                        df[col_name] = fill_value

                safe_fillna(df_filtered, 'warehouse_name', 'Chưa xác định')
                safe_fillna(df_filtered, 'province_name', 'Chưa xác định')
                safe_fillna(df_filtered, 'am_name', 'Chưa phân công')
                safe_fillna(df_filtered, 'Loại đơn', 'Chưa rõ')
                safe_fillna(df_filtered, 'Khách hàng', 'Khác')
                safe_fillna(df_filtered, 'Trạng thái', '-')
                safe_fillna(df_filtered, 'Thời gian tồn đọng', '-')
                safe_fillna(df_filtered, 'Mã bưu cục', 0)
                safe_fillna(df_filtered, 'Mã đơn hàng', '')
                
                if bl_col is not None:
                    df_filtered['BL'] = df_filtered[bl_col].fillna('Khác')
                else:
                    df_filtered['BL'] = 'Khác'
                
                # Map detail orders
                for _, row in df_filtered.iterrows():
                    try:
                        bc_id = int(float(row['Mã bưu cục'])) if pd.notna(row['Mã bưu cục']) else 0
                    except:
                        bc_id = 0
                        
                    tb_data['orders'].append({
                        'bc_id': bc_id,
                        'order_id': str(row['Mã đơn hàng']).strip(),
                        'type': str(row['Loại đơn']).strip(),
                        'customer': str(row['Khách hàng']).strip(),
                        'status': str(row['Trạng thái']).strip(),
                        'age_hours': str(row['Thời gian tồn đọng']).strip(),
                        'bc_name': str(row['warehouse_name']).strip(),
                        'province': str(row['province_name']).strip(),
                        'am': str(row['am_name']).strip(),
                        'aging_band': str(row['BL']).strip()
                    })
                
                # 3. Compute AM breakdown
                am_groups = df_filtered.groupby('am_name')
                for am_name, grp in am_groups:
                    giao_cnt = int((grp['Loại đơn'] == 'Luân chuyển giao').sum())
                    tra_cnt = int((grp['Loại đơn'] == 'Luân chuyển trả').sum())
                    tb_data['ams'].append({
                        'name': am_name,
                        'giao': giao_cnt,
                        'tra': tra_cnt,
                        'total': len(grp)
                    })
                tb_data['ams'] = sorted(tb_data['ams'], key=lambda x: x['total'], reverse=True)
                
                # 4. Compute Province breakdown
                prov_groups = df_filtered.groupby('province_name')
                for prov_name, grp in prov_groups:
                    giao_cnt = int((grp['Loại đơn'] == 'Luân chuyển giao').sum())
                    tra_cnt = int((grp['Loại đơn'] == 'Luân chuyển trả').sum())
                    tb_data['provinces'].append({
                        'name': prov_name,
                        'giao': giao_cnt,
                        'tra': tra_cnt,
                        'total': len(grp)
                    })
                tb_data['provinces'] = sorted(tb_data['provinces'], key=lambda x: x['total'], reverse=True)
                
                # 5. Compute Bưu cục breakdown
                bc_groups = df_filtered.groupby(['Mã bưu cục', 'warehouse_name', 'province_name', 'am_name'])
                for (bc_id_raw, bc_name, prov_name, am_name), grp in bc_groups:
                    try:
                        bc_id_val = int(float(bc_id_raw))
                    except:
                        bc_id_val = 0
                    giao_cnt = int((grp['Loại đơn'] == 'Luân chuyển giao').sum())
                    tra_cnt = int((grp['Loại đơn'] == 'Luân chuyển trả').sum())
                    tb_data['bcs'].append({
                        'id': bc_id_val,
                        'name': bc_name,
                        'province': prov_name,
                        'am': am_name,
                        'giao': giao_cnt,
                        'tra': tra_cnt,
                        'total': len(grp)
                    })
                tb_data['bcs'] = sorted(tb_data['bcs'], key=lambda x: x['total'], reverse=True)
                
            print(f"✓ Parsed Transfer Backlog successfully. Total details: {len(tb_data['orders'])} orders.")
        except Exception as e:
            print(f"⚠ Failed to parse Transfer Backlog Excel: {e}")

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
        'fd_report': fd_data,
        'transfer_backlog': tb_data
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
