import streamlit as st
import google.generativeai as genai
import random
import time
import numpy as np

# 1. 페이지 기본 설정 및 차별화된 테마(어두운 사운드 스테이지 느낌)
st.set_page_config(
    page_title="Sound Direction Visualizer",
    page_icon="🔊",
    layout="centered"
)

# 커스텀 CSS로 화면 레이아웃 및 애니메이션 연출
st.markdown("""
<style>
    .main { background-color: #0e1117; }
    .sound-stage {
        border: 2px dashed #4e5d6c;
        border-radius: 15px;
        padding: 40px;
        text-align: center;
        background-color: #161b22;
        min-height: 300px;
        position: relative;
    }
    .direction-display {
        font-size: 70px;
        transition: all 0.3s ease-in-out;
    }
    .decibel-high {
        color: #ff4b4b;
        animation: blinker 1s linear infinite;
    }
    @keyframes blinker {
        50% { opacity: 0; }
    }
</style>
""", unsafe_style_with_html=True)

# 2. Gemini API 연결 및 예외 처리 (Streamlit Secrets 활용)
try:
    if "GEMINI_API_KEY" in st.secrets:
        api_key = st.secrets["GEMINI_API_KEY"]
    else:
        # 로컬 테스트용 (Secrets가 없을 경우 sidebar에서 입력 가능하도록 예외 처리)
        api_key = st.sidebar.text_input("GEMINI_API_KEY를 입력하세요:", type="password")
    
    if api_key:
        genai.configure(api_key=api_key)
        # 요구사항에 명시된 모델 설정
        model = genai.GenerativeModel('gemini-2.5-flash-lite')
    else:
        st.warning("⚠️ Streamlit Cloud의 Secrets에 'GEMINI_API_KEY'를 설정하거나 사이드바에 입력해주세요.")
        model = None
except Exception as e:
    st.error(f"Gemini API 인증 중 오류가 발생했습니다: {e}")
    model = None

# 3. 앱 타이틀 및 설명
st.title("🔊 소리 방향 이모티콘 시각화기")
st.caption("Gemini AI와 함께 소리의 방향과 크기(데시벨)를 감지하여 스크린에 이모티콘을 표시합니다.")

# 4. 기능 차별화: 테마별 랜덤 이모티콘 셋 목록
EMOJI_SETS = {
    "동물 친구들 🐱": ["🐱", "🐶", "🦁", "🦊", "🐻", "🐼"],
    "자연과 날씨 ⚡": ["⚡", "🔥", "💧", "🌈", "⭐", "🌙"],
    "재미있는 표정 🤪": ["🤪", "😎", "🤩", "🥳", "😱", "🤣"],
    "우주 판타지 🚀": ["🚀", "🛸", "👾", "🌠", "🔮", "👽"]
}

# 사이드바 설정 (초보자도 조작하기 쉽게 직관적으로 구성)
st.sidebar.header("🎛️ 오디오 설정 및 시뮬레이션")
selected_theme = st.sidebar.selectbox("이모티콘 테마 선택", list(EMOJI_SETS.keys()))
db_level = st.sidebar.slider("소리 크기 설정 (데시벨: dB)", 0, 120, 60)
mode = st.sidebar.radio("작동 모드 선택", ["AI 방향 분석 (시뮬레이션)", "수동 방향 테스트"])

# 소리 방향 정의
DIRECTIONS = ["상 (Top)", "하 (Bottom)", "좌 (Left)", "우 (Right)", "중앙 (Center)"]

# 5. Gemini AI를 활용한 소리 감정 및 방향 텍스트 분석 가상 함수
def analyze_sound_with_gemini(db, user_desc):
    if not model:
        return "중앙 (Center)", "Gemini API 키가 설정되지 않아 기본 모드로 작동합니다."
    
    # AI에게 소리 상황을 주고 방향과 분위기를 예측하도록 프롬프트 작성
    prompt = f"""
    사용자가 묘사한 소리 상황: "{user_desc}"
    현재 소리의 크기: {db} dB

    위 상황을 분석하여 소리가 주로 들려올 법한 '방향'을 다음 5개 중 하나로만 정확히 선택하세요: ['상 (Top)', '하 (Bottom)', '좌 (Left)', '우 (Right)', '중앙 (Center)']
    그리고 소리에 대한 짧은 한 줄 평을 남겨주세요.
    
    출력 형식:
    방향: [선택한 방향]
    한줄평: [소리 분석 내용]
    """
    try:
        response = model.generate_content(prompt)
        text = response.text
        
        # 간단한 파싱
        detected_dir = "중앙 (Center)"
        for d in DIRECTIONS:
            if d in text:
                detected_dir = d
                break
        return detected_dir, text
    except Exception as api_err:
        return "중앙 (Center)", f"API 호출 중 오류가 발생했습니다: {api_err}"

