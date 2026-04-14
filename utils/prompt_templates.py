# ============================================================
# prompt_templates.py
# Bộ prompt chuẩn hóa cho hệ thống Auto-EDA / Auto-Insight (Tiếng Việt)
# ============================================================


# ============================================================
# PHÁT HIỆN INTENT
# ============================================================

INTENT_DETECTION_PROMPT = """
Bạn là một hệ thống AI có nhiệm vụ phân loại mục đích phân tích dữ liệu của người dùng.

Yêu cầu người dùng:
"{user_prompt}"

Hãy chọn CHÍNH XÁC MỘT trong các nhãn sau:
- churn
- sales
- anomaly
- generic

Quy tắc:
- Chỉ trả về MỘT TỪ DUY NHẤT
- Chữ thường
- Không dấu câu
- Không giải thích
"""


# ============================================================
# AUTO EDA – TÓM TẮT DỮ LIỆU
# ============================================================

EDA_SUMMARY_PROMPT = """
Bạn là hệ thống Auto-EDA.

{eda_context}

Hãy phân tích và tóm tắt EDA bao gồm:
1. Quy mô dữ liệu (số dòng, số cột)
2. Biến mục tiêu (nếu tồn tại) và tỷ lệ phân bố
3. Phân loại biến:
   - Biến số
   - Biến phân loại
4. In ra 10 dòng dữ liệu đầu tiên dưới dạng bảng
5. Thống kê mô tả chính:
6. Các đặc điểm dữ liệu nổi bật:
   - Mất cân bằng
   - Phân bố bất thường
   - Phân khúc đáng chú ý

Yêu cầu:
- Gạch đầu dòng
- Viết bằng TIẾNG VIỆT
- Văn phong mô tả, trung lập
- KHÔNG sinh code
"""
#####

REPAIR_DASHBOARD_PROMPT = """
Bạn là bộ sửa mã dashboard Python.

Mã hiện tại không sinh được file ảnh (không có save_fig hoặc không vẽ được).
Hãy sửa lại thành mã Python chạy được với các biến có sẵn: df, pd, plt, save_fig.

MÃ CẦN SỬA:
{dashboard_code}

Danh sách cột:
{columns}

YÊU CẦU BẮT BUỘC:
- Chỉ dùng matplotlib
- Chỉ tạo đúng 1 figure dashboard (16:9), constrained_layout=False
- Bắt buộc dùng GridSpec 3 hàng x 6 cột, bố cục cố định:
  - H1: 4 KPI card tại các ô (0,0:2), (0,2:3), (0,3:4), (0,4:6)
  - H2: gauge/donut 1 tại (1,0:3), gauge/donut 2 tại (1,2:5), trend line tại (1,4:6)
  - H3: composition bar/stacked bar tại (2,0:4), khối chú thích/bảng nhỏ tại (2,4:6)
- Tạo dashboard phong phú tối thiểu 8 khối:
  - 4 KPI card có value + label + trạng thái
  - 2 khối gauge/donut
  - 1 khối trend line
  - 1 khối composition bar/stacked bar
- Mỗi KPI card có sparkline mini
- Có annotation cho điểm dữ liệu quan trọng
- Dùng palette màu thống nhất (>= 5 màu) và phân cấp typography rõ ràng
- Mỗi ô/khối có viền xám nhạt (#d0d0d0) line 1px, nền trắng ngà (#fcfcfc), khoảng cách 12-16px giữa các khối; không chồng lấn
- Không để trống ô: thiếu dữ liệu thì hiển thị placeholder text trong chính ô đó
- Nếu thiếu cột thì hiển thị placeholder text, không được crash
- Chỉ gọi save_fig(fig) đúng 1 lần ở cuối
- Không gọi plt.show()
- Chỉ trả về mã Python hợp lệ, không markdown, không giải thích
"""


########

