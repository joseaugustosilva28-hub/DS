temperaturas = (36.5, 37.2, 38.0, 36.8, 39.1)

for temperatura in temperaturas:
    if temperatura < 37.5:
        print(temperatura, " Normal")
    elif temperatura <= 38.5:
        print(temperatura, " Febre moderada")
    else:
        print(temperatura, " Febre alta")
