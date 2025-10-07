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

# Custom CSS - Light Theme
st.markdown("""
<style>
    .main {
        background-color: #ffffff;
    }
    .stApp {
        max-width: 1200px;
        margin: 0 auto;
    }
    h1, h2, h3 {
        color: #2c3e50;
        font-family: 'Segoe UI', sans-serif;
    }
    .stButton button {
        background-color: #3498db;
        color: white;
        border-radius: 8px;
    }
    .stButton button:hover {
        background-color: #2980b9;
        color: white;
    }
    .plan-container {
        background-color: #f8f9fa;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
        border-left: 5px solid #3498db;
    }
    .sidebar .stButton button {
        background-color: #3498db;
    }
    .developer-info {
        background-color: #f8f9fa;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
        margin-bottom: 20px;
        border: 1px solid #e9ecef;
    }
    .social-links a {
        color: #3498db;
        text-decoration: none;
        margin-right: 15px;
    }
    .social-links a:hover {
        text-decoration: underline;
    }
    .how-it-works {
        background-color: #f8f9fa;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
        border: 1px solid #e9ecef;
    }
    .step-container {
        display: flex;
        align-items: center;
        margin-bottom: 10px;
    }
    .step-number {
        background-color: #3498db;
        color: white;
        width: 25px;
        height: 25px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        margin-right: 10px;
        font-weight: bold;
    }
    /* Fix for sidebar white box */
    div[data-testid="stVerticalBlock"] div[style*="flex-direction: column"] {
        background-color: transparent !important;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state variables
if 'generated_diet_plan' not in st.session_state:
    st.session_state.generated_diet_plan = None
if 'generated_workout_plan' not in st.session_state:
    st.session_state.generated_workout_plan = None
if 'personal_info' not in st.session_state:
    st.session_state.personal_info = {}

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
    # Custom CSS for styling
    st.markdown("""
    <style>
    /* Using default Streamlit theme with minimal custom styling */
    .stButton>button {
        width: 100%;
    }
    </style>
    """, unsafe_allow_html=True)
    
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
    
    # Display welcome section and developer info if no plans have been generated yet
    if 'generated_diet_plan' not in st.session_state or not st.session_state.generated_diet_plan:
        st.markdown("## 👋 Welcome to AI Diet & Workout Planner")
        st.markdown("""
        This app creates personalized diet and workout plans tailored to your specific needs and goals.
        Simply fill out your information in the sidebar and click 'Generate Plans' to get started!
        """)
        
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("How It Works")
            st.write("1. Enter your personal details in the sidebar")
            st.write("2. Click 'Generate Plans' button")
            st.write("3. View your personalized diet and workout plans")
            st.write("4. Download PDF versions for offline use")
        
        with col2:
            st.subheader("About the Developer")
            st.write("Created by Vraj Patel")
            
            st.write("[GitHub](https://github.com/pvraj1011) | [LinkedIn](https://linkedin.com/in/vraj10) | [Portfolio](https://vrajpatel10.vercel.app)")
            
            st.write("I'm passionate about health, fitness, and using AI to help people achieve their wellness goals.")
    
    # Sidebar for user inputs
    with st.sidebar:
        st.header("Enter Your Information!!")
        
        # Personal Details Section
        with st.expander("👤 Personal Details", expanded=True):
            st.text_input("Name (optional)", key="name", help="Enter your full name")
            
            # Age and Gender in one row
            col1, col2 = st.columns(2)
            with col1:
                age = st.number_input("Age *", min_value=15, max_value=100, value=30, 
                                    help="Your current age in years")
            with col2:
                gender = st.selectbox("Gender *", ["Male", "Female", "Other"])
            
            # Height and Weight in one row with same input style
            col1, col2 = st.columns(2)
            with col1:
                height = st.number_input("Height (cm)*", min_value=100, max_value=250, value=170,
                                       help="Your height in centimeters")
            with col2:
                weight = st.number_input("Weight (kg)*", min_value=30, max_value=250, value=70,
                                       help="Your current weight in kilograms")
        
        # Activity and Goals Section
        with st.expander("🎯 Activity & Goals", expanded=True):
            activity_level = st.select_slider(
                "Activity Level *",
                options=["Sedentary", "Lightly Active", "Moderately Active", "Very Active", "Extremely Active"],
                value="Moderately Active",
                help="How active you are in your daily life"
            )
            diet_goal = st.selectbox(
                "Diet Goal *",
                ["Weight Loss", "Weight Maintenance", "Weight Gain", "Muscle Building", "Improved Energy", "Better Health"],
                help="What you want to achieve with your diet"
            )
            fitness_goal = st.selectbox(
                "Fitness Goal *",
                ["Weight Loss", "Muscle Building", "Endurance", "Flexibility", "General Fitness", "Strength"],
                help="What you want to achieve with your fitness routine"
            )
        
        # Diet Preferences Section
        with st.expander("🍽️ Diet Preferences"):
            diet_type = st.selectbox(
                "Diet Type *",
                ["No Restrictions", "Vegetarian", "Vegan", "Pescatarian", "Keto", "Paleo", "Mediterranean"],
                help="Select your dietary preference"
            )
            
            allergies = st.multiselect(
                "Allergies/Intolerances (optional)",
                ["None", "Dairy", "Eggs", "Peanuts", "Tree Nuts", "Shellfish", "Wheat", "Soy", "Fish"],
                default=["None"],
                help="Select any food allergies or intolerances you have"
            )
            
            foods_to_avoid = st.text_area(
                "Foods to Avoid (optional)",
                help="List any specific foods you want to avoid, separated by commas"
            )
            
            meals_per_day = st.slider(
                "Meals per Day *",
                min_value=3,
                max_value=6,
                value=3,
                help="Number of meals you prefer per day"
            )
        
        # Workout Specifics Section
        with st.expander("💪 Workout Specifics", expanded=False):
            available_equipment = st.multiselect(
                "Available Equipment",
                ["None", "Dumbbells", "Resistance Bands", "Treadmill", "Exercise Bike", "Full Gym Access", "Pull-up Bar", "Yoga Mat"],
                default=["None"],
                help="Equipment you have access to for workouts"
            )
            time_available = st.slider("Time Available Per Day (minutes)", 15, 120, 45,
                                     help="How much time you can dedicate to exercise each day")
            exercise_experience = st.select_slider(
                "Exercise Experience",
                options=["Beginner", "Intermediate", "Advanced"],
                value="Beginner",
                help="Your current level of exercise experience"
            )
            exercise_preferences = st.multiselect("Exercise Preferences (optional)",
                                                ["Cardio", "Strength Training", "HIIT", "Yoga", "Pilates", "Calisthenics"],
                                                default=["Cardio", "Strength Training"],
                                                help="Types of exercises you prefer")
        
        # Medical Information Section
        with st.expander("🏥 Medical Information", expanded=False):
            medical_conditions = st.text_area("Medical Conditions (optional)", "",
                                            help="Any medical conditions that might affect your diet or exercise routine")
            medications = st.text_area("Medications (optional)", "",
                                     help="Any medications you're taking that might affect your diet or workout plan")
            injuries = st.text_area("Injuries/Limitations (optional)", "",
                                  help="Any injuries or physical limitations to consider")
        
        # Generate button
        generate_button = st.button("Generate Plans", use_container_width=True)
    
    # Main content area
    if generate_button:
        with st.spinner("Generating your personalized plans... This may take a minute."):
            # Get name from session state (from text_input with key="name")
            user_name = st.session_state.get('name', '')
            
            # Collect user data
            user_data = {
                'age': age,
                'gender': gender,
                'height': height,
                'weight': weight,
                'activity_level': activity_level,
                'diet_goal': diet_goal,
                'fitness_goal': fitness_goal,
                'dietary_restrictions': diet_type,
                'food_preferences': foods_to_avoid,
                'allergies': ', '.join(allergies),
                'available_equipment': ', '.join(available_equipment),
                'time_available': time_available,
                'exercise_experience': exercise_experience,
                'medical_conditions': medical_conditions
            }
            
            # IMPORTANT: Store personal info in session state for PDF generation
            st.session_state.personal_info = {
                'name': user_name if user_name else 'User',
                'age': age,
                'gender': gender,
                'height': height,
                'weight': weight,
                'activity_level': activity_level,
                'diet_goal': diet_goal,
                'fitness_goal': fitness_goal
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
        
        # Create formatted user details string (do this once, outside the buttons)
        personal_info = st.session_state.get('personal_info', {})
        user_details = f"""<b>Name:</b> {personal_info.get('name', 'User')}<br/>
<b>Age:</b> {personal_info.get('age', 'N/A')} years | <b>Gender:</b> {personal_info.get('gender', 'N/A')}<br/>
<b>Height:</b> {personal_info.get('height', 'N/A')} cm | <b>Weight:</b> {personal_info.get('weight', 'N/A')} kg<br/>
<b>Activity Level:</b> {personal_info.get('activity_level', 'N/A')}<br/>
<b>Diet Goal:</b> {personal_info.get('diet_goal', 'N/A')} | <b>Fitness Goal:</b> {personal_info.get('fitness_goal', 'N/A')}"""
        
        with col1:
            if st.button("Generate Diet Plan PDF"):
                st.session_state.diet_pdf_path = generate_pdf(
                    st.session_state.generated_diet_plan,
                    f"Diet_Plan_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                    "Personalized Diet Plan",
                    user_details
                )
                st.success("Diet Plan PDF generated successfully!")
            
            # Only show download button if PDF has been generated
            if st.session_state.diet_pdf_path:
                with open(st.session_state.diet_pdf_path, "rb") as f:
                    st.download_button(
                        label="📥 Download Diet Plan",
                        data=f,
                        file_name=os.path.basename(st.session_state.diet_pdf_path),
                        mime="application/pdf",
                        use_container_width=True
                    )
        
        with col2:
            if st.button("Generate Workout Plan PDF"):
                st.session_state.workout_pdf_path = generate_pdf(
                    st.session_state.generated_workout_plan,
                    f"Workout_Plan_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                    "Personalized Workout Plan",
                    user_details
                )
                st.success("Workout Plan PDF generated successfully!")
            
            # Only show download button if PDF has been generated
            if st.session_state.workout_pdf_path:
                with open(st.session_state.workout_pdf_path, "rb") as f:
                    st.download_button(
                        label="📥 Download Workout Plan",
                        data=f,
                        file_name=os.path.basename(st.session_state.workout_pdf_path),
                        mime="application/pdf",
                        use_container_width=True
                    )
        
        with col3:
            if st.button("Generate Combined PDF"):
                combined_content = "# PERSONALIZED DIET PLAN\n\n" + st.session_state.generated_diet_plan + "\n\n# PERSONALIZED WORKOUT PLAN\n\n" + st.session_state.generated_workout_plan
                st.session_state.combined_pdf_path = generate_pdf(
                    combined_content,
                    f"Combined_Plan_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                    "Combined Diet & Workout Plan",
                    user_details
                )
                st.success("Combined PDF generated successfully!")
            
            # Only show download button if PDF has been generated
            if st.session_state.combined_pdf_path:
                with open(st.session_state.combined_pdf_path, "rb") as f:
                    st.download_button(
                        label="📥 Download Combined Plan",
                        data=f,
                        file_name=os.path.basename(st.session_state.combined_pdf_path),
                        mime="application/pdf",
                        use_container_width=True
                    )

if __name__ == "__main__":
    main()