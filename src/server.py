# Server imports
import socketio
import eventlet
import id_gen

# Pokemon imports
import pokemons

pokemons.new()
pokemon_user1 = pokemons.gens["I"][0]
pokemon_user2 = pokemons.gens["I"][3]
pokemons_battle = [pokemon_user1, pokemon_user2]

def check_rooms(all_rooms):
    full_rooms = 0
    for room in all_rooms:
        if len(all_battle_rooms[room]) == 1:
            print("battle avaliable for user.")
            return True
        elif len(all_battle_rooms[room]) == 2:
            full_rooms += 1
        if full_rooms == len(list(all_rooms.keys())):
            print("All battles are full, creating new one...")
            return False
    print("No battles, creating new one...")
    return False

sio = socketio.Server()
app = socketio.WSGIApp(sio)

ID_list = {}
all_battle_rooms = {}

gen_id = id_gen.generate_game_ID()

@sio.event
def client_connected(sid, data):
    ID_list[sid] = [data, pokemons_battle[len(ID_list)]]
    print(f"User connceted to the server as\nID: {sid}\nUsername: {data}")
    empty_rooms_check = check_rooms(all_battle_rooms)
    if not empty_rooms_check:
        battle_room = []
        print("Setting user on queue...")
        user_info = [sid, ID_list[sid][1]]
        battle_room.append(user_info)
        battle_ID = str(next(gen_id))
        all_battle_rooms[battle_ID] = battle_room
        sio.emit("in_queue", user_info, to=sid)
    elif empty_rooms_check:
        keys_list = list(all_battle_rooms.keys())
        for battle in keys_list:
            print("Checking room...")
            if len(all_battle_rooms[battle]) == 1:
                print("Coonecting user to room...")
                user_info = [sid, ID_list[sid][1]]
                all_battle_rooms[battle].append(user_info)
                room_data = all_battle_rooms[battle]
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