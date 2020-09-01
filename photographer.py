import serial
import json
import cv2

with open("config.json", "r") as file:
    config = json.load(file)

index = 0
flag = False

V4L_TO_CV2_NAMES = {"Brightness": cv2.CAP_PROP_BRIGHTNESS, "Contrast": cv2.CAP_PROP_CONTRAST,
                    "Saturation": cv2.CAP_PROP_SATURATION, "Hue": cv2.CAP_PROP_HUE,
                    "White Balance Temperature, Auto": cv2.CAP_PROP_AUTO_WB, "Gamma": cv2.CAP_PROP_GAMMA,
                    "Gain": cv2.CAP_PROP_GAIN, "White Balance Temperature": cv2.CAP_PROP_WB_TEMPERATURE,
                    "Sharpness": cv2.CAP_PROP_SHARPNESS, "Backlight Compensation": cv2.CAP_PROP_BACKLIGHT,
                    "Exposure, Auto": cv2.CAP_PROP_AUTO_EXPOSURE, "Exposure (Absolute)": cv2.CAP_PROP_EXPOSURE}


def set_camera_settings(filename: str, capture: cv2.VideoCapture):
    with open(filename, "r") as f:
        for line in f:
            parts = line.split(":")
            if len(parts) == 3 and parts[1] in V4L_TO_CV2_NAMES:
                capture.set(V4L_TO_CV2_NAMES[parts[1]], int(parts[2]))


cap = cv2.VideoCapture(int(config["camera"]))
set_camera_settings("camera-settings.txt", cap)

serial_connection = serial.Serial(config["serial"], '115200', parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE)
# serial_connection.open()

while True:
    recv = serial_connection.read(1)
    letter = chr(recv[0])
    if letter.isdecimal() and letter != "0":
        if not flag:
            print("picture time")
            return_value, image = cap.read()
            cv2.imwrite("well_pics/{:03d}.png".format(index), image)
            index += 1
            flag = True
    elif flag and letter.isdecimal():
        flag = False
