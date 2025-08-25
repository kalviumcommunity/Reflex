import os
import json # NEW: Import the JSON library
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

def generate_game_commentary(event_type: str, player_name: str, game_name: str) -> dict: # NEW: Return type is now a dictionary
    """
    Generates structured commentary as a JSON object.

    Args:
        event_type: The type of event that occurred.
        player_name: The name of the player.
        game_name: The name of the game.

    Returns:
        A dictionary containing the AI-generated commentary and hashtags.
    """
    try:
        model = genai.GenerativeModel('gemini-pro')

        config = genai.types.GenerationConfig(
            temperature=0.8,
            max_output_tokens=100
        )

        system_prompt = (
            "You are 'Reflex,' a witty esports commentator AI. Your responses must be "
            "in a valid JSON format."
        )

        # NEW: The prompt now explicitly asks for a JSON structure
        user_prompt = (
            f"For the event '{event_type}' by player '{player_name}' in the game {game_name}, "
            "generate a commentary line and three relevant hashtags. "
            "Provide the output as a JSON object with two keys: 'commentary_line' and 'suggested_hashtags'."
        )

        full_prompt = f"{system_prompt}\n\n{user_prompt}"

        response = model.generate_content(full_prompt, generation_config=config)
        
        # NEW: Parse the JSON string into a Python dictionary
        return json.loads(response.text)

    except Exception as e:
        return {"error": str(e)}

def main():
    """
    Main function to set up the API and run an example.
    """
    print("Initializing AI Game Analyst...")
    setup_api_key()
    print("Setup complete.\n")

    # --- Example: Structured JSON Output ---
    commentary_data = generate_game_commentary(
        event_type="Flawless Round",
        player_name="Sova",
        game_name="Valorant"
    )

    print("--- Structured Commentary (JSON) ---")
    if "error" in commentary_data:
        print(f"An error occurred: {commentary_data['error']}")
    else:
        # NEW: Access data using dictionary keys
        print(f"Commentary: {commentary_data.get('commentary_line')}")
        print(f"Hashtags: {commentary_data.get('suggested_hashtags')}")

if __name__ == "__main__":
    main()