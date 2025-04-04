import streamlit as st
import requests

# Streamlit App Configuration
st.set_page_config(layout="wide", page_title="Personal Carbon Calculator")
st.title("Personal Carbon Calculator 🌱")

# Sidebar for Navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Home", "Carbon Calculator", "Blog"])

# API Details
API_URL = "https://www.carboninterface.com/api/v1/estimates"  # Correct API
API_KEY = "1kTR7NvPWNhVbf6fCA67w"  # Replace with your actual key
HEADERS = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}

# Function to Get Carbon Emission from API
def get_carbon_emission(vehicle_type, distance):
    data = {
        "type": "vehicle",
        "vehicle_model_id": vehicle_type,  # Change this if needed
        "distance_value": distance,
        "distance_unit": "km"
    }
    try:
        response = requests.post(API_URL, json=data, headers=HEADERS)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"⚠️ API Error: {e}")
        return None

if page == "Home":
    st.header("Welcome to the Personal Carbon Calculator! 🌍")
    st.write("This tool helps you estimate your carbon footprint based on daily activities.")
    st.write("Navigate to the **Carbon Calculator** section to begin.")

elif page == "Carbon Calculator":
    st.sidebar.header("User Inputs")

    vehicle_type = st.sidebar.text_input("🚗 Enter Vehicle Model ID (e.g., toyota_camry_2019)")
    distance = st.sidebar.number_input("🚗 Distance traveled per year (in km)", min_value=1, value=1000)

    if st.sidebar.button("Calculate CO2 Emissions"):
        if vehicle_type:
            result = get_carbon_emission(vehicle_type, distance)
            if result:
                st.subheader("🌍 Your Carbon Footprint Summary")
                st.json(result)  # Display raw API result
            else:
                st.error("⚠️ Failed to fetch emission data.")
        else:
            st.warning("Please enter a valid vehicle model ID.")

elif page == "Blog":
    st.header("🌍 Learn About Carbon Footprint Reduction")
    st.write("Reducing your carbon footprint helps combat climate change. Here are some tips:")
    st.markdown("- 🚴 Use bicycles or public transport instead of cars.")
    st.markdown("- 💡 Switch to energy-efficient appliances.")
    st.markdown("- 🥗 Reduce meat consumption and opt for plant-based diets.")
    st.markdown("- ♻️ Recycle and reduce waste production.")

st.sidebar.info("Developed with ❤️ using Streamlit")
