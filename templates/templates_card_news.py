from html import escape
from pathlib import Path
import base64

def image_to_base64(image_path):
  image_path = Path(image_path)

  if not image_path.exists():
      return ""

  with open(image_path, "rb") as f:
      encoded = base64.b64encode(f.read()).decode("utf-8")

  suffix = image_path.suffix.lower().replace(".", "")

  if suffix == "jpg":
      suffix = "jpeg"

  return f"data:image/{suffix};base64,{encoded}"


def get_css():
  return """
:root {
      --color-page-bg: #f8fafc;
      --color-text: #1e293b;
      --color-muted: #64748b;
      --color-light-muted: #94a3b8;
      --color-border: #e2e8f0;
      --color-card-border: #f1f5f9;
      --color-card-bg: #ffffff;
      --color-panel-bg: #f8fafc;
      --color-blue: #2563eb;
      --color-blue-hover: #1d4ed8;
      --color-indigo: #6366f1;
      --color-warning: #f59e0b;
      --color-ethics-bg: #fff1f2;
      --color-ethics-border: #ffe4e6;
      --color-ethics-text: #9f1239;
      --radius-lg: 12px;
      --radius-xl: 16px;
      --radius-2xl: 20px;
      --shadow-card: 0 1px 2px rgba(15, 23, 42, 0.06);
      --shadow-card-hover: 0 8px 20px rgba(15, 23, 42, 0.10);
      --shadow-header: 0 20px 35px rgba(15, 23, 42, 0.18);
    }

    * {
      box-sizing: border-box;
    }

    body {
      font-family: 'Inter', 'Noto Sans KR', sans-serif;
      margin: 0;
      padding: 16px;
      color: var(--color-text);
      background-color: var(--color-page-bg);
      -webkit-font-smoothing: antialiased;
      text-rendering: optimizeLegibility;
    }

    /* Streamlit iframe 내부 스크롤바 */
    ::-webkit-scrollbar {
      width: 6px;
      height: 6px;
    }

    ::-webkit-scrollbar-track {
      background: transparent;
    }

    ::-webkit-scrollbar-thumb {
      background: #cbd5e1;
      border-radius: 4px;
    }

    ::-webkit-scrollbar-thumb:hover {
      background: #94a3b8;
    }

    .app-page {
      max-width: 1280px;
      margin: 0 auto;
    }

    .briefing-header {
      margin-bottom: 24px;
      padding: 22px 24px;
      color: var(--color-text);
      border: 1px solid var(--color-border);
      border-radius: var(--radius-2xl);
      background: #ffffff;
      box-shadow: 0 10px 24px rgba(15, 23, 42, 0.06);
    }

    .header-content {
      display: flex;
      flex-direction: column;
      gap: 18px;
    }

    .header-top {
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      justify-content: space-between;
      gap: 12px;
      padding-bottom: 14px;
      border-bottom: 1px solid var(--color-border);
    }

    .header-meta {
      display: flex;
      align-items: center;
      gap: 10px;
    }

    .date-badge {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      padding: 5px 12px;
      color: var(--color-blue);
      font-size: 12px;
      font-weight: 800;
      letter-spacing: 0.04em;
      border: 1px solid #bfdbfe;
      border-radius: 999px;
      background: #eff6ff;
    }

    .dashboard-label {
      color: #475569;
      font-size: 13px;
      font-weight: 700;
    }

    .selection-note {
      max-width: 448px;
      padding: 5px 10px;
      color: #64748b;
      font-size: 12px;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
      border: 1px solid #e0e7ff;
      border-radius: 999px;
      background: #f8fafc;
    }

    .core-message-section {
      display: grid;
      grid-template-columns: 160px minmax(0, 1fr);
      gap: 18px;
      align-items: start;
    }

    .core-label {
      display: inline-flex;
      align-items: center;
      gap: 8px;
      margin-top: 4px;
      color: #4338ca;
      font-size: 12px;
      font-weight: 900;
      letter-spacing: 0.08em;
      line-height: 1.4;
      text-transform: uppercase;
    }

    .pulse-dot {
      display: inline-block;
      flex: 0 0 auto;
      width: 8px;
      height: 8px;
      border-radius: 999px;
      background: var(--color-blue);
    }

    .core-message {
      position: relative;
      margin: 0;
      padding-left: 18px;
      color: #0f172a;
      font-size: 19px;
      font-weight: 800;
      line-height: 1.75;
      letter-spacing: -0.03em;
      border-left: 4px solid var(--color-blue);
    }

    .news-grid {
      display: grid;
      grid-template-columns: repeat(1, minmax(0, 1fr));
      gap: 24px;
    }

    .news-card {
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      height: 100%;
      overflow: hidden;
      border: 1px solid var(--color-card-border);
      border-radius: var(--radius-2xl);
      background: var(--color-card-bg);
      box-shadow: var(--shadow-card);
      transition: box-shadow 0.3s ease, transform 0.3s ease;
    }

    .news-card:hover {
      box-shadow: var(--shadow-card-hover);
      transform: translateY(-2px);
    }

    .card-body {
      flex: 1;
      padding: 20px;
    }

    .card-top-row {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 12px;
      margin-bottom: 16px;
    }

    .rank-category-group {
      display: flex;
      align-items: center;
      gap: 8px;
      min-width: 0;
    }

    .rank-badge {
      display: inline-flex;
      align-items: center;
      justify-content: center;
      flex: 0 0 auto;
      width: 32px;
      height: 32px;
      color: #ffffff;
      font-size: 14px;
      font-weight: 800;
      border-radius: 10px;
      background: linear-gradient(135deg, #2563eb, #4f46e5);
      box-shadow: 0 4px 10px rgba(59, 130, 246, 0.22);
    }

    .category-badge {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      padding: 4px 10px;
      color: #334155;
      font-size: 11px;
      font-weight: 800;
      border: 1px solid rgba(226, 232, 240, 0.8);
      border-radius: 6px;
      background: #f1f5f9;
    }

    .category-dot {
      width: 6px;
      height: 6px;
      border-radius: 999px;
      background: #10b981;
    }

    .category-industry .category-dot { background: #10b981; }
    .category-tech .category-dot { background: #3b82f6; }
    .category-policy .category-dot { background: #a855f7; }
    .category-education .category-dot { background: #f97316; }
    .category-mobility .category-dot { background: #06b6d4; }
    .category-domestic .category-dot { background: #ec4899; }

    .top-label {
      flex: 0 0 auto;
      color: var(--color-light-muted);
      font-size: 10px;
      font-weight: 700;
    }

    .article-title {
      margin: 0 0 8px;
      color: #0f172a;
      font-size: 18px;
      font-weight: 900;
      line-height: 1.35;
      letter-spacing: -0.03em;
    }

    .article-summary {
      margin: 0 0 16px;
      padding: 12px;
      color: var(--color-muted);
      font-size: 12px;
      line-height: 1.7;
      border: 1px solid rgba(241, 245, 249, 0.9);
      border-radius: 10px;
      background: var(--color-panel-bg);
    }
    
    .news-card {
      overflow: hidden;
    }

    .card-image-wrap {
      position: relative;
      width: 100%;
      height: 180px;
      overflow: hidden;
      background: #e5e7eb;
    }

    .card-image {
      width: 100%;
      height: 100%;
      object-fit: cover;
      display: block;
    }

    .importance-block {
      margin-bottom: 14px;
    }

    .section-label {
      display: flex;
      align-items: center;
      gap: 4px;
      margin: 0 0 4px;
      color: var(--color-light-muted);
      font-size: 10px;
      font-weight: 800;
      letter-spacing: 0.08em;
      text-transform: uppercase;
    }

    .section-icon-warning {
      color: var(--color-warning);
    }

    .importance-text {
      margin: 0;
      padding-left: 6px;
      color: #334155;
      font-size: 12px;
      font-weight: 600;
      line-height: 1.7;
      border-left: 2px solid var(--color-warning);
    }

    .tag-list {
      display: flex;
      flex-wrap: wrap;
      gap: 4px;
      margin-bottom: 14px;
    }

    .tag {
      color: var(--color-muted);
      font-size: 10px;
      font-weight: 600;
    }

    .ethics-box {
      padding: 12px;
      border: 1px solid var(--color-ethics-border);
      border-radius: 10px;
      background: rgba(255, 241, 242, 0.7);
    }

    .ethics-title-row {
      display: flex;
      align-items: center;
      gap: 4px;
      margin-bottom: 4px;
      color: #be123c;
    }

    .ethics-title {
      margin: 0;
      font-size: 10px;
      font-weight: 800;
      letter-spacing: 0.08em;
      text-transform: uppercase;
    }

    .ethics-text {
      margin: 0;
      color: var(--color-ethics-text);
      font-size: 12px;
      line-height: 1.7;
    }

    .card-footer {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 8px;
      padding: 12px 20px;
      border-top: 1px solid var(--color-card-border);
      background: var(--color-panel-bg);
    }

    .source-info {
      display: flex;
      flex-direction: column;
      color: var(--color-light-muted);
      font-size: 10px;
      line-height: 1.5;
    }

    .source-name {
      color: var(--color-muted);
      font-weight: 700;
    }

    .original-link {
      display: inline-flex;
      align-items: center;
      gap: 4px;
      flex: 0 0 auto;
      padding: 6px 12px;
      color: #ffffff;
      font-size: 11px;
      font-weight: 800;
      text-decoration: none;
      border-radius: 8px;
      background: var(--color-blue);
      transition: background 0.2s ease;
    }

    .original-link:hover {
      background: var(--color-blue-hover);
    }

    .icon-xs {
      width: 12px;
      height: 12px;
    }

    .icon-sm {
      width: 14px;
      height: 14px;
    }
        
    @media (min-width: 768px) {
      .briefing-header {
        padding: 28px 32px;
      }

      .core-message {
        font-size: 22px;
      }

      .news-grid {
        grid-template-columns: repeat(2, minmax(0, 1fr));
      }

      .card-body {
        padding: 24px;
      }
    }

    @media (min-width: 1024px) {
      .news-grid {
        grid-template-columns: repeat(2, minmax(0, 1fr));
      }
    }
"""

