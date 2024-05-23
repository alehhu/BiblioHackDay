import pgzero
import random
from pgzero.actor import Actor
from pgzero.screen import Screen

cell = Actor('floor')
char = Actor('down')
tipo1 = Actor('tipo1')

size_w = 10  # Larghezza del campo nelle celle
size_h = 10  # Altezza del campo nelle celle
WIDTH = cell.width * size_w
HEIGHT = cell.height * size_h
TITLE = "BiblioHackDay"  # Titolo della finestra di gioco
FPS = 30  # Numero di frame per secondo

my_map = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

# Variabile di stato per gestire la schermata
game_state = "playing"  # Può essere "playing" o "dialogue"
question = ""

class Enemy:
    def __init__(self, actor):
        self.actor = actor
        self.direction = random.choice(['up', 'down', 'left', 'right'])
        self.speed = 1  # Velocità costante e lenta
        self.change_time = random.randint(60, 120)  # Cambia direzione ogni 60-120 frame

    def move(self):
        if self.direction == 'up':
            if self.actor.top > 0:
                self.actor.y -= self.speed
            else:
                self.change_direction()
        elif self.direction == 'down':
            if self.actor.bottom < HEIGHT:
                self.actor.y += self.speed
            else:
                self.change_direction()
        elif self.direction == 'left':
            if self.actor.left > 0:
                self.actor.x -= self.speed
            else:
                self.change_direction()
        elif self.direction == 'right':
            if self.actor.right < WIDTH:
                self.actor.x += self.speed
            else:
                self.change_direction()

        self.change_time -= 1
        if self.change_time <= 0:
            self.change_direction()

    def change_direction(self):
        self.direction = random.choice(['up', 'down', 'left', 'right'])
        self.change_time = random.randint(60, 120)

enemies = []
def create_enemies():
    for i in range(5):
        x = random.randint(20, WIDTH - 20)
        y = random.randint(20, HEIGHT - 20)
        enemy_actor = Actor("en1", (x, y))
        enemies.append(Enemy(enemy_actor))
create_enemies()

def enemies_draw():
    for enemy in enemies:
        enemy.actor.draw()

def enemies_move():
    for enemy in enemies:
        enemy.move()

def map_draw():
    for i in range(len(my_map)):
        for j in range(len(my_map[0])):
            if my_map[i][j] == 0:
                cell.left = cell.width * j
                cell.top = cell.height * i
                cell.draw()
            elif my_map[i][j] == 1:
                cell2.left = cell.width * j
                cell2.top = cell.height * i
                cell2.draw()

input_text = ""

def draw():
    if game_state == "playing":
        map_draw()
        enemies_draw()
        char.draw()
    elif game_state == "dialogue":
        screen.clear()
        tipo1.draw()
        screen.draw.text(input_text, (20, HEIGHT - 40), fontsize=30, color="white")
        screen.draw.text("Domanda:", (20, HEIGHT - 100), fontsize=20, color="white")
        screen.draw.text(question, (20, HEIGHT - 160), fontsize=20, color="white")
        screen.draw.text("Risposta:", (20, HEIGHT - 220), fontsize=20, color="white")
        screen.draw.text(get_answer("ciao"), (20, HEIGHT - 280), fontsize=20, color="white")


def update(dt):
    global game_state
    if game_state == "playing":
        if keyboard.right:
            char.x += 4
            if char.image != 'right':
                char.image = "right"
        elif keyboard.left:
            char.x -= 4
            if char.image != 'left':
                char.image = "left"
        elif keyboard.up:
            char.y -= 4
            if char.image != 'up':
                char.image = "up"
        elif keyboard.down:
            char.y += 4
            if char.image != 'down':
                char.image = "down"

        enemies_move()  # Chiamata per muovere i nemici

        check_collisions()  # Controllo delle collisioni con i nemici

def check_collisions():
    global game_state
    for enemy in enemies:
        if char.colliderect(enemy.actor):
            game_state = "dialogue"

def get_answer(question):
    return "Ecco la risposta alla tua domanda"

def on_key_down(key):
    global input_text, game_state
    if game_state == "dialogue":
        if key == keys.RETURN:
            # Quando viene premuto INVIO, ottieni la risposta e stampala
            answer = get_answer(input_text)
            print("Domanda:", input_text)
            print("Risposta:", answer)
            input_text = ""  # Resetta il campo di input dopo aver inviato la domanda
        elif key == keys.BACKSPACE:
            input_text = input_text[:-1]  # Rimuove l'ultimo carattere
        elif key.name == 'SPACE':
            input_text += ' '  # Aggiunge uno spazio
        elif key.name == 'QUOTE':
            input_text += '?' 
        elif key.name not in ['LSHIFT', 'RSHIFT', 'LCTRL', 'RCTRL', 'LALT', 'RALT', 'CAPSLOCK', 'TAB']:
            input_text += key.name.lower()  # Aggiunge il carattere digitato al campo di input



