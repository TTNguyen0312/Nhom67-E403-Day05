# Spec Draft: Vinmec AI Triage
**Nhóm 67 - Zone 3**

---

## Problem Statement

**Actor**
Bệnh nhân khi có triệu chứng muốn đặt lịch khám tại nhà qua điện thoại hoặc trực tiếp tại bệnh viện thì nhân viên điều phối tiếp nhận.

**Workflow hiện tại**

- *Tại nhà:* Bệnh nhân muốn đặt lịch trước nhưng không biết chọn khoa nào trên app/website → bỏ cuộc hoặc chọn đại → sai khoa → quay lại từ đầu.
- *Tại bệnh viện:* Bệnh nhân đến viện → xếp hàng tại quầy điều phối → nhân viên hỏi sơ bộ và phân khoa thủ công → bệnh nhân chờ đăng ký → khám → nếu sai khoa thì lặp lại quy trình.

**Bottleneck**
Cả hai kênh đều không có công cụ hỗ trợ phân khoa thông minh. Tại nhà, bệnh nhân phải tự đoán chuyên khoa từ danh sách dài mà không có hướng dẫn. Tại viện, việc phân khoa phụ thuộc hoàn toàn vào kinh nghiệm cá nhân của nhân viên quầy điều phối, và không tận dụng được bất kỳ dữ liệu sinh tồn hay lịch sử bệnh nào của bệnh nhân.

**Impact**
Bệnh nhân đặt sai khoa hoặc phân khoa sai tại quầy điều phối phải chờ thêm 30–90 phút để chuyển tuyến, ảnh hưởng đến trải nghiệm của bệnh nhân → ảnh hưởng đến doanh thu bệnh viện. Bác sĩ mất thời gian tiếp nhận ca không đúng chuyên môn. Bệnh nhân đặt lịch online bỏ cuộc giữa chừng do không biết chọn khoa, làm ảnh hưởng đến doanh thu. Nhân viên điều phối phải xử lý lượng lớn bệnh nhân (hàng trăm người mỗi ngày tại các bệnh viện lớn), dẫn đến tắc nghẽn và mất thời gian, cũng như sai sót do áp lực của nhân viên.

**Success Metric**
- Tỷ lệ bệnh nhân được phân đúng chuyên khoa ngay lần đầu — cả online lẫn tại viện — đều đạt ≥ 85%
- Thời gian từ lúc mô tả triệu chứng đến khi có lịch khám phù hợp giảm xuống dưới 5 phút
- Tỷ lệ chuyển khoa sau khi đã đăng ký giảm ≥ 50% so với hiện tại
- Tỷ lệ hoàn thành đặt lịch online tăng ≥ 30%

**Boundary**
AI được phép hỏi triệu chứng, gợi ý chuyên khoa, đề xuất bác sĩ và đặt lịch sơ bộ cả trên kênh online lẫn hỗ trợ tại quầy lễ tân. AI không được phép đưa ra chẩn đoán bệnh, kê đơn thuốc, hay quyết định điều trị. Mọi ca có dấu hiệu khẩn cấp phải được flag ngay và chuyển sang quy trình cấp cứu do con người xử lý.

---

## 1. AI Product Canvas

### Value / Trust / Feasibility

| | Câu hỏi | Trả lời |
|---|---|---|
| **Value** | User nào? Pain gì? AI giải gì? | **User:** Bệnh nhân khi có triệu chứng muốn đặt lịch khám tại nhà hoặc trực tiếp tại bệnh viện. **Pain:** Cả hai kênh đều không có công cụ hỗ trợ phân khoa thông minh — bệnh nhân tự đoán khoa, nhân viên phân khoa thủ công, không tận dụng được dữ liệu y khoa hay lịch sử bệnh. **AI giải:** Hỏi triệu chứng, thu thập dữ liệu cơ bản → gợi ý chuyên khoa, lịch khám, bác sĩ phù hợp → hỗ trợ đặt lịch luôn → giảm thời gian từ "có triệu chứng" đến "có lịch khám" từ 30–90 phút xuống dưới 5 phút. |
| **Trust** | Khi AI sai thì sao? User sửa bằng cách nào? | Khi AI gợi ý sai → bệnh nhân phản hồi bằng ngôn ngữ tự nhiên hoặc trả lời câu hỏi làm rõ của AI → AI tự điều chỉnh trong cùng cuộc hội thoại, không cần bệnh nhân biết tên chuyên khoa. Chuyển sang nhân viên khi bệnh nhân chủ động yêu cầu hoặc AI hỏi quá 3 vòng mà vẫn chưa đủ tự tin, hoặc bị feedback sai quá 2 lần. |
| **Feasibility** | Cost/latency bao nhiêu? Risk chính? | **Cost:** ~$0.02/lượt triage (800–1200 tokens, GPT-4o). 500 lượt/ngày → ~$300–600/tháng; 2000 lượt/ngày → ~$1,200/tháng (~33 triệu VND) — thấp hơn lương 3–4 nhân viên điều phối. **Latency:** 5–8s câu ngắn, 10–15s phân tích phức tạp — cần streaming để tránh màn hình trắng. |

