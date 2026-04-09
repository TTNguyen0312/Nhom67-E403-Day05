# 📋 Phân Công Công Việc — Hackathon

## 🏷️ Tên Đề Tài
**MedRoute AI — Hệ Thống Agent Tự Động Phân Chuyên Khoa Bệnh Nhân**
> Ứng dụng AI agent phân tuyến bệnh nhân đến đúng chuyên khoa dựa trên mô tả triệu chứng tự nhiên, hỗ trợ giảm tải cho bộ phận tiếp nhận bệnh viện.

---

## 🛠️ Tech Stack

**Frontend**
- React / Next.js — giao diện chat & hiển thị kết quả
- Tailwind CSS — styling 
- Axios — gọi API backend

**Backend**
- Python + FastAPI — API server chính
- LangGraph — orchestration agent pipeline

**Khác**
- JSON — định dạng trao đổi dữ liệu giữa các tầng
- Git / GitHub — quản lý source code & phối hợp nhóm
- Localhost / ngrok — deploy demo live

---

## ✅ To-Do List — Các Đầu Việc Phải Hoàn Thành

### 🖥️ Demo Live
- [ ] Backend API chạy ổn định, không crash
- [ ] Frontend kết nối thành công với backend
- [ ] Luồng chat nhập triệu chứng → nhận kết quả chuyên khoa hoạt động end-to-end
- [ ] Hiển thị đúng: tên chuyên khoa, mức độ ưu tiên (🔴🟡🟢), lý do gợi ý
- [ ] Disclaimer y tế hiển thị trên UI
- [ ] (Testing) 3 kịch bản demo đã test kỹ và chạy mượt (Ngọc chuẩn bị sẵn input)
- [ ] (Testing) Có xử lý edge case: input mơ hồ → agent hỏi lại

### 📊 Slide Thuyết Trình
- [ ] Slide hoàn chỉnh (10–12 slides)
- [ ] Cấu trúc: Vấn đề → Giải pháp → Demo → Kiến trúc → Roadmap → Kết luận
- [ ] Có system architecture diagram
- [ ] Có hình ảnh / screenshot UI thực tế
- [ ] Font, màu sắc đồng nhất, không lỗi chính tả

### 📄 Tài Liệu Kỹ Thuật
- [ ] Mô tả bài toán và giải pháp (1 trang)
- [ ] System architecture diagram
- [ ] Mô tả từng agent (Intake Agent, Triage Agent) và luồng xử lý
- [ ] Danh sách API endpoints (`POST /api/chat`, `POST /api/triage`)
- [ ] Tech stack và lý do lựa chọn
- [ ] README hướng dẫn cài đặt & chạy project

---

## 👥 Phân Công Theo Thành Viên
> ⏰ **Thời gian còn lại: < 12 tiếng**

| Thành viên | Vai trò | Kỹ năng |
|---|---|---|
| Tiến | UI/UX Design + Agent | Design, AI Agent, Computer Vision |
| Quang | AI Agent + Computer Vision | AI Agent, Computer Vision |
| Minh | Frontend + Backend | React/Next.js, Python/FastAPI |
| Lộc | Backend + Agent | Python/FastAPI, AI Agent |
| Ngọc | Data + Nội dung | Không coding — Research, QA, Docs, Slide |

---

### 🎨 Tiến — UI/UX Design + Agent (Mở rộng)

**🔴 Ưu tiên 1 — Chức năng chính (làm ngay)**

| # | Công việc | Ghi chú |
|---|-----------|---------|
| 1 | Hoàn thiện mockup màn hình chat nhập triệu chứng | Màn hình quan trọng nhất của demo |
| 2 | Thiết kế màn hình kết quả: chuyên khoa + mức độ khẩn cấp + lý do | Cần rõ ràng, trực quan với 🔴🟡🟢 |
| 3 | Chuẩn bị assets (màu, font, icon) gửi cho Minh implement | Xong trước giờ 2 |
| 4 | Design slide thuyết trình (10–12 slides) | Phối hợp nội dung với Ngọc |

**🟡 Ưu tiên 2 — Chức năng mở rộng (nếu còn thời gian)**

| # | Công việc | Ghi chú |
|---|-----------|---------|
| 5 | Xây dựng Vision Agent — phân tích ảnh triệu chứng (phát ban, vết thương) | Phối hợp với Quang |
| 6 | Thiết kế màn hình upload ảnh triệu chứng | Chỉ làm sau khi core xong |

---

### 🤖 Quang — AI Agent + Computer Vision

**🔴 Ưu tiên 1 — Chức năng chính (làm ngay)**

