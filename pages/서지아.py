import streamlit as st
import random

st.set_page_config(
    page_title="반장 도우미",
    page_icon="🎓",
    layout="centered"
)

st.title("🎓 반장 도우미")
st.write("자리 뽑기 룰렛으로 새로운 자리를 정해보세요!")

# 세션 상태 초기화
if "students" not in st.session_state:
    st.session_state.students = []

if "result" not in st.session_state:
    st.session_state.result = {}

# 학생 입력
st.header("1️⃣ 학생 명단 입력")

student_text = st.text_area(
    "학생 이름을 한 줄에 한 명씩 입력하세요",
    height=200,
    placeholder="""김민수
이서연
박지훈
최유진"""
)

# 명단 저장
if st.button("명단 저장"):
    try:
        students = [
            name.strip()
            for name in student_text.split("\n")
            if name.strip()
        ]

        if len(students) < 2:
            st.warning("학생을 2명 이상 입력해주세요.")
        else:
            st.session_state.students = students
            st.success(f"{len(students)}명의 학생이 저장되었습니다.")

    except Exception as e:
        st.error(f"오류 발생: {e}")

st.divider()

# 자리 뽑기
st.header("2️⃣ 자리 뽑기 룰렛")

if st.session_state.students:

    cols = st.number_input(
        "한 줄에 몇 자리씩 배치할까요?",
        min_value=1,
        max_value=10,
        value=4
    )

    if st.button("🎲 자리 뽑기 시작"):

        try:
            shuffled = st.session_state.students.copy()
            random.shuffle(shuffled)

            result = {}
            seat_num = 1

            for student in shuffled:
                result[seat_num] = student
                seat_num += 1

            st.session_state.result = result

        except Exception as e:
            st.error(f"자리 뽑기 중 오류 발생: {e}")

    if st.session_state.result:

        st.subheader("📍 배정 결과")

        seats = list(st.session_state.result.items())

        rows = [
            seats[i:i + cols]
            for i in range(0, len(seats), cols)
        ]

        for row in rows:
            columns = st.columns(len(row))

            for col, (seat, student) in zip(columns, row):
                col.metric(
                    label=f"{seat}번 자리",
                    value=student
                )

        st.divider()

        st.subheader("📋 전체 결과")

        for seat, student in st.session_state.result.items():
            st.write(f"{seat}번 자리 : {student}")

else:
    st.info("먼저 학생 명단을 저장해주세요.")

st.divider()

st.caption("반장 도우미 앱 | Streamlit Community Cloud 배포용")
