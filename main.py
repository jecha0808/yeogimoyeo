import streamlit as st
from collections import defaultdict
import uuid

st.set_page_config(
    page_title="Meet Planner",
    page_icon="📅",
    layout="wide"
)

# -----------------
# 세션 초기화
# -----------------

if "participants" not in st.session_state:
    st.session_state.participants = []

if "availability" not in st.session_state:
    st.session_state.availability = [{}]

# -----------------
# 헤더
# -----------------

st.title("📅 Meet Planner")
st.caption("친구들과 가장 좋은 약속 시간을 찾아보세요")

# -----------------
# 방 정보
# -----------------

with st.sidebar:

    st.header("방 정보")

    if "room_code" not in st.session_state:
        st.session_state.room_code = str(uuid.uuid4())[:8]

    st.code(st.session_state.room_code)

# -----------------
# 사용자 정보
# -----------------

st.subheader("🙋 참가자")

name = st.text_input("이름")

start_place = st.text_input(
    "출발 위치",
    placeholder="예: 서울역"
)

# -----------------
# 일정 입력
# -----------------

st.subheader("📅 가능한 일정")

for i in range(len(st.session_state.availability)):

    with st.container():

        c1, c2, c3 = st.columns(3)

        with c1:
            date = st.date_input(
                f"날짜 {i+1}",
                key=f"date_{i}"
            )

        with c2:
            start = st.time_input(
                f"시작 {i+1}",
                key=f"start_{i}"
            )

        with c3:
            end = st.time_input(
                f"종료 {i+1}",
                key=f"end_{i}"
            )

if st.button("➕ 일정 추가"):
    st.session_state.availability.append({})
    st.rerun()

# -----------------
# 저장
# -----------------

if st.button("💾 저장"):

    schedules = []

    for i in range(len(st.session_state.availability)):

        schedules.append(
            {
                "date": str(
                    st.session_state[f"date_{i}"]
                ),
                "start": str(
                    st.session_state[f"start_{i}"]
                ),
                "end": str(
                    st.session_state[f"end_{i}"]
                )
            }
        )

    st.session_state.participants.append(
        {
            "name": name,
            "location": start_place,
            "schedules": schedules
        }
    )

    st.success("저장 완료")

# -----------------
# 참가자 목록
# -----------------

st.divider()

st.subheader("👥 참가자")

if not st.session_state.participants:

    st.info("아직 참가자가 없습니다.")

else:

    for p in st.session_state.participants:

        with st.expander(
            f"{p['name']} ({p['location']})"
        ):

            for s in p["schedules"]:

                st.write(
                    f"📅 {s['date']} "
                    f"{s['start']} ~ {s['end']}"
                )

# -----------------
# 추천 일정
# -----------------

st.divider()

st.subheader("🎯 추천 날짜")

date_counter = defaultdict(int)

for person in st.session_state.participants:

    unique_dates = set()

    for schedule in person["schedules"]:

        unique_dates.add(schedule["date"])

    for d in unique_dates:

        date_counter[d] += 1

ranking = sorted(
    date_counter.items(),
    key=lambda x: x[1],
    reverse=True
)

if ranking:

    medals = ["🥇", "🥈", "🥉"]

    for idx, (date, count) in enumerate(ranking):

        icon = (
            medals[idx]
            if idx < 3
            else "🏅"
        )

        st.metric(
            label=f"{icon} {date}",
            value=f"{count}명 가능"
        )

else:

    st.info("추천할 일정이 없습니다.")

# -----------------
# 중간 장소(임시)
# -----------------

st.divider()

st.subheader("📍 만남 장소")

if st.session_state.participants:

    places = []

    for p in st.session_state.participants:

        if p["location"]:
            places.append(p["location"])

    if places:

        st.write("입력된 출발지")

        for place in places:

            st.write("•", place)

        st.warning(
            "외부 지도 API 없이 실행 중이라 "
            "실제 중간지점 계산은 불가능합니다."
        )
