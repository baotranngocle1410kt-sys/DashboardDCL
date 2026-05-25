# 📖 HƯỚNG DẪN SỬ DỤNG HỆ SINH THÁI QUẢN TRỊ CÔNG VIỆC (LDN PA)

> **Phiên bản:** 1.0 | **Ngày tạo:** 04/05/2026
> Tài liệu này hướng dẫn bạn từng bước cách sử dụng toàn bộ hệ thống quản lý công việc cá nhân kết hợp vận hành GHN.

---

## MỤC LỤC

1. [Tổng quan hệ thống](#1-tổng-quan-hệ-thống)
2. [Cách mở Dashboard (Vitality Compass)](#2-cách-mở-dashboard)
3. [Thao tác trên Dashboard](#3-thao-tác-trên-dashboard)
4. [Cấu trúc thư mục & File quan trọng](#4-cấu-trúc-thư-mục)
5. [Quy trình làm việc hàng ngày](#5-quy-trình-hàng-ngày)
6. [Lưu ý quan trọng](#6-lưu-ý-quan-trọng)

---

## 1. TỔNG QUAN HỆ THỐNG

Hệ thống gồm 2 phần chính:

| Thành phần | Mô tả |
|---|---|
| **Thư mục `LDN PA`** | Chứa toàn bộ file Markdown (.md) là "bộ não" lưu trữ dữ liệu |
| **Vitality Compass** | Dashboard web mở trên trình duyệt, đọc/ghi trực tiếp vào các file .md |

**Không cần cài đặt gì thêm.** Không Node.js, không server, không đám mây. Mọi thứ chạy 100% cục bộ trên máy tính của bạn.

---

## 2. CÁCH MỞ DASHBOARD

### Bước 1: Mở file HTML
- Vào thư mục: `LDN PA > Vitality Compass`
- **Nhấp đúp** vào file `index.html`
- Hoặc kéo thả file vào trình duyệt **Google Chrome** hoặc **Microsoft Edge**

> ⚠️ **Quan trọng:** Chỉ dùng Chrome hoặc Edge. Firefox/Safari KHÔNG hỗ trợ File System Access API.

### Bước 2: Chọn thư mục LDN PA
- Khi mở lần đầu, bạn thấy màn hình chào mừng với nút **"📂 Chọn thư mục LDN PA"**
- Nhấn nút đó → Trình duyệt mở hộp thoại chọn thư mục
- **Chọn đúng thư mục `LDN PA`** (thư mục cha chứa file `Task Systems.md`)
- Nhấn **"Select Folder"** → Trình duyệt hỏi cấp quyền → Nhấn **"Allow" / "Cho phép"**

### Bước 3: Hoàn tất
- Dashboard hiện ra đầy đủ với các tác vụ, thói quen, biểu đồ
- Bạn có thể **Bookmark** trang này để mở nhanh mỗi ngày

> 💡 **Mẹo:** Mỗi lần mở lại trang (F5 hoặc mở mới), bạn cần nhấn nút **"📂 Đổi thư mục"** để cấp quyền lại. Đây là giới hạn bảo mật của trình duyệt.

---

## 3. THAO TÁC TRÊN DASHBOARD

### 3.1 🎯 Tiêu Điểm Tựu Thành (Top 3 Priorities)

Đây là 3 việc quan trọng nhất trong ngày.

| Thao tác | Cách làm |
|---|---|
| **Thêm tiêu điểm** | Gõ vào ô "Thêm tiêu điểm..." → Nhấn nút **+** hoặc **Enter** |
| **Đánh dấu hoàn thành** | Nhấn vào ô vuông bên trái task → Ô chuyển xanh ✓ |
| **Bỏ đánh dấu** | Nhấn lại ô vuông đã xanh → Trở về trạng thái chưa làm |

> File `Task Systems.md` sẽ tự động cập nhật `- [ ]` thành `- [x]` trên ổ cứng.

### 3.2 📋 Các luồng Tác vụ

Dashboard hiển thị 6 loại tác vụ theo phân loại trong `Task Systems.md`:
- ✍️ **Creating** — Sáng tạo, sản xuất
- 🔍 **Reviewing** — Kiểm duyệt, phê duyệt (check mail, phiếu tồn đọng)
- 🔗 **Connecting** — Chuyển tiếp, kết nối
- 🗣️ **Presencing** — Hiện diện, tương tác (họp, đối ngoại)
- 🧘 **Contemplating** — Chiêm nghiệm
- 🔭 **Tầm nhìn xa** — Việc ngày mai & tuần tới

| Thao tác | Cách làm |
|---|---|
| **Thêm tác vụ** | Chọn loại mục từ dropdown → Gõ nội dung → Nhấn **+** |
| **Hoàn thành** | Nhấn ô vuông bên trái |

### 3.3 🔄 Thói quen hôm nay

Thói quen hiển thị dạng **nút bật/tắt (toggle)** thay vì checkbox:

| Thao tác | Cách làm |
|---|---|
| **Bật (đã làm)** | Nhấn nút toggle → Chuyển sang xanh, trượt sang phải |
| **Tắt (chưa làm)** | Nhấn lại → Chuyển về xám |

### 3.4 ⚡ Ghi nhanh vào Notebook

Khu vực bên phải cho phép bạn ghi nhanh ý tưởng/việc phát sinh mà không cần mở Obsidian:

| Tab | Ghi vào đâu trong Notebook.md |
|---|---|
| 💡 **Ý tưởng** | Mục `## 💡 Ý tưởng đột xuất (Ideas)` |
| 🚨 **Gấp hôm nay** | Mục `### 🚨 Gấp trong hôm nay` |
| 🌅 **Ngày mai** | Mục `### 🌅 Gấp trong ngày mai` |
| 🛋️ **Không gấp** | Mục `### 🛋️ Không gấp (Thuộc dự án)` |

**Cách dùng:** Chọn tab → Gõ nội dung → Nhấn **"Gửi"** hoặc **Enter**

### 3.5 📊 Biểu đồ Quân bình Tác vụ (Radar Chart)

Biểu đồ hình mạng nhện tự động cập nhật khi bạn hoàn thành task. Nó đo lường sự cân bằng giữa 6 loại tác vụ:
- Nếu biểu đồ **lệch một phía** → Bạn đang thiên lệch quá nhiều vào một loại công việc
- Biểu đồ **đều các cạnh** → Ngày làm việc quân bình, lý tưởng

### 3.6 📈 Chỉ số Vận hành (KPI)

Khu vực hiển thị các chỉ số GHN:
- **GTC** (Giao Thành Công)
- **FD** (Tỷ lệ trả)
- **Ontime** (Đúng hạn)
- **Backlog >3 ngày**

> 📌 Hiện tại đang hiển thị **dữ liệu mẫu**. Để cập nhật số liệu thực, AI Agent sẽ đọc dữ liệu từ Looker/Excel và ghi vào file `Operations_Insights.md`.

### 3.7 👥 Đánh giá AM

Bảng xếp hạng Area Manager với đánh giá Mạnh/Yếu/Cải thiện. Cũng đang dùng dữ liệu mẫu, sẽ được AI cập nhật qua `Operations_Insights.md`.

### 3.8 🔄 Nút Làm mới

- Nhấn nút **"🔄 Làm mới"** trên thanh header để tải lại dữ liệu mới nhất từ file
- **Không cần reload** cả trang — chỉ cập nhật dữ liệu

---

## 4. CẤU TRÚC THƯ MỤC

```
LDN PA/
├── .agents/workflows/     ← 12 file workflow cho AI Agent
├── Archives/              ← Kho lưu trữ cũ
│   └── Void_Archive.md
├── Daily Notes/           ← Nhật ký theo ngày/tháng
├── Meetings/Archived/     ← Biên bản họp
├── Messages/              ← Log trao đổi
├── Plans/                 ← Kế hoạch
├── Solutions/             ← Giải pháp
├── Vitality Compass/      ← Dashboard Web App
│   ├── index.html
│   ├── styles.css
│   └── app.js
├── Task Systems.md        ← ⭐ Bảng việc chính (Dashboard đọc file này)
├── Notebook.md            ← Trạm nháp ghi chú nhanh
├── Projects.md            ← Quản lý dự án
├── Routine.md             ← Thói quen lặp lại
├── ideas.md               ← Khu vườn ý tưởng
├── Sketch.md              ← Bàn nháp sản xuất
├── insights.md            ← Chiêm nghiệm cá nhân
├── Learning.md            ← Kho tri thức
└── Operations_Insights.md ← Dữ liệu vận hành cho Dashboard
```

### Các file quan trọng nhất:

| File | Vai trò |
|---|---|
| `Task Systems.md` | Bảng việc DUY NHẤT trong ngày. Dashboard đọc/ghi file này |
| `Notebook.md` | Nơi ghi nhanh ý tưởng và việc phát sinh |
| `Routine.md` | Thói quen hàng ngày/tuần/tháng |
| `Operations_Insights.md` | AI ghi phân tích KPI, cảnh báo, dự báo vào đây |

---

## 5. QUY TRÌNH LÀM VIỆC HÀNG NGÀY

### 🌅 Buổi sáng (8h-9h)
1. Mở Dashboard Vitality Compass trên trình duyệt
2. Nhấn **"📂 Chọn thư mục LDN PA"** → Cấp quyền
3. Xem các thói quen → Bật toggle cho những việc đang làm
4. Xem chỉ số vận hành N-1 (GTC, FD, Ontime, Backlog)
5. Thêm 3 Tiêu Điểm Tựu Thành cho hôm nay

### 🏢 Trong ngày
6. Khi hoàn thành việc → Tick ✓ trên Dashboard
7. Khi có ý tưởng đột xuất → Ghi nhanh vào tab "⚡ Ghi nhanh"
8. Khi có việc phát sinh gấp → Chọn tab 🚨 → Ghi vào Notebook
9. Nhấn **"🔄 Làm mới"** để cập nhật dữ liệu mới (nếu AI đã xử lý file)

### 🌙 Cuối ngày
10. Xem Progress Bar → Đánh giá % hoàn thành
11. Xem Radar Chart → Kiểm tra sự quân bình tác vụ
12. Những việc chưa xong sẽ tự nằm lại cho ngày mai

---

## 6. LƯU Ý QUAN TRỌNG

### ⚠️ Quy tắc kỹ thuật TUYỆT ĐỐI không được vi phạm

1. **Không đổi tên các Heading (##)** trong `Task Systems.md` — Dashboard dựa vào tên chính xác để parse dữ liệu
2. **Format task phải đúng:** `- [ ] ` (chưa làm) hoặc `- [x] ` (đã làm)
   - Sai: `- [  ] ` (2 dấu cách) hoặc `- [X] ` (X viết hoa)
3. **Dùng Chrome hoặc Edge** — Trình duyệt khác không hỗ trợ File System Access API

### 💡 Mẹo hay

- **Bookmark** file `index.html` để mở nhanh mỗi ngày
- Dashboard và Obsidian có thể mở **song song** — cả hai đọc cùng file, không xung đột
- Nếu AI Agent (AntiGravity) xử lý file trong nền, chỉ cần nhấn **"🔄 Làm mới"** để thấy thay đổi

---

*Chúc bạn có những ngày làm việc hiệu quả và quân bình! 🧭*
