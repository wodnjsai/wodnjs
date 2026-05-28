import streamlit as st
import random

# 페이지 설정
st.set_page_config(
    page_title="코드 닉네임 생성기",
    page_icon="🚀",
    layout="centered"
)

# 닉네임 데이터
adjectives = [
    "버그잡는",
    "졸린",
    "폭주하는",
    "야근하는",
    "Null인",
    "커밋하는",
    "리팩토링중인",
    "에러없는",
    "배포중인",
    "디버깅하는",
    "AI쓰는",
    "커피중독",
]

nouns = [
    "너구리",
    "개발자",
    "햄스터",
    "고양이",
    "문어",
    "독수리",
    "판다",
    "코알라",
    "해커",
    "빌더",
    "장인",
    "프로",
]

english_names = [
    "NullHunter",
    "BugCrusher",
    "CommitWizard",
    "DebugMaster",
    "SleepyCoder",
    "DeployNinja",
    "RefactorKing",
    "AIWarrior",
    "CoffeeDriven",
    "StackOverflower",
]

# 제목
st.title("🚀 코드 닉네임 생성기")
st.write("개발자 감성 닉네임을 랜덤으로 생성해드립니다.")

st.divider()

# 사용자 이름 입력
user_name = st.text_input("이름 또는 닉네임 입력", placeholder="예: 민수")

# 스타일 선택
style = st.radio(
    "닉네임 스타일 선택",
    ["한글 감성", "영문 감성", "혼합 스타일"]
)

# 생성 버튼
if st.button("🎲 닉네임 생성하기"):

    if style == "한글 감성":
        nickname = random.choice(adjectives) + random.choice(nouns)

    elif style == "영문 감성":
        nickname = random.choice(english_names)

    else:
        nickname = (
            random.choice(adjectives)
            + random.choice(nouns)
            + "_"
            + str(random.randint(1, 999))
        )

    # 이름 추가 옵션
    if user_name:
        final_name = f"{user_name}의 코드명: {nickname}"
    else:
        final_name = nickname

    st.success("닉네임 생성 완료!")

    st.markdown(
        f"""
        ## 😎 {final_name}
        """
    )

    # 재미 점수
    score = random.randint(70, 100)

    st.metric(
        label="개발자 간지 수치",
        value=f"{score}점"
    )

    # 진행바
    st.progress(score / 100)

    # 랜덤 멘트
    comments = [
        "오늘 배포는 성공할 것입니다.",
        "세미콜론 하나가 세상을 바꿉니다.",
        "버그가 아니라 기능입니다.",
        "커밋 전에 테스트는 했나요?",
        "야근력이 +10 증가했습니다.",
    ]

    st.info(random.choice(comments))

st.divider()

st.caption("Made with ❤️ using Streamlit")
