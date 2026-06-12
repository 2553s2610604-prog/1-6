import streamlit as st
import random
import datetime

# 1. 페이지 기본 설정 및 디자인
st.set_page_config(
    page_title="우리가 만드는 무적반장",
    page_icon="👑",
    layout="wide"
)

# 세션 상태(Session State)를 활용한 페이지 이동 처리
if 'current_page' not in st.session_state:
    st.session_state['current_page'] = "🏠 홈 (메인 화면)"

# 사이드바 네비게이션
st.sidebar.title("👑 무적반장 메뉴")
selected_page = st.sidebar.radio(
    "이동할 페이지를 선택하세요:",
    ["🏠 홈 (메인 화면)", "🧹 청소구역 정하기", "🗳️ 학급 투표", "🪑 자리 바꾸기", "✅ 출석 확인"],
    index=["🏠 홈 (메인 화면)", "🧹 청소구역 정하기", "🗳️ 학급 투표", "🪑 자리 바꾸기", "✅ 출석 확인"].index(st.session_state['current_page'])
)
st.session_state['current_page'] = selected_page

# ---------------------------------------------------------
# [PAGE 1] 🏠 홈 (메인 화면)
# ---------------------------------------------------------
if st.session_state['current_page'] == "🏠 홈 (메인 화면)":
    st.title("👑 우리 반의 질서는 내가 지킨다! [무적반장]")
    st.subheader("오늘도 평화로운 학급을 만들기 위한 반장 전용 관제탑입니다.")
    st.markdown("---")
    
    st.markdown("### 🛠️ 반장 전용 특수 무기 (기능 안내)")
    st.write("원하는 기능의 설명을 읽고 아래 버튼을 누르면 해당 페이지로 바로 순간이동합니다.")
    
    # 2x2 그리드로 기능 설명 카드 배치
    col1, col2 = st.columns(2)
    
    with col1:
        st.info("### 🧹 1. 청소구역 정하기\n\n**\"누구도 불만 없게!\"**\n\n매번 싸우는 청소구역 배정은 이제 끝. 공정하게 랜덤으로 청소 구역을 배정하여 학급의 청결과 평화를 유지합니다.")
        if st.button("🧹 청소구역 정하러 가기"):
            st.session_state['current_page'] = "🧹 청소구역 정하기"
            st.rerun()
            
        st.write("") # 공백용
        
        st.success("### 🪑 3. 자리 바꾸기\n\n**\"수업 시간 잡담 방지!\"**\n\n친한 친구들끼리 모여 앉아 떠드는 것을 방지하고, 새로운 친구와 친해질 수 있도록 공정하게 자리를 재배치합니다.")
        if st.button("🪑 자리 바꾸러 가기"):
            st.session_state['current_page'] = "🪑 자리 바꾸기"
            st.rerun()

    with col2:
        st.warning("### 🗳️ 2. 학급 투표\n\n**\"민주적인 의사결정!\"**\n\n학급 축제 준비, 급식 순서 등 예민한 문제를 다수결로 깔끔하게 결정하여 분란을 조기에 차단합니다.")
        if st.button("🗳️ 학급 투표하러 가기"):
            st.session_state['current_page'] = "🗳️ 학급 투표"
            st.rerun()
            
        st.write("") # 공백용
        
        st.error("### ✅ 4. 출석 확인\n\n**\"단 한 명도 놓치지 않는다!\"**\n\n조례, 종례 시간이나 이동 수업 시 자리에 없는 학생을 신속하게 체크하여 담임 선생님께 보고합니다.")
        if st.button("✅ 출석 확인하러 가기"):
            st.session_state['current_page'] = "✅ 출석 확인"
            st.rerun()

    st.markdown("---")
    st.caption("💡 팁: 왼쪽의 사이드바 메뉴를 통해서도 언제든지 페이지를 자유롭게 이동할 수 있습니다.")

# ---------------------------------------------------------
# [PAGE 2] 🧹 청소구역 정하기
# ---------------------------------------------------------
elif st.session_state['current_page'] == "🧹 청소구역 정하기":
    st.title("🧹 공정한 청소구역 정하기")
    st.write("학생 이름과 청소 구역을 입력하면 랜덤으로 매칭해 줍니다.")
    
    students_input = st.text_area("학생 이름을 쉼표(,)로 구분해서 입력하세요:", "김철수, 이영희, 박민수, 최지우, 정항우, 홍길동")
    zones_input = st.text_area("청소 구역을 쉼표(,)로 구분해서 입력하세요:", "칠판/교탁, 창문, 바닥 쓸기, 바닥 닦기, 분리수거, 사물함 위")
    
    if st.button("🎲 청소 구역 랜덤 배치 시작!"):
        try:
            students = [s.strip() for s in students_input.split(",") if s.strip()]
            zones = [z.strip() for z in zones_input.split(",") if z.strip()]
            
            if not students or not zones:
                st.error("학생 이름과 청소 구역을 모두 입력해주세요.")
            else:
                random.shuffle(students)
                st.subheader("📊 배정 결과")
                
                # 매칭 결과 테이블 출력
                result_data = []
                for i in range(max(len(students), len(zones))):
                    student = students[i] if i < len(students) else "💡 인원 부족 (공석)"
                    zone = zones[i] if i < len(zones) else "💡 구역 남음 (자원봉사)"
                    result_data.append({"청소 구역": zone, "담당 학생": student})
                st.table(result_data)
        except Exception as e:
            st.error(f"오류가 발생했습니다: {e}")
            
    if st.button("🏠 메인 화면으로 돌아가기"):
        st.session_state['current_page'] = "🏠 홈 (메인 화면)"
        st.rerun()