### Automation hay Augmentation?

☑ **Augmentation**

**Justify:** Bệnh nhân luôn là người xác nhận cuối trước khi lịch được đặt. AI gợi ý nhưng không tự động đặt mà không có sự đồng ý. Cost of reject = 0 vì bệnh nhân chỉ cần phản hồi bằng ngôn ngữ tự nhiên để AI điều chỉnh lại.

---

### Learning Signal

**1. User correction đi vào đâu?**

Toàn bộ correction signal nằm trong vòng hội thoại giữa AI và bệnh nhân, không phụ thuộc vào bác sĩ:

- Bệnh nhân nói "không đúng", "không phải", hoặc phản hồi tiêu cực → log cặp (gợi ý AI đưa ra → phản hồi của bệnh nhân)
- Bệnh nhân mô tả thêm triệu chứng khiến AI phải điều chỉnh khoa → log toàn bộ chuỗi hội thoại kèm khoa cuối cùng bệnh nhân bấm xác nhận
- Bệnh nhân bỏ cuộc giữa chừng → log điểm thoát ra, đây là tín hiệu AI đang hỏi quá phức tạp hoặc gợi ý không thuyết phục
- Sau khi đặt lịch xong, hỏi bệnh nhân 1 câu duy nhất: *"Bạn có cảm thấy được gợi ý đúng khoa không?"* → Yes/No

Log hội thoại được label tự động theo hành vi bệnh nhân, dùng để cải thiện prompt hàng tuần và fine-tune model hàng tháng, giúp AI gợi ý chính xác hơn theo thời gian.

**2. Product thu signal gì để biết tốt lên hay tệ đi?**

- **Acceptance rate:** Tỷ lệ bệnh nhân đồng ý với gợi ý khoa ngay vòng hội thoại đầu tiên
- **Re-routing rate:** Tỷ lệ bị chuyển khoa sau khi đã đặt lịch — chỉ số quan trọng nhất phản ánh độ chính xác thực tế
- **Conversation length:** Số vòng hỏi-đáp trung bình mỗi lượt triage — dài bất thường là dấu hiệu AI đang lúng túng
- **Completion rate:** Tỷ lệ hoàn thành đặt lịch không bỏ giữa chừng
- **Escalation rate:** Tỷ lệ phải chuyển sang nhân viên — tăng là tín hiệu xấu

**3. Data thuộc loại nào?**

- ☑ **Human-judgment** — bác sĩ xác nhận đúng/sai khoa sau mỗi ca là nhãn dữ liệu không thể tự động hóa, có giá trị cao nhất
- ☑ **Domain-specific** — mapping triệu chứng → chuyên khoa theo cấu trúc từng bệnh viện tại Việt Nam
- ☑ **User-specific** — lịch sử triệu chứng, các chỉ số, xét nghiệm của từng bệnh nhân tích lũy theo thời gian
- ☑ **Real-time** — dữ liệu từng khoa, lịch khám trống thay đổi liên tục trong ngày

**Có marginal value không?**

Có — rất cao. GPT-4o đã biết triệu chứng y khoa phổ thông nhưng hoàn toàn không biết cấu trúc chuyên khoa cụ thể của từng bệnh viện, không có dữ liệu liên kết giữa triệu chứng và quy trình khám thực tế. Chính phần dữ liệu này — tích lũy từng ngày qua mỗi ca khám — là moat cạnh tranh dài hạn mà model nền không thể thay thế.

---

## 2. User Stories

### User Story 1: Bệnh nhân ở nhà

> *"Là bệnh nhân ở nhà, tôi muốn mô tả triệu chứng và được gợi ý chuyên khoa phù hợp để có thể đặt lịch khám mà không cần biết trước mình cần khám khoa nào."*

