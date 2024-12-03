# Server imports
import socketio
import eventlet
import id_gen

# Pokemon imports
import main

def check_rooms(all_rooms):
    full_rooms = 0
    for room in all_rooms:
        if len(all_battle_rooms[room]) == 1:
            print("Battle avaliable for user.")
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
    ID_list[sid] = data
    print(f"User connceted to the server\nID: {sid}\nPokemon: {data["N"]}")
    empty_rooms_check = check_rooms(all_battle_rooms)
    if not empty_rooms_check:
        battle_room = []
        print("Setting user on queue...")
        user_info = [sid, ID_list[sid]]
        battle_room.append(user_info)
        battle_ID = str(next(gen_id))
        all_battle_rooms[battle_ID] = battle_room
        sio.emit("in_queue", to=sid)
    elif empty_rooms_check:
        keys_list = list(all_battle_rooms.keys())
        for battle in keys_list:
            print("Checking room...")
            if len(all_battle_rooms[battle]) == 1:
                print("Coonecting user to room...")
                user_info = [sid, ID_list[sid]]
                all_battle_rooms[battle].append(user_info)
                # all_battle_rooms = {ID: [[sid1, pokemon1], [sid2, pokemon2]]}
                rival_info = [all_battle_rooms[battle][0][0], [all_battle_rooms[battle][0][1]["N"], all_battle_rooms[battle][0][1]["CHP"]]]
                battle_info = [user_info, rival_info, battle]
                sio.emit("connected_to_room", battle_info, to=sid)

@sio.event
def battle_started(sid, data):
    # data = [[sid_user, pokemon_user], [sid_rival, [pokemon_rival_name, pokemon_rival_hp]], battle_ID]
    for user in data:
        if user[0] != sid:
            other_user = user[0]
            break
    battle_ID = data[2]
    for user in all_battle_rooms[battle_ID]:
        if user[0] == sid:
            pokemon_rival_raw = user[1]
        else:
            pokemon_user = user[1]
    pokemon_rival = [pokemon_rival_raw["N"], pokemon_rival_raw["CHP"]]
    battle_info = [[other_user, pokemon_user], [sid, pokemon_rival], battle_ID]
    sio.emit("battle_start", battle_info, to=other_user)

@sio.event
def opc_chosen(sid, data):
    # data = [opc, opc_atk, battle_ID]
    opc = data[0]
    opc_atk = data[1]
    battle_ID = data[2]
    # all_battle_rooms = {ID: [[sid1, pokemon1], [sid2, pokemon2]]}
    for user in all_battle_rooms[battle_ID]:
        if user[0] == sid:
            pokemon_user = user[1]
        else:
            pokemon_rival = user[1]
    # both pokemons have all their info
    pokemons_data = [pokemon_user, pokemon_rival]
    dmg = [main.main_battle(pokemons_data ,opc, opc_atk), battle_ID]
    sio.emit("damage_dealt", dmg, to=sid)

@sio.event
def enemy_turn(sid, data):
    dmg = data[0]
    battle_ID = data[1]
    # all_battle_rooms = {ID: [[sid1, pokemon1], [sid2, pokemon2]]}
    for user in all_battle_rooms[battle_ID]:
        if user[0] == sid:
            pokemon_rival = user[1]
        else:
            sid_user = user[0]
            pokemon_user = user[1]
    rival_info = [pokemon_rival["N"], pokemon_rival["CHP"]]
    # battle_info = [[[sid_user, pokemon_user], [sid_rival, [pokemon_rival_name, pokemon_rival_hp]], battle_ID], dmg]
    battle_info = [[[sid_user, pokemon_user], [sid, rival_info], battle_ID], dmg]
    sio.emit("turn_to_attack", battle_info, to=sid_user)

@sio.event
def battle_end(sid, data):
    # data = [dmg, battle_ID]
    dmg = data[0]
    battle_ID = data[1]
    for user in all_battle_rooms[battle_ID]:
        if user[0] != sid:
            other_user = user[0]
    sio.disconnect(sid)
    sio.emit("defeated", dmg, to=other_user)

@sio.event
def disconnect_client(sid):
    sio.disconnect(sid)

eventlet.wsgi.server(eventlet.listen(("", 5000)), app)