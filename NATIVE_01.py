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
import atexit
import signal
import sys
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

## cleanup function##
def cleanup():
    if camera.isOpened():
        camera.release()
        cv2.destroyAllWindows()



## termination signal handling##
def signal_handler(sig, frame):
    print('Received termination signal')
    cleanup()  # Your cleanup function to release resources
    sys.exit(0)  # Exit the script

signal.signal(signal.SIGBREAK, signal_handler)

# Register cleanup function to be called on exit
atexit.register(cleanup)

# Set a flag to indicate if the 'r' key is pressed or not
show_video = False
path = r'C:/Users/Smit/Desktop/Dsa Simulator' #change directoryr
os.chdir(path) #change to above path to save file
ret, live = camera.read()  #read live feed
gray = cv2.cvtColor(live, cv2.COLOR_BGR2GRAY)
# create the opencv window
cv2.namedWindow("angio sim", cv2.WND_PROP_FULLSCREEN)
cv2.namedWindow('angio sim', cv2.WINDOW_NORMAL)
cv2.setWindowProperty('angio sim', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
# Function to display the message box
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




# To show a notification, call the function with the desired text
show_notification("Native mode. Press R to view default irradiation view.")
key=cv2.waitKey(1)
#main program loop
while True:
        # Read a frame from the video capture object
    ret, live = camera.read()  #read live feed
    gray = cv2.cvtColor(live, cv2.COLOR_BGR2GRAY)
    key=cv2.waitKey(1) & 0xFF
    #bg=None
    # If the frame was successfully read
    if ret:
        # Display the frame if the 'r' key is pressed
        key=cv2.waitKey(1)  & 0xFF #to run live feed smoothly
        if key == ord('7'):
            exit()
        elif key==ord('1'):
          show_notification("already in Native modem press r for Irradiation View.")
          
        elif key == ord('r'): #if condition for keypress r
          show_video = True  #change value of flag
        elif not keyboard.is_pressed('r'):
          show_video = False        
        if show_video:
          cv2.imshow('angio sim', gray)  #create a blank window
          # Wait for a key press and check if the 'r' key is pressed
          key=cv2.waitKey(1)  & 0xFF #for making the live feed run smoothly      
        
        if key==ord('s'):
                 target = pyautogui.getActiveWindow()
                 location = (
                 target.left,
                 target.top,
                 target.width,
                 target.height
                 )
                 image = pyautogui.screenshot(region=location)
                 now = datetime.now() #get current date and time
                 dt_string = now.strftime("%Y-%m-%d-%H-%M-%S")
                 #image.show()
                 filename1 = 'Screenshot_' + dt_string  +'.jpg'
                 image=image.save(filename1)
                 show_notification("Screenshot saved, please view in folder Dsa Simulator")
                 # Get the handle of the window by its title
        elif key==ord('2'):
                  # To show a notification, call the function with the desired text
        
                  # initialize a frame counter
                  count = 1
        ret, frame = camera.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    acc = gray.astype('float')
    blended = None  # Initialize blended image to None
   