**Path 1 — Happy**
Bệnh nhân mở app → mô tả triệu chứng rõ ràng → AI hỏi 1–2 câu làm rõ → gợi ý chuyên khoa kèm lý giải ngắn gọn, hỏi bệnh nhân có muốn đặt lịch không → bệnh nhân đồng ý → AI đưa ra danh sách bác sĩ và lịch khám → user chọn bác sĩ và slot → đặt lịch thành công → nhận xác nhận và nhắc lịch.

**Path 2 — Low confidence**
Bệnh nhân mô tả triệu chứng mơ hồ ("người mệt, không rõ chỗ nào") → AI không đủ tự tin → chủ động hỏi thêm từng câu một (thời gian xuất hiện, mức độ, kèm theo triệu chứng nào khác) → sau 2–3 vòng thu hẹp được → gợi ý khoa kèm giải thích → bệnh nhân xác nhận → đặt lịch.

**Path 3 — Failure**
Bệnh nhân mô tả triệu chứng quá phức tạp hoặc đa bệnh lý → AI hỏi quá 3 vòng vẫn không đủ tự tin → không ép đưa ra gợi ý → hiển thị:

> *"Mình chưa chắc chắn về trường hợp của bạn. Để đảm bảo bạn được tư vấn chính xác nhất, mình sẽ kết nối bạn với nhân viên hỗ trợ ngay bây giờ."*

→ Toàn bộ nội dung hội thoại được chuyển kèm sang nhân viên → nhân viên tiếp tục từ đúng điểm bệnh nhân đang dừng, không hỏi lại từ đầu → nhân viên phân khoa và hỗ trợ đặt lịch trực tiếp.

**Path 4 — Correction**
AI gợi ý Tim mạch → bệnh nhân phản hồi "không liên quan đến tim" → AI hỏi thêm → bệnh nhân bổ sung triệu chứng → AI điều chỉnh sang Tiêu hóa → bệnh nhân xác nhận → đặt lịch. Toàn bộ hội thoại được log để cải thiện model.

---

### User Story 2: Bệnh nhân tại bệnh viện

> *"Là bệnh nhân đi khám tại bệnh viện, tôi muốn được tư vấn nhanh chuyên khoa phù hợp để đến khám dựa theo triệu chứng của tôi mà không phải thông qua quầy điều phối."*

**Path 1 — Happy**
Bệnh nhân quét QR tại sảnh hoặc mở app → mô tả triệu chứng → AI gợi ý chuyên khoa → bệnh nhân đồng ý → chọn: đặt lịch online ngay hoặc nhận hướng dẫn đến quầy mua vé → nếu chọn online: đặt slot trong ngày, nhận mã số thứ tự → nếu chọn quầy: nhận chỉ dẫn phòng và số quầy cụ thể, không cần hỏi thêm ai.

**Path 2 — Low confidence**
Bệnh nhân cao tuổi mô tả triệu chứng không rõ ràng → AI hỏi từng câu ngắn, ngôn ngữ đơn giản → nếu vẫn không đủ tự tin sau 2 vòng → gợi ý Nội tổng quát là điểm khởi đầu an toàn → giải thích ngắn lý do → bệnh nhân chọn hướng đến quầy → nhận chỉ dẫn cụ thể.

**Path 3 — Failure**
Bệnh nhân mô tả triệu chứng có dấu hiệu red flag (đau ngực dữ dội, khó thở đột ngột) → AI không gợi ý khoa, không hỏi thêm → hiển thị ngay:

> *"Vui lòng đến quầy Cấp cứu ngay lập tức hoặc nhờ nhân viên hỗ trợ."*

→ Kèm chỉ dẫn đường đến phòng cấp cứu trong bệnh viện.

**Path 4 — Correction**
AI gợi ý Cơ xương khớp → bệnh nhân nói "tôi đã khám khoa đó rồi, không đúng" → AI hỏi thêm về lần khám trước và triệu chứng hiện tại → điều chỉnh sang Thần kinh → bệnh nhân xác nhận → chọn đặt lịch online trong ngày → nhận mã thứ tự ưu tiên vì đã có lịch sử khám tại viện.

---

## 3. Eval Metrics & Threshold

Trong bài toán này, hệ thống làm nhiệm vụ đọc triệu chứng + sinh tồn + xét nghiệm, gợi ý đúng chuyên khoa phù hợp, và đặc biệt không bỏ sót ca nguy hiểm. Ở bước phân luồng đầu tiên, rủi ro lớn nhất là bỏ sót khoa cần thiết hoặc bỏ sót ca nặng/cấp cứu. **Hệ thống ưu tiên recall cao.**


