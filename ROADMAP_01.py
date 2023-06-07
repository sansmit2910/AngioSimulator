import pygame
import cv2
from datetime import datetime
import pyautogui
#import matplotlib
import os
import time
import keyboard
import tkinter as tk
#matplotlib.use("TkAgg")
import os
import numpy as np
from datetime import datetime
#import RPi.GPIO as GPIO
import time
import subprocess
# Set the GPIO pin numbering mode
#GPIO.setmode(GPIO.BCM)

# Set the GPIO pin to output mode
#GPIO.setup(17, GPIO.OUT)
camera = cv2.VideoCapture(0)                   # Initialize the video capture object to access the default camera, if not accessible change index
# Set the frame size of the camera capture object to 1280x720
camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
camera.set(cv2.CAP_PROP_FPS, 20)

if not camera.isOpened():                      # if webcam cannot be accessed
   raise IOError("Webcam cannot be opened! Change index!")
ret, live=camera.read()
gray=cv2.cvtColor(live,cv2.COLOR_BGR2GRAY)
script_a_path = r"C:\Users\Smit\Downloads\NATIV_01.py"
script_b_path = r"C:\Users\Smit\Downloads\ROADMAP_01.py"
script_c_path = r"C:\Users\Smit\Downloads\DSA_01.py"
def start_script_a():
    print("Starting script A...")
    subprocess.call(["python", script_a_path])
    print("Script A has been closed.")

def start_script_b():
    print("Starting script B...")
    subprocess.call(["python", script_b_path])
    print("Script B has been closed.")

def start_script_c():
    print("Starting script C...")
    subprocess.call(["python", script_c_path])
    print("Script C has been closed.")

# create the opencv window
cv2.namedWindow("angio sim", cv2.WND_PROP_FULLSCREEN)
cv2.namedWindow('angio sim', cv2.WINDOW_NORMAL)
cv2.setWindowProperty('angio sim', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
# Function to display the message box
# Function to display the message box
# Create a Tkinter window as notification for start
import tkinter as tk

def show_notification(text):
    window = tk.Tk()
    window.overrideredirect(True)
    window.geometry("+{}+{}".format(window.winfo_screenwidth() // 2 - 100, window.winfo_screenheight() // 2 - 50))
    window.attributes("-alpha", 0.7)
    window.attributes("-topmost", True)

    # Create a frame to hold the label
    frame = tk.Frame(window, bg="black")
    frame.pack(fill="both", expand=True)

    # Create a label with the specified font and text, set it to wrap text and fill available space
    label = tk.Label(frame, text=text, font=("Arial", 20), bg='black', fg='white', wraplength=500, justify="center")
    label.pack(fill="both", expand=True)

    # Destroy the window after 3 seconds
    window.after(3000, window.destroy)
    window.mainloop()



acc = gray.astype('float')
blended = None  # Initialize blended image to None
# To show a notification, call the function with the desired text
show_notification("Roadmap Mode. Press r until satisfactory background picture is formed, then d for starting the subtraction and actual roadmap.")
key=cv2.waitKey(1)
count=0
while True:
        key = cv2.waitKey(1)
        if key == ord('2'):
         show_notification("Roadmap Mode. Press r until satisfactory background picture is formed, then d for starting the subtraction and actual roadmap.")
         blended = None
         acc = None
         continue
    
        # Read the next frame
        ret, frame = camera.read()

        if not ret:
         break
    
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        if acc is None:  # If acc is None, set it to the first frame
            acc = gray.astype('float')
       
        if key == ord('1'):  # Escape key
            show_notification(" Native mode, press r for irradiation")
            start_script_a()
            flag = False
        elif key == ord('7'):
            exit()
        elif key == ord('r'):
            # Compute the minimum blend of the current frame and the accumulator
            # Turn on the relay for 5 seconds
            start_time=time.monotonic()
            #GPIO.output(17, GPIO.HIGH)
            acc = np.minimum(acc, gray.astype('float'))

            # Increment the frame counter
            count += 1

            # Convert the blended frame to an unsigned 8-bit integer
            blended = acc.astype('uint8')

            # Display the blended frame
            cv2.imshow("angio sim", blended)
        
        elif key == ord('d'):
            if blended is None:
                continue  # If blended is None, skip the current frame
            # Compute the difference between the current frame and the blended frame
            result = cv2.subtract(gray, blended)
            # Set the result to white
            result = cv2.cvtColor(result, cv2.COLOR_GRAY2BGR)
            result[np.where((result == [255, 255, 255]).all(axis=2))] = [0, 0, 255]
            # Set the background to light gray
            background = np.zeros_like(result)
            background.fill(192)
            # Combine the background and the result
            output = cv2.addWeighted(background, 0.5, result, 0.5, 0.0)
            # Display the difference frame
            cv2.imshow("angio sim", output)

            key = cv2.waitKey(1)
        if key==ord('3'):
            show_notification("DSA mode, press r and release to take background, then d for subtraction sequence which is automatically recorded, and 8 for replazing subtraction sequence")
            start_script_c     
        #if time.monotonic-start_time>=30:
            #GPIO.output(17, GPIO.LOW)
            # Clean up the GPIO pins
            #GPIO.cleanup()     
         #else: 
         #key=cv2.waitKey(1)
        #key=cv2.waitKey(1)        