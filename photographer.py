import serial
import json
import cv2

with open("config.json", "r") as file:
    config = json.load(file)

index = 0
flag = False

V4L_TO_CV2_NAMES = {"brightness": cv2.CAP_PROP_BRIGHTNESS, "contrast": cv2.CAP_PROP_CONTRAST,
                    "saturation": cv2.CAP_PROP_SATURATION, "hue": cv2.CAP_PROP_HUE,
                    "white_balance_temperature_auto": cv2.CAP_PROP_AUTO_WB, "gamma": cv2.CAP_PROP_GAMMA,
                    "gain": cv2.CAP_PROP_GAIN, "white_balance_temperature": cv2.CAP_PROP_WB_TEMPERATURE,
                    "sharpness": cv2.CAP_PROP_SHARPNESS, "backlight_compensation": cv2.CAP_PROP_BACKLIGHT,
                    "exposure_auto": cv2.CAP_PROP_AUTO_EXPOSURE, "exposure_absolute": cv2.CAP_PROP_EXPOSURE}


def set_camera_settings(filename: str, capture: cv2.VideoCapture):
    with open(filename, "r") as f:
        for line in f:
            prop_name = line.split(" ")[0].strip()
            prop_val = line.split("=")[-1].strip()
            if prop_name in V4L_TO_CV2_NAMES:
                capture.set(V4L_TO_CV2_NAMES[prop_name], int(prop_val))


cap = cv2.VideoCapture(int(config["camera"]))
set_camera_settings("camera-settings.txt", cap)

with serial.Serial(config["serial"], '115200', parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE) as serial_connection:
    print("connected")
    while True:
        recv = serial_connection.read(1)
        letter = chr(recv[0])
        if letter.isdecimal() and letter != "0":
            if not flag:
                print("picture time")
                return_value, image = cap.read()
                cv2.imwrite("./well_pics/{:03d}.png".format(index), image)
                index += 1
                flag = True
        elif flag and letter.isdecimal():
            flag = False
