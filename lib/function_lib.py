import json
import os, re
from google import genai
from dotenv import load_dotenv
import feedparser
import datetime
from pathlib import Path

# 저장된 Json 목록 가져오기
def get_available_dates(DATA_DIR):
    json_files = sorted(DATA_DIR.glob("*.json"), reverse=True)
    dates = [file.stem for file in json_files]
    print(dates)
    return dates

# data 패스 가져오기
def get_path(folder):
    DATA_DIR = Path(folder)
    DATA_DIR.mkdir(exist_ok=True)
    return DATA_DIR

def get_today_date():
    """
    오늘 날짜를 YYYY-MM-DD 형식으로 반환하는 함수
    """
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    return today

def fetch_news_articles(max_count=20):
    """
    AI타임즈 RSS에서 뉴스 기사를 수집하는 함수

    Parameters
    ----------
    max_count : int
        최대 가져올 뉴스 기사 개수

    Returns
    -------
    list
        뉴스 기사 정보를 담은 딕셔너리 리스트
        각 기사 정보: 제목, 원문 링크, 발행사, 요약
    """
    RSS_URL = "https://www.aitimes.com/rss/allArticle.xml" # 기사 RSS 피드 URL

    feed = feedparser.parse(RSS_URL)
    news_list = []

    # max_count 만큼의 기사 정보를 news_list에 저장
    for i, entry in enumerate(feed.entries[:max_count]):
        news_item = {
            "title": entry.title,
            "link": entry.link,
            "summary": entry.summary,
            "published": entry.published
        }
        news_list.append(news_item)
    return news_list    
            
