import streamlit as st
import lib.function_lib as lb
import templates.templates_card_news  as tp

st.set_page_config(
    page_title="오늘의 AI 뉴스",
    page_icon="📰"
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
title_html = tp.render_header(today_info)
st.html(title_html)

###############
## 검색 영역
###############
##검색
with st.container(border=True):
    ###############
    ## 오늘의 단어        
    st.badge("하루에 하나씩 쌓아가는 AI·IT 지식",color="yellow", icon="📝")
    st.success(today_word)
    st.caption(today_description)     
    st.divider()
    cols = st.columns([1.8, 2.2], vertical_alignment="center")
    with cols[0]:
        st.badge("지난 레포트 조회",color="violet",icon="🔎")
    with cols[1]:
        select_date = st.selectbox(
            "날짜 조회",
            available_date,
            index=0,
            label_visibility="collapsed"
        )

         

if select_date != "":
    search_today = select_date
##################


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
# html = render_page(today_info, news_list)
# st.html(html)