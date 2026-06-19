from collections import defaultdict
from datetime import datetime, timedelta


# -------------------------
# HH:MM → datetime
# -------------------------

def parse_time(time_str):

    return datetime.strptime(
        time_str,
        "%H:%M"
    )


# -------------------------
# 30분 단위 분해
# -------------------------

def create_time_slots(
    start_time,
    end_time
):

    slots = []

    current = parse_time(start_time)
    end = parse_time(end_time)

    while current < end:

        slots.append(
            current.strftime("%H:%M")
        )

        current += timedelta(
            minutes=30
        )

    return slots


# -------------------------
# 날짜별 가능 인원 계산
# -------------------------

def calculate_overlap(records):

    availability = defaultdict(set)

    for row in records:

        person = row["name"]

        date = str(row["date"])

        slots = create_time_slots(
            str(row["start"]),
            str(row["end"])
        )

        for slot in slots:

            key = (
                date,
                slot
            )

            availability[key].add(
                person
            )

    ranking = []

    for key, users in availability.items():

        ranking.append({

            "date": key[0],

            "time": key[1],

            "count": len(users),

            "users": list(users)
        })

    ranking.sort(

        key=lambda x: (
            x["count"],
            x["date"]
        ),

        reverse=True
    )

    return ranking


# -------------------------
# 날짜별 요약
# -------------------------

def summarize_dates(records):

    date_users = defaultdict(set)

    for row in records:

        date_users[
            str(row["date"])
        ].add(
            row["name"]
        )

    result = []

    for date, users in date_users.items():

        result.append({

            "date": date,

            "count": len(users),

            "users": list(users)
        })

    result.sort(

        key=lambda x: x["count"],

        reverse=True
    )

    return result


# -------------------------
# TOP 추천
# -------------------------

def get_best_meeting_times(
    records,
    top_n=10
):

    ranking = calculate_overlap(
        records
    )

    return ranking[:top_n]
