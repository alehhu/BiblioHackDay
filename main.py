import pgzrun
import requests
import json

# Impostazioni di base di Pygame Zero
WIDTH = 800
HEIGHT = 600

def draw():
    screen.clear()
    screen.draw.text("Premi 'S' per parlare con il personaggio", (10, 10), fontsize=40)

def update():
    pass

def on_key_down(key):
    if key == keys.S:
        user_input = input("Tu: ")
        response = get_response_from_chatgpt(user_input)
        print("AI:", response)

def get_response_from_chatgpt(prompt):
    api_key = "YOUR_OPENAI_API_KEY"
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    data = {
        "model": "gpt-4",
        "messages": [
            {"role": "system", "content": "Sei un personaggio di un videogioco."},
            {"role": "user", "content": prompt}
        ]
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    response_json = response.json()
    return response_json['choices'][0]['message']['content']

pgzrun.go()
