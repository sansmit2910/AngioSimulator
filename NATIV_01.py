import cv2
import keyboard
import threading
import keyboard
import subprocess
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




# To show a notification, call the function with the desired text
show_notification("Native mode. Press R for default irradiation.")
key=cv2.waitKey(1)
class WebcamThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        self.frame = None
        self.running = True
    
    def run(self):
        while self.running:
            ret, frame = self.cap.read()
            if ret:
                frame = cv2.resize(frame, (0, 0), fx=3, fy=3)
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                self.frame = frame
    
    def stop(self):
        self.running = False
        self.cap.release()

def show_webcam():
    webcam_thread = WebcamThread()
    webcam_thread.start()

    r_pressed = False
    frozen_frame = None

    try:
        while True:
            ####################################################Key###########################################################
            if keyboard.is_pressed("r") and not r_pressed:
                r_pressed = True
            elif not keyboard.is_pressed("r") and r_pressed:
                r_pressed = False
                frozen_frame = webcam_thread.frame.copy() if webcam_thread.frame is not None else None

            ####################################################Show IMAGE###########################################################
            if r_pressed:
                frame = webcam_thread.frame.copy() if webcam_thread.frame is not None else None
            else:
                frame = frozen_frame
            
            cv2.namedWindow('Webcam', cv2.WINDOW_NORMAL)
            cv2.setWindowProperty('Webcam', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
            if frame is not None:
                cv2.imshow('Webcam', frame)
            ####################################################Show IMAGE###########################################################

            key = cv2.waitKey(1) & 0xFF
            if key == ord('7'):  # Check if 'q' key is pressed
                break

    except KeyboardInterrupt:
        pass

    # Release the webcam and close all windows
    webcam_thread.stop()
    webcam_thread.join()
    cv2.destroyAllWindows()

show_webcam()