# 6. 메인 로직 및 화면 구상
detected_direction = "중앙 (Center)"
ai_commentary = ""

if mode == "AI 방향 분석 (시뮬레이션)":
    st.subheader("🤖 AI 기반 소리 상황 시뮬레이터")
    sound_description = st.text_input(
        "어떤 소리가 들리는 상황인가요? (예: '오른쪽에서 천둥이 번쩍했다', '하늘에서 새가 운다', '발밑에서 고양이가 야옹한다')", 
        "하늘에서 헬리콥터가 지나가고 있다"
    )
    
    if st.button("🔊 소리 분석 및 시각화 시작"):
        with st.spinner("Gemini AI가 소리 분석 중..."):
            detected_direction, ai_commentary = analyze_sound_with_gemini(db_level, sound_description)
            if ai_commentary:
                st.info(f"💬 AI 분석 리포트:\n{ai_commentary}")

else:
    st.subheader("🕹️ 수동 방향 지정 테스트")
    detected_direction = st.selectbox("소리가 들려오는 방향을 직접 선택하세요", DIRECTIONS)

# 7. 핵심 기능: 소리가 들리는 방향으로 이모티콘 스크린 상하좌우 표시 구현
st.markdown("### 🖥️ 이모티콘 사운드 스크린")

# 데시벨이 높을 때(80dB 이상) 조건 처리 -> 사이렌 이모티콘 강제 고정 및 경고 효과
if db_level >= 80:
    display_emoji = "🚨"
    status_text = f"🔥 위험! 고데시벨 감지 ({db_level} dB) - 사이렌 가동!"
    st.error(status_text)
else:
    display_emoji = random.choice(EMOJI_SETS[selected_theme])
    st.success(f"🎵 안정적인 소리 수준 ({db_level} dB) - 테마 이모티콘 작동 중")

# 5x5 그리드 레이아웃을 이용해 상, 하, 좌, 우, 중앙 스크린 위치 시각화
grid_slots = {
    "상 (Top)": (1, 2),
    "좌 (Left)": (2, 0),
    "중앙 (Center)": (2, 2),
    "우 (Right)": (2, 4),
    "하 (Bottom)": (3, 2)
}

# 5행 5열의 가상 공간 생성
container = st.container()
with container:
    st.markdown('<div class="sound-stage">', unsafe_style_with_html=True)
    
    # 레이아웃 배치를 위한 공백 및 컴포넌트 구조화
    row1 = st.columns([1, 1, 2, 1, 1])
    row2 = st.columns([1, 1, 2, 1, 1])
    row3 = st.columns([1, 1, 2, 1, 1])
    
    # 1행 (상)
    with row1[2]:
        if detected_direction == "상 (Top)":
            st.markdown(f'<div class="direction-display {"decibel-high" if db_level>=80 else ""}">{display_emoji}</div>', unsafe_style_with_html=True)
            st.caption("▲ UPPER")
        else: st.write("")
            
    # 2행 (좌, 중앙, 우)
    with row2[0]:
        if detected_direction == "좌 (Left)":
            st.markdown(f'<div class="direction-display {"decibel-high" if db_level>=80 else ""}">{display_emoji}</div>', unsafe_style_with_html=True)
            st.caption("◀ LEFT")
        else: st.write("")
        
    with row2[2]:
        if detected_direction == "중앙 (Center)":
            st.markdown(f'<div class="direction-display {"decibel-high" if db_level>=80 else ""}">{display_emoji}</div>', unsafe_style_with_html=True)
            st.caption("● CENTER")
        else:
            st.markdown("<h3 style='color:#4e5d6c; margin-top:20px;'>STAGE</h3>", unsafe_style_with_html=True)
            
    with row2[4]:
        if detected_direction == "우 (Right)":
            st.markdown(f'<div class="direction-display {"decibel-high" if db_level>=80 else ""}">{display_emoji}</div>', unsafe_style_with_html=True)
            st.caption("RIGHT ▶")
        else: st.write("")
            
    # 3행 (하)
    with row3[2]:
        if detected_direction == "하 (Bottom)":
            st.markdown(f'<div class="direction-display {"decibel-high" if db_level>=80 else ""}">{display_emoji}</div>', unsafe_style_with_html=True)
            st.caption("▼ LOWER")
        else: st.write("")

    st.markdown('</div>', unsafe_style_with_html=True)

# 부가 기능: 시각적인 사운드 이퀄라이저 바 바인딩 (차별화 포인트)
st.markdown("#### 오디오 주파수 시각화 (가상)")
chart_data = np.random.randn(20) * (db_level / 100.0)
st.bar_chart(chart_data)
