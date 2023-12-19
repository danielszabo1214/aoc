with open("2.input") as f:
    s = 0
    power = 0
    for line in f:
        line = line.rstrip()
        game, hands = line.split(": ")
        game = int(game.split(" ")[-1])
        possible = True
        mr, mb, mg = 0, 0, 0
        for hand in hands.split("; "):
            # if not possible:
            #     break
            r, b, g = 0, 0, 0
            cubes = hand.split(", ")
            for cube in cubes:
                n, color = cube.split(" ")
                if color == "red":
                    r = int(n)
                if color == "blue":
                    b = int(n)
                if color == "green":
                    g = int(n)
            print(game, "\t", r, "\t", b, "\t", g)
            mr = max(r, mr)
            mb = max(b, mb)
            mg = max(g, mg)
            if not (r <= 12 and g <= 13 and b <= 14):
                possible = False
                print(game, "not possible")
        if possible:
            print(game, "possible")
            s += game
        power += mr * mb * mg
    print(s)
    print(power)
