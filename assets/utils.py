import json
from openai import OpenAI

# Initialize the OpenAI client with your API key
client = OpenAI(api_key="sk-svcacct-8dcUrtOCCiU3jO3ysuZ29D-DeYPWd3Vk_BKZf4s5Ya-UuWekdRLkG2LzQGCKYwIT3BlbkFJ0gsmApPqJnvNjSnyvcQI7UinZ3vehK1O3RJCCCG3qAjxxlUxbFXiQTG2fZwu_AA")

def fetch_random_cities():
    """
    Fetches details about two random cities using the OpenAI API.
    """
    prompt = """
    Provide a JSON object with the following details about two random cities:
    - Name of the city
    - Country of the city
    - Distance between the cities in kilometers
    - Estimated flight time between the cities in hours
    - Fun fact about each city
    - A detailed breakdown of walking and swimming time, assuming:
      - Humans walk 5 km per hour, walking 8 hours per day.
      - Swimming speed is 2 km per hour, swimming 6 hours per day.
      - The walking time is calculated based on an approximate percentage of the total distance being over land, e.g., 70% land and 30% sea. Adjust walking and swimming times accordingly.
    
    Example:
    {
        "city1": {"name": "Paris", "country": "France", "fun_fact": "Paris has a hidden vineyard in Montmartre."},
        "city2": {"name": "New York", "country": "USA", "fun_fact": "New York's Central Park is larger than Monaco."},
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
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt},
            ]
        )
        # Extract and parse the response content
        content = response.choices[0].message.content.strip()
        return json.loads(content)
    except json.JSONDecodeError:
        return "Error: Unable to parse the response as JSON."
    except Exception as e:
        return f"An error occurred: {e}"

if __name__ == "__main__":
    cities_info = fetch_random_cities()
    print("City Details:", cities_info)


def guess_eval(target_distance, user_guess):

    guess_quality = abs(target_distance - user_guess)
    is_correct = target_distance == user_guess
    return is_correct, guess_quality
    
# Example distances
target_distance = 5837  # Actual distance in kilometers
user_guess = 6000       # User's guessed distance

# Evaluate the guess
result = guess_eval(target_distance, user_guess)
print("Result:", result)  # Output: (False, 163)

