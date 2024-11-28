import streamlit as st
import matplotlib.pyplot as plt


def stats():
    st.title("Game Statistics")

    if 'rounds' in st.session_state and st.session_state.rounds:
        # Extract data for plotting
        round_labels = [round_data.get('label', f"Game {i+1}") for i, round_data in enumerate(st.session_state.rounds)]
        target_distances = [round_data['target_distance'] for round_data in st.session_state.rounds]
        total_differences = [round_data['total_difference'] for round_data in st.session_state.rounds]
        num_guesses = [round_data['num_guesses'] for round_data in st.session_state.rounds]

        # Plot 1: Target Distance vs Total Difference
        st.subheader("Total Differences Across Rounds")
        fig1, ax1 = plt.subplots()
        ax1.bar(round_labels, total_differences, color='blue', alpha=0.7)
        ax1.set_title("Total Differences Across Rounds")
        ax1.set_ylabel("Total Difference (km)")
        ax1.set_xlabel("Rounds")
        plt.xticks(rotation=45)
        st.pyplot(fig1)

        # Plot 2: Target Distance vs Number of Guesses
        st.subheader("Number of Guesses Per Round")
        fig2, ax2 = plt.subplots()
        ax2.bar(round_labels, num_guesses, color='green', alpha=0.7)
        ax2.set_title("Number of Guesses Per Round")
        ax2.set_ylabel("Number of Guesses")
        ax2.set_xlabel("Rounds")
        plt.xticks(rotation=45)
        st.pyplot(fig2)

        # Detailed Round Stats
        st.subheader("Detailed Round Statistics")
        for i, round_data in enumerate(st.session_state.rounds, start=1):
            st.write(f"**{round_data['label']}:**")
            st.write(f"- Target Distance: {round_data['target_distance']} km")
            st.write(f"- Total Difference Across Guesses: {round_data['total_difference']:.2f} km")
            st.write(f"- Number of Guesses: {round_data['num_guesses']}")
            st.write("---")
    else:
        st.write("No completed rounds yet. Start playing to see your stats!")


if __name__ == "__main__":
    stats()
