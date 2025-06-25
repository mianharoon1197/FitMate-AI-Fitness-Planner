import streamlit as st
import joblib
import numpy as np
import plotly.graph_objects as go


# Load model and encoders
model = joblib.load("fitness_model.pkl")
label_encoders = joblib.load("label_encoders.pkl")

# Set Streamlit page config
st.set_page_config(page_title="FitMate - AI Fitness Planner", layout="wide")

# Inject CSS
st.markdown("""
<style>
.navbar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.4rem 1rem;
    background-color: #4CAF50;
    color: white;
    border-radius: 0.5rem;
    margin-bottom: 0.5rem;
    height: 50px;
}
.navbar h2 {
    margin: 0;
    font-size: 1.3rem;
}
.hero-text {
    background: rgba(76, 175, 80, 0.1);
    padding: 2rem;
    border-radius: 1rem;
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    color: white;
    margin-bottom: 1.5rem;
}
.hero-text h1 {
    color: white;
    font-size: 2rem;
    margin-bottom: 0.5rem;
}
.hero-text p {
    color: white;
    font-size: 1rem;
    margin-bottom: 1rem;
}
.hero-btn {
    background-color: #4CAF50;
    color: white;
    border: none;
    padding: 0.6rem 1.2rem;
    font-size: 1rem;
    border-radius: 6px;
    cursor: pointer;
    transition: background-color 0.3s ease;
}
.hero-btn:hover {
    background-color: #388e3c;
}
         
.section-nav {
    display: flex;
    width: 100%;
    margin-bottom: 1rem;
    gap: 4px;
}
.section-nav button {
    flex: 1;
    padding: 0.4rem;
    border-radius: 30px;
    border: none;
    font-weight: 600;
    font-size: 0.85rem;
    cursor: pointer;
    background-color: #ddd;
    color: black;
}
.section-nav .completed {
    background-color: rgba(76, 175, 80, 0.25) !important; /* translucent green */
    backdrop-filter: blur(6px); /* glass effect */
    -webkit-backdrop-filter: blur(6px); /* Safari support */
    border: 1px solid rgba(76, 175, 80, 0.4); /* subtle green border */
    color: #2e7d32 !important; /* deep green text */
}

.section-nav .active {
    background-color: rgba(66, 165, 245, 0.25) !important; /* translucent blue */
    backdrop-filter: blur(6px); /* glass effect */
    -webkit-backdrop-filter: blur(6px); /* Safari support */
    border: 1px solid rgba(66, 165, 245, 0.4); /* subtle blue border */
    color: #1565C0 !important; /* deeper blue text */
}

.tips-box {
    background-color: #eafce9;
    color: #222;
    padding: 1rem;
    border-left: 5px solid #4CAF50;
    border-radius: 0.5rem;
    margin-top: 1rem;
    font-size: 0.95rem;
    font-weight: 500;
}
.plan-box {
    background-color: #e3f2e1;
    color: #222;
    padding: 1rem 1.5rem;
    border-radius: 0.75rem;
    margin-top: 1rem;
    box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    font-size: 1rem;
}
.plan-box ul {
    list-style: none;
    padding-left: 0;
    line-height: 1.9;
}
.plan-box li::before {
    content: "\1F4CB";
    display: inline-block;
    margin-right: 0.5rem;
}
.error-message {
    background-color: #ffe6e6;
    color: #cc0000;
    padding: 10px;
    border-radius: 6px;
    margin-top: 10px;
    font-weight: 500;
}
</style>
""", unsafe_allow_html=True)

# Navbar
st.markdown("""
<div class="navbar">
    <h2>🏋‍♂ FitMate</h2>
</div>
""", unsafe_allow_html=True)

# Hero section

st.markdown("""
<div class="hero-text">
    <h1>Start Your Personalized Fitness Journey</h1>
    <p>AI-powered guidance to help you reach your health goals with tailored diet, exercise, and lifestyle tips.</p>
    <a href="#form-start"><button class="hero-btn">Get Started</button></a>
</div>
""", unsafe_allow_html=True)


# Step indicator
step_titles = ["1. Personal Info", "2. Exercise Info", "3. Diet Info", "4. Goal Info"]
if 'step' not in st.session_state:
    st.session_state.step = 1

with st.container():
    nav_html = "<div class='section-nav'>"
    for i, title in enumerate(step_titles):
        btn_class = "completed" if st.session_state.step > i + 1 else ("active" if st.session_state.step == i + 1 else "")
        nav_html += f"<button class='{btn_class}'>{title}</button>"
    nav_html += "</div>"
    st.markdown(nav_html, unsafe_allow_html=True)

# Forms
if st.session_state.step == 1:
    with st.form("personal_form"):
        col1, col2 = st.columns(2)
        with col1:
            age = st.number_input("Age", min_value=10, max_value=100, value=None)
            height = st.number_input("Height (cm)", min_value=100, max_value=250, value=None)
        with col2:
            weight = st.number_input("Weight (kg)", min_value=30, max_value=200, value=None)
            gender = st.selectbox("Gender", ["Select", "Male", "Female", "Other"])
        sleep_hours = st.number_input("Sleep Hours", min_value=0.0, value=None)
        work_type = st.selectbox("Work Type", ["Select", "Desk job", "Field work", "Shift work", "Student"])
        if st.form_submit_button("Continue"):
            if None in [age, height, weight, sleep_hours] or "Select" in [gender, work_type]:
                st.markdown('<div class="error-message">❌ Please complete all fields in Personal Info.</div>', unsafe_allow_html=True)
            else:
                st.session_state.personal_data = locals()
                st.session_state.step = 2

