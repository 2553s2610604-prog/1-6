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

if "topic" not in st.session_state:
    st.session_state.topic = ""

if "options" not in st.session_state:
    st.session_state.options = []

if "votes" not in st.session_state:
    st.session_state.votes = []

st.title("🗳️ 학급 투표")

# 설정 화면
if not st.session_state.started:

    st.subheader("반장 설정")

    topic = st.text_input("투표 주제")

    num_options = st.number_input(
        "선택지 개수",
        min_value=2,
        max_value=20,
        value=2
    )

    options = []

    for i in range(num_options):
        option = st.text_input(
            f"선택지 {i+1}",
            key=f"option_{i}"
        )
        options.append(option)

    if st.button("투표 시작"):

        if topic.strip() == "":
            st.error("주제를 입력하세요.")

        elif any(opt.strip() == "" for opt in options):
            st.error("모든 선택지를 입력하세요.")

        else:
            st.session_state.topic = topic
            st.session_state.options = options
            st.session_state.votes = [0] * len(options)
            st.session_state.started = True
            st.rerun()

# 투표 화면
if st.session_state.started and not st.session_state.ended:

    st.header(f"📌 {st.session_state.topic}")

    st.write("원하는 선택지를 눌러 투표하세요.")

    cols = st.columns(2)

    for i, option in enumerate(st.session_state.options):

        with cols[i % 2]:
            if st.button(option, key=f"vote_{i}"):
                st.session_state.votes[i] += 1

    st.divider()

    st.info("투표 수는 결과 발표 전까지 공개되지 않습니다.")

    if st.button("투표 종료"):
        st.session_state.ended = True
        st.rerun()

# 결과 화면
if st.session_state.ended:

    st.header("🏆 투표 결과")

    max_vote = max(st.session_state.votes)

    winners = []

    for option, vote in zip(
        st.session_state.options,
        st.session_state.votes
    ):
        st.write(f"**{option}** : {vote}표")

        if vote == max_vote:
            winners.append(option)

    st.divider()

    if len(winners) == 1:
        st.success(f"우승: {winners[0]}")
    else:
        st.info(
            "동점: " + ", ".join(winners)
        )

    if st.button("새 투표 만들기"):

        st.session_state.started = False
        st.session_state.ended = False
        st.session_state.topic = ""
        st.session_state.options = []
        st.session_state.votes = []

        st.rerun()
