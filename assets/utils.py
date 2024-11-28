import json
from openai import OpenAI
import streamlit as st
import toml


# Initialize the OpenAI client with the API key from the secrets file
api_key = st.secrets["api_key"]
client = OpenAI(api_key=api_key)

# fetch function that will get the requested data from the gpt-3.5-turbo model and provide it in json format
def fetch_random_cities():
    """
    Fetches details about two random cities using the OpenAI API.
    """
    prompt = """
    Provide a JSON object with the following details about two random capitals:
    - Name of the capital
    - Country of the capital
    - Distance between the two capitals in kilometers
    - Estimated flight time between the cities in hours
    - Fun fact about each cit
    - A detailed breakdown of walking and swimming time, assuming:
      - Humans walk 5 km per hour, walking 8 hours per day.
      - Swimming speed is 2 km per hour, swimming 6 hours per day.
      - The walking time is calculated based on an approximate percentage of the total distance being over land, e.g., 70% land and 30% sea. Adjust walking and swimming times accordingly.
    
    Example:
    {
        "capital_1": {"name": "Paris", "country": "France", "fun_fact": "Paris has a hidden vineyard in Montmartre."},
        "capital_2": {"name": "New York", "country": "USA", "fun_fact": "New York's Central Park is larger than Monaco."},
        "distance_km": 5837,
        "flight_time_hours": 7.2,
        "walking_swimming_time": "You will need 120 days walking + 60 days swimming."
    }
    """
    try:
        # Create a chat completion request
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a fact and geography expert and provide the requested data accurately and you dont favor popular capitals over others, the probability is even across all capitals."},
                {"role": "user", "content": prompt},
            ],
            temperature=1.0 #we make it 1.0 to be as random as possible
        )
        # Extract and parse the response content
        content = response.choices[0].message.content.strip()
        return json.loads(content)
    except json.JSONDecodeError:
        return "We are experiencing a server issue, play try again."
    except Exception as e:
        return f"An error occurred: {e}"

if __name__ == "__main__":
    cities_info = fetch_random_cities()
    print("City Details:", cities_info)

# functin that evaluates user input and compares it using gpt 3.5 

def evaluate_guess(city_details, user_guess):
    """
    Evaluate the user's guess in the context of the city game.

    Args:
        city_details (dict): Dictionary containing city details and distance information.
        user_guess (str): The city guessed by the user.

    Returns:
        dict: Evaluation result including correctness, capital status, and distance.
    """
    # Construct the prompt for the OpenAI model
    prompt = f"""
    Reference City: {city_details['capital_1']['name']}
    Correct City: {city_details['capital_2']['name']}
    User Guess: {user_guess}

    Evaluate the user's guess following these instructions:
    -Is the guess correct?
    -Is it a capital of a country?
    -is the guessed city a real city (valid)? 
    -if the city does not exist, return null.  
    -if the city is a valid city (real) calculate the distance in kilometers from the reference city to the guessed city.
    -Provide the output in this JSON format:
    {{
        "guess_correct": <true/false>,
        "is_capital": <true/false>,
        "valid_city": <true/false>,
        "distance_to_reference_km": <distance or null>
    }}
    """

    try:
        # Use the chat completion API
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a geography and distance expert that evaluates accurately if a certain input is a city, capital, and how far is it from the given capital."},
                {"role": "user", "content": prompt},
            ],
            temperature=0  # Set temperature for deterministic responses
        )
        # Extract and parse the response content
        content = response.choices[0].message.content.strip()
        result = json.loads(content)  # Parse JSON-like string into a Python dictionary

        # Additional check: If the city is not valid, set the distance to None
        if not result.get("valid_city", False):
            result["distance_to_reference_km"] = None
        return result

    except json.JSONDecodeError:
        return {"error": "Failed to parse the response. Please try again."}
    except Exception as e:
        return {"error": str(e)}