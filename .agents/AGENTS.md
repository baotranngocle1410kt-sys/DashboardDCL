# Project-Scoped Rules & Knowledge

## 1. Số liệu vận hành (GTC & Volume)
*   **Sử dụng dữ liệu mới nhất:** Số liệu GTC và sản lượng (Volume) cần được cập nhật theo báo cáo Looker Studio mới nhất (ví dụ: ngày 03/08/2026 là `60.22%` GTC, sản lượng `67,438`).
*   **Xử lý Link 1 (Performance Report):** Google Sheet Link 1 là link riêng tư (Private). Khi chạy tự động không có session cookie, urllib/requests sẽ báo lỗi 401 Unauthorized. Hệ thống cần sử dụng các giá trị ghi đè (overrides) hoặc đọc từ tệp `link1_live.xlsx` do người dùng tải xuống thủ công.

## 2. Loại bỏ trùng lặp dữ liệu Nhân sự (Recruitment Double-Counting)
*   **Cấu trúc bảng Tuyển dụng (Recruitment Sheet):** Sheet báo cáo tuần (ví dụ: `Tổng hợp (T32)`) bao gồm **1 bảng Master tổng hợp** bên trái (bắt đầu từ cột `Bưu cục` đầu tiên, index 9) và 5 bảng chi tiết các tỉnh bên phải.
*   **Tránh double-counting:** Chỉ parse duy nhất bảng Master đầu tiên (`subtables[:1]`). Tuyệt đối không được gộp các bảng con bên phải để tránh việc cộng dồn gấp đôi số thiếu hụt shipper, số tuyển mới (OB) và số nghỉ việc.

## 3. Hiển thị động thông tin HRBP & Intern
*   Tên các **HRBP phụ trách** và **HRBP Intern** hiển thị tại bảng tổng hợp tỉnh trong file `app.js` phải được render động lấy trực tiếp từ thuộc tính `p.hr.hrbp` và `p.hr.intern` của dữ liệu JSON, không được hardcode bằng tay trong code giao diện.
