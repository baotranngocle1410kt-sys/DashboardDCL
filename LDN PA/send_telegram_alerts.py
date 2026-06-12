import json
import os
import sys
import urllib.request
import urllib.error

# Ensure UTF-8 output
sys.stdout.reconfigure(encoding='utf-8')

p_json = r"C:\Users\Administrator\Desktop\AI 2026\LDN PA\Vitality Compass\operations_data.json"
p_config = r"C:\Users\Administrator\Desktop\AI 2026\LDN PA\telegram_config.json"

def main():
    print("Checking for anomalies and preparing Telegram alerts...")
    
    if not os.path.exists(p_json):
        print(f"Error: JSON data file not found at {p_json}")
        sys.exit(1)
        
    if not os.path.exists(p_config):
        print(f"Error: Telegram configuration file not found at {p_config}")
        sys.exit(1)
        
    # 1. Load config
    with open(p_config, 'r', encoding='utf-8') as f:
        config = json.load(f)
        
    token = config.get("BOT_TOKEN")
    chat_id = config.get("CHAT_ID")
    
    if not token or token == "YOUR_TELEGRAM_BOT_TOKEN" or not chat_id or chat_id == "YOUR_TELEGRAM_CHAT_ID":
        print("Telegram bot token or chat ID is not configured. Skipping alert transmission.")
        print("Please configure telegram_config.json with your actual bot credentials.")
        sys.exit(0)
        
    # 2. Load data
    with open(p_json, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    latest_date = data.get("latest_date")
    bcs = data.get("bcs", [])
    ams = data.get("ams", [])
    kpis = data.get("kpis", {})
    
    # Format date strings for example: 09/05/26 and 08/05/26
    from datetime import datetime, timedelta
    dt = datetime.strptime(latest_date, "%Y-%m-%d")
    latest_date_str = dt.strftime("%d/%m/%y")
    yest_dt = dt - timedelta(days=1)
    yest_date_str = yest_dt.strftime("%d/%m/%y")
    
    # 3. Find anomalies
    # Criteria: GTC < 55% or Backlog > 100 or shortage_actual >= 2
    critical_bcs = []
    for bc in bcs:
        hr = bc.get("hr", {})
        shortage = hr.get("shortage_actual", 0)
        if bc["gtc"] < 0.55 or bc["backlog"] > 100 or shortage >= 2:
            critical_bcs.append(bc)
            
    if not critical_bcs:
        print("No critical post offices found. All parameters are within normal ranges.")
        return
        
    # 4. Format Message
    message = f"🚨 *[BÁO CẢNH BÁO VẬN HÀNH & NHÂN SỰ DCL]* 🚨\n📅 *Ngày dữ liệu:* {latest_date_str}\n\n"
    message += f"📊 *Chỉ số toàn vùng:*\n"
    message += f"• GTC: {kpis.get('gtc', {}).get('value', 0)*100:.2f}%\n"
    message += f"• FD (Trả): {kpis.get('fd', {}).get('value', 0)*100:.2f}%\n"
    message += f"• Backlog: {kpis.get('backlog', {}).get('value', 0):,} đơn\n"
    message += f"• Nhân sự: Thiếu {kpis.get('hr', {}).get('total_shortage_actual', 0)} shipper\n\n"
    
    message += f"🔥 *Danh sách bưu cục bất ổn:*\n\n"
    for bc in critical_bcs[:10]: # limit to top 10
        change_n1 = abs(bc["gtc_change"]) * 100
        # Compare to specific post office's GTC last week if available, otherwise fallback to 90%
        gtc_vs_lw = bc.get("gtc_vs_lastweek", bc["gtc"] - 0.90)
        change_baseline = abs(gtc_vs_lw) * 100
        
        hr = bc.get("hr", {})
        shortage = hr.get("shortage_actual", 0)
        target = hr.get("target_headcount", 0)
        tuyen_thieu = hr.get("tuyen_thieu", "")
        
        hr_text = f"nhân sự đang thiếu {shortage}/{target} định biên"
        tuyen_text = f", tuyến thiếu ({tuyen_thieu})" if tuyen_thieu else ""
        
        clean_cause = bc['cause']
            
        message += f"📍 *{bc['name']}*\n"
        message += f"  • {bc['name']} có chỉ số GTC ngày {latest_date_str} thấp hơn ngày hôm N-1 ({yest_date_str}) {change_n1:.2f}%. So với cùng kỳ giảm {change_baseline:.2f}% do {clean_cause}, {hr_text}{tuyen_text}.\n"
        message += f"  • AM: {bc['am']} ({bc['am_tele'] or '@chua_co_tele'})\n"
        message += f"  • Đơn tồn >5 ngày: *{bc['backlog']} đơn*\n\n"
        
    if len(critical_bcs) > 10:
        message += f"_...và {len(critical_bcs) - 10} bưu cục khác._\n\n"
        
    message += "👉 Đề nghị các AM và HRBP phối hợp giải tỏa backlog và tuyển bổ sung shipper gấp!"
    bc_col_idx = 0 # dummy line for formatting
    
    # 5. Send message
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "Markdown"
    }
    
    data_bytes = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(
        url,
        data=data_bytes,
        headers={'Content-Type': 'application/json'}
    )
    
    try:
        with urllib.request.urlopen(req) as response:
            res_data = json.loads(response.read().decode('utf-8'))
            if res_data.get("ok"):
                print("Successfully sent Telegram alert notification!")
            else:
                print(f"Failed to send Telegram alert: {res_data.get('description')}")
    except urllib.error.HTTPError as e:
        try:
            res_err = json.loads(e.read().decode('utf-8'))
            print(f"Failed to send Telegram alert (HTTP Error {e.code}): {res_err.get('description')}")
        except:
            print(f"Failed to send Telegram alert: HTTP Error {e.code}")
    except Exception as e:
        print(f"Error sending request to Telegram: {e}")

if __name__ == '__main__':
    main()
