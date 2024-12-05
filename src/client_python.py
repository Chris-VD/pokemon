# Server imports
import socketio
from os import system as sy
from time import sleep as s

# Pokemon imports
import interfaz as show
import pokemons as p

p.new()

def selec_pokemon():
    while True:
        try:
            show.display_gens()
            selec = input("Select a generation"
                          "\n\t*Note: Gen X is an experimental generation with fake pokemons!\n")
            if int(selec) not in range(1, len(p.gens)+1):
                raise ValueError
            keys = list(p.gens.keys())
            selec = keys[int(selec)-1]
            pokemons = p.gens[selec]
            show.display_pokemons(pokemons)
            selec = input("Seleccione o pokemon que queres empregar (1, 2, 3...):\n")
            if (int(selec) not in range(1, len(pokemons)+1)):
                raise ValueError
            break
        except:
            print("Opción inválida.")
    pokemon_usuario = pokemons[int(selec)-1]
    return pokemon_usuario

def selec_opc(data):
    opc = None
    while True:
        try:
            s(0.5)
            opc = input("\nSelect action:\na)Show battle details\nb)Attack\nc)Flee\n")
            opciones = ["A", "a", "B", "b", "C", "c"]
            if opc not in opciones:
                raise ValueError
            if opc == "a" or opc == "A":
                print("\n")
                stats(data)
                continue
            print("\n\n")
            break
        except:
            print("Invalid option.")
    return opc

def selec_atk(data):
    # data = [[sid_user, pokemon_user], [sid_rival, [pokemon_rival_name, pokemon_rival_hp]], battle_ID]
    pokemon_usuario = data[0][1]
    while True:
        try:
            s(0.2)
            show.mostrar_ataques(pokemon_usuario)
            opc_atk = int(input("Select an attack(1, 2, 3...):"))
            if int(opc_atk) not in range(1,len(pokemon_usuario["ATK"])+1) or int(pokemon_usuario["ATK"][(opc_atk-1)]["CAP"]) == 0:
                print("Selected attack doesn't exist or it doesn't have remaining action points.")
            else:
                return opc_atk
        except:
            print("Invalid option.")

def stats(data):
    # data = [[sid_user, pokemon_user], [sid_rival, [pokemon_rival_name, pokemon_rival_hp]], battle_ID]
    show.mostrar_stats([data[0][1]])
    print("Rival:\n\t", data[1][1][0], ": HP -->",data[1][1][1])

sio = socketio.Client()

@sio.event
def connect():
    print("Connected to the server.")
    while True:
        print("Welcome to this pokemon game!")
        pokemon = selec_pokemon()
        sio.emit("client_connected", pokemon)
        sio.wait()

@sio.event
def in_queue():
    print("No arena avaliable, you're curerntly in queue...")
    sio.wait()

@sio.event
def connected_to_room(data):
    # data = [[sid_user, pokemon_user], [sid_rival, [pokemon_rival_name, pokemon_rival_hp]], battle_ID]
    print("Your prokemon is", data[0][1]["N"], "\nYou've been connectd to an arena!")
    stats(data)
    print("\nWaiting for rival to attack...")
    sio.emit("battle_started", data)
    sio.wait()

@sio.event
def battle_start(data):
    # data = [[sid_user, pokemon_user], [sid_rival, [pokemon_rival_name, pokemon_rival_hp]], battle_ID]
    print("Your prokemon is", data[0][1]["N"], "\nYou've been connectd to an arena!")
    stats(data)
    opc = selec_opc(data)
    if opc == "b" or opc == "B":
        opc_atk = selec_atk(data)
    elif opc == "c" or opc == "C":
        opc_atk = None
    options = [opc, opc_atk, data[2]]
    sio.emit("opc_chosen", options)
    sio.wait()

@sio.event
def damage_dealt(data):
    # data = [dmg(int/["defeated", int]), battle_ID]
    dmg = data[0]
    battle_ID = data[1]
    BS = None
    if type(dmg) == list:
        BS = dmg[0]
        damage = dmg[1]
    else:
        damage = dmg
    if BS == "defeated" or damage == 0:
        print("You dealt",damage,"points of damage and defeated your opponent!")
        damage_info = [damage, battle_ID]
        sio.emit("battle_end", damage_info)
        sio.wait()
    else:
        print("Your attack dealt",damage,"points of damage!\nWaiting for opponent to attack...")
    damage_info = [damage, battle_ID]
    sio.emit("enemy_turn", damage_info)
    sio.wait()

@sio.event
def turn_to_attack(data):
    # data = [[[sid_user, pokemon_user], [sid_rival, [pokemon_rival_name, pokemon_rival_hp]], battle_ID], dmg]
    dmg = data[1]
    battle_info = data[0]
    battle_ID = battle_info[2]
    print("Your oponent attacked and dealt",dmg,"poinst of damage!")
    opc = selec_opc(battle_info)
    if opc == "b" or opc == "B":
        opc_atk = selec_atk(battle_info)
    options = [opc, opc_atk, battle_ID]
    sio.emit("opc_chosen", options)
    sio.wait()

@sio.event
def defeated(data):
    dmg = data
    print("Your oponent attacked and dealt",dmg,"poinst of damage!")
    print("You have been defeated!")
    sio.emit("disconnect_client")
    sio.wait()

@sio.event
def disconnect():
    print("Disconnecting from server...")
    exit()

sio.connect("http://localhost:5000")
sio.wait()