| Metric | Threshold | Red flag (Dừng khi) |
|---|---|---|
| Trong tất cả các ca có kết quả khám thực tế, bao nhiêu ca mà khoa đúng nằm trong các khoa AI đề xuất | ≥ 95% | < 90% trong 1 tuần |
| Bao nhiêu ca mà khoa AI gợi ý đầu tiên trùng với khoa bệnh nhân thực sự khám/phù hợp nhất | ≥ 85% | < 70% trong 1 tuần |
| % ca thực sự nguy cấp được nhận diện đúng | ≥ 98% | < 95% trong bất kỳ tuần nào |


---

## 4. Top 3 Failure Modes

| # | Trigger | Hậu quả | Mitigation |
|---|---|---|---|
| 1 | Người dùng nhập triệu chứng mơ hồ/sai lệch (ví dụ: "đau bụng nhẹ", "hơi khó thở") hoặc thiếu thông tin quan trọng | AI suy luận sai bệnh, gợi ý sai chuyên khoa (ví dụ đáng lẽ tim mạch → lại đi tiêu hóa) | Bắt buộc flow hỏi lại (clarifying questions), yêu cầu input có cấu trúc (thời lượng, cường độ, vị trí), nhấn mạnh sự không chắc chắn cho user |
| 2 | Model overconfidence | User tin tuyệt đối → delay khám đúng chuyên khoa → rủi ro sức khỏe nghiêm trọng | Luôn hiển thị kèm theo giải thích, kiểm tra dựa trên quy tắc dự phòng cho các triệu chứng nguy hiểm (red flags), nếu có dấu hiệu quan trọng bị bỏ qua thì AI → khuyến nghị cấp cứu |
| 3 | Feedback loop sai lệch (model học từ dữ liệu thực tế nhưng data bị bias hoặc label sai) | Hệ thống ngày càng "tự tin sai" (ví dụ: hay đề xuất sai 1 chuyên khoa nhưng vẫn cứ reinforce chính nó) | Thiết kế human-in-the-loop (bác sĩ xác thực), weight feedback theo độ tin cậy (doctor > user), audit model định kỳ |

---

## 5. ROI — 3 Kịch Bản

| | Conservative | Realistic | Optimistic |
|---|---|---|---|
| **Assumption** | Ít người dùng, nhiều người vẫn hỏi trực tiếp nhân viên | Một phần bệnh nhân dùng agent, phần còn lại vẫn hỏi người | Phần lớn bệnh nhân dùng agent ngay từ đầu |
| **Cost** | Tốn chi phí duy trì hệ thống nhưng ít người dùng nên chưa tận dụng hết | Chi phí tăng theo lượng dùng, nhưng bắt đầu "đáng tiền" | Chi phí trên mỗi người dùng giảm nhờ dùng nhiều, hệ thống ổn định |
| **Benefit** | Nhân viên đỡ việc một chút, bệnh nhân đỡ phải hỏi nhiều | Nhân viên đỡ việc rõ rệt, bệnh nhân được hướng dẫn nhanh hơn | Gần như không cần xếp hàng hỏi, vào khám nhanh và đúng khoa hơn |
| **Net** | Lợi ích chưa rõ ràng, chủ yếu để thử nghiệm | Bắt đầu thấy lợi ích rõ ràng so với chi phí | Lợi ích lớn, dùng càng nhiều càng hiệu quả |

---

## 6. Mini AI Spec

Hệ thống giải quyết một vấn đề đơn giản nhưng tốn kém: bệnh nhân không biết mình cần khám khoa nào, dẫn đến phân khoa sai, chờ đợi lâu, và bỏ cuộc giữa chừng khi đặt lịch online. Đối tượng chính là bệnh nhân phổ thông — cả người đang ở nhà muốn đặt lịch trước lẫn người đã có mặt tại bệnh viện muốn được hướng dẫn nhanh mà không cần xếp hàng chờ nhân viên điều phối.

