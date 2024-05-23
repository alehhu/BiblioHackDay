
import pgzrun
import requests

# Chiave API di OpenAI
API_KEY = 'your_openai_api_key'

# Funzione per ottenere la risposta di ChatGPT (GPT-3.5)
def get_chatgpt_response(prompt):
    url = "https://api.openai.com/v1/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }
    data = {
        "model": "text-davinci-003",  # Usa il modello GPT-3.5
        "prompt": prompt,
        "max_tokens": 150
    }
    response = requests.post(url, headers=headers, json=data)
    return response.json()['choices'][0]['text'].strip()

# Variabili globali
WIDTH = 800
HEIGHT = 600
character_response = ""

def draw():
    screen.clear()
    screen.draw.text("Parla con il personaggio:", (10, 10), color="white")
    screen.draw.textbox(character_response, Rect(10, 50, 780, 200), color="white")

def on_key_down(key):
    global character_response
    if key == keys.RETURN:
        user_input = input("Tu: ")
        prompt = f"Il personaggio dice: {user_input}"
        character_response = get_chatgpt_response(prompt)

pgzrun.go()

