import serial
import json
import subprocess

with open("config.json", "r") as file:
    config = json.load(file)

index = 0
flag = False

subprocess.run(["v4l2ctrl", "-d", config["camera"], "-l", "camera-settings.txt"])

serial_connection = serial.Serial(config["serial"], '115200', parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE)
# serial_connection.open()

while True:
    recv = serial_connection.read(1)
    letter = chr(recv[0])
    if letter.isdecimal() and letter != "0":
        if not flag:
            print("picture time")
            subprocess.run(["streamer", "-f", "jpeg", "-o", "/home/noa/PycharmProjects/photographer/well_pics/{:03d}.jpeg".format(index), "-c", config["camera"]])
            index += 1
            flag = True
    elif flag and letter.isdecimal():
        flag = False
