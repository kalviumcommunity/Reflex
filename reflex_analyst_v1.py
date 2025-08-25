import os
import google.generativeai as genai

def setup_api_key():
    """
    Loads the Google API key from an environment variable and configures the SDK.
    Raises an error if the key is not found.
    """
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError(
            "API key not found. Please set the GOOGLE_API_KEY environment variable."
        )
    genai.configure(api_key=api_key)

def generate_game_commentary(event_type: str, player_name: str, game_name: str) -> str:
    """
    Generates commentary for a specific game event using a dynamic prompt.

    Args:
        event_type: The type of event that occurred (e.g., "Triple Kill").
        player_name: The name of the player.
        game_name: The name of the game.

    Returns:
        The AI-generated commentary as a string.
    """
    try:
        # Initialize the model
        model = genai.GenerativeModel('gemini-pro')

        # This is the System Prompt that defines the AI's personality.
        system_prompt = (
            "You are 'Reflex,' a witty and insightful esports commentator AI. "
            "You specialize in creating short, exciting, and shareable text descriptions "
            "of gameplay moments for social media."
        )

        # This is the User Prompt, built dynamically with the function's inputs.
        user_prompt = (
            f"In the game {game_name}, the player '{player_name}' just performed the event: "
            f"'{event_type}'. Generate one hype commentary line for this."
        )

        full_prompt = f"{system_prompt}\n\n{user_prompt}"

        # Generate the content and return the text
        response = model.generate_content(full_prompt)
        return response.text

    except Exception as e:
        # Provide a helpful error message if the API call fails
        return f"An error occurred: {e}"

def main():
    """
    Main function to set up the API and run a few examples.
    """
    print("Initializing AI Game Analyst...")
    setup_api_key()
    print("Setup complete.\n")

    # --- Example 1: Valorant Event ---
    event1_commentary = generate_game_commentary(
        event_type="Clutch Ace",
        player_name="TenZ",
        game_name="Valorant"
    )
    print("--- Valorant Event ---")
    print(f"Generated Commentary: {event1_commentary}\n")

    # --- Example 2: Apex Legends Event ---
    event2_commentary = generate_game_commentary(
        event_type="Squad Wipe",
        player_name="ImperialHal",
        game_name="Apex Legends"
    )
    print("--- Apex Legends Event ---")
    print(f"Generated Commentary: {event2_commentary}\n")



if __name__ == "__main__":
    main()