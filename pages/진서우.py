import streamlit as st

st.set_page_config(
    page_title="학급 투표",
    page_icon="🗳️",
    layout="centered"
)

# 상태 초기화
if "started" not in st.session_state:
    st.session_state.started = False

if "ended" not in st.session_state:
    st.session_state.ended = False

if "vote1" not in st.session_state:
    st.session_state.vote1 = 0

if "vote2" not in st.session_state:
    st.session_state.vote2 = 0

if "topic" not in st.session_state:
    st.session_state.topic = ""

if "option1" not in st.session_state:
    st.session_state.option1 = "1번"

if "option2" not in st.session_state:
    st.session_state.option2 = "2번"

st.title("🗳️ 학급 투표")

# 투표 설정
if not st.session_state.started:
    st.subheader("반장 설정")

    topic = st.text_input("투표 주제")
    option1 = st.text_input("1번 선택지", value="1번")
    option2 = st.text_input("2번 선택지", value="2번")

    if st.button("투표 시작"):
        if topic.strip() == "":
            st.error("주제를 입력하세요.")
        else:
            st.session_state.topic = topic
            st.session_state.option1 = option1
            st.session_state.option2 = option2
            st.session_state.started = True
            st.rerun()

# 투표 화면
if st.session_state.started and not st.session_state.ended:
    st.header(f"📌 {st.session_state.topic}")

    col1, col2 = st.columns(2)

    with col1:
        if st.button(f"1️⃣ {st.session_state.option1}"):
            st.session_state.vote1 += 1

    with col2:
        if st.button(f"2️⃣ {st.session_state.option2}"):
            st.session_state.vote2 += 1

    st.divider()

    st.subheader("현재 투표 수")
    st.write(f"{st.session_state.option1}: {st.session_state.vote1}표")
    st.write(f"{st.session_state.option2}: {st.session_state.vote2}표")

    if st.button("투표 종료"):
        st.session_state.ended = True
        st.rerun()

# 결과 화면
if st.session_state.ended:
    st.header("🏆 투표 결과")

    st.write(f"{st.session_state.option1}: {st.session_state.vote1}표")
    st.write(f"{st.session_state.option2}: {st.session_state.vote2}표")

    if st.session_state.vote1 > st.session_state.vote2:
        st.success(
            f"승리: {st.session_state.option1}"
        )

    elif st.session_state.vote2 > st.session_state.vote1:
        st.success(
            f"승리: {st.session_state.option2}"
        )

    else:
        st.info("동점입니다!")

    if st.button("새 투표 만들기"):
        st.session_state.started = False
        st.session_state.ended = False
        st.session_state.vote1 = 0
        st.session_state.vote2 = 0
        st.session_state.topic = ""
        st.session_state.option1 = "1번"
        st.session_state.option2 = "2번"
        st.rerun()
