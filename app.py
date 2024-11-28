from assets.utils import fetch_random_cities, guess_eval
import streamlit as st


def main():
    st.title("Guess the Distance Between Two Cities")

    # Initialize session state variables
    if 'game_data' not in st.session_state:
        st.session_state.game_data = fetch_random_cities()
        st.session_state.guesses = []
        st.session_state.rounds = []

    game_data = st.session_state.game_data

    # Handle potential errors in fetching data
    if isinstance(game_data, str):
        st.error(game_data)
        return

    city1 = game_data['city1']
    city2 = game_data['city2']
    target_distance = game_data['distance_km']

    # Display current round information
    st.write(f"Guess the distance between **{city1['name']}**, {city1['country']} and **{city2['name']}**, {city2['country']}.")
    st.write(f"Fun fact about {city1['name']}: {city1['fun_fact']}")
    st.write(f"Fun fact about {city2['name']}: {city2['fun_fact']}")

    with st.form(key='guess_form'):
        user_guess = st.number_input("Enter your guess in kilometers:", min_value=0)
        submit_button = st.form_submit_button(label='Submit')

    if submit_button:
        is_correct, difference = guess_eval(target_distance, user_guess)
        st.session_state.guesses.append(difference)

        if is_correct:
            st.success("Congratulations! Your guess is correct.")
            # Create a label for the round
            round_label = f"Game {len(st.session_state.rounds) + 1}: {city1['name']}, {city2['name']}"
            # Save the current round's stats
            st.session_state.rounds.append({
                'label': round_label,
                'target_distance': target_distance,
                'total_difference': sum(st.session_state.guesses),
                'num_guesses': len(st.session_state.guesses)
            })
            # Reset for the next round
            st.session_state.game_data = fetch_random_cities()
            st.session_state.guesses = []
        else:
            st.info(f"Your guess was off by {difference:.2f} km. Try again!")

    # Display statistics
    st.write("---")
    st.subheader("Statistics")
    
    # Current round stats
    if st.session_state.guesses:
        st.write("**Current Round:**")
        st.write(f"- Total Guesses: {len(st.session_state.guesses)}")
        st.write(f"- Total Difference Across Guesses: {sum(st.session_state.guesses):.2f} km")
    
    # Previous rounds stats
    if st.session_state.rounds:
        st.write("**Previous Rounds:**")
        for i, round_data in enumerate(st.session_state.rounds, start=1):
            # Safely access 'label' with a fallback
            round_label = round_data.get('label', f"Game {i}")
            st.write(f"**{round_label}:**")
            st.write(f"- Target Distance: {round_data['target_distance']} km")
            st.write(f"- Total Difference Across Guesses: {round_data['total_difference']:.2f} km")
            st.write(f"- Number of Guesses: {round_data['num_guesses']}")
            st.write("---")

if __name__ == "__main__":
    main()