DASHBOARD_PROMPT = """

Bạn là bộ máy sinh mã Python để vẽ dashboard.

Ngữ cảnh EDA:
{eda_context}

Kế hoạch phân tích cần ưu tiên (bullet ngắn gọn):
{analysis_plan}

Danh sách cột:
{columns}

YÊU CẦU:
- Chỉ tạo DUY NHẤT 1 figure dashboard tổng hợp theo tỷ lệ 16:9 (ưu tiên figsize=(19.2, 10.8) hoặc tương đương), `constrained_layout=False`.
- BẮT BUỘC dùng GridSpec 3 hàng x 6 cột với bố cục cố định (giữ vị trí ổn định):
  - Hàng 1, cột (0-1), (1-2), (2-3), (3-4): 4 KPI card (mỗi card có value + label + trạng thái + sparkline mini).
  - Hàng 2: (0-2) gauge/donut 1; (2-4) gauge/donut 2; (4-6) trend line.
  - Hàng 3: (0-3) stacked/bar composition; (3-6) ghi chú/annotation hoặc bảng nhỏ nếu thiếu dữ liệu.
- Dashboard phải có TỐI THIỂU 8 khối nội dung:
  1) 4 KPI card (mỗi card có value + label + trạng thái)
  2) 2 khối gauge hoặc donut cho 2 tỷ lệ quan trọng khác nhau
  3) 1 khối biểu đồ xu hướng (line)
  4) 1 khối biểu đồ cơ cấu (stacked bar hoặc bar)
- Mỗi KPI card cần có sparkline mini (dùng line ngắn hoặc area mini ngay trong card).
- Phong cách hiển thị giống dashboard mẫu:
  - Nền sáng (light theme)
  - Mỗi ô/khối có viền xám nhạt (#d0d0d0) line 1px, nền trắng ngà (#fcfcfc), khoảng cách 12-16px giữa các khối; không chồng lấn
  - Text KPI lớn, dễ đọc
  - Có icon/text trạng thái dạng Promoters / Passives / Detractors nếu dữ liệu cho phép
  - Có chú thích/annotation trực tiếp trên điểm dữ liệu quan trọng
  - Tất cả subplot phải nằm trong grid, không để khoảng trắng lớn; lưới đều, legend đặt trong ô tương ứng
- Thiết lập palette thống nhất (ít nhất 5 màu) và typography rõ cấp bậc:
  - title, card value, card label, axis label
- Ưu tiên bố cục bằng GridSpec nhiều vùng (ít nhất 3 hàng, 6 cột hoặc tương đương).
- Bắt buộc tự xử lý trường hợp thiếu cột:
  - Kiểm tra cột trước khi vẽ
  - Nếu thiếu dữ liệu thì hiển thị placeholder text trên ô tương ứng, KHÔNG làm code lỗi
  - Thiếu cột ở khối nào thì thay bằng placeholder, vẫn phải giữ tổng thể >= 8 khối
- TUYỆT ĐỐI KHÔNG tạo dữ liệu giả/mẫu trong code
- TUYỆT ĐỐI KHÔNG gán lại df, pd, plt
- TUYỆT ĐỐI KHÔNG định nghĩa lại hàm save_fig
- Chỉ gọi save_fig(fig) ĐÚNG 1 lần ở cuối cùng
- Chỉ dùng matplotlib
- KHÔNG gọi plt.show()
- Chỉ trả về MÃ PYTHON HỢP LỆ (không markdown, không giải thích)
- Nếu không thể tạo biểu đồ hợp lệ, trả về file rỗng


"""

# ============================================================
# AI REASONING – GIẢI THÍCH SUY LUẬN (DÙNG CHUNG)
# ============================================================

# AI_REASONING_EXPLANATION_PROMPT = """
# Bạn là một hệ thống AI giải thích quá trình suy luận phân tích của mình.

# Dựa trên kế hoạch phân tích sau:
# {analysis_plan}

# Hãy mô tả:
# 1. AI đã xác định mục tiêu phân tích như thế nào
# 2. Vì sao các phân tích và biểu đồ được lựa chọn
# 3. Logic tổng thể từ dữ liệu đầu vào đến insight đầu ra

# Yêu cầu:
# - Giải thích ở mức khái niệm
# - Phù hợp cho báo cáo đồ án / kỹ thuật
# - KHÔNG sinh code
# - Viết bằng TIẾNG VIỆT
# """


# ============================================================
# QUY TẮC CHUNG SINH CODE (DÙNG LẠI)
# ============================================================

