import base64
import html
import re
from pathlib import Path
from typing import Optional


def _remove_markdown_table(text: str) -> str:
    if not text:
        return text

    pattern = r"""
    (\n?\|.+?\|\n\|[-:\s|]+\|\n(?:\|.*?\|\n?)*)
    """

    cleaned = re.sub(pattern, "", text, flags=re.VERBOSE | re.DOTALL)

    # remove dòng trống dư
    cleaned = re.sub(r"\n{2,}", "\n\n", cleaned)

    return cleaned.strip()


def _img_to_data_uri(path: str) -> str:
    data = Path(path).read_bytes()
    b64 = base64.b64encode(data).decode("ascii")
    return f"data:image/png;base64,{b64}"


def _render_image_cards(paths, title_prefix: str) -> str:
    if not paths:
        return '<div class="empty">Chưa có hình cho mục này.</div>'

    blocks = []
    for i, p in enumerate(paths, start=1):
        try:
            uri = _img_to_data_uri(p)
            blocks.append(
                f"""
                <div class="img-card">
                  <div class="img-title">Hình {i}: {html.escape(title_prefix)}</div>
                  <img src="{uri}" alt="chart-{i}" />
                </div>
                """
            )
        except Exception:
            blocks.append(
                f"""
                <div class="img-card">
                  <div class="img-title">Hình {i}: {html.escape(title_prefix)}</div>
                  <div class="empty">Không thể đọc ảnh: {html.escape(str(p))}</div>
                </div>
                """
            )
    return "\n".join(blocks)


def _render_table(df):
    if df is None or df.empty:
        return '<div class="empty">Không có dữ liệu bảng.</div>'

    return df.head(10).to_html(
        index=False,
        classes="data-table",
        border=0
    )


def build_report_html(
    df,
    eda_summary: str,
    dashboard_paths,
    chart_paths,
    insight_text: str,
    ketluan: str
) -> str:

    cols = ", ".join(map(str, df.columns))
    dashboard_html = _render_image_cards(dashboard_paths, "Dashboard phân tích dữ liệu")
    charts_html = _render_image_cards(chart_paths, "Biểu đồ phân tích dữ liệu")
    table_html = _render_table(df)
    clean_eda = _remove_markdown_table(eda_summary or "")

    return f"""<!doctype html>
<html lang="vi">
<head>
  <meta charset="utf-8" />
  <title>AI Data Report</title>

  <style>
    * {{ box-sizing: border-box; }}

    body {{
      margin: 0;
      font-family: "Segoe UI", Arial, sans-serif;
      background: #ffffff;
      color: #000000;
      line-height: 1.6;
      padding: 28px;
    }}

    .wrap {{
      max-width: 1100px;
      margin: 0 auto;
    }}

    .title {{
      font-size: 28px;
      font-weight: 700;
      margin-bottom: 10px;
    }}

    .caption {{
      color: #555;
      margin-bottom: 20px;
    }}

    .section {{
      background: #ffffff;
      border: 1px solid #ddd;
      border-radius: 10px;
      padding: 16px;
      margin-bottom: 16px;
    }}

    h2 {{
      margin: 0 0 10px;
      font-size: 20px;
      border-left: 4px solid #333;
      padding-left: 8px;
    }}

    .img-card {{
      background: #ffffff;
      border: 1px solid #ccc;
      border-radius: 8px;
      padding: 10px;
      margin: 10px 0;
    }}

    .img-title {{
      margin-bottom: 6px;
      font-weight: 600;
    }}

    img {{
      width: 100%;
      border-radius: 6px;
      display: block;
    }}

    ul {{
      margin-left: 18px;
    }}

    .empty {{
      color: #b91c1c;
      background: #fee2e2;
      padding: 8px;
      border-radius: 6px;
    }}

    .text {{
      white-space: pre-wrap;
    }}

    .data-table {{
      width: 100%;
      border-collapse: collapse;
      margin-top: 10px;
      font-size: 13px;
    }}

    .data-table th,
    .data-table td {{
      border: 1px solid #d0d0d0;
      padding: 8px;
      text-align: center;
    }}

    .data-table th {{
      background-color: #f3f3f3;
      font-weight: 600;
    }}

    .data-table tr:nth-child(even) {{
      background-color: #fafafa;
    }}

    @media print {{
      body {{
        background: #fff;
        color: #000;
      }}
      .section {{
        page-break-inside: avoid;
      }}
      img {{
        page-break-inside: avoid;
      }}
      .data-table {{
        page-break-inside: auto;
      }}
      .data-table tr {{
        page-break-inside: avoid;
      }}
      thead {{
        display: table-header-group;
      }}
    }}
  </style>
</head>

<body>
  <div class="wrap">
    <h1 class="title">BÁO CÁO PHÂN TÍCH DỮ LIỆU TỰ ĐỘNG BẰNG AI</h1>
    <div class="caption">Upload → Dashboard → EDA → Charts → Insight → PDF</div>

    <section class="section">
      <h2>1. Dashboard</h2>
      {dashboard_html}
    </section>

    <section class="section">
      <h2>2. Tổng quan dữ liệu</h2>
      <ul>
        <li><b>Số dòng:</b> {len(df)}</li>
        <li><b>Số cột:</b> {len(df.columns)}</li>
        <li><b>Danh sách cột:</b> {html.escape(cols)}</li>
      </ul>
    </section>

    <section class="section">
      <h2>3. 10 dòng dữ liệu đầu tiên</h2>
      {table_html}
    </section>

    <section class="section">
      <h2>4. Auto EDA</h2>
      <div class="text">{html.escape(clean_eda or "Không có nội dung EDA.")}</div>
    </section>

    <section class="section">
      <h2>5. Biểu đồ</h2>
      {charts_html}
    </section>

    <section class="section">
      <h2>6. Insight</h2>
      <div class="text">{html.escape(insight_text or "Không có insight.")}</div>
    </section>

    <section class="section">
      <h2>7. Kết luận</h2>
      <div class="text">{html.escape(ketluan or "Không có kết luận.")}</div>
    </section>
  </div>
</body>
</html>
"""


def export_html(
    df,
    eda_summary,
    dashboard_paths,
    chart_paths,
    insight_text,
    ketluan
) -> bytes:
    html_doc = build_report_html(
        df,
        eda_summary,
        dashboard_paths,
        chart_paths,
        insight_text,
        ketluan
    )
    return html_doc.encode("utf-8")
