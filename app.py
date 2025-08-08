import streamlit as st
import openai

# ---- CONFIG ----
st.set_page_config(page_title="Car Fit & Upgrade Advisor", page_icon="🚗", layout="centered")

# ---- APP HEADER ----
st.title("🚗 Car Fit & Upgrade Advisor")
st.markdown("Compare your current car to luxury upgrade options, using NERD 2.3 scoring + regional fit rules.")

# ---- INPUTS ----
# Your current car (pre-filled with Arteon R specs)
baseline_car = {
    "name": "VW Arteon R",
    "length_mm": 4862,
    "width_mm": 1871,
    "cargo_l": 563
}

# Candidate car options
cars_data = {
    "Audi A7": {"length_mm": 4969, "width_mm": 1908, "cargo_l": 535},
    "Mercedes E-Class": {"length_mm": 4949, "width_mm": 1880, "cargo_l": 540},
    "BMW 5 Series": {"length_mm": 5060, "width_mm": 1900, "cargo_l": 520},
    "Genesis G80": {"length_mm": 4995, "width_mm": 1925, "cargo_l": 480},
    "Volvo S90": {"length_mm": 4963, "width_mm": 1879, "cargo_l": 500},
    "Mercedes CLS": {"length_mm": 4988, "width_mm": 1890, "cargo_l": 505}
}

region = st.selectbox("🌍 Region", ["Korea", "Portugal"])
selected_cars = st.multiselect("Choose cars to compare", list(cars_data.keys()), default=["Audi A7"])

weights = {
    "practicality": 10,
    "reliability": 9,
    "interior": 8,
    "sound_system": 7,
    "driving_dynamics": 7,
    "seat_comfort": 6,
    "looks": 6,
    "fuel_economy": 5,
    "cost_value": 5
}

# ---- API KEY ----
st.markdown("### 🔑 OpenAI API Key")
api_key = st.text_input("Enter your OpenAI API key", type="password")
if api_key:
    openai.api_key = api_key

# ---- BUTTON ----
if st.button("Compare Cars"):
    if not api_key:
        st.error("Please enter your OpenAI API key first.")
    else:
        # Build prompt for OpenAI
        prompt = f"""
        You are a car upgrade advisor for Vincent.
        Base car: {baseline_car}
        Candidate cars: {[{c: cars_data[c]} for c in selected_cars]}
        Region: {region}
        NERD 2.3 weights: {weights}
        Penalize excessive width for Korea and excessive length for Portugal.
        Compare each candidate against the Arteon R in:
        - Dimensional fit
        - Luxury upgrade delta
        - Practicality
        - Final Buy/Hold recommendation
        Return a clear human-friendly summary.
        """

        try:
            response = openai.ChatCompletion.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a car upgrade advisor."},
                    {"role": "user", "content": prompt}
                ]
            )
            st.markdown("### 📊 Results")
            st.write(response.choices[0].message.content)

        except Exception as e:
            st.error(f"Error: {e}")
