# Server imports
import eventlet
import id_gen
from flask import Flask, request
from flask_socketio import SocketIO
from flask_cors import CORS

# Pokemon imports
import main

def check_rooms(all_rooms):
    """Checks every room to find onr for the client

    Args:
        all_rooms (dict): dictionary with all rooms {room_ID: [[sid1,pokemon1],[sid2,pokemon2]]}

    Returns:
        True: If there's any avaliable room for the user (a room with only one user inside)
        False: If there are no rooms whatsoever or all rooms are full (with 2 users)
    """
    # Assume there are no full rooms before checking
    full_rooms = 0
    # Check every room one by one
    for room in all_rooms:
        # If the room only has one user inside...
        if len(all_battle_rooms[room]) == 1:
            print("Battle avaliable for user.")
            # it's an avaliable room for our client so we connect it.
            return True
        # If the room has 2 users (is full)...
        elif len(all_battle_rooms[room]) == 2:
            # add 1 to the full_rooms counter
            full_rooms += 1
        # If the full_room counter is the same as the number of rooms, aka, all rooms are full...
        if full_rooms == len(list(all_rooms.keys())):
            print("All battles are full, creating new one...")
            # create a new room for the client
            return False
    # If there are no rooms at all, create the first room for client
    print("No battles, creating new one...")
    return False

# Weird shit to make the server work on js and html, don't ask questions
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
sio = SocketIO(app, cors_allowed_origins="*")

# Call for the generate_game_ID function, that creates the unique room_ID
gen_id = id_gen.generate_game_ID()

# The ID_list is barely used but it's important to save the sid with it's assigned pokemon ID_list = {sid:pokemon}
ID_list = {}
all_battle_rooms = {}

# First connection
@sio.on("client_connected")
# Upon connecting to the server, the user selects a pokemon (the selection is client sided because I'm lazy and don't wanna adapt it here) and sends all the info to the server
def client_connected(data):
    # data = pokemon
    # Because of flask, we have to get the sid like this, it honestly makes everything cleaner that having to put (sid) in every function
    sid = request.sid
    # Add the user to the ID list
    ID_list[sid] = data
    print(f"User connceted to the server\nID: {sid}\nPokemon: {data["N"]}")
    # Check the rooms status
    avaliable_rooms_check = check_rooms(all_battle_rooms)
    # If there are no empty rooms or no rooms at all...
    if not avaliable_rooms_check:
        # Create a new battle room for the clients
        battle_room = []
        print("Setting user on queue...")
        # save the user info
        user_info = [sid, ID_list[sid]]
        # add the user to the battle room
        battle_room.append(user_info)
        # generate the unique room ID
        battle_ID = str(next(gen_id))
        # add the battle room to the general dictionary
        all_battle_rooms[battle_ID] = battle_room
        # emit this to client to put him in queue
        sio.emit("in_queue", to=sid)
    # If there's any room with only one user...
    elif avaliable_rooms_check:
        # get a list of all room IDs
        keys_list = list(all_battle_rooms.keys())
        for battle in keys_list:
            # check every room
            print("Checking room...")
            # if the battle only has one user inside...
            if len(all_battle_rooms[battle]) == 1:
                print("Coonecting user to room...")
                user_info = [sid, ID_list[sid]]
                # connect the client to the battle
                all_battle_rooms[battle].append(user_info)
                # all_battle_rooms = {ID: [[sid1, pokemon1], [sid2, pokemon2]]}
                # the information we send to each client is different, they have all the info about their pokemon but only know the name and HP or the rival's
                rival_info = [all_battle_rooms[battle][0][0], [all_battle_rooms[battle][0][1]["N"], all_battle_rooms[battle][0][1]["CHP"]]]
                # save all the info we want to send
                battle_info = [user_info, rival_info, battle]
                # emit the info to the client. 
                sio.emit("connected_to_room", battle_info, to=sid)

# Battle started
@sio.on("battle_started")
# when the last user is connected to the room, the info is shown to them first and then to the first client
def battle_started(data):
    sid = request.sid
    # data = [[sid_user, pokemon_user], [sid_rival, [pokemon_rival_name, pokemon_rival_hp]], battle_ID]
    # this is used several time sin the server to get the sid of the other user, as we only get the sid of the user that emitted the event
    # inside of data we find both user's info, so we check each one
    for user in data:
        # if the sid of the user isn't the same sid that emitted the event, it's the other user
        if user[0] != sid:
            # so we save their sid in a new variable
            other_user = user[0]
            break
    # in the same way, the battle_ID is the most important info to get all the pokemon info quickly without having to do 500 checks, si it's sent in every evmit
    battle_ID = data[2]
    # also used a lot throughout the code, we save each pokemon in different variables so we can sort the info quicker
    # we have the battle_ID so we check the user info in all of it
    for user in all_battle_rooms[battle_ID]:
        # and save the respective pokemons for each user
        # note that the pokemon_user is for the other user, not the event emitter
        if user[0] == sid:
            pokemon_rival_raw = user[1]
        else:
            pokemon_user = user[1]
    # once we have all the info stored, we save the info that we want to send the other user
    pokemon_rival = [pokemon_rival_raw["N"], pokemon_rival_raw["CHP"]]
    battle_info = [[other_user, pokemon_user], [sid, pokemon_rival], battle_ID]
    sio.emit("battle_start", battle_info, to=other_user)

# Option chosen
@sio.on("opc_chosen")
# Once any of the clients chose the action (either b or c because a is client sided, and if it's b, we also include the atk_option (if opc = c -> opc_atk = None)),
# we send the chosen option to the main python program to calculate damage
def opc_chosen(data):
    sid = request.sid
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
    # we need ot create this list because it's the one we send to the main program
    pokemons_data = [pokemon_user, pokemon_rival]
    # the main program calculates the damage deat
    dmg = [main.main_battle(pokemons_data ,opc, opc_atk), battle_ID]
    # if damage dealt is 0, it means the oponent has fled. It's not usper conventional but fuck you
    sio.emit("damage_dealt", dmg, to=sid)

# Enemy turn
@sio.on("enemy_turn")
# Once any of the clients attack, we display the damage they dealt and set the in queue waiting for the oponent to take action
def enemy_turn(data):
    sid = request.sid
    # data = [dmg, battle_ID]
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
    # after sorting all the info again, we just send it to the other user so it can chose the next action
    sio.emit("turn_to_attack", battle_info, to=sid_user)

# Battle end
@sio.on("battle_end")
# Once any of the users is defeated, we disconnect first the winner and then use this to notidy the other user that they've been defeated
def battle_end(data):
    sid = request.sid
    # data = [dmg, battle_ID]
    dmg = data[0]
    battle_ID = data[1]
    for user in all_battle_rooms[battle_ID]:
        if user[0] != sid:
            other_user = user[0]
    # disconnecting the user
    sio.disconnect(sid)
    # emitting the last info before disconnecting the other user
    sio.emit("defeated", dmg, to=other_user)

# Disconnect client
@sio.on("disconnect_client")
# Just a small function to disconnect the client server based upon client request
def disconnect_client():
    sid = request.sid
    sio.disconnect(sid)

# Once again just bullshitery to make the server work on html and json, don't ask
# eventlet.wsgi.server(eventlet.listen(('', 5000)), app)
eventlet.monkey_patch()
sio.run(app, host="0.0.0.0", port=5000)
