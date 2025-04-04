import streamlit as st
st.set_page_config(layout="wide", page_title="Personal Carbon Calculator")

import requests

# Sidebar Navigation
st.sidebar.title("🌍 Navigation")
page = st.sidebar.radio("Go to", ["Home", "Carbon Calculator", "About"])

# Define emission factors (example values, replace with API integration)
EMISSION_FACTORS = {
    "India": {
        "Bike": 0.05,  # kgCO2/km
        "Car": 0.14,  # kgCO2/km
        "Bus": 0.03,  # kgCO2/km
        "Electricity": 0.82,  # kgCO2/kWh
        "Diet": 1.25,  # kgCO2/meal
        "Waste": 0.1  # kgCO2/kg
    }
}
CLIMATIQ_API_KEY = "4K1SZNTKRH6H13R0ERP4CYX48W"
CLIMATIQ_ENDPOINT = "https://beta4.api.climatiq.io/estimate"
# Set wide layout and page title
st.set_page_config(layout="wide", page_title="Personal Carbon Calculator")

# Page Content
if page == "Home":
    st.title("🌍 Welcome to the Carbon Footprint App!")
    st.subheader("📢 Learn how your daily activities impact the environment.")
    st.write("Use the sidebar to navigate to the calculator and estimate your footprint.")

elif page == "Carbon Calculator":
    st.title("Personal Carbon Calculator ⚠️")

    # User inputs
    st.subheader("🌍 Your Country")
    country = st.selectbox("Select", ["India"])

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🚗 Type of Vehicle")
        vehicle_type = st.selectbox("Select Vehicle", ["Bike", "Car", "Bus"])

        st.subheader("🚗 Daily commute distance (in km)")
        distance = st.slider("Distance", 0.0, 100.0)

        st.subheader("💡 Monthly electricity consumption (in kWh)")
        electricity = st.slider("Electricity", 0.0, 1000.0)

    with col2:
        st.subheader("🛫 Flights taken per year")
        flights = st.number_input("Flights", min_value=0, value=0)

        st.subheader("🍽️ Number of meals per day")
        meals = st.number_input("Meals", min_value=0, value=0)

        st.subheader("🗑️ Waste generated per week (in kg)")
        waste = st.slider("Waste", 0.0, 100.0)

    # Normalizing Inputs
    distance = max(0, distance) * 365
    flights = max(0, flights) * 250
    electricity = max(0, electricity) * 12
    meals = max(0, meals) * 365
    waste = max(0, waste) * 52

    # Carbon Emissions Calculation
    transportation_emissions = EMISSION_FACTORS[country][vehicle_type] * distance / 1000
    flight_emissions = flights / 1000
    electricity_emissions = EMISSION_FACTORS[country]["Electricity"] * electricity / 1000
    diet_emissions = EMISSION_FACTORS[country]["Diet"] * meals / 1000
    waste_emissions = EMISSION_FACTORS[country]["Waste"] * waste / 1000

    total_emissions = round(
        transportation_emissions + flight_emissions + electricity_emissions + diet_emissions + waste_emissions, 2
    )

    if st.button("Calculate CO2 Emissions"):
        st.subheader("Results")
        st.info(f"🚗 Transportation ({vehicle_type}): {transportation_emissions:.2f} tonnes CO2 per year")
        st.info(f"✈️ Flights: {flight_emissions:.2f} tonnes CO2 per year")
        st.info(f"💡 Electricity: {electricity_emissions:.2f} tonnes CO2 per year")
        st.info(f"🍽️ Diet: {diet_emissions:.2f} tonnes CO2 per year")
        st.info(f"🗑️ Waste: {waste_emissions:.2f} tonnes CO2 per year")

        st.success(f"🌍 Your total carbon footprint: {total_emissions} tonnes CO2 per year")

elif page == "About":
    st.title("About This App")
    st.write("This app helps users estimate their personal carbon footprint based on their lifestyle choices.")
    st.write("📊 The calculations use predefined emission factors for India.")
    st.write("🔬 Future updates may include integration with real-time carbon data APIs.")