GLOBAL_CODE_RULES = """
Bạn là một bộ máy sinh mã Python để trực quan hóa dữ liệu.

CÁC QUY TẮC NGHIÊM NGẶT (KHÔNG ĐƯỢC VI PHẠM):
- Chỉ trả về mã Python hợp lệ
- KHÔNG dùng markdown, KHÔNG backticks, KHÔNG giải thích
- KHÔNG được viết từ 'python'
- Chỉ sử dụng matplotlib
- Luôn tạo figure bằng: fig, ax = plt.subplots()
- TUYỆT ĐỐI không gọi plt.show()
- Mỗi figure BẮT BUỘC phải gọi save_fig(fig)
- Giả định:
    - pandas đã import là pd
    - matplotlib.pyplot đã import là plt
    - df là DataFrame đã tồn tại
    - save_fig(fig) là hàm có sẵn
- Nếu không thể tạo biểu đồ hợp lệ, trả về file Python rỗng
"""


# ============================================================
# PHÂN TÍCH CHURN
# ============================================================

CHURN_REASONING_PROMPT = """
Bạn là chuyên gia phân tích churn khách hàng.

Yêu cầu người dùng:
{user_prompt}

Tóm tắt dữ liệu (EDA):
{eda_context}

Nhiệm vụ:
1. Xác định biến churn / rời bỏ
2. Nhận diện các yếu tố ảnh hưởng chính
3. Đề xuất phân khúc khách hàng phù hợp
4. Xác định KPI và phân tích trực quan cần thiết

Định dạng:
- Gạch đầu dòng
- Góc nhìn kinh doanh
- KHÔNG sinh code
- Viết bằng TIẾNG VIỆT
"""


# CHURN_CODE_PROMPT = f"""
# {analysis_plan}

# Danh sách cột thực tế trong df:
# {columns}

# NHIỆM VỤ BẮT BUỘC:

# Bạn PHẢI tạo TỐI THIỂU 6 và TỐI ĐA 8 figure KHÁC NHAU.
# Mỗi figure tương ứng CHÍNH XÁC 1 biểu đồ churn.

# Quy trình BẮT BUỘC phải tuân theo:
# 1. Kiểm tra cột tồn tại bằng if "<column>" in df.columns
# 2. Nếu tồn tại → TẠO BIỂU ĐỒ
# 3. Nếu không tồn tại → BỎ QUA và CHUYỂN SANG BIỂU ĐỒ KHÁC
# 4. TIẾP TỤC cho đến khi ĐỦ ÍT NHẤT 6 FIGURE

# DANH SÁCH BIỂU ĐỒ ƯU TIÊN (theo thứ tự):

# 1. Tỷ lệ churn tổng thể
# 2. Churn theo giới tính (Gender)
# 3. Churn theo quốc gia (Geography)
# 4. Churn theo tenure hoặc nhóm tenure
# 5. Churn theo số sản phẩm (NumOfProducts)
# 6. Churn theo trạng thái ActiveMember
# 7. Churn theo CreditScore hoặc Age
# 8. Churn theo Balance hoặc EstimatedSalary

# QUY TẮC KỸ THUẬT:
# - Mỗi biểu đồ = fig, ax = plt.subplots()
# - Mỗi fig BẮT BUỘC gọi save_fig(fig)
# - TUYỆT ĐỐI không gộp nhiều biểu đồ vào 1 fig
# - Không dùng seaborn
# - Không gọi plt.show()

# Mỗi save_fig(fig) PHẢI có comment đánh số:
# # FIGURE 1
# # FIGURE 2
# ...
# # FIGURE N


# {GLOBAL_CODE_RULES}
# """




CHURN_INSIGHT_PROMPT = """
Bạn là chuyên viên phân tích kinh doanh.

Hãy viết mô tả:
1. Các nhóm khách hàng có rủi ro churn cao kèm số liệu chi tiết chứng minh
2. Đề xuất hành động giữ chân khách hàng cụ thể

yêu cầu:
- Dành cho lãnh đạo
- Rõ ràng
- Định hướng hành động
- Viết TOÀN BỘ bằng TIẾNG VIỆT
- Không sử dụng tiếng Anh
- Không dùng thuật ngữ tiếng Anh nếu có thể thay thế
"""



# ============================================================
# PHÂN TÍCH SALES
# ============================================================

