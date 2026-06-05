import streamlit as st
from google import genai
from google.genai import types
from google.genai.errors import APIError

# 1. 페이지 설정 및 제목
st.set_page_config(page_title="오늘 뭐 먹지? 🤖", page_icon="🍔", layout="centered")
st.title("🍔 오늘 뭐 먹지? 음식 추천 챗봇")
st.write("오늘 뭘 먹을지 고민이신가요? 취향, 기분, 또는 상황을 말씀해주시면 딱 맞는 음식을 추천해 드려요!")

# 2. Streamlit Secrets에서 API 키 불러오기 및 클라이언트 초기화
# Streamlit Community Cloud에 배포 시 설정한 Secret 값을 자동으로 가져옵니다.
if "GEMINI_API_KEY" not in st.secrets:
    st.error("Secrets에 'GEMINI_API_KEY'가 설정되지 않았습니다. Streamlit 대시보드에서 설정해주세요.")
    st.stop()

@st.cache_resource
def get_gemini_client():
    # google-genai SDK의 클라이언트를 초기화합니다.
    return genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

client = get_gemini_client()

# 3. 세션 상태(Session State)로 채팅 기록 유지
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "안녕하세요! 오늘 어떤 음식을 찾으시나요? (예: '매콤하고 국물 있는 거 추천해줘', '다이어트 중인데 가벼운 점심 메뉴 알려줘')"
        }
    ]

# 4. 기존 채팅 기록 화면에 표시
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# 5. 사용자 입력 처리
if user_input := st.chat_input("당신의 입맛이나 현재 기분을 알려주세요!"):
    # 사용자 메시지를 화면에 표시 및 세션에 저장
    with st.chat_message("user"):
        st.write(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    # 챗봇 응답 생성
    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        with st.spinner("🤖 맛있는 메뉴를 고민하는 중..."):
            try:
                # 챗봇에게 페르소나 부여 (시스템 지침 설정)
                system_instruction = (
                    "당신은 친절하고 위트 있는 음식 추천 전문가입니다. "
                    "사용자의 요구사항(기분, 날씨, 예산 등)을 분석하여 "
                    "구체적인 음식 메뉴와 그렇게 추천한 이유를 맛있게 설명해주세요."
                )

                # 최신 google-genai SDK 방식으로 gemini-2.5-flash-lite 호출
                response = client.models.generate_content(
                    model='gemini-2.5-flash-lite',
                    contents=user_input,
                    config=types.GenerateContentConfig(
                        system_instruction=system_instruction,
                        temperature=0.7,
                    )
                )
                
                # 응답 검증 및 예외 처리
                if response.text:
                    ai_response = response.text
                    response_placeholder.write(ai_response)
                    # 세션에 AI 응답 저장
                    st.session_state.messages.append({"role": "assistant", "content": ai_response})
                else:
                    error_msg = "죄송합니다. 답변을 생성하지 못했습니다. 다시 시도해주세요."
                    response_placeholder.error(error_msg)
                    st.session_state.messages.append({"role": "assistant", "content": error_msg})

            except APIError as e:
                # Gemini API 관련 오류 처리
                error_msg = f"Gemini API 오류가 발생했습니다: {e.message}"
                response_placeholder.error(error_msg)
            except Exception as e:
                # 기타 일반 오류 처리
                error_msg = f"예상치 못한 오류가 발생했습니다: {str(e)}"
                response_placeholder.error(error_msg)
