import os
import json
import numpy as np # NEW: Import NumPy for calculations
import google.generativeai as genai

# --- In-Memory "Vector Database" ---
# In a real app, you would use a dedicated vector database.
# For this project, a simple list will store our memories.
commentary_memory = []

def setup_api_key():
    """Loads the Google API key from an environment variable."""
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("API key not found. Set GOOGLE_API_KEY environment variable.")
    genai.configure(api_key=api_key)

# --- NEW: Function to create embeddings ---
def get_embedding(text: str) -> list:
    """Generates an embedding for a given text."""
    try:
        result = genai.embed_content(
            model="models/embedding-001",
            content=text
        )
        return result['embedding']
    except Exception as e:
        print(f"Error creating embedding: {e}")
        return []

# --- NEW: Function to find the most similar commentary ---
def find_most_similar(new_embedding: list, memory: list) -> str:
    """Finds the most similar text in memory using dot product."""
    if not memory or not new_embedding:
        return ""
    
    max_similarity = -1
    most_similar_text = ""

    for item in memory:
        # Calculate similarity using dot product (a simple similarity measure)
        similarity = np.dot(new_embedding, item['embedding'])
        if similarity > max_similarity:
            max_similarity = similarity
            most_similar_text = item['text']
            
    return most_similar_text

def generate_game_commentary(event_type: str, player_name: str, game_name: str, context: str = "") -> dict:
    """Generates structured commentary, now with optional context."""
    try:
        model = genai.GenerativeModel('gemini-pro')
        config = genai.types.GenerationConfig(temperature=0.8, max_output_tokens=100)
        
        system_prompt = "You are 'Reflex,' an AI esports commentator. Your responses must be in JSON format."
        
        # NEW: The prompt now includes context from past similar events
        user_prompt = (
            f"Event: '{event_type}' by '{player_name}' in {game_name}. "
            f"{context} "
            "Generate a new, unique commentary line and three hashtags. "
            "Provide the output as a JSON object with keys: 'commentary_line' and 'suggested_hashtags'."
        )
        
        full_prompt = f"{system_prompt}\n\n{user_prompt}"
        response = model.generate_content(full_prompt, generation_config=config)
        return json.loads(response.text)
        
    except Exception as e:
        return {"error": str(e)}

def main():
    """Main function to demonstrate the AI memory workflow."""
    print("Initializing AI Game Analyst with Memory...")
    setup_api_key()

    # --- Pre-populate our memory with a past event ---
    initial_commentary = "What a stunning sniper shot from across the map!"
    initial_embedding = get_embedding(initial_commentary)
    if initial_embedding:
        commentary_memory.append({"text": initial_commentary, "embedding": initial_embedding})
    print(f"AI Memory initialized with {len(commentary_memory)} item(s).\n")

    # --- A new event occurs ---
    new_event = "Player 'Shroud' just got a long-range sniper kill in PUBG."
    print(f"--- New Event --- \n{new_event}\n")
    
    # 1. Create an embedding for the new event
    new_embedding = get_embedding(new_event)

    # 2. Find the most similar event in memory
    similar_context = find_most_similar(new_embedding, commentary_memory)
    context_prompt = ""
    if similar_context:
        print(f"Found similar past event: '{similar_context}'")
        context_prompt = f"For context, you previously described a similar play as: '{similar_context}'. Do not repeat this phrase."

    # 3. Generate a new commentary with this context
    new_commentary_data = generate_game_commentary(
        event_type="Long-range sniper kill",
        player_name="Shroud",
        game_name="PUBG",
        context=context_prompt
    )

    # 4. Print the new, context-aware commentary
    print("\n--- New, Context-Aware Commentary ---")
    if "error" in new_commentary_data:
        print(f"An error occurred: {new_commentary_data['error']}")
    else:
        new_text = new_commentary_data.get('commentary_line')
        print(f"Commentary: {new_text}")
        print(f"Hashtags: {new_commentary_data.get('suggested_hashtags')}")
        
        # 5. Add the new commentary to our memory for the future
        new_text_embedding = get_embedding(new_text)
        if new_text_embedding:
            commentary_memory.append({"text": new_text, "embedding": new_text_embedding})
            print(f"\nAI Memory updated. Now contains {len(commentary_memory)} item(s).")

if __name__ == "__main__":
    main()