elif st.session_state.step == 2:
    with st.form("exercise_form"):
        activity_level = st.selectbox("Activity Level", ["Select", "Sedentary", "Lightly Active", "Active", "Very Active"])
        activity_type = st.selectbox("Activity Type", ["Select", "Gym", "Walking", "Yoga", "Sports", "Home Workouts"])
        activity_duration = st.number_input("Activity Duration (min)", min_value=0, value=None)
        if st.form_submit_button("Continue"):
            if "Select" in [activity_level, activity_type] or activity_duration is None:
                st.markdown('<div class="error-message">❌ Please complete all fields in Exercise Info.</div>', unsafe_allow_html=True)
            else:
                st.session_state.exercise_data = locals()
                st.session_state.step = 3

elif st.session_state.step == 3:
    with st.form("diet_form"):
        diet = st.selectbox("Diet", ["Select", "Vegetarian", "Non-Vegetarian", "Vegan", "Keto"])
        allergies = st.selectbox("Allergies", ["Select", "Gluten", "Dairy", "Nuts", "Soy"])
        condition = st.selectbox("Health Condition", ["Select", "Diabetes", "Asthma", "Hypertension"])
        if st.form_submit_button("Continue"):
            if "Select" in [diet, allergies, condition]:
                st.markdown('<div class="error-message">❌ Please complete all fields in Diet Info.</div>', unsafe_allow_html=True)
            else:
                st.session_state.diet_data = locals()
                st.session_state.step = 4

elif st.session_state.step == 4:
    with st.form("goal_form"):
        goal = st.selectbox("Fitness Goal", ["Select", "Weight Loss", "Muscle Gain", "Maintenance", "Endurance"])
        target_weight = st.number_input("Target Weight (kg)", min_value=30, value=None)
        timeline = st.number_input("Target Timeline (days)", min_value=1, value=None)
        if st.form_submit_button("Get Fitness Plan"):
            if "Select" in [goal] or None in [target_weight, timeline]:
                st.markdown('<div class="error-message">❌ Please complete all fields to generate your plan.</div>', unsafe_allow_html=True)
            else:
                with st.spinner("Generating your personalized plan..."):
                    try:
                        p = st.session_state.personal_data
                        e = st.session_state.exercise_data
                        d = st.session_state.diet_data

                        bmi = round(p['weight'] / ((p['height'] / 100) ** 2), 1)
                        input_data = np.array([[
                            p['age'],
                            label_encoders['Gender'].transform([p['gender']])[0],
                            p['height'], p['weight'], bmi,
                            label_encoders['Activity_Level'].transform([e['activity_level']])[0],
                            label_encoders['Activity_Type'].transform([e['activity_type']])[0],
                            e['activity_duration'],
                            label_encoders['Work_Type'].transform([p['work_type']])[0],
                            p['sleep_hours'],
                            label_encoders['Diet'].transform([d['diet']])[0],
                            label_encoders['Allergies'].transform([d['allergies']])[0],
                            label_encoders['Health_Condition'].transform([d['condition']])[0],
                            label_encoders['Fitness_Goal'].transform([goal])[0],
                            target_weight, timeline
                        ]])

                        prediction = model.predict(input_data)[0]
                        calories, protein, exercise_time = map(int, prediction)

                        tips = [
                            f"➞Fitness Goal: {goal}",
                            "✅ Reduce refined carbs and do cardio" if goal == "Weight Loss" else
                            "✅ Increase protein intake and strength training" if goal == "Muscle Gain" else
                            "✅ Focus on HIIT and stamina building" if goal == "Endurance" else
                            "✅ Maintain current diet & routine",
                            f"🩺 Manage condition: {d['condition']}" if d['condition'] != "None" else "",
                            "💤 Increase sleep for better recovery" if p['sleep_hours'] < 7.5 else ""
                        ]

                        st.markdown(f"""
                        <div class='plan-box'>
                            <h4>📋 Your Personalized Fitness Plan</h4>
                            <ul>
                                <li><strong>Calories/day:</strong> {calories} kcal</li>
                                <li><strong>Protein/day:</strong> {protein} g</li>
                                <li><strong>Exercise Duration:</strong> {exercise_time} min/day</li>
                                <li><strong>Recommended Sleep:</strong> 7.5 hrs/day</li>
                            </ul>
                        </div>
                        """, unsafe_allow_html=True)

                        st.markdown(f"""
                        <div class='tips-box'>
                            <strong>💡 Pro Tips:</strong><br>
                            {'<br>'.join(filter(None, tips))}
                        </div>
                        """, unsafe_allow_html=True)

                        fig = go.Figure(go.Bar(
                            x=[calories, protein, exercise_time],
                            y=['Calories', 'Protein (g)', 'Exercise (min)'],
                            orientation='h',
                            marker=dict(color=['#FF6B6B', '#6BCB77', '#4D96FF']),
                            width=[0.45, 0.45, 0.45]
                        ))
                        fig.update_layout(
                            title='📊 Fitness Plan Breakdown',
                            height=350,
                            xaxis=dict(tickmode='linear', dtick=100, title='Amount', range=[0, max(calories, protein, exercise_time) + 100])
                        )
                        st.plotly_chart(fig)

                    except Exception as e:
                        st.markdown(f'<div class="error-message">❌ Error: {e}</div>', unsafe_allow_html=True)