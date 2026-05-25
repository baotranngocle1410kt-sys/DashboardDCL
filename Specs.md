# PRODUCT SPECIFICATION: HỆ SINH THÁI QUẢN TRỊ CÔNG VIỆC CÁ NHÂN (AI-DRIVEN)
**Phiên bản:** 4.0 (Kiến trúc Dòng chảy 5 Tầng & System Bootstrap)
**Tác giả:** Lương Dũng Nhân
**Trạng thái:** Hoạt động (Active Production)
**Hệ điều hành cốt lõi:** Obsidian (Markdown) + Local Web App (File System Access) + AI CLI Agents

Bản Hiến pháp này quy định toàn bộ nguyên lý thiết kế, cấu trúc dữ liệu, và quy tắc vận hành nghiêm ngặt cho bất kỳ Hệ thống AI Agent nào (VD: AntiGravity) tương tác với bộ não thứ hai của Lương Dũng Nhân. Specs này cũng đóng vai trò là sách hướng dẫn tự mọc rễ (Bootstrap Guide) để AI khởi tạo hệ thống từ con số 0.

---

## 1. TRIẾT LÝ NỀN TẢNG (CORE PHILOSOPHY)

Hệ thống được thiết kế dựa trên Tâm lý học Thần kinh (Neuroscience) để giải quyết "Nghịch lý Năng suất":
- **Triết lý "AI làm việc để ta được làm người" (AI fast for human slow):** Máy móc xử lý tốc độ cao để giải phóng băng thông nhận thức (cognitive bandwidth), tạo khoảng không cho việc sống chậm lại, suy nghĩ sâu, và hiện diện trọn vẹn.
- **Phân tách Tầng Thao tác & Tầng Nhận thức:** AI đảm nhiệm 100% công việc "chân tay kỹ thuật số" (cào dữ liệu, trích xuất, gán nhãn, chuyển file, báo cáo). Người dùng chỉ tập trung duy nhất vào việc tạo ra giá trị, từ chối việc kéo thả hay dọn dẹp hệ thống.
- **Hoạt hóa Hệ Thần kinh Phó giao cảm (Parasympathetic activation):** Giao diện bị giới hạn ngặt nghèo ở 3 Tiêu điểm cốt lõi, loại bỏ hoàn toàn notification và danh sách vô tận gây "brain fry".

---

## 2. DÒNG CHẢY 5 TẦNG DỮ LIỆU (THE 5-TIER LIFECYCLE)

### TẦNG 1 - THU NẠP (INPUT LAYER)
Nơi tiếp nhận nguyên liệu thô (raw materials). Sự hỗn độn được định sẵn và chấp nhận tuyệt đối.
- **`Notebook.md`**: Trạm nháp nhanh thu lại mọi suy nghĩ phát sinh.
- **`Meetings/`**: Chứa Biên bản họp.
- **`Messages/`**: Chứa log trao đổi (VD: `Messages/Donald.md`).
- **`Daily Notes/[YYYY-MM-DD].md`**: File đồng bộ lịch từ Google Calendar/Outlook.

### TẦNG 2 - CẤU TRÚC HÓA (STRUCTURE LAYER)
Quá trình AI khởi chạy các Workflow "nhai" dữ liệu Tầng 1, chiết xuất ra action-items tinh khiết.
- **Trích xuất & Điều hướng:** Biến đổi văn bản thành list tác vụ (`- [ ] `) và chuyển về Bảng việc (`Task Systems.md`) hoặc `Projects.md`. Chuyển ý tưởng sang `ideas.md`.
- **Deadline Chủ động:** Task chứa `{DD/MM}` $\le$ 1 tuần bốc thẳng lên Bảng việc Hôm nay. 1 tuần $<$ Deadline $\le$ 2 tuần đưa vào `🔭 Tầm nhìn xa`.
- **Artifact Recap (Báo cáo Tĩnh tại):** AI bắt buộc báo cáo: **Nội dung Task | Nguồn xuất xứ | Context (1-2 câu)** để chủ nhân nắm bắt bối cảnh, chống đứt gãy thông tin (lose track).
- **Dọn dẹp Bể rác:** Cắt biên bản cũ vào `Meetings/Archived/`, block chat cũ đẩy xuống `## 🗄️ Đã xử lý (Old)`.