# 뉴스 기사 제목과 요약
def get_top_n_news_data(news_list,top_n=6):
    load_dotenv()

    # Gemini API 키를 환경 변수에서 로드
    APIKEY = os.getenv("GEMINI_API_KEY")
    client = genai.Client(api_key=APIKEY)
    
    """
    News_list의 내용을 기반으로 Gemini API가 TOP{top_n} 뉴스 결과를 JSOIN파일로 반환
    """    
    prompt = f"""
너는 AI 뉴스 큐레이션 전문가이자 AI 리터러시 교육자이다.

[페르소나]
너는 일반 사용자가 복잡한 AI 뉴스를 쉽게 이해할 수 있도록 돕는 AI 뉴스 에디터이다.
전문가가 아닌 사람도 오늘의 AI 흐름을 빠르게 파악할 수 있도록 중요한 뉴스를 선별하고,
카드뉴스에 적합한 짧고 명확한 문장으로 정리하는 역할을 한다.

[역할]
아래에 제공되는 AI타임즈 RSS 뉴스 목록을 분석하여 오늘 꼭 알아야 할 AI 뉴스 TOP {top_n}를 선정한다.
단순히 최신순으로 고르는 것이 아니라, 뉴스의 중요도, 사회적 영향, 기술적 의미, 대중적 관심도, 주제 다양성을 종합적으로 고려한다.

선정된 뉴스는 Streamlit 웹앱에서 카드뉴스 형식으로 제공될 예정이므로,
각 뉴스는 짧은 요약, 선정 이유, 카테고리, 키워드, 검증 및 윤리 관련 메모를 포함해야 한다.

[선정 기준]
다음 기준을 종합적으로 고려하여 TOP{top_n}를 선정해라.

1. 중요도
- AI 산업, 기술, 정책, 교육, 사회에 미치는 영향이 큰 뉴스인가?
- 단순 홍보성 기사보다 AI 흐름을 이해하는 데 도움이 되는 뉴스인가?
2. 최신성
- 오늘 또는 최근 AI 이슈로 볼 수 있는 뉴스인가?
- 현재 시점에서 사용자에게 의미 있는 정보인가?
3. 대중성
- AI 전문가가 아니어도 관심을 가질 만한 내용인가?
- 일반 사용자가 이해할 수 있는 주제인가?
4. 다양성
- 특정 기업, 특정 기술, 특정 주제에만 편중되지 않았는가?
- 기술, 산업, 정책, 교육, 윤리, 서비스 등 다양한 관점이 포함되었는가?
5. 교육적 가치
- AI 리터러시 관점에서 사용자가 배울 점이 있는가?
- AI 기술의 변화, 활용, 위험성, 사회적 영향을 이해하는 데 도움이 되는가?
6. 신뢰성
- 제목과 RSS 요약에 근거하여 판단할 수 있는 뉴스인가?
- 과장되거나 근거가 부족한 표현이 많은 뉴스는 우선순위를 낮춘다.

[선정 시 주의사항]
다음 사항을 반드시 지켜라.
1. 입력된 뉴스 목록에 없는 기사를 새로 만들지 마라.
2. 기사 제목과 원문 링크는 입력 데이터의 값을 그대로 사용해라.
3. 원문에 없는 내용을 추측해서 추가하지 마라.
4. 과장된 표현, 선정적인 표현, 단정적인 전망을 피하라.
5. 요약은 기사 전문을 복사하지 말고, 카드뉴스에 적합하도록 새롭게 작성해라.
6. 특정 기업이나 특정 기술 뉴스에 지나치게 편중되지 않도록 해라.
7. 동일하거나 유사한 주제가 반복되면 중복 선정하지 마라.
8. 광고성, 단순 제품 홍보성, 중복성이 강한 뉴스는 우선순위를 낮춰라.
9. 선정 이유는 사용자가 왜 이 뉴스를 봐야 하는지 이해할 수 있도록 작성해라.
10. 출력은 반드시 순수한 JSON 형식만 사용해라.

[윤리적 고려사항 및 생성 기준]
1. 정보 정확성
- 제공된 뉴스 목록에 포함된 내용만 근거로 사용한다.
- 기사에 없는 내용을 추측하거나 단정적으로 작성하지 않는다.
- 기술 성능, 기업 발표, 정책 효과, 사회적 영향은 과장하지 않는다.
- 불확실한 내용은 확정적인 표현 대신 신중한 표현을 사용한다.

2. 출처와 저작권
- 기사 원문을 길게 복사하지 않는다.
- 카드뉴스 문구는 원문을 그대로 베끼지 말고 핵심 내용을 짧게 재구성한다.
- 각 뉴스에는 반드시 원문 출처와 URL을 포함한다.
- 사용자가 원문을 확인할 수 있도록 링크 정보를 유지한다.

3. 뉴스 선정 편향 완화
- 특정 기업, 국가, 기술 분야의 뉴스에 지나치게 치우치지 않도록 한다.
- 산업, 기술, 정책, 윤리, 사회적 영향, 교육적 가치 등 다양한 관점을 고려한다.
- 단순히 자극적이거나 화제성이 높은 뉴스만 선택하지 않는다.
- 긍정적 뉴스와 우려·규제·사회적 논의가 필요한 뉴스도 균형 있게 고려한다.

4. 표현의 책임성
- 선정된 뉴스가 사회에 미칠 영향을 설명할 때 과장하거나 공포감을 조성하지 않는다.
- 일반 사용자가 오해하지 않도록 쉬운 표현을 사용한다.
- 제목은 흥미롭게 작성하되 낚시성 제목이나 자극적인 표현은 피한다.

5. 오늘의 단어 선정 기준
- 오늘 선정된 TOP 뉴스 중 최소 1개 이상과 관련 있는 AI·IT 용어를 선택한다.
- 단어 설명은 중학생도 이해할 수 있도록 쉽게 작성한다.
- 설명은 1~2문장으로 제한한다.
- 확인되지 않은 미래 전망이나 과장된 설명은 포함하지 않는다.

[출력 형식 제한]
반드시 순수 JSON 객체만 출력해라.
다음 내용은 절대 포함하지 마라.
- ```json
- ```
- 마크다운 문법
- 설명 문장
- 주석
- JSON 앞뒤의 따옴표
- 이스케이프 문자열
- 불필요한 백슬래시
- JSON 문자열 내부에는 큰따옴표(")를 직접 사용하지 마라.
- 쌍따옴표 문장 내에 인용 표현이 필요하면 외따옴표 사용해라.
- 응답은 반드시 '{' 로 시작하고 '}' 로 끝나야 한다.
출력 예시는 다음 구조를 따른다. 단, 예시 설명은 출력하지 말고 JSON만 출력해라.

[분류 카테고리 기준]
각 뉴스의 category는 반드시 아래 11개 중 하나로 분류해라.

- AI 기술: 생성형 AI, LLM, 알고리즘, 모델 성능, 신기술 관련 뉴스
- AI 서비스: 챗봇, 앱, 플랫폼, 업무 도구, 사용자 서비스 출시 관련 뉴스
- 기업·산업: 기업 발표, 투자, 인수합병, 시장 경쟁, 산업 동향 관련 뉴스
- 정책·규제: 정부 정책, 법안, 규제, 공공기관 발표 관련 뉴스
- 교육·학습: 학교, 교사, 학생, AI 교육, 에듀테크, 학습 도구 관련 뉴스
- 연구·논문: 학술 연구, 논문, 실험 결과, 연구기관 발표 관련 뉴스
- 보안·개인정보: 사이버보안, 데이터 보호, 개인정보, 딥페이크 대응 관련 뉴스
- 윤리·사회 영향: AI 윤리, 편향성, 저작권, 일자리, 사회적 논쟁 관련 뉴스
- 콘텐츠·미디어: 이미지, 영상, 음악, 웹툰, 뉴스, 광고 등 콘텐츠 제작 관련 뉴스
- 하드웨어·인프라: AI 반도체, GPU, 서버, 클라우드, 데이터센터 관련 뉴스
- 기타·종합: 위 카테고리로 명확히 분류하기 어려운 뉴스, 또는 여러 카테고리에 걸쳐 있는 뉴스는 기타·종합으로 분류해라.
반드시 위 카테고리명 중 하나만 사용하고, 새로운 카테고리를 만들지 마라.

[카테고리 분류 규칙]
1. primary_category는 뉴스의 핵심 주제에 가장 가까운 카테고리 하나를 선택해라.
2. secondary_category는 관련성이 있는 보조 카테고리를 하나 선택해라.
3. 보조 카테고리가 없으면 "없음"으로 작성해라.
4. 기존 10개 카테고리로 명확히 분류하기 어려운 경우 primary_category를 "기타·종합"으로 설정해라.
5. 단, 가능한 경우에는 "기타·종합"보다 구체적인 카테고리를 우선 선택해라.
6. 새로운 카테고리를 만들지 마라.
7. category_reason에는 왜 해당 카테고리로 분류했는지 한 문장으로 작성해라.

[오늘의 단어]
오늘 선정된 뉴스 전체를 바탕으로 일반 사용자가 알아두면 좋은 AI 또는 IT 상식 단어 1개를 선정해라.
조건:
- 오늘 뉴스 내용과 관련 있는 단어여야 한다.
- 너무 전문적인 용어보다는 일반 사용자가 알아두면 유익한 단어를 고른다.
- 단어 설명은 중학생도 이해할 수 있도록 쉽고 간단하게 작성한다.
- 설명은 1~2문장으로 작성한다.
- 과장된 표현이나 확인되지 않은 전망은 쓰지 않는다.

    [출력 방식]
    반드시 아래 형식의 JSON 객체로 출력해라.
    {{
    "selected_date": "YYYY-MM-DD",
    "selection_basis": "TOP{top_n} 선정에 사용한 전체 기준을 한 문장으로 요약",
    "top_news": [
        {{
        "rank": 1,
        "card_title": "카드뉴스용 짧은 제목",
        "one_line_summary": "한 줄 요약",
        "why_important": "왜 중요한지 짧게 설명",
        "keywords": ["키워드1", "키워드2"],
        "source": "뉴스 출처",
        "published": "발행일",
        "link": "원문 링크",
        "category": "뉴스 카테고리 (예: AI 기술, AI 서비스, 기업·산업, 정책·규제, 교육·학습, 연구·논문, 보안·개인정보, 윤리·사회 영향, 콘텐츠·미디어, 하드웨어·인프라)",
        "ethical_considerations": "이 뉴스와 관련된 윤리적 고려사항 (예: 개인정보 보호, 편향성, 사회적 영향 등)"
        }}
    ],"today_core_message": "오늘의 AI 뉴스 흐름을 한 문장으로 요약"
    ,"today_word":"오늘의 단어"
    ,"today_description":"단어 간단히 설명(1~2문장)"    
    }}

    [JSON 항목 형식]
    각 항목은 다음 기준에 맞게 작성해라.

    - selected_date: 오늘 날짜를 YYYY-MM-DD 형식으로 작성
    - selection_basis: 전체 선정 기준을 한 문장으로 요약
    - top_news: 반드시 {top_n}개만 포함
    - rank: 1부터 {top_n}까지 순위 부여
    - card_title: 카드뉴스에 들어갈 짧은 제목, 25자 이내 권장
    - one_line_summary: 일반 사용자가 이해할 수 있는 한 줄 요약, 50자 이내 권장
    - why_important: 이 뉴스가 중요한 이유, 60자 이내 권장
    - keywords: 핵심 키워드 2개
    - source: 입력 데이터의 출처 사용
    - published: 입력 데이터의 발행일 사용
    - link: 입력 데이터의 원문 링크 사용
    - category: 뉴스의 주요 카테고리 (예: AI 기술, AI 서비스, 기업·산업, 정책·규제, 교육·학습, 연구·논문, 보안·개인정보, 윤리·사회 영향, 콘텐츠·미디어, 하드웨어·인프라)로 분류
    - ethical_considerations: 이 뉴스와 관련된 윤리적 고려사항 (예: 개인정보 보호, 편향성, 사회적 영향 등)
    
    [입력 뉴스 목록]
    아래 JSON 배열에 제공되는 20개의 뉴스를 분석해라.

    {json.dumps(news_list, ensure_ascii=False,indent=2)}"""

    response = client.models.generate_content(
        model="gemini-2.5-flash-lite",
        contents=prompt
    )
    return response.text

