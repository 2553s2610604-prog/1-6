import streamlit as st

# 1. 페이지 기본 설정
st.set_page_config(
    page_title="우리가 만드는 무적반장",
    page_icon="👑",
    layout="wide"
)

# 2. 내비게이션을 위한 세션 상태 초기화
if 'current_page' not in st.session_state:
    st.session_state['current_page'] = "🏠 홈 (메인 화면)"

# 3. 사이드바 내비게이션 메뉴 구성
st.sidebar.title("👑 무적반장 메뉴")
menu_options = ["🏠 홈 (메인 화면)", "🧹 청소구역 정하기", "🗳️ 학급 투표", "🪑 자리 바꾸기", "✅ 출석 확인"]

selected_page = st.sidebar.radio(
    "이동할 페이지 선택:",
    menu_options,
    index=menu_options.index(st.session_state['current_page'])
)
st.session_state['current_page'] = selected_page

# 4. 각 페이지 연결 함수 (친구들의 파일을 불러오는 안전장치)
def load_page(file_name, page_title):
    try:
        with open(file_name, encoding='utf-8') as f:
            code = compile(f.read(), file_name, 'exec')
            exec(code, globals())
    except FileNotFoundError:
        st.warning(f"⚠️ `{file_name}` 파일이 아직 업로드되지 않았습니다.")
        st.info(f"💡 이 구역은 **[{page_title}]** 담당 친구가 만든 코드가 보여질 자리입니다.")
        if st.button("🏠 메인 화면으로 돌아가기"):
            st.session_state['current_page'] = "🏠 홈 (메인 화면)"
            st.rerun()

# ---------------------------------------------------------
# [화면 분기 처리]
# ---------------------------------------------------------

# 1) 메인 화면인 경우 (내가 꾸미는 공간)
if st.session_state['current_page'] == "🏠 홈 (메인 화면)":
    st.title("👑 우리 반의 질서는 내가 지킨다! [무적반장]")
    st.subheader("오늘도 평화로운 학급을 만들기 위한 반장 전용 관제탑입니다.")
    st.markdown("---")
    
    st.markdown("### 🛠️ 우리 반 특수 기능 안내")
    st.write("원하는 기능의 설명을 읽고 버튼을 누르면 해당 담당자가 만든 페이지로 바로 이동합니다.")
    
    # 2x2 카드 레이아웃 구성
    col1, col2 = st.columns(2)
    
    with col1:
        st.info("### 🧹 1. 청소구역 정하기\n\n**담당자: 친구 A**\n\n매번 싸우는 청소구역 배정은 이제 끝! 공정하게 랜덤으로 청소 구역을 배정하여 학급의 청결을 유지합니다.")
        if st.button("🧹 청소구역 정하러 가기", use_container_width=True):
            st.session_state['current_page'] = "🧹 청소구역 정하기"
            st.rerun()
            
        st.write("") 
        
        st.success("### 🪑 3. 자리 바꾸기\n\n**담당자: 친구 C**\n\n수업 시간 잡담을 방지하고, 새로운 친구와 친해질 수 있도록 공정하게 자리를 재배치하는 마법의 툴입니다.")
        if st.button("🪑 자리 바꾸러 가기", use_container_width=True):
            st.session_state['current_page'] = "🪑 자리 바꾸기"
            st.rerun()

    with col2:
        st.warning("### 🗳️ 2. 학급 투표\n\n**담당자: 친구 B**\n\n학급 축제나 건의사항 등 예민한 문제를 다수결로 깔끔하게 결정하여 분란을 조기에 차단합니다.")
        if st.button("🗳️ 학급 투표하러 가기", use_container_width=True):
            st.session_state['current_page'] = "🗳️ 학급 투표"
            st.rerun()
            
        st.write("") 
        
        st.error("### ✅ 4. 출석 확인\n\n**담당자: 친구 D**\n\n조례, 종례 시간이나 이동 수업 시 자리에 없는 학생을 신속하게 체크하여 담임 선생님께 전달합니다.")
        if st.button("✅ 출석 확인하러 가기", use_container_width=True):
            st.session_state['current_page'] = "✅ 출석 확인"
            st.rerun()

    st.markdown("---")
    st.caption("💡 팁: 왼쪽의 사이드바 메뉴를 통해서도 언제든지 페이지를 자유롭게 이동할 수 있습니다.")

# 2) 다른 친구들의 페이지인 경우 (외부 파일 호출)
elif st.session_state['current_page'] == "🧹 청소구역 정하기":
    load_page("cleaning.py", "청소구역 정하기")

elif st.session_state['current_page'] == "🗳️ 학급 투표":
    load_page("vote.py", "학급 투표")

elif st.session_state['current_page'] == "🪑 자리 바꾸기":
    load_page("seating.py", "자리 바꾸기")

elif st.session_state['current_page'] == "✅ 출석 확인":
    load_page("attendance.py", "출석 확인")
