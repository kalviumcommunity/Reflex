import os
import json
import numpy as np 
import google.generativeai as genai

# All of your functions (setup_api_key, generate_game_commentary, etc.) remain the same...

def setup_api_key():
    """Loads the Google API key from an environment variable."""
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("API key not found. Set GOOGLE_API_KEY environment variable.")
    genai.configure(api_key=api_key)

def generate_game_commentary(event_type: str, player_name: str, game_name: str, config: genai.types.GenerationConfig) -> dict:
    """Generates structured commentary using a provided generation config."""
    try:
        model = genai.GenerativeModel('gemini-pro')
        system_prompt = "You are 'Reflex,' an AI esports commentator. Your responses must be in a valid JSON format."
        user_prompt = (
            f"Event: '{event_type}' by '{player_name}' in {game_name}. "
            "Generate a commentary line and three hashtags. "
            "Provide the output as a JSON object with keys: 'commentary_line' and 'suggested_hashtags'."
        )
        full_prompt = f"{system_prompt}\n\n{user_prompt}"
        response = model.generate_content(full_prompt, generation_config=config)
        return json.loads(response.text)
    except Exception as e:
        return {"error": str(e)}

def main():
    """Main function to demonstrate different generation configurations."""
    print("Initializing AI Game Analyst...")
    setup_api_key()
    print("Setup complete.\n")

    # --- Example 1: Using Temperature and Top_P ---
    print("--- Example using Temperature & Top_P (Hype Style) ---")
    hype_config = genai.types.GenerationConfig(
        temperature=0.9,
        top_p=0.95
    )
    hype_commentary = generate_game_commentary(
        "Team Wipe", "Bangalore", "Apex Legends", config=hype_config
    )
    print(f"Commentary: {hype_commentary.get('commentary_line')}\n")

    # --- NEW: Example 2: Using Top_K ---
    # Top K limits the choices to the top 40 most likely words.
    # It provides a balance between creativity and predictability.
    print("--- Example using Top_K (Balanced Style) ---")
    top_k_config = genai.types.GenerationConfig(
        temperature=0.7,
        top_k=40
    )
    top_k_commentary = generate_game_commentary(
        "Last second objective steal", "Tracer", "Overwatch", config=top_k_config
    )
    print(f"Commentary: {top_k_commentary.get('commentary_line')}\n")

if __name__ == "__main__":
    main()