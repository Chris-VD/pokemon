# Server imports
import socketio

# Pokemon imports


sio = socketio.Client()

@sio.event
def connect():
    print("Connected to the server.\nWrite a username:")
    username = input()
    sio.emit("client_connected", username)
    sio.wait()

@sio.event
def in_queue():
    print("No room avaliable, you're curerntly in queue...")
    sio.wait()

@sio.event
def user_found():
    print("User found!")
    sio.wait()

@sio.event
def connected_to_room(data):
    print("You've been connectd to a room! Say something:")
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

sio.connect("http://localhost:5000")
sio.wait()