### TẦNG 3 - TẬP TRUNG (FOCUS LAYER)
Buồng lái tác chiến theo thời gian thực (Real-time Execution).
- **`Task Systems.md`**: Bản đồ công việc DUY NHẤT trong ngày, bị giới hạn tối đa 3 Tiêu Điểm Tựu Thành.
- **`Vitality Compass`:** Ứng dụng Web App (Local HTML5), kết nối trực tiếp với file gốc qua `File System Access API`.

### TẦNG 4 - SẢN PHẨM (OUTPUT LAYER)
Nơi AI và con người thiết lập khế ước đồng sáng tạo giá trị.
- **`Sketch.md`**: Bàn nháp. AI tham chiếu nội dung nguyên thủy để thảo text (email, kế hoạch). Con người là Human-in-the-loop duyệt và chỉnh giọng văn (Authentic Tone) rồi gửi.

### TẦNG 5 - HỌC HỎI (LEARNING LAYER)
Ký ức ngoài (External Memory). Chuyển hóa những việc đã kết thúc thành tri thức.
- **`Daily Notes/[YYYY-MM].md`**: Cuối ngày, AI dọn dẹp task `- [x] ` dồn vào đây đúc thành "Nhật ký Thành tựu".
- **`Learning.md`**: Đình làng tri thức chứa bài học kinh nghiệm phân theo Domain (ngách kỹ năng).
- **`insights.md`**: Đền thờ các chiêm nghiệm tâm lý, triết lý cá nhân. Lớp "phù sa" tinh túy nhất.

---

## 3. KHO TÀNG 12 LỆNH PHÉP VẬN HÀNH (WORKFLOWS)

Linh hồn hệ thống chia làm 4 Nhóm tại `.agents/workflows/`. AI tự động tuân thủ thứ tự lệnh cực kỳ nghiêm ngặt.

### 3.1 Nhóm Vận Hành Đầu Cuối (Operations)
- **`/pa-start`**: Bình minh. Cào lịch sự kiện, ném Routine và task cũ, soi xét Deadline Chủ động, ép định đoạt 3 Tiêu điểm. Trả về Artifact Recap. Cắt đứt hôm qua bằng việc xoá file Calendar cũ.
- **`/pa-sync`**: Giữa dòng. Hút dữ liệu từ `Meeting`, `Messages`, `Notebook`. Ép thành tác vụ đẩy về `Task Systems`. Dọn dẹp đồ cũ xuống mục `Old`. Bắt buộc Trả về Artifact Recap.
- **`/pa-summarize`**: Hoàng hôn. Tổng kết task đã xong (`- [x] `) đắp vào `Daily Notes` làm lịch sử. Tự động rút ngẫu nhiên bài học sâu sắc ghi vào `Learning`. DỌN TRẮNG bộ khung `Task Systems.md` để xả não.

### 3.2 Nhóm Kỷ Luật Thời Gian (Time Management)
- **`/pa-schedule-start`**: Quét ngầm. Lọc tất cả task chực chờ `- [ ] ` CHƯA MANG định dạng `{...}` trong toàn hệ thống, tự động nối thêm chuỗi ` {}` và đẩy ra `Need-scheduling.md` (giữ nguyên nhóm heading dự án). Đợi User điền ngày.
- **`/pa-schedule-end`**: Phục hồi. Đọc `Need-scheduling.md`, phớt lờ các empty `{}`, String Matching hoàn hảo để ghi đè `{DD/MM}` ngược lại vào file gốc. Xoá nháp.

### 3.3 Nhóm Phân Tích & Giác Quan (Contemplation & Analysis)
- **`/pa-search`**: Radar toàn quang. Khảo sát thông tin toàn hệ thống 5S và trả về bức tranh toàn cảnh (Search) cho User trước khi ra quyết định lớn.
- **`/pa-seek`**: Ánh sáng gầm giường. Khảo sát thâm sâu phát hiện mô thức & điểm mù hệ thống nằm rải rác trong thói quen làm việc (Seek).
- **`/pa-sense`**: Lăng kính tâm lý. Khảo sát tĩnh tại, quét toàn diện tâm thế của dữ liệu đa hệ thống để tư vấn Somatic Coaching.
- **`/pa-solve`**: Máy gia tốc tư duy. Tư duy thấu đáo đa chiều để giải quyết gốc rễ một "Pain point" cụ thể.
- **`/pa-speculate`**: Phản tư định kỳ. Đọc lại Tàng thư `Learning` & `Daily Notes` hàng tháng/quý để chiêm nghiệm.