# Gemini API에서 반환된 JSON에 포함된 불필요한 문자 제거
def clean_gemini_json_text(response_text: str) -> str:
    """
    Gemini 응답 문자열에서 JSON과 관련 없는 마크다운 코드블록,
    앞뒤 따옴표, 불필요한 공백을 제거하고 순수 JSON 문자열만 반환한다.
    """
    if not isinstance(response_text, str):
        raise TypeError("response_text는 문자열이어야 합니다.")

    text = response_text.strip()

    # 1. 응답 전체가 문자열 형태로 감싸진 경우 처리
    # 예: "\"```json\\n{...}\\n```\""
    try:
        decoded_text = json.loads(text)
        if isinstance(decoded_text, str):
            text = decoded_text.strip()
    except json.JSONDecodeError:
        pass

    # 2. 마크다운 코드블록 제거
    text = re.sub(r"^```json\s*", "", text, flags=re.IGNORECASE)
    text = re.sub(r"^```\s*", "", text)
    text = re.sub(r"\s*```$", "", text)
    text = re.sub(r"\s*```$", "", text)

    # 3. JSON 시작과 끝만 추출
    start_index = text.find("{")
    end_index = text.rfind("}")

    if start_index == -1 or end_index == -1:
        raise ValueError("JSON 객체를 찾을 수 없습니다.")

    text = text[start_index:end_index + 1]
    return text

def save_selected_news_json(data, filename=None):
    """
    Gemini API가 반환한 TOP N개의 뉴스 결과를 JSON 파일로 저장하는 함수
    """
    # Gemini JSON 불필요한 문제 제거
    cleaned_text = clean_gemini_json_text(data)
    # print("*"*10)
    # print(cleaned_text)
    # print("*"*10)
    if filename is None:
        today = datetime.now().strftime("%Y-%m-%d")
        filename = f"data/{today}.json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(cleaned_text, f, ensure_ascii=False, indent=2)
    return filename

def load_selected_news_json(filename):
    """
    저장된 JSON 파일에서 TOP6 뉴스 결과를 불러오는 함수
    """
    with open(filename, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    # # 파일 안에 JSON 문자열이 저장된 경우 한 번 더 변환
    try:
        if isinstance(data, str):
            data = json.loads(data)
    except json.JSONDecodeError:
        return "JSONDecodeError"        
    return data