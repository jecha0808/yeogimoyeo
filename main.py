import streamlit as st
import pandas as pd
import uuid
from scheduler import find_best_times

st.set_page_config(
    page_title="Meet Planner",
    page_icon="📅",
    layout="wide"
)

st.title("📅 Meet Planner")
st.caption("친구들과 약속 시간을 쉽게 찾기")

if "slots" not in st.session_state:
    st.session_state.slots = [
        {"date": None, "start": "09:00", "end": "18:00"}
    ]

with st.sidebar:

    st.header("방 생성")

    room_code = st.text_input(
        "방 코드",
        value=str(uuid.uuid4())[:8]
    )

    st.success(
        f"공유 코드: {room_code}"
    )

name = st.text_input("이름")

location = st.text_input(
    "출발 위치",
    placeholder="서울역"
)

st.subheader("가능 시간")

for i, slot in enumerate(st.session_state.slots):

    c1, c2, c3 = st.columns(3)

    with c1:
        slot["date"] = st.date_input(
            f"날짜{i}",
            key=f"d{i}"
        )

    with c2:
        slot["start"] = st.text_input(
            "시작",
            value=slot["start"],
            key=f"s{i}"
        )

    with c3:
        slot["end"] = st.text_input(
            "종료",
            value=slot["end"],
            key=f"e{i}"
        )

if st.button("➕ 일정 추가"):
    st.session_state.slots.append(
        {
            "date": None,
            "start": "09:00",
            "end": "18:00"
        }
    )
    st.rerun()

if st.button("저장"):

    data = {
        "name": name,
        "location": location,
        "availability": st.session_state.slots
    }

    st.session_state.setdefault(
        "participants",
        []
    )

    st.session_state.participants.append(data)

    st.success("저장 완료")

st.divider()

if "participants" in st.session_state:

    result = find_best_times(
        st.session_state.participants
    )

    st.subheader("🎯 추천 시간")

    for idx, r in enumerate(result[:5]):

        medal = ["🥇", "🥈", "🥉", "🏅", "🏅"]

        st.metric(
            label=f"{medal[idx]} {r['date']}",
            value=f"{r['count']}명 가능"
        )

st.divider()

if "participants" in st.session_state:

    st.subheader("참여자")

    for p in st.session_state.participants:
        st.write(
            f"👤 {p['name']} - {p['location']}"
        )
