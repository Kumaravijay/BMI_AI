import streamlit as st
import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

# Add this right after your imports
if 'bmi' not in st.session_state:
    st.session_state.bmi = 0

# --- Page and API Configuration ---
st.set_page_config(page_title="BMI Calculator", page_icon="🚻")

# It's good practice to check if the API key exists
api_key = os.getenv("Google_API_KEY")
if api_key:
    genai.configure(api_key=api_key)
else:
    # This won't stop the app, just informs the user.
    st.warning("Google API Key not found. AI features will be disabled.")


# --- UI Setup ---
st.title("BMI Calculator ")
st.header("Know Your Numbers, Empower Your Health.")
st.subheader("A single number is the first step on your wellness journey.")
st.markdown("---")


# --- Sidebar for Inputs ---
st.sidebar.header("Your Details")

# Use st.number_input for better numeric entry and assign the result to variables
# This is a more robust way to handle numeric inputs than st.text_input
height = st.sidebar.number_input("Enter your height in cm")
weight = st.sidebar.number_input("Enter your weight in kg")


# --- Calculation Logic ---
if st.sidebar.button("Calculate BMI"):
    if height > 0 and weight > 0:
        st.session_state.bmi = weight / ((height / 100) ** 2) # <--- FIXED LINE
        st.sidebar.success(f"Your BMI is {st.session_state.bmi:.2f}")
        # ... Now, update the rest of this block to use st.session_state.bmi
        st.sidebar.success(f"Your BMI is {st.session_state.bmi:.2f}")
        st.header(f"Result")
        st.write(f"A BMI of **{st.session_state.bmi:.2f}** is considered:")
        
        if st.session_state.bmi < 18.5:
            st.info("Underweight")
        elif 18.5 <= st.session_state.bmi < 25:
            st.success("Normal weight")
        elif 25 <= st.session_state.bmi < 30:
            st.warning("Overweight")
        else:
            st.error("Obese")

    else:
        st.sidebar.error("Please enter a positive value for height and weight.")


input=st.text_input('Ask your question here 🔍')

submit=st.button('Click here 👈')

model=genai.GenerativeModel('gemini-1.5-flash')
    
def generate_result(bmi,input):
    if input is not None:
        prompt=f''' 
        Your are health assistant now so you need to get results based on the fitness or other health related 
        questions.
        Use the bmi{st.session_state.bmi} for suggestion.
        You can suggest some diet to be followed and also some fitness exercise to the user,
        if any medication or medicine related question areasked always mention that 
        'Check with the nearby doctors for the medication'    
        '''
    result=model.generate_content(input+prompt)
    
    return result.text


if submit:
        with st.spinner('Generating response...'):
            response = generate_result(st.session_state.bmi, input)
        st.markdown("Good luck on your wellness journey! Remember, small steps lead to big changes.")
        st.write(response)
