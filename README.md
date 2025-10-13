# AI Diet and Workout Planner

An AI-powered application that generates personalized diet and workout plans based on user inputs using Google's Generative AI.

## Features

- Clean and intuitive Streamlit UI
- Personalized diet plan generation based on user preferences and goals
- Customized workout plan creation considering equipment availability and experience
- PDF export functionality for generated plans
- Responsive design for various screen sizes

## Requirements

- Python 3.8 or higher
- Google Generative AI API key

## Installation

1. Clone this repository or download the files
2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

1. Run the Streamlit application:

```bash
streamlit run app.py

or

python -m streamlit run app.py
```

2. Enter your Google Generative AI API key when prompted

   - If you don't have an API key, you can get one from [Google AI Studio](https://makersuite.google.com/app/apikey)

3. Fill in your personal details, preferences, and goals in the sidebar
4. Click "Generate Plans" to create your personalized diet and workout plans
5. View your plans in the respective tabs
6. Export your plans as PDF files using the export buttons

## Project Structure

- `app.py`: Main Streamlit application
- `pdf_generator.py`: Module for generating PDF files
- `requirements.txt`: List of required Python packages
- `generated_pdfs/`: Directory where generated PDF files are stored

## Customization

You can customize the application by:

- Modifying the prompts in the `generate_diet_plan` and `generate_workout_plan` functions
- Adjusting the UI styling in the CSS section
- Adding additional input fields for more personalized plans
