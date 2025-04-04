import streamlit as st
import requests

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

CLIMATIQ_API_KEY = "YOUR_API_KEY"
CLIMATIQ_ENDPOINT = "https://beta4.api.climatiq.io/estimate"

def get_api_estimate(activity_id, parameters):
    if CLIMATIQ_API_KEY == "YOUR_API_KEY":
        st.warning("⚠️ API key not set. Some features may not work.")
        return {}

    headers = {"Authorization": f"Bearer {CLIMATIQ_API_KEY}"}
    response = requests.post(CLIMATIQ_ENDPOINT, json={"activity_id": activity_id, "parameters": parameters}, headers=headers)
    return response.json() if response.status_code == 200 else {}

# Set wide layout and page name
st.set_page_config(layout="wide", page_title="Personal Carbon Calculator")

st.title("Personal Carbon Calculator App ⚠️")

# User inputs
st.subheader("🌍 Your Country")
country = st.selectbox("Select", ["India"])

col1, col2 = st.columns(2)

with col1:
    st.subheader("🚗 Type of Vehicle")
    vehicle_type = st.selectbox("Select Vehicle", ["Bike", "Car", "Bus"], key="vehicle_input")

    st.subheader("🚗 Daily commute distance (in km)")
    distance = st.slider("Distance", 0.0, 100.0, key="distance_input")

    st.subheader("💡 Monthly electricity consumption (in kWh)")
    electricity = st.slider("Electricity", 0.0, 1000.0, key="electricity_input")

with col2:
    st.subheader("🛫 Flights taken per year")
    flights = st.number_input("Flights", min_value=0, value=0, key="flights_input")

    st.subheader("🏠 Home size (sq meters)")
    home_size = st.number_input("Home Size", min_value=10, value=10, key="home_size_input")

    st.subheader("🍽️ Number of meals per day")
    meals = st.number_input("Meals", min_value=0, value=0, key="meals_input")

    st.subheader("🗑️ Waste generated per week (in kg)")
    waste = st.slider("Waste", 0.0, 100.0, key="waste_input")

# Normalize inputs
distance = max(0, distance) * 365
flights = max(0, flights) * 250  # Approximate CO2 per flight (kg)
electricity = max(0, electricity) * 12
meals = max(0, meals) * 365
waste = max(0, waste) * 52

# Calculate carbon emissions
transportation_emissions = EMISSION_FACTORS[country][vehicle_type] * distance
flight_emissions = flights / 1000 if flights > 0 else 0  # Convert kg to tonnes
electricity_emissions = EMISSION_FACTORS[country]["Electricity"] * electricity / 1000
diet_emissions = EMISSION_FACTORS[country]["Diet"] * meals / 1000
waste_emissions = EMISSION_FACTORS[country]["Waste"] * waste / 1000

total_emissions = round(
    transportation_emissions / 1000 + flight_emissions + electricity_emissions + diet_emissions + waste_emissions, 2
)

# Debugging Output
st.write("Debug Info:")
st.write(f"Vehicle: {vehicle_type}, Distance: {distance}, Electricity: {electricity}")
st.write(f"Flights: {flights}, Meals: {meals}, Waste: {waste}")

if st.button("Calculate CO2 Emissions"):
    with st.container():
        st.header("Results")
        col3, col4 = st.columns(2)

        with col3:
            st.subheader("Carbon Emissions by Category")
            st.info(f"🚗 Transportation ({vehicle_type}): {transportation_emissions / 1000:.2f} tonnes CO2 per year")
            st.info(f"✈️ Flights: {flight_emissions:.2f} tonnes CO2 per year")
            st.info(f"💡 Electricity: {electricity_emissions:.2f} tonnes CO2 per year")
            st.info(f"🍽️ Diet: {diet_emissions:.2f} tonnes CO2 per year")
            st.info(f"🗑️ Waste: {waste_emissions:.2f} tonnes CO2 per year")

        with col4:
            st.subheader("Total Carbon Footprint")
            st.success(f"🌍 Your total carbon footprint is: {total_emissions} tonnes CO2 per year")
            st.warning(
                "In 2021, CO2 emissions per capita for India was 1.9 tons of CO2 per capita. "
                "Between 1972 and 2021, CO2 emissions per capita of India grew substantially from 0.39 to 1.9 tons of CO2 per capita."
            )

