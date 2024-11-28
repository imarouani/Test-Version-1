import streamlit as st
import pandas as pd
from assets.utils import fetch_random_cities, evaluate_guess

# Initialize session state variables
if "game_data" not in st.session_state:
    st.session_state.game_data = pd.DataFrame(
        columns=["City_Given-Target_City", "Guesses", "Distance_Target_Named", "How_Far_Off"]
    )
if "current_round" not in st.session_state:
    st.session_state.current_round = None
if "guesses_this_round" not in st.session_state:
    st.session_state.guesses_this_round = 0
if "non_capitals_this_round" not in st.session_state:
    st.session_state.non_capitals_this_round = 0
if "round_complete" not in st.session_state:
    st.session_state.round_complete = False

# Start a new round
def start_new_round():
    st.session_state.current_round = fetch_random_cities()  # Fetch data for the round
    st.session_state.guesses_this_round = 0
    st.session_state.non_capitals_this_round = 0
    st.session_state.round_complete = False

# Check if the round needs to start
if st.session_state.current_round is None:
    start_new_round()

# Display the game prompt
current_data = st.session_state.current_round
reference_city = current_data["capital_1"]["name"]
reference_country = current_data["capital_1"]["country"]
distance = current_data["distance_km"]

st.title("Guess the City!")
st.write(f"Guess which capital is {distance} km away from {reference_city}, {reference_country}.")

# Input for the user's guess
user_guess = st.text_input("Enter your guess:", key="user_guess")
if user_guess:
    # Evaluate the guess
    evaluation = evaluate_guess(current_data, user_guess)
    st.session_state.guesses_this_round += 1

    # Track non-capital guesses
    if not evaluation["is_capital"]:
        st.session_state.non_capitals_this_round += 1

    # Provide feedback to the user
    if evaluation["guess_correct"]:
        st.success("Congrats, that's the right answer!")
        st.session_state.round_complete = True
    else:
        st.error(f"Wrong! {user_guess} is {'not a capital.' if not evaluation['is_capital'] else ''}")
        st.info(f"You were {evaluation['distance_to_reference_km']} km off.")

    # Update game data
    if st.session_state.round_complete:
        new_entry = {
            "City_Given-Target_City": f"{reference_city}-{current_data['capital_2']['name']}",
            "Guesses": st.session_state.guesses_this_round,
            "Distance_Target_Named": user_guess,
            "How_Far_Off": evaluation.get("distance_to_reference_km", 0),
        }
        st.session_state.game_data = pd.concat(
            [st.session_state.game_data, pd.DataFrame([new_entry])],
            ignore_index=True
        )

        # Display "Play Again" button
        if st.button("Play Again"):
            start_new_round()

# Display stats after the round
if st.session_state.round_complete:
    st.subheader("Round Summary")
    st.write("Here are the stats for this round:")
    st.write(f"Guesses: {st.session_state.guesses_this_round}")
    st.write(f"Non-Capitals Named: {st.session_state.non_capitals_this_round}")
