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

def generate_game_commentary(event_type: str, player_name: str, game_name: str, style: str = 'hype') -> str:
    """
    Generates commentary for a specific game event using a dynamic prompt and creative styles.

    Args:
        event_type: The type of event that occurred.
        player_name: The name of the player.
        game_name: The name of the game.
        style: The desired commentary style ('hype' or 'analytical').

    Returns:
        The AI-generated commentary as a string.
    """
    try:
        model = genai.GenerativeModel('gemini-pro')

        # --- NEW: Configure generation based on style ---
        # This demonstrates the "Temperature" and "Top_P" concepts.
        if style.lower() == 'hype':
            # High temperature for more creative, less predictable responses.
            config = genai.types.GenerationConfig(temperature=0.9, top_p=0.95)
        else: # 'analytical'
            # Low temperature for more factual, focused responses.
            config = genai.types.GenerationConfig(temperature=0.2, top_p=0.8)

        system_prompt = (
            "You are 'Reflex,' a witty esports commentator AI who creates short, exciting "
            "descriptions of gameplay moments."
        )

        user_prompt = (
            f"In the game {game_name}, the player '{player_name}' just performed the event: "
            f"'{event_type}'. Generate one commentary line in an '{style}' tone."
        )

        full_prompt = f"{system_prompt}\n\n{user_prompt}"

        # --- NEW: Pass the configuration to the model ---
        response = model.generate_content(full_prompt, generation_config=config)
        return response.text

    except Exception as e:
        return f"An error occurred: {e}"

def main():
    """
    Main function to set up the API and run a few examples.
    """
    print("Initializing AI Game Analyst...")
    setup_api_key()
    print("Setup complete.\n")

    # --- Example 1: Hype Style ---
    hype_commentary = generate_game_commentary(
        event_type="Team Wipe",
        player_name="Bangalore",
        game_name="Apex Legends",
        style="hype"
    )
    print("--- Hype Commentary ---")
    print(f"Generated: {hype_commentary}\n")

    # --- Example 2: Analytical Style ---
    analytical_commentary = generate_game_commentary(
        event_type="Clutch Defuse",
        player_name="Cypher",
        game_name="Valorant",
        style="analytical"
    )
    print("--- Analytical Commentary ---")
    print(f"Generated: {analytical_commentary}\n")

if __name__ == "__main__":
    main()