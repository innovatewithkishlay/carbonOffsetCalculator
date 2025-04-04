import streamlit as st
import requests

CLIMATIQ_API_KEY = "4K1SZNTKRH6H13R0ERP4CYX48W"  # Replace with your actual API key
CLIMATIQ_ENDPOINT = "https://beta4.api.climatiq.io/estimate"

# Fetch real emission factors from Climatiq API
def get_emission_factor(activity_id, parameters):
    if CLIMATIQ_API_KEY == "YOUR_API_KEY":
        st.warning("⚠️ API key not set. Some features may not work.")
        return 0  # Return zero if API is unavailable

    headers = {"Authorization": f"Bearer {CLIMATIQ_API_KEY}"}
    response = requests.post(CLIMATIQ_ENDPOINT, json={"activity_id": activity_id, "parameters": parameters}, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        return data.get("co2e", 0)  # Get CO2 equivalent
    else:
        st.error("❌ Failed to fetch emission data from API.")
        return 0

# Streamlit UI Setup
st.set_page_config(layout="wide", page_title="Personal Carbon Calculator")
st.title("🌱 Real-time Carbon Footprint Calculator")

# User Inputs
st.subheader("🌍 Select Your Country")
country = st.selectbox("Select", ["India", "USA", "UK", "Canada"])

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

# Fetch real emission data from API
transportation_emissions = get_emission_factor("passenger_vehicle-transport", {"distance": distance, "vehicle_type": vehicle_type})
flight_emissions = get_emission_factor("air_travel", {"flights": flights})
electricity_emissions = get_emission_factor("electricity_consumption", {"consumption": electricity})
diet_emissions = get_emission_factor("food_diet", {"meals": meals})
waste_emissions = get_emission_factor("waste_disposal", {"waste": waste})

# Calculate total emissions
total_emissions = round(transportation_emissions + flight_emissions + electricity_emissions + diet_emissions + waste_emissions, 2)

# Display Results
if st.button("Calculate CO2 Emissions"):
    with st.container():
        st.header("Results")
        col3, col4 = st.columns(2)

        with col3:
            st.subheader("Carbon Emissions by Category")
            st.info(f"🚗 Transportation ({vehicle_type}): {transportation_emissions:.2f} tonnes CO2 per year")
            st.info(f"✈️ Flights: {flight_emissions:.2f} tonnes CO2 per year")
            st.info(f"💡 Electricity: {electricity_emissions:.2f} tonnes CO2 per year")
            st.info(f"🍽️ Diet: {diet_emissions:.2f} tonnes CO2 per year")
            st.info(f"🗑️ Waste: {waste_emissions:.2f} tonnes CO2 per year")

        with col4:
            st.subheader("Total Carbon Footprint")
            st.success(f"🌍 Your total carbon footprint is: {total_emissions} tonnes CO2 per year")
