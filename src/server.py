# Server imports
import socketio
import eventlet
import id_gen

# Pokemon imports
import pokemons

pokemons.new()
pokemon_user1 = pokemons.gens["I"][0]
pokemon_user2 = pokemons.gens["I"][3]
print(pokemon_user1, pokemon_user2)

def check_rooms(all_rooms):
    full_rooms = 0
    for room in all_rooms:
        if len(all_chat_rooms[room]) == 1:
            print("Room avaliable for user.")
            return True
        elif len(all_chat_rooms[room]) == 2:
            full_rooms += 1
        if full_rooms == len(list(all_rooms.keys())):
            print("All rooms are full, creating new one...")
            return False
    print("No rooms, creating new one...")
    return False

sio = socketio.Server()
app = socketio.WSGIApp(sio)

ID_list = {}
all_chat_rooms = {}

gen_id = id_gen.generate_game_ID()

@sio.event
def client_connected(sid, data):
    ID_list[sid] = data
    print(f"User connceted to the server as\nID: {sid}\nUsername: {data}")
    empty_rooms_check = check_rooms(all_chat_rooms)
    if not empty_rooms_check:
        chat_room = []
        print("Setting user on queue...")
        chat_room.append(sid)
        room_ID = str(next(gen_id))
        all_chat_rooms[room_ID] = chat_room
        sio.emit("in_queue", to=sid)
    elif empty_rooms_check:
        keys_list = list(all_chat_rooms.keys())
        for room in keys_list:
            print("Checking room...")
            if len(all_chat_rooms[room]) == 1:
                print("Coonecting user to room...")
                all_chat_rooms[room].append(sid)
                room_data = all_chat_rooms[room]
                #sio.emit("user_found", to=sid)
                sio.emit("connected_to_room", room_data, to=sid)

@sio.event
def client_turn(sid, data):
    sender = ID_list[sid]
    for i in data[0]:
        if i != sid:
            receiver = i
    info = [sender, data]
    sio.emit("turn_to_speak", info, to=receiver)

eventlet.wsgi.server(eventlet.listen(("", 5000)), app)