import streamlit as st
from google import genai
from google.genai import types
from google.genai.errors import APIError

# 페이지 설정
st.set_page_config(page_title="오성고 급식 챗봇", page_icon="🍱", layout="centered")
st.title("🍱 오성고등학교 급식 안내 챗봇")
st.caption("오성고의 맛있는 급식 메뉴를 물어보세요! (예: 오늘 점심 뭐야?, 내일 급식 알려줘)")

# 1. Streamlit Secrets에서 API 키 로드 및 클라이언트 초기화
if "GEMINI_API_KEY" not in st.secrets:
    st.error("Streamlit Secrets에 'GEMINI_API_KEY'가 설정되지 않았습니다. 배포 설정을 확인해주세요.")
    st.stop()

try:
    client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
except Exception as e:
    st.error(f"Gemini 클라이언트 초기화 중 오류가 발생했습니다: {e}")
    st.stop()

# 2. 채팅 기록 세션 상태(Session State) 초기화
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "안녕하세요! 오성고등학교 급식 안내 챗봇입니다. 무엇을 도와드릴까요?"}
    ]

# 3. 기존 채팅 기록 화면에 표시
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 4. 사용자 입력 받기
if user_input := st.chat_input("오늘 급식 메뉴가 뭐야?"):
    # 사용자 메시지 추가 및 화면 표시
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # 5. 모델 답변 생성 및 오류 처리
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown("🔄 메뉴판 확인 중...")
        
        try:
            # 급식 답변에 최적화된 페르소나 부여 (System Instruction)
            system_instruction = (
                "당신은 오성고등학교의 친절하고 유쾌한 급식 안내 AI 비서입니다. "
                "사용자가 급식 메뉴를 물어보면 친절하게 답변해주세요. "
                "만약 오늘 날짜의 실제 정확한 급식 데이터를 모른다면, "
                "솔직하게 실시간 급식 정보를 가져오지 못했다고 안내하고 나이스(NEIS) 급식 정보 등을 확인하라고 권유하세요. "
                "답변할 때는 이모지를 적절히 섞어서 학생들에게 말하듯 친근하게 해주세요."
            )

            # API 호출 (gemini-2.5-flash-lite 모델 사용)
            response = client.models.generate_content(
                model='gemini-2.5-flash-lite',
                contents=user_input,
                config=types.GenerateContentConfig(
                    system_instruction=system_instruction,
                    temperature=0.7,
                )
            )
            
            # 답변 출력 및 세션 저장
            answer = response.text
            message_placeholder.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})

        except APIError as ae:
            # Gemini API 자체 오류 처리
            error_msg = f"❌ Gemini API 오류가 발생했습니다: {ae.message}"
            message_placeholder.markdown(error_msg)
        except Exception as e:
            # 기타 일반 오류 처리
            error_msg = f"⚠️ 예상치 못한 오류가 발생했습니다: {str(e)}"
            message_placeholder.markdown(error_msg)
