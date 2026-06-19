import streamlit as st
import random
import pandas as pd
from io import StringIO

st.set_page_config(
    page_title="반장 도우미 - 청소구역 배정기",
    page_icon="🧹",
    layout="centered"
)

st.title("🧹 반장 도우미")
st.subheader("청소구역 랜덤 배정기")

st.markdown("""
학생 명단과 청소구역을 입력하면 랜덤으로 배정합니다.

예시 학생:
- 김민수
- 이서준
- 박지호

예시 청소구역:
- 교실 바닥
- 복도
- 창문
- 분리수거
""")

student_text = st.text_area(
    "학생 명단 (한 줄에 한 명)",
    height=200,
    placeholder="김민수\n이서준\n박지호"
)

area_text = st.text_area(
    "청소구역 (한 줄에 하나)",
    height=150,
    placeholder="교실 바닥\n복도\n창문\n분리수거"
)

if st.button("🎲 랜덤 배정하기", type="primary"):

    try:
        students = [
            s.strip()
            for s in student_text.splitlines()
            if s.strip()
        ]

        areas = [
            a.strip()
            for a in area_text.splitlines()
            if a.strip()
        ]

        if len(students) == 0:
            st.error("학생 명단을 입력해주세요.")
            st.stop()

        if len(areas) == 0:
            st.error("청소구역을 입력해주세요.")
            st.stop()

        random.shuffle(students)

        assignments = []

        for i, student in enumerate(students):
            area = areas[i % len(areas)]
            assignments.append(
                {
                    "학생": student,
                    "청소구역": area
                }
            )

        df = pd.DataFrame(assignments)

        st.success("배정 완료!")

        st.subheader("📋 배정 결과")
        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )

        area_summary = {}

        for area in areas:
            assigned_students = df[
                df["청소구역"] == area
            ]["학생"].tolist()

            area_summary[area] = ", ".join(assigned_students)

        summary_df = pd.DataFrame(
            {
                "청소구역": list(area_summary.keys()),
                "담당 학생": list(area_summary.values())
            }
        )

        st.subheader("🏫 구역별 담당 학생")
        st.table(summary_df)

        csv = df.to_csv(index=False).encode("utf-8-sig")

        st.download_button(
            label="📥 CSV 다운로드",
            data=csv,
            file_name="cleaning_assignment.csv",
            mime="text/csv"
        )

    except Exception as e:
        st.error(f"오류가 발생했습니다: {e}")

st.divider()

st.caption("반장이 쉽고 공정하게 청소구역을 배정할 수 있는 도우미 앱")