AI đóng vai trò augmentation, không automation. Bệnh nhân luôn là người xác nhận cuối — AI dẫn dắt hội thoại, hỏi từng câu ngắn bằng ngôn ngữ thường ngày, và chỉ đưa ra gợi ý khi đủ tự tin. Khi bệnh nhân phản hồi không đồng ý, AI hỏi thêm và tự điều chỉnh trong cùng cuộc hội thoại mà không cần bệnh nhân biết tên chuyên khoa. Khi vượt quá 3 vòng mà vẫn không đủ tự tin, hệ thống chuyển toàn bộ ngữ cảnh sang nhân viên để tiếp tục — bệnh nhân không phải kể lại từ đầu. Model sử dụng GPT-4o với chi phí ước tính $0.02–0.04 mỗi lượt triage, latency dưới 3 giây, chấp nhận được cho luồng hội thoại thời gian thực.

Về chất lượng, precision được ưu tiên hơn recall — thà nói "chưa chắc, cần hỗ trợ thêm" còn hơn gợi ý sai với độ tự tin cao. Ngưỡng thành công là 85% bệnh nhân được phân đúng khoa ngay lần đầu và tỷ lệ chuyển khoa sau đăng ký giảm ít nhất 50%. Rủi ro lớn nhất không phải gợi ý sai khoa thông thường mà là bỏ sót ca khẩn cấp — được xử lý bằng một safety layer rule cứng chạy độc lập trước khi GPT-4o xử lý bất kỳ input nào, không phụ thuộc vào model. Rủi ro pháp lý được kiểm soát bằng disclaimer rõ ràng: mọi output chỉ là gợi ý điều phối, không phải chẩn đoán.

Data flywheel được xây hoàn toàn từ hành vi bệnh nhân trong vòng hội thoại — không cần nhãn từ bác sĩ. Mỗi lần bệnh nhân từ chối gợi ý, mỗi lần hội thoại phải điều chỉnh, mỗi câu Yes/No sau khi đặt lịch xong đều được log và label tự động. Dữ liệu này nuôi hai luồng song song: cải thiện prompt hàng tuần cho các nhóm triệu chứng AI đang yếu, và fine-tune model hàng tháng khi đủ volume. Càng nhiều bệnh nhân dùng, model càng hiểu đặc thù triệu chứng và cấu trúc chuyên khoa của từng bệnh viện — đây là phần GPT-4o nền không có và không thể thay thế.

## 7. Kiến trúc Hệ thống (Multi-Agent Design)
Với yêu cầu "Augmentation" và giới hạn "3 vòng hội thoại", bạn nên sử dụng LangGraph để kiểm soát luồng (State Management) chặt chẽ hơn là để Agent tự chạy tự do.

Sơ đồ đề xuất:
Node 1: Safety Guardrail (Rule-based): Kiểm tra "Red Flags" (đau ngực, khó thở cấp...). Nếu dính, chuyển thẳng sang Emergency Path.

Node 2: Triage Agent (LLM): Đóng vai trò thực hiện hội thoại, đặt câu hỏi làm rõ.

Node 3: Knowledge Retriever (RAG): Truy xuất thông tin chuyên khoa/bác sĩ từ dữ liệu nội bộ Vinmec.

Node 4: Router/Orchestrator: Đếm số vòng hội thoại. Nếu turn_count > 3 hoặc confidence < threshold, chuyển sang Human Handoff.

## 8. Cách xây dựng Bộ dữ liệu Kiểm thử (Internal Benchmark)
Vì Spec của bạn nhấn mạnh vào Recall 98% cho ca cấp cứu và 85% chính xác phân khoa, bạn cần tạo 3 tập dữ liệu kiểm thử sau:

a. Tập "Red Flag" (Safety Test)
Nguồn: Danh mục các triệu chứng cấp cứu của Vinmec.

Cách làm: Tạo 100 câu input biến thể (ví dụ: "tôi thấy nặng ngực như có đá đè" thay vì nói "đau ngực").

Mục tiêu: 100% các câu này phải kích hoạt Safety Guardrail.

b. Tập "Triage Golden Set" (Accuracy Test)
Cấu trúc: { Triệu chứng } -> { Chuyên khoa đúng }.

Nguồn: Lấy dữ liệu lịch sử khám (đã anonymized). Lọc những ca mà "Lý do khám" và "Khoa kết luận" khớp nhau.

Cách chạy: Chạy batch qua Agent và đo tỷ lệ khớp (Top-1 và Top-3 chuyên khoa).

c. Tập "Correction Logic" (Trust Test)
Kịch bản: User cố tình đưa thông tin sai hoặc phản đối gợi ý (ví dụ Path 4 trong User Story).

Mục tiêu: Kiểm tra xem Agent có bị "cố chấp" không, hay có khả năng tiếp nhận feedback để đổi khoa.
