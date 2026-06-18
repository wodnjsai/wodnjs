import streamlit as st

# ======================
# 페이지 설정
# ======================
st.set_page_config(
    page_title="소리온",
    page_icon="🦻",
    layout="wide"
)

# ======================
# 팀원 앱 주소
# 배포 후 실제 주소로 변경
# ======================
AUTO_CAPTION_URL = "https://your-auto-caption-app.streamlit.app"
SOS_URL = "https://your-sos-app.streamlit.app"
SOUND_ALERT_URL = "https://your-sound-alert-app.streamlit.app"

# ======================
# 헤더
# ======================
st.title("🦻 소리온")
st.subheader("들리지 않아도, 세상과 연결되다")

st.info(
    """
    소리온은 청각 장애인을 위한 통합 지원 플랫폼입니다.

    🎤 자동 자막 서비스  
    🚨 SOS 구조 요청 서비스  
    🔔 소리 감지 알림 서비스

    필요한 기능을 선택하여 이용하세요.
    """
)

st.divider()

# ======================
# 메인 서비스
# ======================
st.header("🚀 주요 서비스")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### 🎤 자동 자막")
    st.write(
        """
        음성을 실시간으로
        텍스트 자막으로 변환하여
        대화와 수업, 회의를 돕습니다.
        """
    )

    st.link_button(
        "자동 자막 서비스 이동",
        AUTO_CAPTION_URL,
        use_container_width=True
    )

with col2:
    st.markdown("### 🚨 SOS 구조 요청")
    st.write(
        """
        긴급 상황 발생 시
        구조 요청 기능을 통해
        빠르게 도움을 요청할 수 있습니다.
        """
    )

    st.link_button(
        "SOS 서비스 이동",
        SOS_URL,
        use_container_width=True
    )

with col3:
    st.markdown("### 🔔 소리 감지 알림")
    st.write(
        """
        초인종, 경보음, 호출음 등
        중요한 소리를 감지하여
        시각적으로 알려줍니다.
        """
    )

    st.link_button(
        "소리 감지 서비스 이동",
        SOUND_ALERT_URL,
        use_container_width=True
    )

st.divider()

# ======================
# 서비스 소개
# ======================
st.header("📖 소리온 소개")

st.write(
    """
    청각 장애인은 중요한 소리를 듣지 못해
    위험 상황이나 의사소통에서 어려움을 겪을 수 있습니다.

    소리온은 이러한 문제를 해결하기 위해
    자동 자막, SOS 구조 요청, 소리 감지 알림 기능을
    하나의 플랫폼에서 제공합니다.
    """
)

st.divider()

# ======================
# 긴급 안내
# ======================
st.header("🚨 긴급 상황 안내")

col1, col2 = st.columns(2)

with col1:
    st.success("112 문자 신고 가능")
    st.success("119 문자 신고 가능")

with col2:
    st.success("보호자 비상 연락망 등록 권장")
    st.success("위치 공유 기능 사용 권장")

st.divider()

# ======================
# 의견 제출
# ======================
st.header("💬 사용자 의견")

try:
    feedback = st.text_area(
        "서비스 개선 의견을 입력해주세요.",
        height=150
    )

    if st.button("의견 제출"):
        if feedback.strip():
            st.success("소중한 의견 감사합니다.")
        else:
            st.warning("내용을 입력해주세요.")

except Exception:
    st.error("입력 처리 중 오류가 발생했습니다.")

st.divider()

# ======================
# 푸터
# ======================
st.caption("© 2026 소리온 | 청각 장애인을 위한 통합 지원 플랫폼")
