import streamlit as st

# 페이지 설정
st.set_page_config(
    page_title="HearBridge",
    page_icon="🦻",
    layout="wide"import streamlit as st

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
)

# 안전한 스타일 적용
st.markdown("""
<style>
.main-title {
    text-align:center;
    font-size:42px;
    font-weight:bold;
    color:#1f77b4;
}

.sub-title{
    text-align:center;
    font-size:18px;
    color:#666666;
}

.feature-card{
    padding:20px;
    border-radius:12px;
    background-color:#f5f7fa;
    border:1px solid #dce3ea;
    margin-bottom:10px;
}

.info-box{
    background-color:#eef7ff;
    padding:15px;
    border-radius:10px;
    border-left:5px solid #1f77b4;
}
</style>
""", unsafe_allow_html=True)

# 헤더
st.markdown(
    '<p class="main-title">🦻 HearBridge</p>',
    unsafe_allow_html=True
)

st.markdown(
    '<p class="sub-title">청각 장애인을 위한 소통 지원 플랫폼</p>',
    unsafe_allow_html=True
)

st.divider()

# 환영 메시지
st.markdown("""
<div class="info-box">
<h4>환영합니다!</h4>
청각 장애인의 일상 소통과 정보 접근을 돕기 위한 메인 페이지입니다.
필요한 서비스를 빠르게 확인해 보세요.
</div>
""", unsafe_allow_html=True)

st.write("")

# 주요 기능
st.header("📌 주요 서비스")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="feature-card">
    <h4>📝 실시간 자막</h4>
    음성 내용을 텍스트로 확인할 수 있는 기능을 제공합니다.
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-card">
    <h4>🤟 수어 학습</h4>
    한국수어 기초 표현과 학습 자료를 제공합니다.
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="feature-card">
    <h4>📢 알림 서비스</h4>
    중요한 공지와 생활 정보를 빠르게 전달합니다.
    </div>
    """, unsafe_allow_html=True)

st.divider()

# 오늘의 정보
st.header("📅 오늘의 소통 정보")

tips = [
    "회의 시 자동 자막 기능을 활용해 보세요.",
    "공공기관 방문 전 문자 상담 가능 여부를 확인해 보세요.",
    "영상 시청 시 자막 제공 여부를 먼저 확인하면 편리합니다.",
    "스마트폰의 실시간 텍스트 기능을 활용할 수 있습니다."
]

for tip in tips:
    st.success(tip)

st.divider()

# 긴급 지원
st.header("🚨 긴급 도움 안내")

with st.expander("긴급 상황 시 확인하기"):
    st.write("""
    - 112 문자 신고 가능
    - 119 문자 신고 가능
    - 보호자 및 비상 연락망 사전 등록 권장
    - 위치 공유 기능 활용 권장
    """)

st.divider()

# 지원 정보
st.header("🏛️ 지원 정보")

support_data = {
    "서비스": [
        "보청기 지원",
        "수어 통역",
        "재활 서비스",
        "직업 지원"
    ],
    "대상": [
        "청각 장애인",
        "청각 장애인",
        "등록 장애인",
        "구직 희망자"
    ]
}

st.table(support_data)

st.divider()

# 사용자 의견
st.header("💬 의견 남기기")

try:
    feedback = st.text_area(
        "서비스 개선 의견을 입력하세요",
        height=120
    )

    if st.button("제출"):
        if feedback.strip():
            st.success("의견이 정상적으로 접수되었습니다.")
        else:
            st.warning("의견을 입력해 주세요.")
except Exception:
    st.error("입력 처리 중 오류가 발생했습니다.")

st.divider()

st.caption("© HearBridge | 청각 장애인을 위한 소통 지원 메인 페이지")