### 3.4 Nhóm Sản Xuất & Thanh Tẩy (Production & Sanitization)
- **`/pa-sketch`**: Trạm sản xuất. Khảo sát các đầu việc giao tiếp và sơ thảo nháp tin nhắn theo văn phong nguyên bản qua `Sketch.md`.
- **`/pa-clean`**: Đại thanh tẩy. Quét toàn bộ vùng `## 🗄️ Đã xử lý (Old)`, CẮT (Cut) text và ĐÀY (Append) vào `Archives/Void_Archive.md` để hệ thống siêu nhẹ.

---

## 4. LẰN RANH ĐỎ KỸ THUẬT (STRICT TECHNICAL CONSTRAINTS)

Nếu bạn là AI Agent chuẩn bị chạm tay vào hệ thống này, BẠN PHẢI TUÂN THỦ:
1. **Toàn vẹn Cấu trúc DOM (DOM Integrity):** Local Web App dựa vào vị trí Headings (Dấu `##`) và Substring Index. ĐỔI TÊN HEADING HAY TẠO HEADING LẠ TRONG `Task Systems.md` SẼ DẪN ĐẾN CRASH SERVER APP.
2. **Quy tắc Terminal Physical Deletion:** Việc xoá file như `Need-scheduling.md` hay `Daily Notes/...` BẮT BUỘC dùng Bash script thông qua Terminal (`rm file`). Việc "Edit To Empty String" bị cấm.
3. **Quy tắc String Match:** Trạng thái task phụ thuộc vào 6 ký tự lõi: `- [ ] ` và `- [x] `. Dư 1 dấu cách `- [  ] `, hay viết Hoa `- [X] ` sẽ khiến thuật toán DOM Regex từ chối dịch mã (Fail-fast).

---

## 5. HƯỚNG DẪN CẮM RỄ HỆ THỐNG (SYSTEM BOOTSTRAP GUIDE)

Nếu hệ sinh thái bị sập hoặc phải thiết lập cho User mới, AI có trách nhiệm dựa vào 2 sơ đồ dưới đây để khôi phục cõi nhân gian này bằng Terminal và Write_file.

### 5.1 Sơ Đồ Cây Thư Mục (Folder Tree)
```text
LDN PA/
├── .agents/
│   └── workflows/
│       ├── pa-clean.md, pa-schedule-end.md, pa-schedule-start.md, pa-search.md, pa-seek.md, pa-sense.md, pa-sketch.md, pa-solve.md, pa-speculate.md, pa-start.md, pa-summarize.md, pa-sync.md
├── Archives/
│   └── Void_Archive.md
├── Daily Notes/
│   ├── YYYY-MM-DD.md
│   └── YYYY-MM.md
├── Meetings/
│   └── Archived/
├── Messages/
├── Plans/
├── Solutions/
├── Vitality Compass/
├── Task Systems.md
├── Notebook.md
├── Projects.md
├── Routine.md
├── Sketch.md
├── ideas.md
├── insights.md
└── Learning.md
```

### 5.2 Bộ Sườn Khung Xương (Markdown Headings Skeleton)

Tuyệt đối không sử dụng sai text của các Heading này khi Bootstrap. Các lệnh `.replace` đè lên chúng.

#### A. File `Task Systems.md`
```markdown
# 📅 Bảng Việc Ngày [Hôm Nay]

## 🎯 Tiêu Điểm Tựu Thành (Top 3 Priorities)
*(Vui lòng chọn 3 việc cốt lõi nhất để tập trung 80% năng lượng hôm nay)*

## 🔄 Thói quen (Daily/Weekly Routines)

## ✍️ Creating (Sáng tạo, sản xuất)

## 🔍 Reviewing (Kiểm duyệt, phê duyệt)

## 🔗 Connecting (Chuyển tiếp, kết nối)

## 🗣️ Presencing (Hiện diện, tương tác)

## 🧘 Contemplating (Chiêm nghiệm)

---
## 🔭 Tầm nhìn xa (Ngày mai & Tuần tới)

```

