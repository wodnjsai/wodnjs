import streamlit as st

# 페이지 설정
st.set_page_config(
    page_title="HearConnect",
    page_icon="🦻",
    layout="wide"
)

# ------------------
# CSS
# ------------------
st.markdown("""
<style>

.main-title{
    text-align:center;
    font-size:50px;
    font-weight:bold;
    color:#1976D2;
}

.sub-title{
    text-align:center;
    font-size:20px;
    color:gray;
}

.card{
    padding:20px;
    border-radius:15px;
    background-color:#F7F9FC;
    border:1px solid #DDE5ED;
    text-align:center;
    margin-bottom:20px;
}

.big-box{
    padding:25px;
    border-radius:15px;
    background-color:#EEF6FF;
    border-left:6px solid #1976D2;
}

.footer{
    text-align:center;
    color:gray;
    margin-top:30px;
}

</style>
""", unsafe_allow_html=True)

# ------------------
# 헤더
# ------------------
st.markdown(
    '<div class="main-title">🦻 HearConnect</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="sub-title">청각 장애인을 위한 통합 지원 플랫폼</div>',
    unsafe_allow_html=True
)

st.write("")

st.markdown("""
<div class="big-box">
<h3>환영합니다!</h3>

HearConnect는 청각 장애인의 일상생활을 지원하기 위한 통합 플랫폼입니다.

아래 서비스 버튼을 눌러 팀원들이 개발한 기능으로 이동할 수 있습니다.
</div>
""", unsafe_allow_html=True)

st.write("")
st.divider()

# ------------------
# 서비스 이동
# ------------------
st.header("🚀 주요 서비스")

col1, col2, col3 = st.columns(3)

# 팀원 앱 URL 입력
AUTO_CAPTION_URL = "https://your-auto-caption-app.streamlit.app"
SOS_URL = "https://your-sos-app.streamlit.app"
SOUND_ALERT_URL = "https://your-sound-alert-app.streamlit.app"

with col1:
    st.markdown("""
    <div class="card">
    <h3>🎤 자동 자막</h3>
    음성을 실시간 자막으로 변환하는 서비스
    </div>
    """, unsafe_allow_html=True)

    st.link_button(
        "자동 자막 페이지 이동",
        AUTO_CAPTION_URL,
        use_container_width=True
    )

with col2:
    st.markdown("""
    <div class="card">
    <h3>🚨 SOS 구조 요청</h3>
    긴급 상황 발생 시 도움 요청 기능
    </div>
    """, unsafe_allow_html=True)

    st.link_button(
        "SOS 페이지 이동",
        SOS_URL,
        use_container_width=True
    )

with col3:
    st.markdown("""
    <div class="card">
    <h3>🔔 소리 감지 알림</h3>
    중요한 소리를 감지하면 알림 제공
    </div>
    """, unsafe_allow_html=True)

    st.link_button(
        "소리 감지 페이지 이동",
        SOUND_ALERT_URL,
        use_container_width=True
    )

st.divider()

# ------------------
# 이용 안내
# ------------------
st.header("📋 이용 안내")

guide_col1, guide_col2 = st.columns(2)

with guide_col1:
    st.info("""
    🎤 자동 자막

    회의, 수업, 대화 내용을
    텍스트로 확인할 수 있습니다.
    """)

with guide_col2:
    st.info("""
    🔔 소리 감지

    초인종, 경보음, 호출음 등을
    시각적으로 알려줍니다.
    """)

st.divider()

# ------------------
# 긴급 연락
# ------------------
st.header("🚨 긴급 연락 정보")

st.success("112 문자 신고 가능")
st.success("119 문자 신고 가능")
st.success("보호자 비상 연락망 등록 권장")

st.divider()

# ------------------
# 피드백
# ------------------
st.header("💬 의견 남기기")

try:
    feedback = st.text_area(
        "서비스 개선 의견을 입력해주세요.",
        height=120
    )

    if st.button("제출"):
        if feedback.strip():
            st.success("의견이 접수되었습니다.")
        else:
            st.warning("내용을 입력해주세요.")

except Exception as e:
    st.error("입력 처리 중 오류가 발생했습니다.")

# ------------------
# 푸터
# ------------------
st.markdown(
    '<div class="footer">© 2026 HearConnect Team Project</div>',
    unsafe_allow_html=True
)
