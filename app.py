import streamlit as st
import requests
from datetime import datetime

# 1. 페이지 설정 및 제목
st.set_page_config(page_title="오성고 급식 알리미", page_icon="🍱")
st.title("🍱 오성고등학교 급식 알리미")
st.write("오늘의 맛있는 급식 메뉴를 확인하세요!")

# 2. 나이스 API 정보 설정 (대구오성고등학교 기준)
# ※ 만약 다른 지역 오성고라면 아래 교육청코드(ATPT_OFCDC_SC_CODE)와 학교코드(SD_SCH_CODE)를 수정하세요.
ATPT_CODE = "R10"       # 대구광역시교육청
SCH_CODE = "7240061"    # 대구오성고등학교 고유코드

# 3. 날짜 선택 (기본값: 오늘 날짜)
today = datetime.today()
selected_date = st.date_input("날짜를 선택하세요", today)
date_str = selected_date.strftime("%Y%m%d") # API 요청용 날짜 형식 (YYYYMMDD)

# 4. 나이스 API 호출 URL 만들기
url = "https://open.neis.go.kr/hub/mealServiceDietInfo"
params = {
    "KEY": "", # 인증키 없이도 기본 호출 가능
    "Type": "json",
    "pIndex": 1,
    "pSize": 10,
    "ATPT_OFCDC_SC_CODE": ATPT_CODE,
    "SD_SCH_CODE": SCH_CODE,
    "MLSV_YMD": date_str
}

# 5. 데이터 가져오기 및 화면 표시
try:
    response = requests.get(url, params=params)
    data = response.json()

    # 급식 데이터가 있는지 확인
    if "mealServiceDietInfo" in data:
        meal_info = data["mealServiceDietInfo"][1]["row"]
        
        # 제공되는 급식(조식/중식/석식) 만큼 반복해서 출력
        for meal in meal_info:
            meal_type = meal["MMEAL_SC_NM"] # 조식, 중식, 석식 구분
            # <br/> 태그를 줄바꿈(\n)으로 바꾸고, 요리명 뒤의 알레르기 번호 제거
            raw_menu = meal["DDISH_NM"].replace("<br/>", "\n")
            
            # 깔끔하게 UI 구성
            st.subheader(f"🍴 {meal_type}")
            st.text(raw_menu)
            st.caption(f"칼로리: {meal['CAL_INFO']}")
            st.divider()
            
    else:
        st.warning("선택하신 날짜에는 급식 정보가 없습니다. (주말, 공휴일 또는 미등록)")

except Exception as e:
    st.error("급식 정보를 가져오는 중 오류가 발생했습니다. 인터넷 연결을 확인해 주세요.")