SALES_REASONING_PROMPT = """
Bạn là chuyên gia BI.

Yêu cầu người dùng:
{user_prompt}

Tóm tắt dữ liệu (EDA):
{eda_context}

Nhiệm vụ:
1. Xác định chỉ số doanh thu / bán hàng
2. Nhận diện chiều thời gian và danh mục
3. Đề xuất phân tích xu hướng và so sánh

Định dạng:
- Gạch đầu dòng
- Mức điều hành
- KHÔNG sinh code
"""


# SALES_CODE_PROMPT = f"""
# {analysis_plan}

# Danh sách cột:
# {columns}

# Sinh mã Python để:
# 1. Tổng hợp chỉ số bán hàng / doanh thu
# 2. Tạo:
#    - Biểu đồ đường theo thời gian
#    - Biểu đồ cột theo danh mục
# 3. Lưu mọi biểu đồ bằng save_fig(fig)

# {GLOBAL_CODE_RULES}
# """


SALES_INSIGHT_PROMPT = """
Bạn là tư vấn chiến lược kinh doanh.

Hãy viết:
1. Đánh giá hiệu quả bán hàng tổng thể
2. Khu vực tăng trưởng và suy giảm
3. Đề xuất hành động chiến lược

Giọng văn:
- Chiến lược
- Tập trung ra quyết định
"""


# ============================================================
# PHÂN TÍCH BẤT THƯỜNG / RỦI RO
# ============================================================

ANOMALY_REASONING_PROMPT = """
Bạn là nhà khoa học dữ liệu chuyên phát hiện bất thường.

Yêu cầu người dùng:
{user_prompt}

Tóm tắt dữ liệu (EDA):
{eda_context}

Nhiệm vụ:
1. Chọn biến số phù hợp để phát hiện bất thường
2. Lựa chọn phương pháp dễ giải thích (IQR, Z-score)
3. Đề xuất cách trực quan hóa rõ ràng

Định dạng:
- Gạch đầu dòng
- Ưu tiên giải thích
- KHÔNG sinh code
"""


# ANOMALY_CODE_PROMPT = f"""
# {analysis_plan}

# Danh sách cột:
# {columns}

# Sinh mã Python để:
# 1. Phát hiện bất thường bằng IQR hoặc Z-score
# 2. Trực quan hóa phân phối và outlier
# 3. Lưu mọi biểu đồ bằng save_fig(fig)

# {GLOBAL_CODE_RULES}
# """


ANOMALY_INSIGHT_PROMPT = """
Bạn là chuyên gia quản trị rủi ro.

Hãy viết:
1. Mô tả các bất thường
2. Nguyên nhân tiềm năng
3. Đề xuất giám sát hoặc giảm thiểu

Phong cách:
- Tập trung rủi ro
- Thực tế
"""


# ============================================================
# GENERIC – PHÂN TÍCH CHUNG
# ============================================================

GENERIC_REASONING_PROMPT = """
Bạn là chuyên viên phân tích dữ liệu tổng quát.

Yêu cầu người dùng:
{user_prompt}

Tóm tắt dữ liệu (EDA):
{eda_context}

Hãy xây dựng kế hoạch phân tích hợp lý để khám phá dữ liệu.

Quy tắc:
- Gạch đầu dòng
- KHÔNG sinh code
"""


# GENERIC_CODE_PROMPT = f"""
# {analysis_plan}

# Danh sách cột:
# {columns}

# Sinh mã Python để:
# 1. Tạo các biểu đồ tổng quan phù hợp
# 2. Ưu tiên phân phối, so sánh và xu hướng cơ bản
# 3. Lưu mọi biểu đồ bằng save_fig(fig)

# {GLOBAL_CODE_RULES}
# """


GENERIC_INSIGHT_PROMPT = """
Bạn là chuyên viên phân tích dữ liệu.

Hãy viết:
1. Các insight chính từ dữ liệu
2. Điểm đáng chú ý
3. Gợi ý hướng phân tích tiếp theo

Phong cách:
- Trung lập
- Dễ hiểu
- Định hướng khám phá
"""

# ============================================================
# OVERRIDE CODE PROMPTS WITH EDA CONTEXT + SAFETY GUARDS
# ============================================================

