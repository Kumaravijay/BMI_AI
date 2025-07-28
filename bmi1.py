import streamlit as st
import plotly.graph_objects as go

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="BMI Calculator",
    page_icon="💪",
    layout="centered",
    initial_sidebar_state="auto",
)

# --- CUSTOM CSS ---
st.markdown("""
<style>
    /* General App Styling */
    .stApp {
        background-color: #1a1a2e;
        color: #e0e0e0;
    }

    /* Main Title */
    h1 {
        font-family: 'Garamond', serif;
        color: #ffffff;
        text-align: center;
        padding-bottom: 10px;
    }
    
    /* Subheader */
    .st-emotion-cache-1y4p8pa {
        text-align: center;
        font-style: italic;
        color: #b3b3b3;
    }

    /* Sidebar Styling */
    .st-emotion-cache-16txtl3 {
        background-color: #16213e;
        padding: 20px;
    }
    
    /* Markdown links in sidebar */
    .st-emotion-cache-16txtl3 a {
        color: #e94560 !important;
        text-decoration: none;
    }
    .st-emotion-cache-16txtl3 a:hover {
        text-decoration: underline;
    }

</style>
""", unsafe_allow_html=True)


# --- GAUGE CHART FUNCTION ---
def create_bmi_gauge(bmi):
    """Creates a Plotly gauge chart for the given BMI value."""
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = bmi,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "BMI Gauge", 'font': {'size': 24, 'color': 'white'}},
        number= {'font': {'color': 'white'}},
        gauge = {
            'axis': {'range': [None, 50], 'tickwidth': 1, 'tickcolor': "white", 'tickfont': {'color': 'white'}},
            'bar': {'color': "rgba(0,0,0,0)"}, # invisible bar
            'bgcolor': "#16213e",
            'borderwidth': 2,
            'bordercolor': "#e0e0e0",
            'steps': [
                {'range': [0, 18.5], 'color': '#3b71ca'},   # Blue
                {'range': [18.5, 25], 'color': '#198754'}, # Green
                {'range': [25, 30], 'color': '#ffc107'},   # Yellow
                {'range': [30, 50], 'color': '#dc3545'}    # Red
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.9,
                'value': bmi
            }
        }))
    fig.update_layout(
        paper_bgcolor="#1a1a2e",
        font={'color': "white", 'family': "Arial"},
        height=350
    )
    return fig


# --- HEADER SECTION ---
st.title("Interactive BMI Calculator 🚻")
st.markdown("##### Know Your Numbers, Empower Your Health.")
st.markdown("A single number is the first step on your wellness journey.")
st.markdown("---")


# --- SIDEBAR FOR INPUTS ---
with st.sidebar:
    st.header("Your Details")
    # Using sliders for a more interactive input
    height = st.slider("Height (cm)", min_value=50.0, max_value=250.0, value=170.0, step=1.0)
    weight = st.slider("Weight (kg)", min_value=10.0, max_value=300.0, value=70.0, step=0.5)
    
    st.markdown("---")
    st.write("Made with ❤️ by an AI enthusiast")


# --- MAIN CONTENT & REAL-TIME CALCULATION ---
if height > 0 and weight > 0:
    # BMI Calculation
    bmi = weight / ((height / 100) ** 2)

    # Display the gauge chart
    st.plotly_chart(create_bmi_gauge(bmi), use_container_width=True)

    # Interpretation of the BMI
    st.subheader(f"Your BMI is {bmi:.2f}")
    if bmi < 18.5:
        st.info("This is considered **Underweight**.")
        with st.expander("See advice"):
            st.write("""
                - Consider eating more frequent, nutrient-dense meals.
                - Incorporate strength training to build lean muscle mass.
                - Consult a nutritionist for a personalized plan.
            """)
    elif 18.5 <= bmi < 25:
        st.success("This is within the **Normal** weight range.")
        with st.expander("See advice"):
            st.write("""
                - Continue with your balanced diet and regular exercise.
                - Focus on maintaining your healthy habits for long-term wellness.
            """)
    elif 25 <= bmi < 30:
        st.warning("This is considered **Overweight**.")
        with st.expander("See advice"):
            st.write("""
                - Focus on a balanced diet with portion control.
                - Aim for at least 150 minutes of moderate aerobic activity per week.
                - Strength training can help increase metabolism.
            """)
    else:
        st.error("This is considered **Obese**.")
        with st.expander("See advice"):
            st.write("""
                - It is highly recommended to consult a healthcare provider for a comprehensive management plan.
                - Focus on gradual, sustainable lifestyle changes rather than quick fixes.
            """)
else:
    st.error("Please use the sliders in the sidebar to enter a valid height and weight.")