def render_header(today_info):
    date = escape(today_info.get("date", ""))
    service_name = escape(today_info.get("service_name", "Daily AI Briefing"))
    core_message = escape(today_info.get("core_message", ""))

    return f"""
    <header class="briefing-header">
      <div class="header-content">
        <div class="header-top">
          <div class="header-meta">
            <span class="date-badge">
              {date}
            </span>
            <span class="dashboard-label">{service_name}</span>
          </div>
        </div>
        <section class="core-message-section">
          <span class="core-label">
            <span class="pulse-dot"></span>
            Today's Core Message
          </span>
          <h1 class="core-message">
            {core_message}
          </h1>
        </section>   
      </div>         
    </header>
    """
def render_tags(tags):
    tag_html = ""
    for tag in tags:
        safe_tag = escape(str(tag))
        if not safe_tag.startswith("#"):
            safe_tag = "#" + safe_tag
        tag_html += f'<span class="tag">{safe_tag}</span>'
    return tag_html

def render_card(news):
    title = escape(news.get("card_title", ""))
    summary = escape(news.get("one_line_summary", ""))
    importance = escape(news.get("why_important", ""))
    keywords = news.get("keywords", [])
    source = escape(news.get("source", ""))
    published_at = escape(news.get("published", ""))
    url = escape(news.get("url", "#"))
    category = escape(news.get("category", "기타"))
    ethics = escape(news.get("ethical_considerations", ""))
    index = news.get("rank", 1)

    category_name = ["","AI 기술","AI 서비스","기업·산업","정책·규제",
                     "교육·학습","연구·논문","보안·개인정보",
                     "윤리·사회 영향","콘텐츠·미디어",
                     "하드웨어·인프라","기타·종합"]
    
    category_image = f"/app/static/img/{category_name.index(category)}.jpg"
    category_image = image_to_base64(category_image)
    return f"""
    <article class="news-card">
      <div class="card-image-wrap">
        <img src="{category_image}" class="card-image">
      </div>
      <div class="card-body">
        <div class="card-top">
          <div class="rank-category">
            <span class="rank-badge">{index}</span>
            <span class="category-badge">{category}</span>
          </div>
          <span class="top-label">TOP {index}</span>
        </div>
        <h2 class="article-title">{title}</h2>
        <p class="article-summary">
          {summary}
        </p>
        <div class="section-label">왜 중요할까요?</div>
        <p class="importance-text">
          {importance}
        </p>
        <div class="tag-list">
          {render_tags(keywords)}
        </div>
        <div class="ethics-box">
          <div class="ethics-title">Ethical Considerations</div>
          <p class="ethics-text">{ethics}</p>
        </div>
      </div>
      <footer class="card-footer">
        <div class="source-info">
          <span class="source-name">{source}</span>
          <span>{published_at}</span>
        </div>
        <a href="{url}" target="_blank" class="original-link">원문 보기</a>
      </footer>
    </article>
    """

def render_cards(news_list):
    card_html = ""
    for idx in range(len(news_list["top_news"])):
      dict_news = news_list["top_news"][idx]
      card_html += render_card(dict_news)    
    return f"""
    <main class="news-grid">
      {card_html}
    </main>
    """

def render_html_header():
    return f"""
      <!DOCTYPE html>
      <html lang="ko">
      <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&family=Noto+Sans+KR:wght@300;400;500;700;900&display=swap" rel="stylesheet">
        <style>
          {get_css()}
        </style>
      </head>
      <body>
    """

def render_html_footer():
  return f"""
      </body>
    </html>
  """
  
def render_page(today_info, news_list):
    return f"""
    <!DOCTYPE html>
    <html lang="ko">
    <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <link rel="preconnect" href="https://fonts.googleapis.com">
      <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
      <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&family=Noto+Sans+KR:wght@300;400;500;700;900&display=swap" rel="stylesheet">
      <style>
        {get_css()}
      </style>
    </head>
    <body>
      <div class="page-container">
        {render_header(today_info)}
        {render_cards(news_list)}
      </div>
    </body>
    </html>
    """