import streamlit as st
import requests

# Expanded emission factors (example values, replace with API integration)
EMISSION_FACTORS = {
    "India": {"Bike": 0.05, "Car": 0.14, "Bus": 0.03, "Electricity": 0.82, "Diet": 1.25, "Waste": 0.1},
}

# Streamlit App Configuration
st.set_page_config(layout="wide", page_title="Personal Carbon Calculator")
st.title("Personal Carbon Calculator 🌱")

# Sidebar Navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Home", "Carbon Calculator", "Blog"])

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
