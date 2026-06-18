import streamlit as st
import google.generativeai as genai

# =================================================================
# 1. 페이지 초기 설정
# =================================================================
st.set_page_config(
    page_title="AI 음성 자동 자막 생성기", 
    page_icon="🎙️", 
    layout="wide"
)

# =================================================================
# 2. 하단 자막용 CSS 스타일 정의
# =================================================================
css_style = """
<style>
.subtitle-container {
    position: fixed;
    left: 0;
    bottom: 0;
    width: 100%;
    background-color: rgba(0, 0, 0, 0.85);
    color: #ffffff;
    text-align: center;
    padding: 25px;
    font-size: 26px;
    font-weight: bold;
    z-index: 9999;
    border-top: 4px solid #FF4B4B;
    font-family: 'Malgun Gothic', sans-serif;
}
.main-content {
    margin-bottom: 180px;
}
</style>
"""
st.markdown(css_style, unsafe_allow_html=True)

# 메인 콘텐츠 레이아웃 시작
st.markdown('<div class="main-content">', unsafe_allow_html=True)

# =================================================================
# 3. 타이틀 영역
# =================================================================
st.title("🎙️ AI 음성 자동 자막 시스템")
st.caption("외부 소리를 녹음하거나 음성 파일을 업로드하면 AI가 자동으로 한글 자막을 생성합니다.")
st.write("---")

# =================================================================
# 4. API 인증 및 환경 검증
# =================================================================
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
else:
    st.error("⚠️ Secrets에 GEMINI_API_KEY가 설정되지 않았습니다. Streamlit Cloud 설정에서 추가해주세요.")
    st.stop()

# =================================================================
# 5. 오디오 입력 처리 (UI 및 데이터 로드)
# =================================================================
col1, col2 = st.columns([1, 1])
audio_bytes = None

with col1:
    st.subheader("📥 음성 입력")
    input_method = st.radio("음성 입력 방식을 선택하세요:", ["오디오 파일 업로드", "직접 마이크 녹음"])
    
    if input_method == "오디오 파일 업로드":
        uploaded_file = st.file_uploader(
            "음성 파일을 선택하세요 (mp3, wav, m4a, ogg 등)", 
            type=["mp3", "wav", "m4a", "ogg"]
        )
        if uploaded_file is not None:
            audio_bytes = uploaded_file.read()
            st.audio(audio_bytes, format="audio/mp3")
    else:
        recorded_file = st.audio_input("마이크 버튼을 눌러 소리를 녹음하세요")
        if recorded_file is not None:
            audio_bytes = recorded_file.read()

# =================================================================
# 6. Gemini API 연동 및 자막 생성 처리
# =================================================================
subtitles_text = ""

if audio_bytes is not None:
    with col1:
        generate_btn = st.button("✨ 자동 한글 자막 생성 시작", type="primary", use_container_width=True)
    
    if generate_btn:
        with st.spinner("AI가 음성을 분석하여 자막을 만들고 있습니다..."):
            try:
                # 최신 경량 모델 호출
                model = genai.GenerativeModel("gemini-2.5-flash-lite")
                
                audio_data = {
                    "mime_type": "audio/mp3",
                    "data": audio_bytes
                }
                
                prompt = (
                    "주어진 오디오 음성을 듣고 정확한 한국어 자막(텍스트)으로 변환해줘. "
                    "배경음이나 소음은 제외하고 말소리만 자연스러운 문장으로 받아써줘. "
                    "아무런 부연 설명 없이 오직 자막 내용만 출력해줘."
                )
                
                response = model.generate_content([prompt, audio_data])
                subtitles_text = response.text.strip()
                
                with col2:
                    st.success("✅ 자막 변환 완료!")
                    
            except Exception as e:
                st.error(f"❌ API 호출 중 오류가 발생했습니다: {e}")
else:
    with col1:
        st.info("💡 음성 파일을 업로드하거나 마이크로 녹음하면 자막 생성이 시작됩니다.")

# =================================================================
# 7. 화면 출력 및 최종 렌더링
# =================================================================
with col2:
    st.subheader("📝 전체 스크립트 보기")
    if subtitles_text:
        st.text_area("변
