import streamlit as st
import lib.function_lib as lb
import templates.templates_card_news  as tp

st.set_page_config(
    page_title="오늘의 AI 뉴스",
    page_icon="📰",
    layout="wide"
)
###############
## Header 영역
header_html = tp.render_html_header()
st.html(header_html)
###############

DIR_PATH = lb.get_path("data")
# 저장된 json 데이터 가져오기
available_date = lb.get_available_dates(DIR_PATH)
search_today = lb.get_today_date()

with st.sidebar:
    # =========================
    # 사이드바 헤더
    # =========================
    st.markdown("""
    <div class="sidebar-header">
        <div class="sidebar-title">AI Briefing Desk</div>
        <div class="sidebar-subtitle">
            복잡한 AI 뉴스를 핵심 흐름 중심으로 정리했습니다.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="sidebar-divider"></div>', unsafe_allow_html=True)
        
    # =========================
    # 날짜 조회
    # =========================
    st.markdown("""
    <div class="sidebar-section-title">🔎 지난 리포트 조회</div>
    <div class="sidebar-desc">
        저장된 날짜의 AI 뉴스 브리핑을 다시 확인할 수 있습니다.
    </div>
    """, unsafe_allow_html=True)
    select_date = st.selectbox(
        "날짜 조회",
        available_date,
        index=0,
        label_visibility="collapsed"
    )
    
    if select_date != "":
        search_today = select_date

    # 오늘 날짜의 뉴스가 없는 경우 RSS 데이터 가져오기    
    if search_today not in available_date:
        ## 뉴스 기사 수집
        news_list = lb.fetch_news_articles(max_count=20)
        # # 뉴스 기사 선정 및 카드뉴스용 JSON 생성
        today_top_news_json = lb.get_top_n_news_data(news_list)
        # # 테스트를 위해 json파일로 저장
        lb.save_selected_news_json(today_top_news_json, f"data/{search_today}.json")
        # 뉴스 기사 선정 및 카드뉴스용 JSON 생성
        today_top_news_json = lb.load_selected_news_json(f"data/{search_today}.json")
        available_date = lb.get_available_dates(DIR_PATH)

    #################
    ## 메인 title 영역
    #################
    # 전체 뉴스 가져오기
    news_list = lb.load_selected_news_json(f"data/{search_today}.json")
    
    # #############
    # # header 구성
    # #############
    selected_date = news_list["selected_date"]
    selection_basis = news_list["selection_basis"]
    today_core_message = news_list["today_core_message"]
    today_word = news_list["today_word"]
    today_description = news_list["today_description"]
    today_info = {
        "date": search_today,
        "service_name": "오늘의 AI 뉴스 Briefing",
        "core_message": today_core_message,
        "selection_note": selection_basis
    }
    ###############
    ## 오늘의 단어       
    ###############
    st.markdown(f"""
    <div class="sidebar-section-title">📘 오늘의 AI·IT 단어</div>

    <div class="sidebar-word-card">
        <div class="sidebar-word-badge">하루에 하나씩 쌓아가는 AI 지식</div>
        <div class="sidebar-word-term">{today_word}</div>
        <div class="sidebar-word-desc">{today_description}</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('<div class="sidebar-divider"></div>', unsafe_allow_html=True)

cols = st.columns([3,3])
with cols[0]:
    # #############
    # # Header 출력
    # #############
    title_html = tp.render_header(today_info)
    st.html(title_html)

    # #############
    # # 카드 뉴스 구성
    # #############
    card_html = tp.render_cards(news_list)
    st.html(card_html)
    # #############

    # #############
    # # Footer 구성
    # #############
    footer_html = tp.render_html_footer()
    st.html(footer_html)
with cols[1]:
    pass