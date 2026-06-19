import streamlit as st
import random
import pandas as pd

# 1. 페이지 기본 설정
st.set_page_config(
    page_title="우리 반 질서 수호자",
    page_icon="🛡️",
    layout="wide"
)

# 2. Session State (데이터 초기화)
if "noisy_students" not in st.session_state:
    st.session_state.noisy_students = {}

if "notices" not in st.session_state:
    st.session_state.notices = ["1. 내일 수학 수행평가 준비물 챙기기", "2. 급식 질서 지키기"]

# 멘탈 케어 메시지 저장소 초기화
if "mental_msg" not in st.session_state:
    st.session_state.mental_msg = "아직 치료제를 복용하지 않았습니다. 아래 버튼을 눌러보세요!"

# 멘탈 케어 메시지 풀
MENTAL_MESSAGES = [
    "반장님, 오늘도 정말 고생이 많아요! 👏👏",
    "교실이 시끄러운 건 여러분 탓이 아닙니다. 힘내세요! 🔥",
    "이 또한 지나가리라... 졸업이 머지않았습니다! 🎓",
    "쉬는 시간에 매점 가서 초코우유 하나 때리세요! 🧃",
    "선생님은 언제나 반장 편이랍니다. 👍"
]

# --- 메인 화면 레이아웃 ---

st.title("🛡️ 우당탕탕 우리 반 질서 수호자")
st.caption("수업 질서를 지키기 위한 반장 전용 시크릿 대시보드")
st.markdown("---")

# 🌟 [오류 완전 해결] 이름은 지우고, 내부 파일 매핑으로 정상 이동 구현
st.subheader("👥 우리 반 맞춤형 학급 기능 바로가기")
st.info("💡 버튼을 누르면 해당 기능 페이지로 즉시 이동합니다.")

# 실제 pages 폴더 안의 파일명과 1:1 매칭 (이름 노출 제거)
menu_items = [
    {"file": "김건우", "label": "🪑 번호 추첨"},
    {"file": "서지아", "label": "📝 출석 확인"},
    {"file": "이상훈", "label": "🧹 청소구역 정하기"},
    {"file": "학급투표", "label": "🗳️ 학급 투표"}
]

# 4개의 칸(Column)을 만들어 가로로 정렬
member_cols = st.columns(len(menu_items))

for i, item in enumerate(menu_items):
    with member_cols[i]:
        st.page_link(f"pages/{item['file']}.py", label=item['label'], use_container_width=True)

st.markdown("---")

# 왼쪽 사이드바: 교실 상태 컨트롤러
with st.sidebar:
    st.header("🚨 현재 교실 상태 설정")
    classroom_status = st.radio(
        "교실 분위기를 선택하세요:",
        ("🟢 평화로움 (수업 집중)", "🟡 웅성웅성 (쉬는 시간 수준)", "🔴 폭발 직전 (시장바닥)"),
        index=0
    )
    
    st.markdown("---")
    st.header("🧼 오늘의 주번 점검")
    st.success("오늘의 주번: **김철수, 이영희**")
    st.info("🧹 청소 상태: 양호")

# 메인 화면 2분할 (Left: 단속반, Right: 전달사항 및 멘탈케어)
col1, col2 = st.columns([3, 2])

with col1:
    st.subheader("📢 실시간 소란 학생 단속 목록")
    
    # 학생 추가 입력 폼
    with st.form("add_student_form", clear_on_submit=True):
        student_name = st.text_input("떠드는 학생 이름을 입력하세요:", placeholder="예: 홍길동")
        submit_btn = st.form_submit_button("🚨 블랙리스트 추가/경고")
        
        if submit_btn:
            if student_name.strip() == "":
                st.warning("이름을 입력해주세요!")
            else:
                name = student_name.strip()
                if name in st.session_state.noisy_students:
                    st.session_state.noisy_students[name] += 1
                else:
                    st.session_state.noisy_students[name] = 1
                st.success(f"[{name}] 학생에게 경고를 1회 누적했습니다.")

    # 단속 목록 출력
    if st.session_state.noisy_students:
        st.markdown("#### 📉 누적 적발 현황")
        
        df = pd.DataFrame(
            list(st.session_state.noisy_students.items()), 
            columns=["학생 이름", "경고 횟수"]
        ).sort_values(by="경고 횟수", ascending=False)
        
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        st.markdown("##### 😇 반장의 자비 (경고 리셋)")
        reset_name = st.selectbox("리셋할 학생 선택:", ["선택하세요"] + list(st.session_state.noisy_students.keys()))
        if st.button("경고 초기화") and reset_name != "선택하세요":
            del st.session_state.noisy_students[reset_name]
            st.rerun()
            
        if st.button("🗑️ 전체 목록 초기화 (종례 시간)"):
            st.session_state.noisy_students = {}
            st.success("클린한 교실이 되었습니다!")
            st.rerun()
    else:
        st.info("🎉 현재 교실이 매우 조용합니다! 평화 유지 중...")

with col2:
    # 1. 교실 상태 알림창
    st.subheader("📊 교실 분위기 모니터")
    if "🟢" in classroom_status:
        st.balloons()
        st.success("🕊️ 교실이 아주 평화롭습니다. 이대로만 갑시다!")
    elif "🟡" in classroom_status:
        st.warning("⚠️ 조금씩 시끄러워지고 있습니다. 주의를 주세요!")
    elif "🔴" in classroom_status:
        st.error("💥 시장바닥입니다! 교탁을 탁! 탁! 치거나 선생님을 모셔오세요!")

    st.markdown("---")

    # 2. 알림장 및 전달사항
    st.subheader("📝 오늘 공지사항")
    for notice in st.session_state.notices:
        st.write(notice)
        
    new_notice = st.text_input("추가할 공지사항:", placeholder="예: 5교시 체육관으로 이동")
    if st.button("공지 추가") and new_notice.strip() != "":
        st.session_state.notices.append(f"- {new_notice.strip()}")
        st.rerun()

    st.markdown("---")

    # 3. 반장 멘탈 케어 존 
    st.subheader("🧘 반장 멘탈 케어 힐링존")
    st.write("질서 지키느라 지친 반장님, 버튼을 눌러 위로를 받으세요.")
    
    if st.button("💖 멘탈 치료제 복용"):
        st.session_state.mental_msg = random.choice(MENTAL_MESSAGES)
        st.rerun()
        
    st.info(st.session_state.mental_msg)
