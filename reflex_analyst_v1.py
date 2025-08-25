import os
import json
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

def generate_game_commentary(event_type: str, player_name: str, game_name: str) -> dict:
    """
    Generates structured commentary as a JSON object.
    """
    try:
        model = genai.GenerativeModel('gemini-pro')
        config = genai.types.GenerationConfig(temperature=0.8, max_output_tokens=100)
        system_prompt = (
            "You are 'Reflex,' a witty esports commentator AI. Your responses must be "
            "in a valid JSON format."
        )
        user_prompt = (
            f"For the event '{event_type}' by player '{player_name}' in the game {game_name}, "
            "generate a commentary line and three relevant hashtags. "
            "Provide the output as a JSON object with two keys: 'commentary_line' and 'suggested_hashtags'."
        )
        full_prompt = f"{system_prompt}\n\n{user_prompt}"
        response = model.generate_content(full_prompt, generation_config=config)
        return json.loads(response.text)
    except Exception as e:
        return {"error": str(e)}

# --- NEW FUNCTION TO DEMONSTRATE STOP SEQUENCE ---
def generate_hype_list(event_type: str, game_name: str) -> str:
    """
    Generates a list of hype phrases and uses a stop sequence to limit the output.

    Args:
        event_type: The type of event that occurred.
        game_name: The name of the game.
    
    Returns:
        A string containing a numbered list of hype phrases.
    """
    try:
        model = genai.GenerativeModel('gemini-pro')

        # NEW: Configure the model with a stop sequence
        # This tells the model to stop generating as soon as it produces "4."
        config = genai.types.GenerationConfig(
            temperature=0.7,
            stop_sequences=['4.']
        )

        prompt = f"For the event '{event_type}' in the game {game_name}, generate a numbered list of hype words or short phrases."
        
        response = model.generate_content(prompt, generation_config=config)
        return response.text

    except Exception as e:
        return f"An error occurred: {e}"


def main():
    """
    Main function to set up the API and run examples.
    """
    print("Initializing AI Game Analyst...")
    setup_api_key()
    print("Setup complete.\n")

    # --- Example 1: Structured JSON Output ---
    commentary_data = generate_game_commentary(
        event_type="Flawless Round",
        player_name="Sova",
        game_name="Valorant"
    )
    print("--- Structured Commentary (JSON) ---")
    if "error" in commentary_data:
        print(f"An error occurred: {commentary_data['error']}\n")
    else:
        print(f"Commentary: {commentary_data.get('commentary_line')}")
        print(f"Hashtags: {commentary_data.get('suggested_hashtags')}\n")

    # --- Example 2: Stop Sequence ---
    hype_list = generate_hype_list(
        event_type="Clutch Victory",
        game_name="Fortnite"
    )
    print("--- Hype List with Stop Sequence ---")
    print(hype_list)


if __name__ == "__main__":
    main()