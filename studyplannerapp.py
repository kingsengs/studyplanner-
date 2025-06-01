import streamlit as st
import datetime
import random

st.title("📚 Middle School Smart Study Planner")

# Step 1: Input
all_subjects = ["Math", "Science", "ELA", "Texas History", "Spanish", "Computer Science"]

subjects = st.multiselect(
    "What subjects do you want to study today?", 
    all_subjects
)

home_time = st.time_input("What time do you get home?", value=datetime.time(16, 0))
sleep_time = st.time_input("What time is bedtime?", value=datetime.time(21, 0))

exam_subject = st.selectbox(
    "Do you have a test or homework due soon in any subject?", 
    ["None"] + all_subjects
)

# Step 2: Time calculations
start = datetime.datetime.combine(datetime.date.today(), home_time)
end = datetime.datetime.combine(datetime.date.today(), sleep_time)

available_minutes = int((end - start).total_seconds() // 60)
max_study_minutes = min(180, available_minutes - 30)  # cap at 3 hours, minus buffer

break_every = 30  # minutes

# Fun eye-care tips
eye_tips = [
    "👓 Blink 10 times slowly to refresh your eyes!",
    "🌳 Look outside at something green for 20 seconds!",
    "💧 Splash your eyes with water if they feel dry!",
    "🔄 Roll your eyes gently in a circle for 10 seconds!",
    "🚶‍♀️ Stand up and stretch for a minute!",
    "🦸‍♂️ Stare like a superhero—then relax!"
]

if not subjects:
    st.warning("Please choose at least one subject.")
elif max_study_minutes <= 0:
    st.warning("Not enough time to plan a study schedule today.")
else:
    # Step 3: Weighted time allocation
    weights = {s: 2 if s == exam_subject else 1 for s in subjects}
    total_weight = sum(weights.values())

    schedule = []
    current_time = start
    minutes_left = max_study_minutes

    for subject in subjects:
        subject_time = int((weights[subject] / total_weight) * max_study_minutes)
        chunks = subject_time // break_every

        for _ in range(chunks):
            if minutes_left < break_every:
                break

            # Study block
            end_time = current_time + datetime.timedelta(minutes=break_every)
            schedule.append((current_time.strftime("%I:%M %p"), end_time.strftime("%I:%M %p"), subject))
            current_time = end_time
            minutes_left -= break_every

            # Eye break
            break_end = current_time + datetime.timedelta(seconds=30)
            fun_reminder = random.choice(eye_tips)
            schedule.append((current_time.strftime("%I:%M %p"), break_end.strftime("%I:%M %p"), fun_reminder))
            current_time = break_end

    # Step 4: Display schedule
    st.success("✅ Here's your personalized study plan for today!")

    for start_time, end_time, activity in schedule:
        if any(emoji in activity for emoji in ["👓", "🌳", "💧", "🔄", "🚶‍♀️", "🦸‍♂️"]):
            st.markdown(
                f'''<div style="background-color:#FFF3CD;padding:10px;border-radius:10px;">
                <h4 style="color:#856404;">🕒 {start_time} - {end_time}: <b>{activity}</b></h4>
                </div>''', 
                unsafe_allow_html=True
            )
        else:
            st.write(f"🕒 {start_time} - {end_time}: **{activity}**")

    st.info("✨ Tip: Follow the 20-20-20 rule – every 20 minutes, look 20 feet away for 20 seconds!")
