# Server imports
import socketio
from os import system as sy
from time import sleep as s

# Pokemon imports
import interfaz as show

def selec_opc(data):
    opc = None
    while True:
        try:
            s(0.5)
            opc = input("\nSelecione a acción a tomar:\na)Mostrar detalles da batalla\nb)Atacar\nc)Fuxir\n")
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
            print("Opción inválida.")
    return opc

def selec_atk(data):
    # data = [[sid_user, pokemon_user], [sid_rival, [pokemon_rival_name, pokemon_rival_hp]], battle_ID]
    pokemon_usuario = data[0][1]
    while True:
        s(0.2)
        show.mostrar_ataques(pokemon_usuario)
        opc_atk = int(input("Seleccione o ataque(1, 2, 3...):"))
        if int(opc_atk) not in range(1,len(pokemon_usuario["ATK"])+1) or int(pokemon_usuario["ATK"][opc_atk]["CAP"]) == 0:
            print("O ataque seleccionado non existe ou non ten suficientes puntos de acción.")
        else:
            return opc_atk

def stats(data):
    # data = [[sid_user, pokemon_user], [sid_rival, [pokemon_rival_name, pokemon_rival_hp]], battle_ID]
    show.mostrar_stats([data[0][1]])
    print("Rival:\n\t", data[1][1][0], ": HP -->",data[1][1][1])

def battle_opc():
    """Displays a list of options mid battle for the user to select

    Raises:
        ValueError: If any of the values goes vobe the limit or there's an error
    """
    while True:
        try:
            s(0.5)
            opc = input("Selecione a acción a tomar:\na)Mostrar detalles da batalla\nb)Atacar\nc)Fuxir\n")
            opciones = ["A", "a", "B", "b", "C", "c"]
            if opc not in opciones:
                raise ValueError
            print("\n\n")
            break
        except:
            print("Opción inválida.")
    return opc

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
    options = [opc, opc_atk, data[2]]
    sio.emit("opc_chosen", options)
    sio.wait()

@sio.event
def damage_dealt(data):
    # data = [dmg(int/"defeated"), battle_ID]
    if data[0] == "defeated":
        print("You defeated your opponent!")
        exit()
    else:
        print("Your attack dealt",data[0],"points of damage!\nWaiting for opponent to attack...")
    sio.emit("enemy_turn", data)
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

sio.connect("http://localhost:5000")
sio.wait()