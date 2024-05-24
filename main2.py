import pgzrun
import requests
import json

# Impostazioni di base di Pygame Zero
WIDTH = 800
HEIGHT = 600
user_input = ""
response_text = ""
show_dialog = False

def draw():
    screen.clear()
    screen.draw.text("Premi 'S' per parlare con il personaggio", (10, 10), fontsize=40)
    if show_dialog:
        screen.draw.text(f"Tu: {user_input}", (10, 50), fontsize=30)
        screen.draw.text(f"AI: {response_text}", (10, 100), fontsize=30)

def update():
    pass

def on_key_down(key):
    global user_input, response_text, show_dialog
    if key == keys.S:
        user_input = input("Tu: ")
        response_text = get_response_from_chatgpt(user_input)
        show_dialog = True

def get_response_from_chatgpt(prompt):
    api_key = "YOUR_OPENAI_API_KEY"  # Assicurati di sostituire questo con la tua chiave API valida
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    data = {
        "model": "gpt-4",  # Assicurati che questo sia il modello corretto
        "messages": [
            {"role": "system", "content": "Sei un personaggio di un videogioco."},
            {"role": "user", "content": prompt}
        ]
    }
    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        response.raise_for_status()  # Solleva un'eccezione per errori HTTP
        response_json = response.json()
        print(json.dumps(response_json, indent=2))  # Stampa la risposta formattata
        if 'choices' in response_json and len(response_json['choices']) > 0:
            return response_json['choices'][0]['message']['content']
        else:
            print("Unexpected response format:", response_json)
            return "Errore nella risposta dell'AI."
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        print(response.json())  # Mostra il messaggio di errore dettagliato
    except KeyError as key_err:
        print(f"Key error: {key_err}")
        print(response_json)  # Mostra la risposta per capire cosa manca
    except Exception as err:
        print(f"Other error occurred: {err}")

pgzrun.go()
