import streamlit as st
import pandas as pd

# Example data for demonstration (replace with st.session_state.game_data)
games_data = pd.DataFrame({
    "City_Given-Target_City": ["Tokyo-Berlin", "Game 2", "Game 3", "Game 4", "Game 5"],
    "Guesses": [3, 4, 6, 2, 8],
    "Distance_Target_Named": ["Berlin", "Madrid", "Paris", "Lisbon", "Rome"],
    "How_Far_Off": [200, 500, 1000, 2, 300],
})

# Update metrics
average_guesses_current = games_data["Guesses"].mean()
number_of_rounds = len(games_data)
average_far_off = games_data["How_Far_Off"].mean()

# Display stats
st.title("How did you do? Let's review your stats.")

# Bar chart for guesses
st.bar_chart(
    data=games_data,
    x="City_Given-Target_City",
    y="Guesses",
    use_container_width=True
)

# Metric display
col1, col2 = st.columns(2)
col1.metric("Average Guesses per Game", f"{average_guesses_current:.2f}")
col2.metric("Total Rounds", number_of_rounds)

col1, col2 = st.columns(2)
col1.metric("On average, how far off were your guesses?", f"{average_far_off:.2f} km")
col2.metric("Non-Capitals Named", games_data["Distance_Target_Named"].str.count("non-capital").sum())