#### B. File `Notebook.md`
```markdown
# 📝 Trạm Nháp & Ghi Chú (Notebook)

## 💡 Ý tưởng đột xuất (Ideas)

## ✅ Tác vụ phát sinh (Tasks)
### 🚨 Gấp trong hôm nay
### 🌅 Gấp trong ngày mai
### 🛋️ Không gấp (Thuộc dự án)

---
## 🗄️ Đã xử lý (Old)

```

#### C. File `Projects.md`
```markdown
# 🌳 KHU RỪNG DỰ ÁN (PROJECTS LANDSCAPE)

> *"Mỗi dự án là một hệ sinh thái nhỏ. Có những mầm đang nhú, có những cây đang vươn tán, và có những mùa vụ đã thu hoạch trọn vẹn."*

---

## 🌊 1. CÁC DỰ ÁN HIỆN HÀNH (Active - Đang dồn năng lượng)
### 1.1. Viết lách & Học thuật 🖋️
### 1.2. Vận hành & Hệ thống ⚙️
### 1.3. Khai vấn & Sản phẩm giáo dục 🧠

## 🏔️ 2. DỰ ÁN LƯU TRỮ HOẶC DÀI HẠN (Backlog & Someday)
```

#### D. File `Routine.md`
```markdown
# 🔄 Nhịp điệu & Thói quen (Routines)

Năng lượng của vũ trụ vận hành theo chu kỳ. Hệ thống thói quen này là mỏ neo giúp chúng ta không bị cuốn trôi.

## 🌅 Hàng ngày (Daily)
- [ ] [Daily] 🧘 Somatic Check-in & Hơi thở 5 phút (Khởi tâm đầu ngày).
- [ ] [Daily] Mở đầu ngày mới pa-start, cân nhắc kỹ 3 việc ưu tiên.

## 📅 Hàng tuần (Weekly)
### Thứ Hai
### Thứ Ba
### Thứ Tư
### Thứ Năm
### Thứ Sáu
### Thứ Bảy
### Chủ Nhật

## 🌙 Hàng tháng (Monthly)
### Ngày 1
### Ngày 15
### Ngày Cuối Tháng

## 🍂 Hàng năm (Yearly)
### Ngày 1/1
```

#### E. File `ideas.md`
```markdown
# 💡 Khu vườn Ý tưởng (Ideas)

Lưu trữ và ươm mầm các ý tưởng, concept, insight từ dòng chảy.

## ươm mầm (In Progress / Backlog)

### ✍️ Nội dung & Bài viết

### 📚 Giáo án & Đào tạo

### 🛠️ Hệ thống & Sản phẩm

---

## 🗄️ Đã thu hoạch (Archived - Tự động luân chuyển bởi pa-sync)

```

*(Toàn bộ nội dung của Hiến Pháp phải được hiểu, ghi nhớ, và áp dụng bằng sự cẩn trọng cao nhất.)*

---

## 6. HƯỚNG DẪN CÀI ĐẶT & SỬ DỤNG GIAO DIỆN (DASHBOARD UI SETUP & USAGE)

Hệ sinh thái này không bắt người dùng phải nhìn vào màn hình đen ngòm của Obsidian hay Terminal để quản lý tác vụ hàng ngày. Tầng 3 (Tập trung) được trực quan hóa qua Local Web App mang tên **Vitality Compass**.