| # | Công việc | Ghi chú |
|---|-----------|---------|
| 1 | Xây dựng Intake Agent — hỏi làm rõ triệu chứng bằng lời | Multi-turn conversation flow |
| 2 | Xây dựng Triage Agent — phân tích & map chuyên khoa | Output JSON: tên khoa + lý do + mức độ ưu tiên |
| 3 | Viết & tối ưu system prompt — không chẩn đoán, chỉ gợi ý khoa | Test kỹ với nhiều ca bệnh khác nhau |
| 4 | Xử lý edge case: triệu chứng mơ hồ → agent hỏi lại | Fallback về bác sĩ tổng quát nếu không đủ thông tin |
| 5 | Chuẩn bị 3 kịch bản test sẵn cho demo live | Xem bảng kịch bản cuối file |

**🟡 Ưu tiên 2 — Chức năng mở rộng (nếu còn thời gian)**

| # | Công việc | Ghi chú |
|---|-----------|---------|
| 6 | Xây dựng Vision Agent — nhận ảnh triệu chứng, trích xuất đặc điểm | Phối hợp với Tiến về UI upload ảnh |
| 7 | Kết hợp kết quả Vision Agent vào Triage Agent | Input = lời mô tả + phân tích ảnh |

---

### 💻 Minh — Frontend + Backend

**🔴 Ưu tiên 1 — Chức năng chính (làm ngay)**

| # | Công việc | Ghi chú |
|---|-----------|---------|
| 1 | Build chat interface — nhập triệu chứng bằng lời | Core feature, làm trước tiên |
| 2 | Build màn hình hiển thị kết quả phân khoa | Chuyên khoa + mức độ ưu tiên + lý do |
| 3 | Kết nối frontend ↔ backend API (đồng bộ schema với Lộc) | Thống nhất format JSON trong 2 tiếng đầu |
| 4 | Xử lý loading state & error handling | Tránh màn hình trắng khi demo |
| 5 | Hỗ trợ Lộc dựng API nếu cần thêm người | BE + FE đều làm được |

**🟡 Ưu tiên 2 — Chức năng mở rộng (nếu còn thời gian)**

| # | Công việc | Ghi chú |
|---|-----------|---------|
| 6 | Build tính năng upload ảnh triệu chứng | Sau khi core chat xong |
| 7 | Build màn hình đặt lịch khám (chọn ngày, giờ, bác sĩ) | UI đơn giản, mock data |

---

### ⚙️ Lộc — Backend + Agent Infrastructure

**🔴 Ưu tiên 1 — Chức năng chính (làm ngay)**

| # | Công việc | Ghi chú |
|---|-----------|---------|
| 1 | Dựng API server FastAPI: `POST /api/chat`, `POST /api/triage` | Skeleton xong trong giờ đầu |
| 2 | Tích hợp LLM API (Claude / OpenAI) — kết nối agent của Quang | Phối hợp chặt với Quang về prompt & output schema |
| 3 | Thiết kế & thống nhất request/response JSON schema với Minh | Ưu tiên cao nhất — làm ngay đầu giờ |
| 4 | Xây dựng session management — lưu lịch sử hội thoại | Cần cho multi-turn conversation |
| 5 | Deploy ổn định, xử lý CORS / error / timeout | Test trước giờ thi ít nhất 1 tiếng |

**🟡 Ưu tiên 2 — Chức năng mở rộng (nếu còn thời gian)**

| # | Công việc | Ghi chú |
|---|-----------|---------|
| 6 | Thêm endpoint nhận ảnh: `POST /api/vision` | Sau khi core API ổn định |
| 7 | Thêm endpoint đặt lịch: `POST /api/appointment` | Mock data, không cần DB thật |

---

### 📊 Ngọc — Data, QA & Nội Dung *(không coding)*

**🔴 Ưu tiên 1 — Chức năng chính (làm ngay)**

| # | Công việc | Ghi chú |
|---|-----------|---------|
| 1 | Xây dựng mapping dataset: triệu chứng → chuyên khoa (dạng bảng/Excel) | 8–10 chuyên khoa phổ biến, tham khảo ICD-10 — gửi cho Quang |
| 2 | Chuẩn bị 15–20 ca bệnh mẫu đa dạng để test agent | Bao gồm ca khẩn cấp, thông thường, mơ hồ |
| 3 | Test thủ công toàn bộ luồng — nhập triệu chứng & kiểm tra kết quả | Báo cáo lỗi / kết quả sai cho Quang & Lộc |
| 4 | Soạn nội dung slide (text outline) gửi cho Tiến design | Cấu trúc: Vấn đề → Giải pháp → Demo → Kiến trúc → Roadmap |
| 5 | Soạn tài liệu kỹ thuật (không cần code — mô tả luồng, kiến trúc) | Phối hợp với Quang & Lộc để lấy thông tin kỹ thuật |