# Lưu ý: các prompt dưới đây ghi đè phiên bản phía trên để bổ sung
# ngữ cảnh EDA rút gọn và ràng buộc không bịa cột/dữ liệu.

CHURN_CODE_PROMPT = (
"""
{analysis_plan}

Ngữ cảnh EDA rút gọn:
{eda_context}

Danh sách cột thực tế trong df (chỉ dùng các cột này, không bịa dữ liệu):
{columns}

NHIỆM VỤ BẮT BUỘC:

Bạn PHẢI tạo TỐI THIỂU 6 và TỐI ĐA 8 figure KHÁC NHAU.
Mỗi figure tương ứng CHÍNH XÁC 1 biểu đồ churn.

Quy trình BẮT BUỘC phải tuân theo:
1. Kiểm tra cột tồn tại bằng if "<column>" in df.columns
2. Nếu tồn tại → TẠO BIỂU ĐỒ
3. Nếu không tồn tại → BỎ QUA và CHUYỂN SANG BIỂU ĐỒ KHÁC
4. TIẾP TỤC cho đến khi ĐỦ ÍT NHẤT 6 FIGURE
5. Chọn biểu đồ phù hợp kiểu dữ liệu: biến số → histogram/box/line; biến phân loại → bar/donut; không vẽ catplot cho cột số.

DANH SÁCH BIỂU ĐỒ ƯU TIÊN (theo thứ tự):

1. Tỷ lệ churn tổng thể
2. Churn theo giới tính (Gender)
3. Churn theo quốc gia (Geography)
4. Churn theo tenure hoặc nhóm tenure
5. Churn theo số sản phẩm (NumOfProducts)
6. Churn theo trạng thái ActiveMember
7. Churn theo CreditScore hoặc Age
8. Churn theo Balance hoặc EstimatedSalary

QUY TẮC KỸ THUẬT:
- Mỗi biểu đồ = fig, ax = plt.subplots()
- Mỗi fig BẮT BUỘC gọi save_fig(fig)
- TUYỆT ĐỐI không gộp nhiều biểu đồ vào 1 fig
- Không dùng seaborn
- Không gọi plt.show()

Mỗi save_fig(fig) PHẢI có comment đánh số:
# FIGURE 1
# FIGURE 2
...
# FIGURE N


"""
) + GLOBAL_CODE_RULES


SALES_CODE_PROMPT = (
"""
{analysis_plan}

Ngữ cảnh EDA rút gọn:
{eda_context}

Danh sách cột (chỉ dùng các cột này, không bịa dữ liệu):
{columns}

Sinh mã Python để:
1. Tổng hợp chỉ số bán hàng / doanh thu
2. Tạo:
   - Biểu đồ đường theo thời gian
   - Biểu đồ cột theo danh mục
3. Lưu mọi biểu đồ bằng save_fig(fig)
4. Chọn chart phù hợp kiểu dữ liệu (time/number vs category)
5. Không tạo dữ liệu giả.

"""
) + GLOBAL_CODE_RULES


ANOMALY_CODE_PROMPT = (
"""
{analysis_plan}

Ngữ cảnh EDA rút gọn:
{eda_context}

Danh sách cột (chỉ dùng các cột này, không bịa dữ liệu):
{columns}

Sinh mã Python để:
1. Phát hiện bất thường bằng IQR hoặc Z-score
2. Trực quan hóa phân phối và outlier
3. Lưu mọi biểu đồ bằng save_fig(fig)
4. Chọn chart phù hợp kiểu dữ liệu (numeric vs categorical).

"""
) + GLOBAL_CODE_RULES


GENERIC_CODE_PROMPT = (
"""
{analysis_plan}

Ngữ cảnh EDA rút gọn:
{eda_context}

Danh sách cột (chỉ dùng các cột này, không bịa dữ liệu):
{columns}

Sinh mã Python để:
1. Tạo các biểu đồ tổng quan phù hợp
2. Ưu tiên phân phối, so sánh và xu hướng cơ bản
3. Lưu mọi biểu đồ bằng save_fig(fig)
4. Chọn chart đúng kiểu dữ liệu; không dùng cột ngoài danh sách.

"""
) + GLOBAL_CODE_RULES
