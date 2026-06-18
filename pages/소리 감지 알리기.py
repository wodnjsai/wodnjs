import streamlit as st
import wave
import numpy as np
from twilio.rest import Client
from datetime import datetime

st.set_page_config(
    page_title="소리 감지 문자 알림기",
    page_icon="🔊",
    layout="centered"
)

st.title("🔊 소리 감지 문자 알림기")

st.markdown(
    """
업로드한 WAV 파일에서 큰 소리를 감지하면
설정된 번호로 문자(SMS)를 발송합니다.
"""
)

# ------------------------
# 함수
# ------------------------

def analyze_audio(uploaded_file):
    try:
        with wave.open(uploaded_file, "rb") as wav_file:
            frames = wav_file.readframes(wav_file.getnframes())
            signal = np.frombuffer(frames, dtype=np.int16)

            rms = np.sqrt(np.mean(signal.astype(np.float64) ** 2))
            peak = np.max(np.abs(signal))

            return rms, peak

    except Exception as e:
        raise Exception(f"오디오 분석 실패: {e}")


def send_sms(message, phone_number):
    try:
        account_sid = st.secrets["TWILIO_ACCOUNT_SID"]
        auth_token = st.secrets["TWILIO_AUTH_TOKEN"]
        from_number = st.secrets["TWILIO_PHONE_NUMBER"]

        client = Client(account_sid, auth_token)

        client.messages.create(
            body=message,
            from_=from_number,
            to=phone_number
        )

        return True

    except Exception as e:
        st.error(f"SMS 발송 실패: {e}")
        return False


# ------------------------
# UI
# ------------------------

threshold = st.slider(
    "감지 임계값",
    min_value=100,
    max_value=20000,
    value=3000,
    step=100
)

phone_number = st.text_input(
    "알림 받을 전화번호",
    placeholder="+821012345678"
)

uploaded_file = st.file_uploader(
    "WAV 파일 업로드",
    type=["wav"]
)

if uploaded_file:

    try:
        rms, peak = analyze_audio(uploaded_file)

        st.success("파일 분석 완료")

        col1, col2 = st.columns(2)

        with col1:
            st.metric("평균 음량(RMS)", f"{rms:.0f}")

        with col2:
            st.metric("최대 음량", f"{peak}")

        detected = peak >= threshold

        if detected:

            st.error("🚨 큰 소리 감지")

            if st.button("문자 발송"):

                if not phone_number:
                    st.warning("전화번호를 입력하세요.")
                else:

                    message = (
                        f"[소리 감지 알림]\n"
                        f"큰 소리가 감지되었습니다.\n"
                        f"최대 음량: {peak}\n"
                        f"시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                    )

                    success = send_sms(
                        message,
                        phone_number
                    )

                    if success:
                        st.success("문자 발송 완료")

        else:
            st.info("감지 임계값 이하")

    except Exception as e:
        st.error(str(e))

st.divider()

st.caption(
    "지원 형식: WAV 파일"
)
