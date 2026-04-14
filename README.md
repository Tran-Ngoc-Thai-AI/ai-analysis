# AI Data Analysis Automation (Streamlit)
Ứng dụng Streamlit tự động hóa toàn bộ vòng đời phân tích dữ liệu: upload → dashboard -> Auto EDA → lập kế hoạch phân tích bằng LLM → sinh code & biểu đồ → insight → xuất báo cáo.

### Diễn giải nhanh
- Người dùng bấm **Analyze** khi đã upload file và nhập nhu cầu.
- EDA đầy đủ → rút gọn `eda_context_light` để tiết kiệm token.
- LLM tạo `eda_summary`, xác định `intent` + `analysis_plan`.
- Sinh code phân tích & biểu đồ (`chart_paths`), sinh dashboard code rồi render; tự sửa code dashboard nếu lỗi.
- Sinh insight, lưu mọi thứ vào `st.session_state`, render báo cáo và cho tải HTML.

## Cấu trúc thư mục
```
nhom1/
├── app.py
├── README.md
├── requirements.txt
├── core/
│   ├── code_generator.py
│   ├── dashboard_template.py
│   ├── data_loader.py
│   ├── eda_engine.py
│   ├── insight_generator.py
│   ├── intent_detector.py
│   ├── reasoning_engine.py
│   ├── report_generator.py
│   └── visualization.py
├── outputs/
│   └── charts/
├── utils/
│   ├── openai_client.py
│   ├── prompt_templates.py
```

## Thiết lập nhanh
- Python 3.10+; cài gói: `pip install -r requirements.txt`.
- Biến môi trường Azure OpenAI:
  - `AZURE_OPENAI_API_KEY`
  - `AZURE_OPENAI_ENDPOINT`
  - `AZURE_OPENAI_DEPLOYMENT`
  
[System.Environment]::SetEnvironmentVariable("AZURE_OPENAI_API_KEY","")
[System.Environment]::SetEnvironmentVariable("AZURE_OPENAI_ENDPOINT","")
[System.Environment]::SetEnvironmentVariable("AZURE_OPENAI_DEPLOYMENT","gpt-4.1")

- Chạy app: `streamlit run app.py`.

## Lưu ý vận hành
- Dashboard code tự động được sửa một lần nếu render thất bại.
- `st.session_state` giữ toàn bộ ngữ cảnh để xem lại kết quả.

## Sample prompt
“Phân tích churn khách hàng và đề xuất chiến lược giữ chân tất cả bằng tiếng việt”