import streamlit as st
import random
import datetime

# 1. 페이지 기본 설정 및 디자인 (테마)
st.set_page_config(
    page_title="반장 도와주기 홈",
    page_icon="🎒",
    layout="centered"
)

# 세션 상태(Session State) 초기화 (새로고침해도 데이터가 유지되도록 설정)
if "drawn_numbers" not in st.state_state_keys := st.session_state:
    st.session_state.drawn_numbers = []
if "todo_list" not in st.session_state:
    st.session_state.todo_list = [
        "아침 조회 준비하기",
        "우유/급식 당번 확인하기",
        "교실 환기 및 불 끄기 체크"
    ]

# 앱 타이틀 구역
st.title("🎒 반장 도와주기 치트키 앱")
st.caption("반장님! 오늘도 평화로운 학급을 위해 파이팅! 🔥")
st.markdown("---")

# 2. 첫 번째 기능: [핵심] 1~36번 랜덤 번호 추첨기
st.header("🎯 1~36번 번호 추첨기")
st.write("발표자나 당번을 정할 때 공정하게 뽑아보세요!")

# 학생 수 설정 (기본 36명, 가변성 확보)
max_students = st.number_input("학급 총 인원수 설정", min_value=1, max_value=50, value=36)

col1, col2 = st.columns([1, 1])

with col1:
    if st.button("🎲 번호 뽑기", use_container_width=True):
        # 뽑을 수 있는 번호 추출 (전체 인원 중 이미 뽑힌 번호 제외)
        available_numbers = [i for i in range(1, max_students + 1) if i not in st.session_state.drawn_numbers]
        
        if not available_numbers:
            st.warning("모든 번호가 다 뽑혔습니다! 초기화 해주세요.")
        else:
            picked = random.choice(available_numbers)
            st.session_state.drawn_numbers.append(picked)
            st.balloons() # 축하 효과
            st.success(f"🎉 오늘의 당첨 번호: **{picked}번** 입니다!")

with col2:
    if st.button("🔄 추첨 기록 초기화", use_container_width=True):
        st.session_state.drawn_numbers = []
        st.info("추첨 기록이 초기화되었습니다.")

# 뽑힌 기록 보여주기
if st.session_state.drawn_numbers:
    st.markdown(f"**현재까지 뽑힌 번호:** {', '.join(map(str, st.session_state.drawn_numbers))}")
else:
    st.markdown("*아직 뽑힌 번호가 없습니다.*")

st.markdown("---")

# 3. 두 번째 기능: [차별화] 반장의 오늘의 할 일 캘린더
st.header("📝 반장 전용 To-Do 리스트")
st.write("오늘 학급을 위해 챙겨야 할 일을 관리하세요.")

# 할 일 추가
new_todo = st.text_input("새로운 할 일 추가:", placeholder="예: 3교시 체육관 이동 안내")
if st.button("추가하기"):
    if new_todo.strip():
        st.session_state.todo_list.append(new_todo.strip())
        st.rerun()
    else:
        st.error("내용을 입력해주세요!")

# 할 일 목록 출력 및 삭제
if st.session_state.todo_list:
    for idx, todo in enumerate(st.session_state.todo_list):
        col_text, col_btn = st.columns([4, 1])
        col_text.write(f"- {todo}")
        if col_btn.button("삭제", key=f"todo_{idx}"):
            st.session_state.todo_list.pop(idx)
            st.rerun()
else:
    st.write("👍 모든 할 일을 끝냈습니다! 완벽한 반장이군요.")

st.markdown("---")

# 4. 세 번째 기능: [재미 요소] 오늘의 학급 한마디 (포춘쿠키)
st.header("🔮 오늘의 칠판 한마디 추천")
messages = [
    "“서로 배려하는 하루를 보냅시다!”",
    "“급식 질서를 잘 지키는 멋진 우리 반!”",
    "“수업 시작 1분 전, 자리에 앉아주세요!”",
    "“선생님께 예의 바르게 인사하기!”",
    "“떠들 때는 조용히, 대답할 때는 크게!”"
]

if st.button("💡 추천 문구 보기"):
    random_msg = random.choice(messages)
    st.info(f"오늘 아침 조례 때 이 말을 해보는 건 어떨까요?\n\n**{random_msg}**")
