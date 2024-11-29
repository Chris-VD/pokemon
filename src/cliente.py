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
def in_queue(data):
    # data = [sid, pokemon = {"N": "", "T": "", "LVL": "", "DEF": "", "MHP": "", "CHP": "", "ATK": [{"N": "", "T": "", "P": "", "MAP": "", "CAP": ""}]}]
    print("Your prokemon is", data[1]["N"], "\nNo arena avaliable, you're curerntly in queue...")
    sio.wait()

@sio.event
def connected_to_room(data):
    # data = [[sid, pokemon] (usuario1), [sid, pokemon] (usuario2)]
    print("Your prokemon is", data[1][1]["N"], "\nYou've been connectd to an arena!")
    show.mostrar_stats([data[0][1], data[1][1]])
    msg = input()
    info = [data, msg]
    sio.emit("client_turn", info)
    sio.wait()

@sio.event
def turn_to_speak(data):
    room = data[1][0]
    print(f"{data[0]} says: {data[1][1]}")
    msg = input("Your answer: ")
    info = [room, msg]
    sio.emit("client_turn", info)
    sio.wait()

sio.connect("http://0.0.0.0:5000")
sio.wait()