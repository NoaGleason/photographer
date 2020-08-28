
with open("tour.gcode", "w") as file:
    file.write("G90\n")
    file.write("G0X0Y0\n")
    file.write("S1\n")
    file.write("F1000\n")
    for row in range(15):
        if row % 2 == 0:
            order = range(20)
        else:
            order = range(19, -1, -1)
        for col in order:
            file.write("G01X{}Y{}\n".format(1.5+col*5, row*-2.5))
            file.write("G04P0.25\n")
            file.write("M3\n")
            file.write("G04P0.25\n")
            file.write("M5\n")
