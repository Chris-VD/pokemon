def generate_game_ID():
    ID = 1
    while True:
        yield str(ID)
        ID += 1