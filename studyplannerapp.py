import streamlit as st
import datetime

st.set_page_config(page_title="Smart Study Planner", layout="centered")
st.title("📚 Middle School Smart Study Planner")

all_subjects = ["Math", "Science", "ELA", "Texas History", "Spanish", "Computer Science", "Art", "US History", "Digital Graphics & Animation"]

def time_input(label, value):
    return st.time_input(label, value=value)

subjects = st.multiselect("What subjects do you want to study today?", all_subjects)
home_time = time_input("What time did you get home?", value=datetime.time(16, 0))
sleep_time = time_input("What time is your bedtime?", value=datetime.time(21, 0))

num_classes = st.number_input("How many special classes (e.g., Math Tuition, Karate, Yoga, Tennis) do you have today?", min_value=0, max_value=5, step=1)
special_classes = []
for i in range(num_classes):
    class_name = st.text_input(f"Special class {i+1} name")
    class_start = time_input(f"Start time for {class_name}", value=datetime.time(17, 0))
    class_end = time_input(f"End time for {class_name}", value=datetime.time(18, 0))
    special_classes.append((class_name, class_start, class_end))

test_subjects = st.multiselect("Do you have a test or homework due soon in any subject?", all_subjects)

# Button with just calendar icon
generate = st.button("📅 Generate My Schedule")

if generate:
    start = datetime.datetime.combine(datetime.date.today(), home_time)
    end = datetime.datetime.combine(datetime.date.today(), sleep_time)
    now = start

    me_time_end = now + datetime.timedelta(hours=1)
    schedule = [(now, me_time_end, "🎮 Me Time - Relax and recharge!")]
    now = me_time_end

    special_classes_sorted = sorted(special_classes, key=lambda x: x[1])

    special_icons = {
        "Yoga": "🧘‍♂️",
        "Tennis": "🎾",
        "Karate": "🥋",
        "Math Tuition": "📐",
    }

    for idx, (class_name, class_start, class_end) in enumerate(special_classes_sorted):
        ready_buffer = datetime.timedelta(minutes=5)
        commute = datetime.timedelta(minutes=15)
        return_buffer = datetime.timedelta(minutes=15)

        before_class = datetime.datetime.combine(datetime.date.today(), class_start)
        after_class = datetime.datetime.combine(datetime.date.today(), class_end)
        icon = special_icons.get(class_name, "🎓")

        if idx == 0:
            ready_start = before_class - (ready_buffer + commute)
            if now < ready_start:
                schedule.append((now, ready_start, "---"))
                now = ready_start
            schedule.append((ready_start, before_class, f"🚌 Get ready & travel for {class_name}"))
        else:
            prev_end = datetime.datetime.combine(datetime.date.today(), special_classes_sorted[idx - 1][2])
            travel_start = prev_end
            travel_end = before_class
            schedule.append((travel_start, travel_end, f"🚌 Travel from previous class to {class_name}"))

        schedule.append((before_class, after_class, f"{icon} {class_name} class"))

        if idx == len(special_classes_sorted) - 1:
            recovery_end = after_class + return_buffer
            schedule.append((after_class, recovery_end, "🏡 Return home and settle in"))
            now = recovery_end
        else:
            now = after_class

    remaining_time = int((end - now).total_seconds() // 60)
    if remaining_time <= 0 or not (subjects or test_subjects):
        st.warning("Not enough time to plan a study schedule today or no subjects selected.")
    else:
        all_study_subjects = list(set(subjects + test_subjects))

        weights = {}
        for subj in all_study_subjects:
            if subj in test_subjects:
                weights[subj] = 90
            else:
                weights[subj] = 60

        total_alloc = sum(weights.values())
        max_schedule = min(remaining_time, total_alloc)
        adjusted_weights = {k: int((v / total_alloc) * max_schedule) for k, v in weights.items()}

        stretch_interval = 30
        last_stretch = now

        for subj, minutes in adjusted_weights.items():
            max_chunks = minutes // 30
            chunk_time = 30
            for _ in range(max_chunks):
                if now + datetime.timedelta(minutes=chunk_time) > end:
                    break

                if (now - last_stretch).total_seconds() >= stretch_interval * 60:
                    break_end = now + datetime.timedelta(minutes=5)
                    schedule.append((now, break_end, "🤸 Stretch Break - Look 20 feet away for 20 seconds, stretch your arms and legs, and drink a glass of water!"))
                    now = break_end
                    last_stretch = now

                end_block = now + datetime.timedelta(minutes=chunk_time)
                schedule.append((now, end_block, f"📘 Study: {subj}"))
                now = end_block

    st.success("✅ Here's your personalized study plan for today!")
    for start_time, end_time, activity in schedule:
        start_fmt = start_time.strftime("%I:%M %p")
        end_fmt = end_time.strftime("%I:%M %p")

        if "Study:" in activity:
            st.markdown(f'''<div style="background-color:#D0EBFF;padding:12px;border-radius:10px;"><h4 style="color:#084298;font-size:20px;">🕒 {start_fmt} - {end_fmt}: <b>{activity}</b></h4></div>''', unsafe_allow_html=True)
        elif "Stretch Break" in activity:
            st.markdown(f'''<div style="background-color:#D1E7DD;padding:8px;border-radius:8px;"><h5 style="color:#0F5132;font-size:14px;border-top:1px solid #ccc;border-bottom:1px solid #ccc;">🕒 {start_fmt} - {end_fmt}: {activity}</h5></div>''', unsafe_allow_html=True)
        else:
            st.markdown(f'''<div style="background-color:#E2F0D9;padding:10px;border-radius:10px;"><h4 style="color:#2E7D32;">🕒 {start_fmt} - {end_fmt}: {activity}</h4></div>''', unsafe_allow_html=True)

    st.info("🌟 You’ve crushed it! You finished all your work today. Great job!")
