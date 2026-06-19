import streamlit as st
import uuid
from datetime import datetime

from storage import (
    initialize_files,
    save_room,
    save_participant,
    get_room_participants
)

from scheduler import (
    get_best_meeting_times,
    summarize_dates
)

from location import (
    calculate_midpoint,
    get_location_markers
)

# -----------------------------------
# 페이지 설정
# -----------------------------------

st.set_page_config(
    page_title="Meet Planner",
    page_icon="📅",
    layout="wide"
)

initialize_files()

# -----------------------------------
# 세션 초기화
# -----------------------------------

if "schedule_count" not in st.session_state:
    st.session_state.schedule_count = 1

# -----------------------------------
# 스타일
# -----------------------------------

st.markdown("""
<style>

.block-container{
    padding-top:2rem;
    max-width:1200px;
}

.main-title{
    text-align:center;
    font-size:42px;
    font-weight:700;
}

.sub-title{
    text-align:center;
    color:gray;
}

</style>
""", unsafe_allow_html=True)

# -----------------------------------
# 헤더
# -----------------------------------

st.markdown(
    "<div class='main-title'>📅 Meet Planner</div>",
    unsafe_allow_html=True
)

st.markdown(
    "<div class='sub-title'>친구들과 가장 좋은 약속 시간을 찾아보세요</div>",
    unsafe_allow_html=True
)

st.divider()

# -----------------------------------
# 방 생성
# -----------------------------------

left, right = st.columns(2)

with left:

    st.subheader("🆕 새 방 만들기")

    if st.button("방 생성"):

        room_code = str(uuid.uuid4())[:8]

        save_room(
            room_code,
            datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        )

        st.session_state.room_code = room_code

        st.success(
            f"생성 완료: {room_code}"
        )

with right:

    st.subheader("🚪 방 참여")

    room_input = st.text_input(
        "방 코드 입력"
    )

    if st.button("입장"):

        st.session_state.room_code = room_input

# -----------------------------------
# 방 선택 확인
# -----------------------------------

if "room_code" not in st.session_state:

    st.info(
        "먼저 방을 생성하거나 입장하세요."
    )

    st.stop()

room_code = st.session_state.room_code

st.success(
    f"현재 방: {room_code}"
)

st.divider()

# -----------------------------------
# 참가자 정보
# -----------------------------------

st.subheader("🙋 참가자 정보")

name = st.text_input(
    "이름"
)

location = st.text_input(
    "출발 위치",
    placeholder="예) 서울역"
)

st.divider()

# -----------------------------------
# 일정 입력
# -----------------------------------

st.subheader("📅 가능한 일정")

for i in range(
    st.session_state.schedule_count
):

    st.markdown(
        f"### 일정 {i+1}"
    )

    c1, c2, c3 = st.columns(3)

    with c1:

        st.date_input(
            "날짜",
            key=f"date_{i}"
        )

    with c2:

        st.time_input(
            "시작 시간",
            key=f"start_{i}"
        )

    with c3:

        st.time_input(
            "종료 시간",
            key=f"end_{i}"
        )

    st.divider()

# -----------------------------------
# 일정 추가
# -----------------------------------

if st.button("➕ 일정 추가"):

  # -----------------------------------
# 저장 버튼
# -----------------------------------

st.divider()

if st.button("💾 저장"):

    if not name:

        st.error("이름을 입력하세요.")

    else:

        schedules = []

        for i in range(
            st.session_state.schedule_count
        ):

            schedules.append({

                "date": st.session_state[
                    f"date_{i}"
                ].strftime(
                    "%Y-%m-%d"
                ),

                "start": st.session_state[
                    f"start_{i}"
                ].strftime(
                    "%H:%M"
                ),

                "end": st.session_state[
                    f"end_{i}"
                ].strftime(
                    "%H:%M"
                )
            })

        save_participant(

            room_code=room_code,

            name=name,

            location=location,

            schedules=schedules
        )

        st.success(
            "참가 정보 저장 완료!"
        )

# -----------------------------------
# 참가자 조회
# -----------------------------------

st.divider()

st.subheader(
    "👥 참가자 목록"
)

records = get_room_participants(
    room_code
)

if not records:

    st.info(
        "아직 참가자가 없습니다."
    )

else:

    participants = {}

    for row in records:

        user = row["name"]

        if user not in participants:

            participants[user] = {

                "location":
                    row["location"],

                "schedules":[]
            }

        participants[user][
            "schedules"
        ].append(row)

# -----------------------------------
# 참가자 카드 표시
# -----------------------------------

    for user, info in participants.items():

        with st.expander(
            f"🙋 {user}"
        ):

            st.write(
                f"📍 {info['location']}"
            )

            for s in info[
                "schedules"
            ]:

                st.write(

                    f"📅 {s['date']}"

                    f"  "

                    f"{s['start']}"

                    f" ~ "

                    f"{s['end']}"
                )

# -----------------------------------
# 통계
# -----------------------------------

st.divider()

st.subheader(
    "📊 현재 참여 현황"
)

unique_users = set()

for row in records:

    unique_users.add(
        row["name"]
    )

col1, col2 = st.columns(2)

with col1:

    st.metric(
        "참여자 수",
        len(unique_users)
    )

with col2:

    st.metric(
        "등록 일정 수",
        len(records)
    )

    st.session_state.schedule_count += 1

    st.rerun()