**🟡 Ưu tiên 2 — Chức năng mở rộng (nếu còn thời gian)**

| # | Công việc | Ghi chú |
|---|-----------|---------|
| 6 | Chuẩn bị thêm test cases cho tính năng gửi ảnh triệu chứng | Mô tả ca bệnh + ảnh mẫu tương ứng |
| 7 | Nghiên cứu quy trình đặt lịch khám thực tế tại bệnh viện VN | Làm cơ sở cho tính năng mở rộng |

---

## 🗺️ Lộ Trình Tính Năng

### 🔴 Phase 1 — Chức năng chính *(hoàn thành trong hackathon)*
> Tư vấn và phân chuyên khoa dựa trên mô tả triệu chứng bằng lời

```
Bệnh nhân nhập triệu chứng bằng text
        ↓
Intake Agent hỏi làm rõ (multi-turn)
        ↓
Triage Agent phân tích → gợi ý chuyên khoa + mức độ ưu tiên
        ↓
Hiển thị kết quả trực quan trên UI
```

### 🟡 Phase 2 — Mở rộng *(nếu còn thời gian / sau hackathon)*
- **Gửi ảnh triệu chứng:** Bệnh nhân chụp vết thương, phát ban → Vision Agent phân tích → kết hợp với lời mô tả để tư vấn chính xác hơn
- **Đặt lịch khám:** Sau khi có kết quả chuyên khoa → tự động gợi ý slot bác sĩ phù hợp

---

## ⏱️ Gợi Ý Timeline (< 12 Tiếng)

```
Giờ 1–2   │ Lộc + Minh: thống nhất API schema, dựng skeleton backend
           │ Quang: viết system prompt + test Intake & Triage Agent
           │ Ngọc: hoàn thiện mapping dataset, chuẩn bị ca bệnh test
           │ Tiến: hoàn thiện mockup chat + màn hình kết quả

Giờ 3–5   │ Lộc: tích hợp agent của Quang vào backend
           │ Minh: build UI chat + kết nối API
           │ Tiến: bắt đầu design slide (nhận nội dung từ Ngọc)
           │ Ngọc: soạn nội dung slide + bắt đầu test thủ công

Giờ 6–8   │ Cả nhóm: test end-to-end 3 kịch bản demo
           │ Ngọc: báo cáo lỗi → Quang/Lộc fix
           │ Tiến: finalize slide

Giờ 9–10  │ Rehearsal thuyết trình toàn nhóm
           │ Lộc: đảm bảo server ổn định
           │ [Nếu còn thời gian] Tiến + Quang: bắt đầu Vision Agent

Giờ 11–12 │ Buffer — fix lỗi nhỏ, nghỉ ngơi, chuẩn bị tâm lý 🚀
```

---

## 🔗 Điểm Phối Hợp Quan Trọng

| Cặp | Cần đồng bộ |
|-----|-------------|
| **Lộc ↔ Minh** | API schema JSON — thống nhất trong **2 tiếng đầu** |
| **Quang ↔ Lộc** | Output schema của agent để backend parse đúng |
| **Ngọc ↔ Quang** | Mapping dataset triệu chứng → chuyên khoa |
| **Ngọc ↔ Tiến** | Nội dung slide — Ngọc soạn text, Tiến design |
| **Tiến ↔ Minh** | Design assets (màu, font, icon) |
| **Tiến ↔ Quang** | Vision Agent (Phase 2) — nếu có thời gian |

---

## 🎯 3 Kịch Bản Demo Live

| # | Input bệnh nhân | Kết quả mong đợi |
|---|-----------------|-----------------|
| 🔴 | *"Đau ngực dữ dội lan lên vai trái, khó thở, đổ mồ hôi được 1 tiếng"* | Tim mạch / Cấp cứu — **KHẨN CẤP** |
| 🟡 | *"Đau đầu liên tục 3 ngày, buồn nôn, sợ ánh sáng"* | Thần kinh — **Ưu tiên** |
| 🔵 | *"Tôi thấy mệt mỏi"* (mơ hồ) | Agent hỏi làm rõ → sau đó phân khoa |

---

> 💪 **Chúc cả nhóm Tiến, Quang, Minh, Lộc, Ngọc thi thật tốt!**
> Tập trung làm sâu Phase 1 thật hoàn chỉnh — 1 luồng demo mượt mà thuyết phục hơn nhiều tính năng dở dang.
