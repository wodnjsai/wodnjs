# 제작: 김건우, 김율언, 황지우
import streamlit as st
import google.generativeai as genai

# Page 설정
st.set_page_config(
    page_title="AI 자동 자막 생성기",
    page_icon="🎬",
    layout="centered"
)

# 기본 CSS 스타일링 (화면 하단 자막 바 구현)
st.markdown("""
    <style>
    .subtitle-container {
        position: fixed;
        bottom: 40px;
        left: 5%;
        right: 5%;
        background-color: rgba(0, 0, 0, 0.75);
        color: #ffffff;
        text-align: center;
        padding: 15px 25px;
        border-radius: 10px;
        font-size: 20px;
        font-weight: 500;
        z-index: 9999;
        box-shadow: 0px 4px 15px rgba(0,0,0,0.3);
        line-height: 1.5;
    }
    .main-title {
        text-align: center;
        color: #FF4B4B;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='main-title'>🎬 AI 실시간 자동 자막 생성기</h1>", unsafe_allow_html=True)
st.write("외부에서 들리는 음성을 녹음하거나 오디오 파일을 업로드하세요. Gemini AI가 하단에 자막을 생성합니다.")
st.markdown("---")

# API 키 및 클라이언트 초기화 (예외 처리)
try:
    if "GEMINI_API_KEY" in st.secrets:
        api_key = st.secrets["GEMINI_API_KEY"]
    else:
        st.info("💡 배포 전 로컬 테스트 중이시라면 사이드바에 API 키를 입력하세요.")
        api_key = st.sidebar.text_input("Gemini API Key", type="password")

    if api_key:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-2.5-flash-lite")
    else:
        st.warning("🔑 Gemini API Key가 필요합니다. Secrets 설정 또는 사이드바 입력을 확인해주세요.")
        st.stop()
except Exception as e:
    st.error(f"초기화 중 오류 발생: {e}")
    st.stop()

# 오디오 입력 방식 선택
tab1, tab2 = st.tabs(["🎙️ 마이크 녹음", "📁 오디오 파일 업로드"])
audio_data = None
mime_type = "audio/wav"

with tab1:
    recorded_audio = st.audio_input("여기를 눌러 주변 음성을 녹음하세요")
    if recorded_audio:
        audio_data = recorded_audio.read()
        mime_type = recorded_audio.type

with tab2:
    uploaded_file = st.file_uploader("오디오 파일 선택 (mp3, wav, m4a) ", type=["mp3", "wav", "m4a"])
    if uploaded_file:
        audio_data = uploaded_file.read()
        mime_type = uploaded_file.type

# 음성 분석 및 자막 생성 프로세스
if audio_data:
    st.success("🎯 음성 데이터가 성공적으로 수신되었습니다!")
    st.audio(audio_data, format=mime_type)
    
    generate_btn = st.button("✨ 자막 생성하기", type="primary", use_container_width=True)
    
    if generate_btn:
        with st.spinner("🤖 AI가 음성을 분석하여 자막을 생성하는 중입니다..."):
            try:
                audio_part = {
                    "mime_type": mime_type,
                    "data": audio_data
                }
                
                prompt = (
                    "너는 전문 자막 제작자야. 제공된 오디오를 듣고 받아쓰기를 해줘.\n"
                    "규칙:\n"
                    "1. 배경음이나 소음 설명은 제외하고, 들리는 말(대사)만 정확히 텍스트로 변환할 것.\n"
                    "2. 가급적 자연스러운 문장 단위로 작성할 것.\n"
                    "3. 오디오에 아무 소리도 없거나 대사가 없다면 '[음성 없음]'이라고만 출력할 것."
                )
                
                response = model.generate_content([prompt, audio_part])
                subtitle_text = response.text.strip()
                
                st.markdown(
                    f'<div class="subtitle-container">🎬 {subtitle_text}</div>', 
                    unsafe_allow_html=True
                )
                
                st.subheader("📝 생성된 자막 기록")
                st.info(subtitle_text)
                
            except Exception as e:
                st.error(f"자막 생성 중 오류가 발생했습니다. 다시 시도해주세요.\n오류 내용: {e}")
else:
    st.markdown(
        '<div class="subtitle-container">🎙️ 오디오를 입력하면 이곳에 자막이 표시됩니다.</div>', 
        unsafe_allow_html=True
    )
