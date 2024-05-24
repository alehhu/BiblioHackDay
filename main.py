import random
from pgzero.actor import Actor
from pgzero.screen import Screen
import re
import pygame
import requests
import json


cell = Actor('floor')
lib = Actor("library")
tree = Actor("tree")
bookAdult = Actor("book")
bookChild = Actor("childrenbook")
char = Actor('down', (100, 100))
size_w = 10  # Larghezza del campo nelle celle
size_h = 10  # Altezza del campo nelle celle
WIDTH = cell.width * size_w
HEIGHT = cell.height * size_h
TITLE = "BiblioHackDay"  # Titolo della finestra di gioco
FPS = 30  # Numero di frame per secondo

dialogue = Actor("dialogue", (320, 320))


my_map = [[2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
          [2, 0, 0, 0, 0, 0, 0, 0, 0, 2],
          [2, 0, 0, 0, 0, 2, 0, 0, 0, 2],
          [2, 0, 0, 2, 0, 0, 0, 0, 0, 2],
          [2, 0, 0, 0, 0, 0, 0, 0, 0, 2],
          [2, 0, 0, 0, 0, 0, 0, 0, 0, 2],
          [2, 0, 0, 0, 0, 0, 0, 0, 0, 2],
          [2, 0, 0, 0, 0, 0, 0, 0, 0, 2],
          [2, 3, 0, 0, 0, 0, 0, 0, 0, 2],
          [2, 2, 2, 2, 2, 2, 2, 2, 2, 2]]

menu_map = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
          [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
          [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
          [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
          [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
          [1, 0, 0, 4, 0, 0, 3, 0, 0, 1],
          [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
          [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
          [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
          [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]

# Variabile di stato per gestire la schermata
game_state = "menu"  # Può essere "playing" o "dialogue"
previous_state = "menu"
question = ""

class Enemy:
    def __init__(self, actor, name, image, description):
        self.actor = actor
        self.direction = random.choice(['up', 'down', 'left', 'right'])
        self.speed = 1  # Velocità costante e lenta
        self.change_time = random.randint(60, 120)  # Cambia direzione ogni 60-120 frame
        self.name = name
        self.image = image
        self.description = description

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
enemies_names = [
    "Nicola Abbagnano",
    "Ferdinando Accornero",
    "Cesare Agostini",
    "Alfredo Albertini",
    "Giuseppe Amadei"
]
enemies_images = [
    "tipo1",
    "tipo2",
    "tipo3",
    "tipo4",
    "tipo5"
]
enemies_description = [
    "Filosofo italiano tra i maggiori del secondo dopoguerra, si laureò nel 1922 con Antonio Aliotta all'Università di Napoli.",
    "Laureato in medicina e chirurgia all'Università di Roma nel 1935, nel biennio successivo si recò all'estero per un periodo di studio, frequentando nel 1936 la Clinica neurologica e psichiatrica dell'Ospedale della Charité di Berlino, diretta da Karl Bonhoffer, e nel 1937 l'Istituto neurologico di Vienna diretto da Otto Marburg. Dal 1937 al 1939 prestò servizio come assistente presso la Clinica delle malattie nervose e mentali dell'Università di Roma, sotto la direzione di Ugo Cerletti e nel 1938 ottenne la specializzazione in neurologia e psichiatria. Durante la seconda guerra mondiale, dal 1941 al 1944, fu capitano medico di complemento in zona di operazioni, ma nel 1942 riuscì comunque a conseguire la libera docenza in Clinica delle malattie nervose e mentali, seguita nel 1955 da quella in Neuropsichiatria infantile. Fu inoltre dal 1950 al 1985, anno della morte, direttore della Casa di cura romana 'Castello della quiete'. Membro della Società italiana di neurologia (SIN), della Società italiana di psichiatria (SIP) e della sua Sezione di neuropsichiatria infantile (che pubblicava la rivista L'infanzia anormale), rivolse inizialmente la sua attività di ricerca all'applicazione delle terapie convulsivanti in psichiatria, collaborando con Ugo Cerletti e Lucio Bini alla sperimentazione dell'elettroshock, e dedicandosi successivamente allo studio delle anoressie e della neuropsichiatria infantile. Fu autore di 42 pubblicazioni su riviste scientifiche nazionali e di un libro dal titolo L'organizzazione del proprio lavoro intellettuale (Roma, Tumminelli, 1956). Il suo archivio è andato perduto.",
    """
    Figlio di Pasquale Agostini e Giulia Rocchi, conseguì la laurea in medicina e chirurgia all’Istituto di studi superiori di Firenze nel 1889, perfezionandosi poi presso l’Ospedale psichiatrico San Lazzaro di Reggio Emilia e in seguito a Heidelberg, dove fu uno dei migliori studenti di Emil Kraepelin.
    Trascorsi pochi anni dalla laurea, fu nominato medico primario del Manicomio Santa Maria della Pietà di Roma, ruolo che lasciò nel 1901 per accettare l’incarico di vicedirettore del Manicomio Santa Margherita di Perugia, diretto da Roberto Adriani, passando poi nel 1903 come sopraintendente al Pellagrosario di Città di Castello in Umbria. Poco dopo aver ottenuto la nomina a direttore dell’Ospedale psichiatrico provinciale di Arezzo, fu richiamato nel 1904 da Adriani a succedergli nella direzione di quello di Perugia, dove rimase fino al 1928. Qui fondò nel 1907 la rivista Annali del Manicomio di Perugia, di cui fu direttore sino al 1930, anno in cui gli subentrò il figlio Giulio.
    Sempre nel manicomio perugino diede mano a una serie di riforme edilizie, facendo costruire nuovi padiglioni, tra cui merita una menzione il padiglione Bellisari, ultimato nel 1915 e inaugurato come reparto neuro-psichiatrico dipendente dall’Ospedale militare di Perugia, destinato solo dopo la guerra ai pazienti del manicomio. Nel 1916 Agostini si arruolò volontario con il grado di maggiore medico, ottenendo la nomina a direttore della Sezione neurologica militare di Perugia e consulente neuropsichiatra delle malattie nervose presso l’Armata Carnica. In quel periodo si dedicò al funzionamento dei servizi neuropsichiatrici dell’esercito, per i quali ottenne la medaglia d’argento al merito della sanità pubblica e la medaglia di bronzo al valore civile. Si congedò infine nel 1917 con il grado di tenente colonnello.
    """,
    """
    Figlio di Paolo Albertini e Ida Marchei, perde la madre ad appena sei anni; il padre sposa in seconde nozze Elvira Feliciani. Conseguita la maturità classica presso il liceo Francesco Stabili di Ascoli Piceno, nel 1899 s’iscrive alla Facoltà di medicina dell’Università La Sapienza di Roma (gli zii materni erano medici, e proprio a Roma li ritrova), conseguendo la laurea nel luglio 1905. Ottiene subito un posto di assistente nella sezione chirurgica dell’Ospedale Mazzoni di Ascoli, dove lavora con Aristide Mattoli e Cesare Bellati. L’anno successivo diventa medico condotto presso il Comune di Monterubbiano, dove dà vita alle cosiddette "locande sanitarie", centri territoriali dove gli ammalati di pellagra possono ricevere cure adeguate senza dover essere relegati nei pellegrosari. Successivamente si sposta nella condotta di Rocca Priora, in provincia di Roma.
    Nel 1907 frequenta, presso l’ateneo romano, un corso teorico-pratico di perfezionamento in igiene, che si rivelerà fondamentale quando, l’anno successivo, si trasferisce a Milano e – dopo aver sposato Egle Murani, professoressa di calligrafia – si iscrive al concorso per "medico di seconda classe" dell’Ufficio di igiene e sanità del Comune di Milano, ottenendo l’incarico nel novembre 1908. Nel 1911 il sindaco Emanuele Greppi gli assegna anche la direzione del servizio sanitario scolastico, che manterrà fino al 1947.
    """,
    """
    Originario di Cavriana, allora territorio bresciano, dopo aver frequentato il liceo a Brescia fu ammesso nel 1873, per merito, al Collegio Ghislieri di Pavia. Allievo di Cesare Lombroso e Paolo Mantegazza, si laureò in medicina e chirurgia, svolgendo per un breve periodo la professione medica a Campitello e Cavriana.
    Dopo un soggiorno di perfezionamento a Parigi, cominciò a dedicarsi sistematicamente agli studi di craniologia e psichiatria, aderendo inoltre nel 1878 alla Società italiana d'antropologia ed etnologia.
    Scelta definitivamente la carriera psichiatrica, divenne prima assistente nel Manicomio San Lazzaro in Reggio Emilia (1880), poi aiuto al Manicomio di Macerata (1881) e infine primario al Manicomio di Imola (1882). Gli anni di formazione gli permisero di entrare in contatto con illustri personaggi della disciplina, come Luigi Lolli, Enrico Morselli, Augusto Tamburini e Giulio Cesare Ferrari.
    """
]

friends = []
friends_names = [
    "Tartaglia",
    "Leone",
    "Bruno",
    "Lilith",
    "Sofia"
]
friends_images = [
    "tartagliad",
    "leoned",
    "brunod",
    "lilithd",
    "sofiad"
]
friends_description = [
    "sei il protagonista del libro 'il mio nome è Tartaglia' di Guido Quarzo e il personaggio balbetta sempre",
    "sei il protagonista del libro 'Missione democrazione: Sofia e Leone mettono in salvo la Costituzione' di Maria Scolgio",
    "lsei il protagonista del libro 'Di che colore è la liberta' di Roberto Piumini",
    "lsei il protagonista del libro 'Vestiario familiare' di Lilith Moscon",
    "lsei il protagonista del libro 'Missione democrazione: Sofia e Leone mettono in salvo la Costituzione' di Maria Scolgio",
]
def create_enemies():
    for i in range(5):
        x = random.randint(100, WIDTH - 100)
        y = random.randint(100, HEIGHT - 100)
        enemy_actor = Actor(f"en{i+1}", (x, y))
        enemies.append(Enemy(enemy_actor, enemies_names[i], enemies_images[i], enemies_description[i]))
        friends_actor = Actor(friends_names[i].lower(), (x, y))
        friends.append(Enemy(friends_actor, friends_names[i], friends_images[i], friends_description[i]))
create_enemies()

def enemies_draw():
    for enemy in enemies:
        enemy.actor.draw()

def friends_draw():
    for friend in friends:
        friend.actor.draw()

def enemies_move():
    for enemy in enemies:
        enemy.move()

def map_draw(my_map):
    for i in range(len(my_map)):
        for j in range(len(my_map[0])):
            if my_map[i][j] == 0:
                cell.left = cell.width * j
                cell.top = cell.height * i
                cell.draw()
            elif my_map[i][j] == 1:
                lib.left = lib.width * j
                lib.top = lib.height * i
                lib.draw()
            elif my_map[i][j] == 2:
                tree.left = tree.width * j
                tree.top = tree.height * i
                tree.draw()
            elif my_map[i][j] == 3:
                bookAdult.left = bookAdult.width * j
                bookAdult.top = bookAdult.height * i
                bookAdult.draw()
            elif my_map[i][j] == 4:
                bookChild.left = bookChild.width * j
                bookChild.top = bookChild.height * i
                bookChild.draw()

input_text = ""

def draw():
    if game_state == "menu":
        screen.clear()
        map_draw(menu_map)
        char.draw()
    elif game_state == "playing":
        screen.clear()
        map_draw(my_map)
        enemies_draw()
        char.draw()
    elif game_state == "dialogue":
        screen.clear()
        dialogue.draw()
        ce = Actor(current_enemy.image, (115, HEIGHT-115))
        ce.draw()
        screen.draw.text(input_text, (280, HEIGHT - 120), fontsize=30, color="black")
    elif game_state == "answer_display":
        screen.clear()
        dialogue.draw()
        ce = Actor(current_enemy.image, (115, HEIGHT-115))
        ce.draw()
        screen.draw.text(question, (280, HEIGHT - 120), fontsize=30, color="black")
        
        max_line_width = WIDTH - 90
        # Adatta il valore secondo le esigenze
        lines = wrap_text(answer, max_line_width, screen)
        
        # Disegna le linee di testo sulla schermata
        line_y = 70  # Posizione verticale iniziale per la prima riga di testo
        for line in lines:
            screen.draw.text(line, (60, line_y), fontsize=30, color="black")
            line_y += 30  # Spazio verticale tra le linee di testo
    elif game_state == "child":
        screen.clear()
        map_draw(my_map)
        friends_draw()
        char.draw()
            


def update(dt):
    global game_state
    if game_state == "playing" or game_state == "menu" or game_state == "child":
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

        check_collisions()  # Controllo delle collisioni con i nemici

def check_collisions():
    global game_state, current_enemy, previous_state
    if game_state == "playing":
        for enemy in enemies:
            if char.colliderect(enemy.actor) and keyboard.d:
                current_enemy = enemy  # Memorizza il nemico corrente
                game_state = "dialogue"
            elif char.colliderect(bookAdult) and keyboard.d:
                game_state = "menu"
    elif game_state == "child":
        if char.colliderect(bookAdult) and keyboard.d:
                game_state = "menu"
        for friend in friends:
            if char.colliderect(friend.actor) and keyboard.d:
                current_enemy = friend  # Memorizza il nemico corrente
                game_state = "dialogue"
            elif char.colliderect(bookAdult) and keyboard.d:
                game_state = "menu"
    elif game_state == "menu":
        if char.colliderect(bookAdult) and keyboard.d:
            game_state = "playing"
            char.pos = 20,20
            previous_state = "playing"
        elif char.colliderect(bookChild) and keyboard.d:
            game_state = "child"
            char.pos = 20,20
            previous_state = "child"


    

def on_key_down(key):
    global input_text, game_state, question, answer, current_enemy
    if game_state == "dialogue":
        if key == keys.RETURN:
            # Quando viene premuto INVIO, ottieni la risposta e imposta lo stato del gioco per visualizzare la risposta
            question = input_text
            answer = get_answer(input_text, current_enemy.name, current_enemy.description)
            input_text = ""  # Resetta il campo di input dopo aver inviato la domanda
            game_state = "answer_display"  # Imposta lo stato del gioco per visualizzare la risposta
        elif key == keys.BACKSPACE:
            input_text = input_text[:-1]  # Rimuove l'ultimo carattere
        elif key.name == 'SPACE':
            input_text += ' '  # Aggiunge uno spazio
        elif key.name == 'QUOTE':
            input_text += '?' 
        elif key.name == 'COMMA':
            input_text += ',' 
        elif key.name not in ['LSHIFT', 'RSHIFT', 'LCTRL', 'RCTRL', 'LALT', 'RALT', 'CAPSLOCK', 'TAB', 'DOWN', 'LEFT', 'TOP', 'RIGHT']:
            input_text += key.name.lower()  # Aggiunge il carattere digitato al campo di input
        if input_text == "arrivederci":
            if previous_state == "playing":  # Controlla se l'utente ha scritto "arrivederci"
                game_state = "playing"  # Torna alla modalità "playing" iniziale
                input_text = ""  # Resetta il campo di input
            elif previous_state == "child":
                game_state = "child"  # Torna alla modalità "playing" iniziale
                input_text = "" #reset_enemies_position()  # Reimposta la posizione dei nemici
    elif game_state == "answer_display":
        if key == keys.RETURN:
            # Quando viene premuto INVIO dopo aver visualizzato la risposta, lo stato del gioco torna a "dialogue" per consentire una nuova domanda
            game_state = "dialogue"


def wrap_text(text, max_width, screen):
    words = text.split(' ')
    lines = []
    current_line = []

    font = pygame.font.SysFont(None, 30)

    for word in words:
        current_line.append(word)
        line_width, _ = font.size(' '.join(current_line))
        
        if line_width > max_width:
            current_line.pop()
            lines.append(' '.join(current_line))
            current_line = [word]
    
    if current_line:
        lines.append(' '.join(current_line))
    
    return lines


def reset_enemies_position():
    for enemy in enemies:
        enemy.actor.x = random.randint(50, WIDTH - 20)
        enemy.actor.y = random.randint(50, HEIGHT - 20)


def get_answer(prompt, nomePersonaggio, descrizione):
    api_key = "YOUR_API_KEY"
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    data = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": f"Rispondi in prima persona, come se fossi {nomePersonaggio}, ecco la sua descrizione: {descrizione}. Sii sintetico"},
            {"role": "user", "content": prompt}
        ]
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    response_json = response.json()
    return response_json['choices'][0]['message']['content']