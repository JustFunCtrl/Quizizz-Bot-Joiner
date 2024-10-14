import requests
import random
import time

# Liste de prénoms aléatoires
first_names = ["Alice", "Bob", "Charlie", "David", "Eva", "Fiona", "George", "Hannah", "Ivy", "Jack"]

def generate_random_name():
    # Génère un nom aléatoire à partir de la liste de prénoms
    return random.choice(first_names)

def handlePIN(pin):
    # Utilisation de l'API v5/checkRoom pour vérifier la room à partir du PIN
    payload = {
        "mongoId": None,
        "roomCode": pin
    }

    response = requests.post('https://game.quizizz.com/play-api/v5/checkRoom', json=payload)
    
    if response.status_code == 200:
        room_data = response.json()
        # Vérifie si la salle est dans un état valide pour rejoindre
        if 'room' in room_data and room_data['room']['state'] == 'waiting':
            room_hash = room_data['room']['hash']  # Récupère le roomHash
            print(f"Room Hash: {room_hash}")  # Affiche le roomHash pour débogage
            
            # Commencer à rejoindre les joueurs en boucle
            join_multiple_players(room_hash)
        else:
            print("La salle n'est pas dans un état valide pour rejoindre le jeu:", room_data)
    else:
        print("Erreur lors de la vérification de la room:", response.json())

def join_multiple_players(room_hash):
    while True:
        player_name = generate_random_name()
        player_id = f"{player_name.lower()}{random.randint(1000, 9999)}"  # ID unique
        
        if joinGame(room_hash, player_name, player_id):
            print(f"\033[92m[ + ] Joueur {player_name} a rejoint la partie\033[0m")  # Texte en vert
        else:
            print(f"\033[91m[ - ] Une erreur est survenue lors du join de {player_name}\033[0m")  # Texte en rouge
        
        time.sleep(1)  # Attendre 1 seconde avant de rejoindre un autre joueur

def joinGame(room_hash, player_name, player_id):
    # Prépare la charge utile pour l'API v5/join
    payload = {
        "roomHash": room_hash,
        "player": {
            "id": player_id,
            "name": player_name,
            "origin": "web",
            "isGoogleAuth": False,
            "avatarId": 7,
            "startSource": "joinRoom",
            "userAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.0.0",
            "uid": "1439d053-597e-4f1c-a14b-28dd2deafafc",
            "expName": "main_main",
            "expSlot": "1"
        },
        "powerupInternalVersion": "20",
        "serverId": "64f9903e4a7b8500203ba32b",
        "ip": "11.111.11.11",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.0.0",
        "socketId": "YfbpP5cd_gWLmdVN7QAl",
        "authCookie": None,
        "socketExperiment": "authRevamp"
    }

    # Envoie de la requête à l'API v5/join
    response = requests.post('https://game.quizizz.com/play-api/v5/join', json=payload)
    
    # Vérification de la réponse
    if response.status_code == 200:
        join_data = response.json()
        # Vérification de plusieurs conditions
        if join_data.get('success') or ('room' in join_data and 'players' in join_data['room']):
            return True
        else:
            # Affichage de la réponse détaillée pour le débogage
            print(f"Erreur détaillée lors du join: {join_data}")
            return False
    else:
        print(f"Erreur lors de la requête: {response.status_code}, détails: {response.json()}")
        return False

# Demande à l'utilisateur de saisir le code PIN
pin_input = input("Veuillez entrer le code PIN de la partie: ")
handlePIN(pin_input)