### 6.1 Cơ Chế Hoạt Động Của Giao Diện
- **Công nghệ lõi**: Một file `index.html` duy nhất kết hợp với JavaScript nội bộ, chạy độc lập trên trình duyệt máy tính, giao tiếp trực tiếp với hệ điều hành cục bộ (Local Storage). KHÔNG cần backend, KHÔNG dùng server ảo, KHÔNG đưa dữ liệu lên đám mây.
- **File System Access API**: Giao diện dùng quyền hạn HTML5 Native để đọc/ghi trực tiếp lên các file `.md` trong thư mục `LDN PA`. Khi bạn tick hoàn thành một task `[x]` trên Dashboard, JavaScript sẽ ngầm định thay thế chuỗi ký tự trên ổ cứng theo thời gian thực.
- **Triết lý Thiết kế**: Tối giản tuyệt đối, thanh tĩnh (Zen), thanh nhã (elegant), sang trọng hiện đại, màu sắc mượt dịu cho hệ phó giao cảm. Tích hợp thanh Progress Bar (thành tựu trong ngày) và Radar Chart (đánh giá sự quân bình trên 5 loại tác vụ được phân loại trong Task Systems) để kích thích dopamine tích cực.
- **Tính năng**: Hiển thị và cho phép bổ sung Tiêu điểm tựu thành, hiển thị các luồng tác vụ khác theo đúng phân loại trong Task Systems, cũng có thể bổ sung tác vụ trong từng mục. Có chỗ bổ sung ý tưởng và các tác vụ phát sinh (gấp hôm nay, gấp ngày mai, không gấp) đưa vào Notebook theo cấu trúc đồng nhất đang có trong Notebook.md. Có nút làm mới dữ liệu để cập nhật dữ liệu mới thay vì phải load lại nguyên trang. Có phần theo dõi các thói quen trong ngày theo dạng nút bấm on-off thay vì check-box cho thú vị hơn. 

### 6.2 Cài Đặt (Setup)
Việc cấu trúc Dashboard Web App chỉ yêu cầu 1 thao tác tĩnh tại:
1. Đảm bảo bạn có thư mục `Vitality Compass` bên trong thư mục gốc `LDN PA`. Thư mục này phải chứa tối thiểu file `index.html`. 
2. (Tùy chọn) Có thể có thêm file `.css` hoặc `.js` đi kèm nếu hệ thống được module hóa, nhưng lý tưởng nhất là gộp chung (Single-page App) để dễ di chuyển.
3. Không cần cài Node.js, không cần `npm install`.

### 6.3 Hướng Dẫn Sử Dụng (Daily Usage)
1. **Khởi động**: Mở trình duyệt (thường là Google Chrome hoặc Edge do hỗ trợ tốt File System Access API), kéo thả file `Vitality Compass/index.html` vào trình duyệt, hoặc Bookmark cứng trang đó.
2. **Cấp quyền truy cập (Quan trọng nhất)**: 
   - Lần đầu mở trang và mỗi khi Reload, trình duyệt sẽ có một nút bấm (VD: "Chọn thư mục LDN PA" / "Select Vault"). 
   - Nhấn vào nút đó, chọn đúng gốc thư mục `LDN PA` trên ổ cứng. Trình duyệt sẽ hiện popup hỏi xác nhận quyền Xem và Chỉnh sửa (View & Edit). Chọn **Allow (Cho phép)**.
3. **Thao tác trong ngày làm việc**:
   - Màn hình sẽ hiển thị cấu trúc `Task Systems.md` và Trạm ý tưởng.
   - Khi làm xong một việc, chỉ cần **tick vào ô vuông** trên trình duyệt. Tiến trình tự cập nhật, và trong nền Obsidian file tự đổi thành `- [x] `.
   - Khi có ý tưởng đột xuất, nhập thẳng vào thanh công cụ nhập liệu (Input Bar) trên UI, ấn Enter, ý tưởng sẽ bay thẳng vào `Notebook.md` hoặc `Task Systems.md` mà không cần bạn phải rờ tay tới Obsidian.
4. **Mối quan hệ với AI Agent**: Quản gia AI (AntiGravity) chỉ lo phần dọn dẹp và phân loại file Markdown trong bóng tối (Background). Nó không chạy chung luồng với Web App. Bạn cứ mở UI cả ngày, lúc nào AI xử lý xong, UI (nếu có viết hàm refresh tĩnh) sẽ tự động hiển thị nội dung mới, hoặc bạn chỉ cần F5 và cấp quyền lại là xong. Mọi thứ tuyệt đối tách bạch và thông suốt.
