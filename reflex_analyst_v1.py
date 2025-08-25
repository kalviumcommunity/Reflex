import os
import google.generativeai as genai

def setup_api_key():
    """
    Loads the Google API key from an environment variable and configures the SDK.
    """
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError(
            "API key not found. Please set the GOOGLE_API_KEY environment variable."
        )
    genai.configure(api_key=api_key)

def generate_game_commentary(event_type: str, player_name: str, game_name: str, style: str = 'hype', length: str = 'short') -> str:
    """
    Generates commentary with controls for style and length.

    Args:
        event_type: The type of event that occurred.
        player_name: The name of the player.
        game_name: The name of the game.
        style: The creative style ('hype' or 'analytical').
        length: The desired output length ('short' or 'long').

    Returns:
        The AI-generated commentary as a string.
    """
    try:
        model = genai.GenerativeModel('gemini-pro')

        # Set temperature based on style
        temperature = 0.9 if style.lower() == 'hype' else 0.2
        
        # --- NEW: Set max tokens based on length ---
        # This demonstrates the "Tokens and Tokenization" concept.
        max_tokens = 25 if length.lower() == 'short' else 75
        
        config = genai.types.GenerationConfig(
            temperature=temperature,
            top_p=0.95,
            max_output_tokens=max_tokens
        )

        system_prompt = (
            "You are 'Reflex,' a witty esports commentator AI who creates "
            "exciting descriptions of gameplay moments."
        )

        user_prompt = (
            f"In {game_name}, player '{player_name}' just got a '{event_type}'. "
            f"Generate one commentary line in an '{style}' tone. "
            f"Keep the response {length}."
        )

        full_prompt = f"{system_prompt}\n\n{user_prompt}"

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

    # --- Example 1: Short Commentary ---
    short_commentary = generate_game_commentary(
        event_type="Flawless Round",
        player_name="Sova",
        game_name="Valorant",
        style="hype",
        length="short"
    )
    print("--- Short Hype Commentary (Max 25 Tokens) ---")
    print(f"Generated: {short_commentary}\n")

    # --- Example 2: Long Commentary ---
    long_commentary = generate_game_commentary(
        event_type="Winning Kill",
        player_name="Wraith",
        game_name="Apex Legends",
        style="analytical",
        length="long"
    )
    print("--- Long Analytical Commentary (Max 75 Tokens) ---")
    print(f"Generated: {long_commentary}\n")

if __name__ == "__main__":
    main()