# 제작: 김건우, 김율언, 황지우
import streamlit as st
import google.generativeai as genai
import time

# Page 설정
st.set_page_config(
    page_title="AI 실시간 자동 자막기",
    page_icon="🎬",
    layout="centered"
)

# 화면 하단 자막 바 및 애니메이션 CSS
st.markdown("""
    <style>
    .subtitle-container {
        position: fixed;
        bottom: 50px;
        left: 5%;
        right: 5%;
        background-color: rgba(0, 0, 0, 0.85);
        color: #ffffff;
        text-align: center;
        padding: 18px 25px;
        border-radius: 12px;
        font-size: 24px;
        font-weight: bold;
        z-index: 9999;
        box-shadow: 0px 5px 25px rgba(0,0,0,0.6);
        line-height: 1.6;
        border: 2px solid #FF4B4B;
    }
    .main-title {
        text-align: center;
        color: #FF4B4B;
    }
    .status-text {
        text-align: center;
        font-weight: bold;
        color: #2e7d32;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='main-title'>🎬 AI 실시간 자동 자막 시스템</h1>", unsafe_allow_html=True)
st.write("주변 음성을 주기적으로 감지하여 하단에 실시간 스타일로 자막을 업데이트합니다.")
st.markdown("---")

# API 키 설정
api_key = None
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
else:
    api_key = st.sidebar.text_input("Gemini API Key를 입력하세요:", type="password")

if not api_key:
    st.info("🔑 API Key를 등록하시면 실시간 자막 시스템이 활성화됩니다.")
    st.stop()

# Gemini 세팅
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-2.5-flash")

# 세션 상태 초기화 (자막 기억용)
if "live_subtitle" not in st.session_state:
    st.session_state["live_subtitle"] = "🎙️ 음성 입력을 대기 중입니다..."

# 실시간 자막 작동 스위치
st.subheader("⚙️ 자막 제어 판넬")
live_active = st.toggle("🔴 실시간 자동 자막 활성화 (토글 스위치)", value=False)

if live_active:
    st.markdown("<p class='status-text'>🔄 실시간 자막 시스템이 가동 중입니다. 아래 마이크에 대고 말씀하세요!</p>", unsafe_allow_html=True)
    
    # 1. 오디오 입력 받기
    recorded_audio = st.audio_input("주변 소리 녹음 (말을 하고 완료되면 자동으로 변환됩니다)")
    
    if recorded_audio:
        audio_data = recorded_audio.read()
        mime_type = recorded_audio.type
        
        with st.spinner("🤖 AI 가 실시간 음성 분석 중..."):
            try:
                # API 데이터 정제
                audio_part = {
                    "mime_type": "audio/wav" if "wav" in mime_type else mime_type,
                    "data": audio_data
                }
                
                prompt = (
                    "너는 실시간 자막 방송 속기사야. 소리를 듣고 소음은 무시한 채 오직 '인간의 말소리(대사)'만 "
                    "군더더기 없이 정확한 한국어 문장으로 받아쓰기해줘. 설명이나 해설은 절대 쓰지 마."
                )
                
                # Gemini 처리 요청
                response = model.generate_content([prompt, audio_part])
                result_text = response.text.strip()
                
                if result_text:
                    st.session_state["live_subtitle"] = result_text
                else:
                    st.session_state["live_subtitle"] = "[음성 감지 없음]"
                    
            except Exception as e:
                st.session_state["live_subtitle"] = f"[오류 발생: {e}]"
else:
    st.info("💡 위 토글 스위치를 켜면 실시간 자막 모드가 시작됩니다.")
    st.session_state["live_subtitle"] = "⏸️ 자막 시스템 정지됨"

# 🎬 최하단 자막 컴포넌트 강제 노출
st.markdown(
    f'<div class="subtitle-container">🎬 {st.session_state["live_subtitle"]}</div>', 
    unsafe_allow_html=True
)

# 자막 로그 기록 대시보드
st.subheader("📝 자막 로그 리포트")
st.chat_message("assistant").write(st.session_state["live_subtitle"])