# ---------------------------------------------------------
# [PAGE 3] 🗳️ 학급 투표
# ---------------------------------------------------------
elif st.session_state['current_page'] == "🗳️ 학급 투표":
    st.title("🗳️ 신속하고 민주적인 학급 투표")
    st.write("학급의 주요 안건을 투표에 부쳐 질서를 확립하세요.")
    
    topic = st.text_input("투표 안건을 입력하세요:", "이번 학급 축제 때 할 활동은?")
    options_input = st.text_input("투표 선택지를 쉼표(,)로 구분하세요:", "먹거리 장터, 귀신의 집, 보드게임 카페")
    
    options = [o.strip() for o in options_input.split(",") if o.strip()]
    
    if options:
        st.write(f"### 📋 안건: {topic}")
        vote = st.radio("당신의 선택은?", options)
        
        if st.button("🗳️ 투표 제출"):
            st.success(f"🎉 '{vote}'에 성공적으로 투표되었습니다! (실제 운영 시 결과를 취합하는 화면으로 확장 가능)")
            
    if st.button("🏠 메인 화면으로 돌아가기"):
        st.session_state['current_page'] = "🏠 홈 (메인 화면)"
        st.rerun()

# ---------------------------------------------------------
# [PAGE 4] 🪑 자리 바꾸기
# ---------------------------------------------------------
elif st.session_state['current_page'] == "🪑 자리 바꾸기":
    st.title("🪑 떠들기 방지 자리 바꾸기")
    st.write("학생들의 자리를 무작위로 섞어 배치도를 만듭니다.")
    
    students_list = st.text_area("자리 바꿀 학생 이름을 쉼표(,)로 구분하여 입력:", "철수, 영희, 민수, 지우, 정우, 길동, 짱구, 철수2, 유리, 맹구")
    cols_count = st.number_input("교실의 열(가로 줄) 수 입력:", min_value=1, max_value=10, value=3)
    
    if st.button("🪑 새로운 자리 배치도 생성"):
        students = [s.strip() for s in students_list.split(",") if s.strip()]
        if students:
            random.shuffle(students)
            
            # 2차원 교실 배열 만들기
            grid = []
            for i in range(0, len(students), cols_count):
                grid.append(students[i:i+cols_count])
                
            st.subheader("🖥️ [ 교탁 방향 ]")
            for row in grid:
                cols = st.columns(cols_count)
                for idx, student in enumerate(row):
                    cols[idx].button(student, key=f"seat_{student}_{idx}")
        else:
            st.error("학생 이름을 입력해주세요.")
            
    if st.button("🏠 메인 화면으로 돌아가기"):
        st.session_state['current_page'] = "🏠 홈 (메인 화면)"
        st.rerun()

# ---------------------------------------------------------
# [PAGE 5] ✅ 출석 확인
# ---------------------------------------------------------
elif st.session_state['current_page'] == "✅ 출석 확인":
    st.title("✅ 실시간 출석 및 이탈자 체크")
    st.write(f"일시: {datetime.date.today().strftime('%Y년 %m월 %d일')}")
    
    st.markdown("### 🚨 미등교/이탈 학생 체크리스트")
    students_demo = ["김철수", "이영희", "박민수", "최지우", "정항우", "홍길동"]
    
    absent_students = []
    for student in students_demo:
        # 체크박스가 선택되면 '출석', 해제되면 '결석/이탈'
        is_present = st.checkbox(f"{student} (출석함)", value=True)
        if not is_present:
            absent_students.append(student)
            
    st.markdown("---")
    st.subheader("📋 담임 선생님 제출용 보고서")
    if absent_students:
        st.error(f"⚠️ 현재 자리에 없는 학생 ({len(absent_students)}명): {', '.join(absent_students)}")
    else:
        st.success("✨ 전원 출석 완료! 이상 없습니다.")
        
    if st.button("🏠 메인 화면으로 돌아가기"):
        st.session_state['current_page'] = "🏠 홈 (메인 화면)"
        st.rerun()
