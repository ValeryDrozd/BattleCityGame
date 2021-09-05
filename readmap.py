def read_map():
    game_map: list = []
    f = open("map.txt", "r")
    for line in f:
        arr = line.split('\t')
        game_map.append([int(i) for i in arr])
    return game_map
