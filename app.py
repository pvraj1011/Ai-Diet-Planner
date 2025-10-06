import streamlit as st
import os
from dotenv import load_dotenv
import google.generativeai as genai
from pdf_generator import generate_pdf
from datetime import datetime

# Load environment variables
load_dotenv()

# Get API key from environment variables
api_key = os.getenv("GOOGLE_API_KEY")

# Configure page
st.set_page_config(
    page_title="AI Diet & Workout Planner",
    page_icon="🥗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main {
        background-color: #f8f9fa;
    }
    .stApp {
        max-width: 1200px;
        margin: 0 auto;
    }
    h1, h2, h3 {
        color: #2E7D32;
    }
    .stButton button {
        background-color: #2E7D32;
        color: white;
    }
    .stButton button:hover {
        background-color: #1B5E20;
        color: white;
    }
    .plan-container {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state variables
if 'generated_diet_plan' not in st.session_state:
    st.session_state.generated_diet_plan = None
if 'generated_workout_plan' not in st.session_state:
    st.session_state.generated_workout_plan = None

# Configure Google Generative AI with the API key
if api_key:
    genai.configure(api_key=api_key)

def generate_diet_plan(user_data):
    """Generate a diet plan based on user data using Google's Generative AI"""
    try:
        model = genai.GenerativeModel('gemini-2.0-flash-001')
        
        prompt = f"""
        Create a detailed, personalized 7-day diet plan for a person with the following characteristics:
        - Age: {user_data['age']}
        - Gender: {user_data['gender']}
        - Height: {user_data['height']} cm
        - Weight: {user_data['weight']} kg
        - Activity Level: {user_data['activity_level']}
        - Diet Goal: {user_data['diet_goal']}
        - Dietary Restrictions: {user_data['dietary_restrictions']}
        - Food Preferences: {user_data['food_preferences']}
        - Allergies: {user_data['allergies']}
        - Medical Conditions: {user_data['medical_conditions']}
        
        The diet plan should:
        1. Include 3 main meals (breakfast, lunch, dinner) and 2 snacks per day
        2. Specify portion sizes and approximate calories for each meal
        3. Ensure nutritional balance with appropriate macronutrients
        4. Respect all dietary restrictions and allergies
        5. Support their goal of {user_data['diet_goal']}
        6. Include a brief explanation of why this plan suits their needs
        7. Include a shopping list for the ingredients needed
        
        Format the response in a clean, organized way with clear headings for each day and meal.
        """
        
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        st.error(f"Error generating diet plan: {str(e)}")
        return None

def generate_workout_plan(user_data):
    """Generate a workout plan based on user data using Google's Generative AI"""
    try:
        model = genai.GenerativeModel('gemini-2.0-flash-001')
        
        prompt = f"""
        Create a detailed, personalized 7-day workout plan for a person with the following characteristics:
        - Age: {user_data['age']}
        - Gender: {user_data['gender']}
        - Height: {user_data['height']} cm
        - Weight: {user_data['weight']} kg
        - Activity Level: {user_data['activity_level']}
        - Fitness Goal: {user_data['fitness_goal']}
        - Available Equipment: {user_data['available_equipment']}
        - Time Available Per Day: {user_data['time_available']} minutes
        - Exercise Experience: {user_data['exercise_experience']}
        - Medical Conditions: {user_data['medical_conditions']}
        
        The workout plan should:
        1. Include appropriate exercises for each day with sets, reps, and rest periods
        2. Have a mix of cardio, strength, and flexibility exercises as appropriate
        3. Include warm-up and cool-down routines
        4. Be appropriate for their experience level
        5. Respect any medical conditions or limitations
        6. Support their goal of {user_data['fitness_goal']}
        7. Include a brief explanation of why this plan suits their needs
        8. Include rest days as appropriate
        
        Format the response in a clean, organized way with clear headings for each day and exercise.
        """
        
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        st.error(f"Error generating workout plan: {str(e)}")
        return None

def main():
    st.title("🥗 AI Diet & Workout Planner")
    
    # Check if API key is available
    if not api_key:
        st.error("API Key not found. Please add your Google Generative AI API key to the .env file.")
        st.markdown("You need a Google Generative AI API key to use this application. "
                  "If you don't have one, you can get it from [Google AI Studio](https://makersuite.google.com/app/apikey).")
        st.markdown("1. Open the `.env` file in this project directory")
        st.markdown("2. Add your API key after `GOOGLE_API_KEY=`")
        st.markdown("3. Save the file and restart the application")
        return
    
    # Sidebar for user inputs
    with st.sidebar:
        st.header("📋 Your Information")
        
        # Personal Information
        st.subheader("Personal Details")
        age = st.number_input("Age", min_value=15, max_value=100, value=30)
        gender = st.selectbox("Gender", ["Male", "Female", "Other"])
        height = st.number_input("Height (cm)", min_value=100, max_value=250, value=170)
        weight = st.number_input("Weight (kg)", min_value=30, max_value=250, value=70)
        
        # Activity and Goals
        st.subheader("Activity & Goals")
        activity_level = st.select_slider(
            "Activity Level",
            options=["Sedentary", "Lightly Active", "Moderately Active", "Very Active", "Extremely Active"],
            value="Moderately Active"
        )
        diet_goal = st.selectbox(
            "Diet Goal",
            ["Weight Loss", "Weight Maintenance", "Weight Gain", "Muscle Building", "Improved Energy", "Better Health"]
        )
        fitness_goal = st.selectbox(
            "Fitness Goal",
            ["Weight Loss", "Muscle Building", "Endurance", "Flexibility", "General Fitness", "Strength"]
        )
        
        # Diet Specifics
        st.subheader("Diet Specifics")
        dietary_restrictions = st.multiselect(
            "Dietary Restrictions",
            ["None", "Vegetarian", "Vegan", "Gluten-Free", "Dairy-Free", "Keto", "Paleo", "Low-Carb", "Low-Fat"],
            default=["None"]
        )
        food_preferences = st.text_area("Food Preferences (comma separated)", "")
        allergies = st.text_area("Allergies (comma separated)", "")
        
        # Workout Specifics
        st.subheader("Workout Specifics")
        available_equipment = st.multiselect(
            "Available Equipment",
            ["None", "Dumbbells", "Resistance Bands", "Treadmill", "Exercise Bike", "Full Gym Access", "Pull-up Bar", "Yoga Mat"],
            default=["None"]
        )
        time_available = st.slider("Time Available Per Day (minutes)", 15, 120, 45)
        exercise_experience = st.select_slider(
            "Exercise Experience",
            options=["Beginner", "Intermediate", "Advanced"],
            value="Beginner"
        )
        
        # Medical Information
        st.subheader("Medical Information")
        medical_conditions = st.text_area("Medical Conditions (comma separated)", "")
        
        # Generate button
        generate_button = st.button("Generate Plans", use_container_width=True)
    
    # Main content area
    if generate_button:
        with st.spinner("Generating your personalized plans... This may take a minute."):
            # Collect user data
            user_data = {
                'age': age,
                'gender': gender,
                'height': height,
                'weight': weight,
                'activity_level': activity_level,
                'diet_goal': diet_goal,
                'fitness_goal': fitness_goal,
                'dietary_restrictions': ', '.join(dietary_restrictions),
                'food_preferences': food_preferences,
                'allergies': allergies,
                'available_equipment': ', '.join(available_equipment),
                'time_available': time_available,
                'exercise_experience': exercise_experience,
                'medical_conditions': medical_conditions
            }
            
            # Generate plans
            diet_plan = generate_diet_plan(user_data)
            workout_plan = generate_workout_plan(user_data)
            
            if diet_plan and workout_plan:
                st.session_state.generated_diet_plan = diet_plan
                st.session_state.generated_workout_plan = workout_plan
    
    # Display generated plans
    if st.session_state.generated_diet_plan and st.session_state.generated_workout_plan:
        tab1, tab2 = st.tabs(["Diet Plan", "Workout Plan"])
        
        with tab1:
            st.markdown("## 🍽️ Your Personalized Diet Plan")
            with st.container():
                st.markdown('<div class="plan-container">', unsafe_allow_html=True)
                st.markdown(st.session_state.generated_diet_plan)
                st.markdown('</div>', unsafe_allow_html=True)
        
        with tab2:
            st.markdown("## 💪 Your Personalized Workout Plan")
            with st.container():
                st.markdown('<div class="plan-container">', unsafe_allow_html=True)
                st.markdown(st.session_state.generated_workout_plan)
                st.markdown('</div>', unsafe_allow_html=True)
        
        # Export to PDF
        st.markdown("### 📄 Export Your Plans")
        col1, col2, col3 = st.columns([1, 1, 1])
        
        # Store PDF paths in session state
        if "diet_pdf_path" not in st.session_state:
            st.session_state.diet_pdf_path = None
        if "workout_pdf_path" not in st.session_state:
            st.session_state.workout_pdf_path = None
        if "combined_pdf_path" not in st.session_state:
            st.session_state.combined_pdf_path = None
        
        with col1:
            if st.button("Generate Diet Plan PDF"):
                st.session_state.diet_pdf_path = generate_pdf(
                    st.session_state.generated_diet_plan,
                    f"Diet_Plan_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                    "Diet Plan"
                )
                st.success("Diet Plan PDF generated successfully!")
            
            # Only show download button if PDF has been generated
            if st.session_state.diet_pdf_path:
                with open(st.session_state.diet_pdf_path, "rb") as f:
                    st.download_button(
                        label="Download Diet Plan PDF",
                        data=f,
                        file_name=os.path.basename(st.session_state.diet_pdf_path),
                        mime="application/pdf"
                    )
        
        with col2:
            if st.button("Generate Workout Plan PDF"):
                st.session_state.workout_pdf_path = generate_pdf(
                    st.session_state.generated_workout_plan,
                    f"Workout_Plan_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                    "Workout Plan"
                )
                st.success("Workout Plan PDF generated successfully!")
            
            # Only show download button if PDF has been generated
            if st.session_state.workout_pdf_path:
                with open(st.session_state.workout_pdf_path, "rb") as f:
                    st.download_button(
                        label="Download Workout Plan PDF",
                        data=f,
                        file_name=os.path.basename(st.session_state.workout_pdf_path),
                        mime="application/pdf"
                    )
        
        with col3:
            if st.button("Generate Combined PDF"):
                combined_content = "# PERSONALIZED DIET PLAN\n\n" + st.session_state.generated_diet_plan + "\n\n# PERSONALIZED WORKOUT PLAN\n\n" + st.session_state.generated_workout_plan
                st.session_state.combined_pdf_path = generate_pdf(
                    combined_content,
                    f"Combined_Plan_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                    "Combined Diet & Workout Plan"
                )
                st.success("Combined PDF generated successfully!")
            
            # Only show download button if PDF has been generated
            if st.session_state.combined_pdf_path:
                with open(st.session_state.combined_pdf_path, "rb") as f:
                    st.download_button(
                        label="Download Combined PDF",
                        data=f,
                        file_name=os.path.basename(st.session_state.combined_pdf_path),
                        mime="application/pdf"
                    )

if __name__ == "__main__":
    main()