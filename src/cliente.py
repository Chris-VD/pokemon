# Server imports
import socketio
from os import system as sy

# Pokemon imports
import interfaz as show

sio = socketio.Client()

@sio.event
def connect():
    print("Connected to the server.\nWrite a username:")
    username = input()
    sio.emit("client_connected", username)
    sio.wait()

@sio.event
def in_queue():
    print("No arena avaliable, you're curerntly in queue...")
    sio.wait()

@sio.event
def connected_to_room(data):
    # data = [[sid_user, pokemon_user], [sid_rival, [pokemon_rival_name, pokemon_rival_hp]], battle_ID]
    print("Your prokemon is", data[0][1]["N"], "\nYou've been connectd to an arena!")
    show.mostrar_stats([data[0][1]])
    print("Rival:\n\t", data[1][1][0], ": HP -->",data[1][1][1])
    sio.emit("battle_started", data)
    sio.wait()

@sio.event
def turn_to_speak(data):
    room = data[1][0]
    print(f"{data[0]} says: {data[1][1]}")
    msg = input("Your answer: ")
    info = [room, msg]
    sio.emit("client_turn", info)
    sio.wait()

sio.connect("http://localhost:5000")
sio.wait()