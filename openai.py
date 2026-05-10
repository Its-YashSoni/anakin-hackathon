import ollama
import json

def clean_events(events):

    prompt = f"""
    Clean and normalize this event JSON.
    
    Rules:
    - Remove duplicates
    - Remove garbage entries
    - Keep only real events
    - Fix formatting
    - Return ONLY valid JSON
    - No explanations

    Required schema:

    [
      {{
        "title": "",
        "date": "",
        "location": "",
        "organizer": "",
        "link": "",
        "image_url": "",
        "description": "",
        "fee": "",
        "source": "",
        "vibe": "",
        "introvert_friendly": false,
        "networking_level": "",
        "best_for": []
      }}
    ]

    Input:
    {json.dumps(events, indent=2)}
    """

    response = ollama.chat(
        model="mistral",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response["message"]["content"]