
with open("tour.gcode", "w") as file:
    start_x = 8
    start_y = 2
    file.write("G90\n")
    file.write("$HX\n")
    file.write("$HY\n")
    file.write("G0X{}Y{}\n".format(start_x, start_y))
    file.write("S1\n")
    file.write("F1000\n")
    for row in range(15):
        if row % 2 == 0:
            order = range(20)
        else:
            order = range(19, -1, -1)
        for col in order:
            file.write("G01X{}Y{}\n".format(start_x + col * 4.5, start_y - row * 4.5))
            file.write("G04P0.25\n")
            file.write("M3\n")
            file.write("G04P0.25\n")
            file.write("M5\n")
