import streamlit as st
from datetime import datetime, timedelta
import pandas as pd
import matplotlib.pyplot as plt

# Function to calculate total water drank
def calculate_total_water(history):
    return sum(entry['quantity'] for entry in history)

# Function to add water to history
def add_water(history, quantity):
    time_now = datetime.now().strftime("%H:%M:%S")
    history.append({'time': time_now, 'quantity': quantity})

# Function to reset water intake at midnight
def reset_water_intake():
    now = datetime.now()
    return now.replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=1)

# Main function to run the Streamlit app
def main():
    st.title("Daily Drinking Water Tracker")

    # Initialize history and last reset time
    if 'history' not in st.session_state:
        st.session_state.history = []
    if 'last_reset' not in st.session_state:
        st.session_state.last_reset = reset_water_intake()

    # Reset water intake at midnight
    if datetime.now() >= st.session_state.last_reset:
        st.session_state.history = []
        st.session_state.last_reset = reset_water_intake()

    # Display total drank water today
    total_water_placeholder = st.empty()
    total_water_today = calculate_total_water(st.session_state.history)
    total_water_placeholder.header("Total Drank Water Today")
    total_water_placeholder.subheader(f"**{total_water_today} ml**")

    # Slider to add water
    st.header("Add Water")
    # Define the steps for the slider
    step_size = 100
    steps = [i for i in range(100, 1001, step_size)]
    add_water_amount = st.slider("Select Amount to Add (ml)", min_value=100, max_value=1000, step=step_size, value=100)

    if st.button("Add"):
        add_water(st.session_state.history, add_water_amount)
        total_water_today = calculate_total_water(st.session_state.history)
        total_water_placeholder.subheader(f"**{total_water_today} ml**")
        st.success(f"Added {add_water_amount} ml of water!")

    # Current day's history
    st.subheader("Today's Water Intake History")
    for entry in st.session_state.history:
        st.write(f"- **{entry['time']}**: {entry['quantity']} ml")

    # Display history
    st.header("Water Drank Today")
    # Calculate past day's total drank water
    past_day = datetime.now() - timedelta(days=1)
    past_day_data = [(entry['time'], entry['quantity']) for entry in st.session_state.history if datetime.strptime(entry['time'], "%H:%M:%S").date() == past_day.date()]
    if past_day_data:
        past_day_df = pd.DataFrame(past_day_data, columns=['Time', 'Quantity'])
        past_day_total = past_day_df['Quantity'].sum()
        st.subheader("Past Day's Total Drank Water")
        st.write(f"Total: {past_day_total} ml")
        # Show past day's total drank water as a bar plot
        st.bar_chart(past_day_df.set_index('Time'))

if __name__ == "__main__":
    main()
