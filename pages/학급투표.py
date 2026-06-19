import streamlit as st
import math

st.set_page_config(
    page_title="학급 투표",
    page_icon="🗳️",
    layout="wide"
)

# 배경 및 버튼 스타일
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #74ebd5, #ACB6E5);
}

h1, h2, h3 {
    text-align: center;
}

div.stButton > button {
    width: 100%;
    height: 200px;
    font-size: 28px;
    font-weight: bold;
    border-radius: 20px;
}
</style>
""", unsafe_allow_html=True)

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

# -------------------
# 설정 화면
# -------------------
if not st.session_state.started:

    st.subheader("반장 설정")

    topic = st.text_input("투표 주제")

    num_options = st.number_input(
        "선택지 개수",
        min_value=2,
        max_value=20,
        value=2,
        step=1
    )

    options = []

    for i in range(num_options):
        option = st.text_input(
            f"선택지 {i+1}",
            key=f"option_{i}"
        )
        options.append(option)

    if st.button("투표 시작", use_container_width=True):

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

# -------------------
# 투표 화면
# -------------------
elif not st.session_state.ended:

    st.header(st.session_state.topic)

    total_votes = sum(st.session_state.votes)

    st.info(f"현재 투표 인원: {total_votes}명")

    count = len(st.session_state.options)

    if count <= 2:
        cols_per_row = 2
    elif count <= 4:
        cols_per_row = 2
    elif count <= 8:
        cols_per_row = 4
    else:
        cols_per_row = math.ceil(math.sqrt(count))

    for start in range(0, count, cols_per_row):

        cols = st.columns(cols_per_row)

        for c in range(cols_per_row):

            idx = start + c

            if idx >= count:
                continue

            with cols[c]:

                if st.button(
                    st.session_state.options[idx],
                    key=f"vote_{idx}",
                    use_container_width=True
                ):
                    st.session_state.votes[idx] += 1
                    st.rerun()

    st.warning("투표 수는 결과 발표 전까지 공개되지 않습니다.")

    if st.button(
        "투표 종료",
        type="primary",
        use_container_width=True
    ):
        st.session_state.ended = True
        st.rerun()

# -------------------
# 결과 화면
# -------------------
else:

    st.header("🏆 투표 결과")

    total_votes = sum(st.session_state.votes)

    st.subheader(f"총 투표 인원: {total_votes}명")

    if total_votes == 0:
        st.warning("투표가 없습니다.")
    else:

        max_vote = max(st.session_state.votes)

        winners = []

        for option, vote in zip(
            st.session_state.options,
            st.session_state.votes
        ):

            percent = (vote / total_votes) * 100

            st.write(
                f"{option} : {vote}표 ({percent:.1f}%)"
            )

            if vote == max_vote:
                winners.append(option)

        if len(winners) == 1:
            st.success(f"🏆 우승: {winners[0]}")
        else:
            st.info("동점: " + ", ".join(winners))

    if st.button(
        "새 투표 만들기",
        use_container_width=True
    ):
        st.session_state.started = False
        st.session_state.ended = False
        st.session_state.topic = ""
        st.session_state.options = []
        st.session_state.votes = []
        st.rerun()