# -----------------------------------
# 저장 버튼
# -----------------------------------

st.divider()

if st.button("💾 저장"):

    if not name:

        st.error("이름을 입력하세요.")

    else:

        schedules = []

        for i in range(
            st.session_state.schedule_count
        ):

            schedules.append({

                "date": st.session_state[
                    f"date_{i}"
                ].strftime(
                    "%Y-%m-%d"
                ),

                "start": st.session_state[
                    f"start_{i}"
                ].strftime(
                    "%H:%M"
                ),

                "end": st.session_state[
                    f"end_{i}"
                ].strftime(
                    "%H:%M"
                )
            })

        save_participant(

            room_code=room_code,

            name=name,

            location=location,

            schedules=schedules
        )

        st.success(
            "참가 정보 저장 완료!"
        )

# -----------------------------------
# 참가자 조회
# -----------------------------------

st.divider()

st.subheader(
    "👥 참가자 목록"
)

records = get_room_participants(
    room_code
)

if not records:

    st.info(
        "아직 참가자가 없습니다."
    )

else:

    participants = {}

    for row in records:

        user = row["name"]

        if user not in participants:

            participants[user] = {

                "location":
                    row["location"],

                "schedules":[]
            }

        participants[user][
            "schedules"
        ].append(row)

# -----------------------------------
# 참가자 카드 표시
# -----------------------------------

    for user, info in participants.items():

        with st.expander(
            f"🙋 {user}"
        ):

            st.write(
                f"📍 {info['location']}"
            )

            for s in info[
                "schedules"
            ]:

                st.write(

                    f"📅 {s['date']}"

                    f"  "

                    f"{s['start']}"

                    f" ~ "

                    f"{s['end']}"
                )

# -----------------------------------
# 통계
# -----------------------------------

st.divider()

st.subheader(
    "📊 현재 참여 현황"
)

unique_users = set()

for row in records:

    unique_users.add(
        row["name"]
    )

col1, col2 = st.columns(2)

with col1:

    st.metric(
        "참여자 수",
        len(unique_users)
    )

with col2:

    st.metric(
        "등록 일정 수",
        len(records)
    )

# -----------------------------------
# 추천 시간 분석
# -----------------------------------

st.divider()

st.subheader("🎯 추천 약속 시간")

if records:

    best_times = get_best_meeting_times(
        records,
        top_n=10
    )

    if best_times:

        medals = [
            "🥇",
            "🥈",
            "🥉"
        ]

        for idx, item in enumerate(best_times):

            medal = (
                medals[idx]
                if idx < 3
                else "🏅"
            )

            with st.container():

                st.success(

                    f"{medal} "

                    f"{item['date']} "

                    f"{item['time']}"

                    f"  "

                    f"({item['count']}명 가능)"
                )

                st.caption(
                    ", ".join(
                        item["users"]
                    )
                )

# -----------------------------------
# 날짜별 통계
# -----------------------------------

st.divider()

st.subheader("📊 날짜별 가능 인원")

summary = summarize_dates(
    records
)

if summary:

    import pandas as pd
    import plotly.express as px

    chart_df = pd.DataFrame(
        summary
    )

    fig = px.bar(

        chart_df,

        x="date",

        y="count",

        text="count",

        title="날짜별 참여 가능 인원"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# -----------------------------------
# 중간 위치 계산
# -----------------------------------

st.divider()

st.subheader(
    "📍 추천 만남 위치"
)

locations = []

for row in records:

    if row["location"]:

        locations.append(
            row["location"]
        )

if locations:

    midpoint = calculate_midpoint(
        locations
    )

    if midpoint:

        st.success(
            "중간 위치 계산 완료"
        )

        st.write(
            f"위도 : {midpoint['lat']:.5f}"
        )

        st.write(
            f"경도 : {midpoint['lon']:.5f}"
        )

# -----------------------------------
# 지도
# -----------------------------------

        try:

            import folium

            from streamlit_folium import (
                st_folium
            )

            m = folium.Map(

                location=[

                    midpoint["lat"],

                    midpoint["lon"]
                ],

                zoom_start=12
            )

# -----------------------------------
# 참가자 위치
# -----------------------------------

            markers = (
                get_location_markers(
                    locations
                )
            )

            for marker in markers:

                folium.Marker(

                    [

                        marker["lat"],

                        marker["lon"]

                    ],

                    tooltip=marker["name"],

                    icon=folium.Icon(
                        icon="user"
                    )

                ).add_to(m)

# -----------------------------------
# 중간 위치 마커
# -----------------------------------

            folium.Marker(

                [

                    midpoint["lat"],

                    midpoint["lon"]

                ],

                tooltip="추천 만남 위치",

                popup="중간 지점",

                icon=folium.Icon(
                    color="red"
                )

            ).add_to(m)

            st_folium(

                m,

                width=1200,

                height=500
            )

        except Exception as e:

            st.warning(
                "지도 로딩 실패"
            )

            st.text(
                str(e)
            )

# -----------------------------------
# 원본 데이터
# -----------------------------------

st.divider()

with st.expander(
    "🔎 저장된 데이터 보기"
):

    import pandas as pd

    if records:

        st.dataframe(
            pd.DataFrame(records),
            use_container_width=True
        )

# -----------------------------------
# Footer
# -----------------------------------

st.divider()

st.caption(
    "Made with ❤️ using Streamlit"
)
