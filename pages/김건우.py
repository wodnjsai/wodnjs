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
        bottom: 50px;
        left: 5%;
        right: 5%;
        background-color: rgba(0, 0, 0, 0.85);
        color: #ffffff;
        text-align: center;
        padding: 18px 25px;
        border-radius: 12px;
        font-size: 22px;
        font-weight: bold;
        z-index: 9999;
        box-shadow: 0px 5px 20px rgba(0,0,0,0.5);
        line-height: 1.6;
        border: 1px solid rgba(255,255,255,0.1);
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

# API 키 및 클라이언트 초기화
api_key = None
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
else:
    st.sidebar.warning("⚠️ Secrets에 GEMINI_API_KEY가 설정되지 않았습니다.")
    api_key = st.sidebar.text_input("아래에 Gemini API Key를 입력하세요:", type="password")

if api_key:
    try:
        genai.configure(api_key=api_key)
        # 안정적인 처리를 위해 기본 flash 모델 사용
        model = genai.GenerativeModel("gemini-2.5-flash")
    except Exception as e:
        st.error(f"API 인증 설정 중 오류 발생: {e}")
        st.stop()
else:
    st.info("🔑 왼쪽 사이드바에 구글 Gemini API Key를 입력하시면 서비스가 활성화됩니다.")
    st.stop()

# 오디오 입력 방식 선택
tab1, tab2 = st.tabs(["🎙️ 마이크 녹음", "📁 오디오 파일 업로드"])
audio_data = None
mime_type = "audio/wav"

with tab1:
    recorded_audio = st.audio_input("버튼을 눌러 주변 음성을 녹음하세요 (말을 마친 후 다시 눌러 녹음 완료)")
    if recorded_audio:
        audio_data = recorded_audio.read()
        mime_type = recorded_audio.type

with tab2:
    uploaded_file = st.file_uploader("오디오 파일 선택 (mp3, wav, m4a)", type=["mp3", "wav", "m4a"])
    if uploaded_file:
        audio_data = uploaded_file.read()
        mime_type = uploaded_file.type

# 음성 분석 및 자막 생성 프로세스
if audio_data:
    st.success("🎯 음성이 성공적으로 기록되었습니다. 아래 버튼을 눌러 자막을 생성하세요!")
    st.audio(audio_data, format=mime_type)
    
    generate_btn = st.button("✨ 자막 생성하기", type="primary", use_container_width=True)
    
    if generate_btn:
        with st.spinner("🤖 AI가 음성을 듣고 자막을 제작 중입니다..."):
            try:
                # 오디오 포맷 강제 매핑 안정화
                current_mime = mime_type
                if "wav" in current_mime:
                    current_mime = "audio/wav"
                elif "mp3" in current_mime:
                    current_mime = "audio/mp3"
                elif "m4a" in current_mime:
                    current_mime = "audio/m4a"

                audio_part = {
                    "mime_type": current_mime,
                    "data": audio_data
                }
                
                prompt = (
                    "너는 오디오 받아쓰기 전문가야. 오디오를 듣고 들리는 인간의 대사만 정확하게 한국어로 텍스트로 변환해줘.\n"
                    "배경 소음, 음악 소리 등은 무시하고 말소리만 번역해줘."
                )
                
                response = model.generate_content([prompt, audio_part])
                subtitle_text = response.text.strip()
                
                if not subtitle_text:
                    subtitle_text = "[음성이 인식되지 않았습니다. 더 크게 말씀해 보세요.]"
                
                # 세션 상태에 자막 저장하여 화면 유지
                st.session_state["subtitle"] = subtitle_text
                
            except Exception as e:
                st.error(f"🚨 자막 생성 실패! 오류 원인: {e}")
                st.info("팁: API 키가 올바른지, 혹은 오디오 파일이 너무 짧거나 길지 않은지 확인하세요.")

# 자막 출력부 (화면 하단 고정)
if "subtitle" in st.session_state:
    st.markdown(
        f'<div class="subtitle-container">🎬 {st.session_state["subtitle"]}</div>', 
        unsafe_allow_html=True
    )
    st.subheader("📝 자막 텍스트 결과")
    st.code(st.session_state["subtitle"], language="text")
else:
    st.markdown(
        '<div class="subtitle-container">🎙️ 음성을 입력하고 [자막 생성하기]를 누르면 이곳에 표시됩니다.</div>', 
        unsafe_allow_html=True
    )
