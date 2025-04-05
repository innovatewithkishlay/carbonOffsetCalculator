import streamlit as st
import requests
import certifi
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Expanded emission factors (example values, replace with API integration)
EMISSION_FACTORS = {
    "India": {"Bike": 0.05, "Car": 0.14, "Bus": 0.03, "Electricity": 0.82, "Diet": 1.25, "Waste": 0.1},
}

# Gemini API Configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")  # Load API key from .env file
GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta2/models/gemini-pro:generateMessage"

# Streamlit App Configuration
st.set_page_config(layout="wide", page_title="Personal Carbon Calculator")
st.title("Personal Carbon Calculator 🌱")

# Sidebar Navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Home", "Carbon Calculator", "Blog", "Chatbot"])

if page == "Home":
    st.header("🌍 Welcome to the Personal Carbon Calculator")
    st.write("This app helps you calculate your carbon footprint based on your lifestyle choices.")
    st.write("Use the Carbon Calculator to estimate your emissions and explore our blog for tips on reducing your impact.")

elif page == "Carbon Calculator":
    st.sidebar.header("User Inputs")
    country = st.sidebar.selectbox("🌍 Select Your Country", list(EMISSION_FACTORS.keys()))
    
    vehicle_type = st.sidebar.selectbox("🚗 Type of Vehicle", ["Bike", "Car", "Bus"])
    distance = st.sidebar.slider("🚗 Daily commute distance (in km)", 0.0, 100.0, 10.0)
    
    electricity = st.sidebar.slider("💡 Monthly electricity consumption (in kWh)", 0.0, 1000.0, 200.0)
    meals = st.sidebar.number_input("🍽️ Meals per day", min_value=0, value=3)
    waste = st.sidebar.slider("🗑️ Waste generated per week (in kg)", 0.0, 100.0, 5.0)
    
    # Calculating Carbon Footprint
    distance = max(0, distance) * 365
    electricity = max(0, electricity) * 12
    meals = max(0, meals) * 365
    waste = max(0, waste) * 52
    
    transport_emissions = EMISSION_FACTORS[country][vehicle_type] * distance / 1000
    electricity_emissions = EMISSION_FACTORS[country]["Electricity"] * electricity / 1000
    diet_emissions = EMISSION_FACTORS[country]["Diet"] * meals / 1000
    waste_emissions = EMISSION_FACTORS[country]["Waste"] * waste / 1000
    
    total_emissions = round(transport_emissions + electricity_emissions + diet_emissions + waste_emissions, 2)
    
    if st.sidebar.button("Calculate CO2 Emissions"):
        st.subheader("🌍 Your Carbon Footprint Summary")
        st.info(f"🚗 Transport ({vehicle_type}): {transport_emissions:.2f} tonnes CO2 per year")
        st.info(f"💡 Electricity: {electricity_emissions:.2f} tonnes CO2 per year")
        st.info(f"🍽️ Diet: {diet_emissions:.2f} tonnes CO2 per year")
        st.info(f"🗑️ Waste: {waste_emissions:.2f} tonnes CO2 per year")
        st.success(f"🌍 Total Carbon Footprint: {total_emissions} tonnes CO2 per year")

elif page == "Blog":
    st.header("📖 Blog: Understanding Carbon Emissions")
    st.write("Reducing your carbon footprint is essential for a sustainable future.")
    st.subheader("🌿 Simple Ways to Lower Your Carbon Footprint")
    st.write("1. Use public transport or carpool whenever possible.")
    st.write("2. Reduce electricity usage by turning off appliances when not in use.")
    st.write("3. Opt for a plant-based diet to reduce diet-related emissions.")
    st.write("4. Recycle and compost to minimize waste emissions.")
    st.write("5. Support renewable energy initiatives.")

elif page == "Chatbot":
    st.header("💬 AI Chatbot")
    st.write("Ask me anything about carbon footprint, sustainability, or climate change!")

    # Add a "Clear Chat" button at the top
    clear_chat = st.button("🗑️ Clear Chat", key="clear_chat", help="Clear the chat history")
    if clear_chat:
        st.session_state.chat_history = []

    # Initialize session state to store chat history
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Chat container for displaying messages
    chat_container = st.container()

    # Display chat history
    with chat_container:
        for message in st.session_state.chat_history:
            if message["role"] == "user":
                st.markdown(
                    f"<div style='text-align: right; background-color: #DCF8C6; padding: 10px; border-radius: 10px; margin: 5px;'>"
                    f"<strong>You:</strong> {message['content']}</div>",
                    unsafe_allow_html=True,
                )
            elif message["role"] == "bot":
                st.markdown(
                    f"<div style='text-align: left; background-color: #F1F0F0; padding: 10px; border-radius: 10px; margin: 5px;'>"
                    f"<strong>Bot:</strong> {message['content']}</div>",
                    unsafe_allow_html=True,
                )

    # Separator line
    st.markdown("---")

    # Fixed input box and send button at the bottom
    st.markdown(
        """
        <style>
        .fixed-input-box {
            position: fixed;
            bottom: 0;
            left: 0;
            width: 100%;
            background-color: white;
            padding: 10px;
            box-shadow: 0px -2px 5px rgba(0, 0, 0, 0.1);
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    with st.container():
        st.markdown('<div class="fixed-input-box">', unsafe_allow_html=True)
        col1, col2 = st.columns([4, 1])
        with col1:
            user_input = st.text_input(
                "Type your message here:",
                key="user_input",
                placeholder="Ask me anything...",
                label_visibility="collapsed",
            )
        with col2:
            send_button = st.button("Send", use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # Handle user input and send to backend
    if send_button and user_input:
        # Call the Node.js chatbot backend
        chatbot_backend_url = "http://localhost:5001/chatbot"
        try:
            # Send user input to the chatbot backend
            response = requests.post(chatbot_backend_url, json={"prompt": user_input})
            response_data = response.json()

            if response.status_code == 200:
                # Get the chatbot's reply
                bot_reply = response_data.get("reply", "No reply received.")
            else:
                bot_reply = f"Error: {response_data.get('error', 'Unknown error')}"
        except requests.exceptions.RequestException as e:
            bot_reply = f"Error: {str(e)}"

        # Add user input and bot reply to chat history
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        st.session_state.chat_history.append({"role": "bot", "content": bot_reply})
