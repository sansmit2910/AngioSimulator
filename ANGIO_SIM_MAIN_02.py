import keyboard
import subprocess
import threading
import pygame
import tkinter as tk
import cv2
import signal
import os
import textwrap

# initialize pygame
pygame.init()

# define some colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# set the screen size
screen_size = (1920, 1080)

# create the screen
screen = pygame.display.set_mode(screen_size, pygame.FULLSCREEN)

# set the window title
pygame.display.set_caption("Title Slide")

# load font and set font size
font = pygame.font.SysFont(None, 100)

# render the title text
title_text = font.render("Angio Simulator", True, BLACK)

# get the size of the title text
title_rect = title_text.get_rect()

# center the title text
title_rect.center = screen.get_rect().center

# render the instructions text
font = pygame.font.SysFont(None, 50)
instructions = "Welcome to Angio Simulator, press r foot pedal to start, then press 1 for Native mode, 2 for Roadmap or 3 for DSA modes respectively"

# Wrap the text
instructions_wrapped = textwrap.wrap(instructions, width=50)

# Render each line and blit them one after the other, with a line height as the vertical offset
line_height = font.get_height()
for i, line in enumerate(instructions_wrapped):
    instructions_text = font.render(line, True, BLACK)
    screen.blit(instructions_text, (20, title_rect.bottom + 50 + i*line_height))

# set up the buttons
button_width = 200
button_height = 50
button_margin = 20
button_y = screen_size[1] - button_height - button_margin
next_button_x = button_margin
close_button_x = screen_size[0] - button_width - button_margin
next_button = pygame.Rect(next_button_x, button_y, button_width, button_height)
close_button = pygame.Rect(close_button_x, button_y, button_width, button_height)

# render the text for the buttons
font = pygame.font.SysFont(None, 30)
next_text = font.render("Next", True, WHITE)
close_text = font.render("Close", True, WHITE)

# flag to track whether the program should start
start_program = False

# flag to track whether the program is running
running = True

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

def start_script_a():
    global current_process
    if current_process is not None:
        current_process.terminate()
        current_process.wait()
    print("Starting script A...")
    current_process = subprocess.Popen(["python", script_a_path])
    current_process.wait()
    print("Script A has been closed.")

def start_script_b():
    global current_process
    if current_process is not None:
        current_process.terminate()
        current_process.wait()
    print("Starting script B...")
    current_process = subprocess.Popen(["python", script_b_path])
    current_process.wait()
    print("Script B has been closed.")

def start_script_c():
    global current_process
    if current_process is not None:
        current_process.terminate()
        current_process.wait()
    print("Starting script C...")
    current_process = subprocess.Popen(["python", script_c_path])
    current_process.wait()
    print("Script C has been closed.")

def main_program():
    print("ANGIO_SIM is running.")
    running = True
    while running:
        # Check for key press events
        if keyboard.is_pressed('1'):
            start_script_a()
        elif keyboard.is_pressed('2'):
            start_script_b()
        elif keyboard.is_pressed('3'):
            start_script_c()
        elif keyboard.is_pressed('7'):
            running = False
            print("ANGIO_SIM has been closed.")
        else:
            # Do other tasks in the main program
            pass

if __name__ == "__main__":
    # Start the main program in a separate thread
    main_thread = threading.Thread(target=main_program)
    main_thread.start()

    # main event loop
    while running:
        # fill the screen with white
        screen.fill(WHITE)

        # draw the title and buttons
        screen.blit(title_text, title_rect)
        pygame.draw.rect(screen, BLACK, next_button)
        pygame.draw.rect(screen, BLACK, close_button)
        screen.blit(next_text, next_button)
        screen.blit(close_text, close_button)

        # update the screen
        pygame.display.update()

        # handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # quit if the close button is clicked
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # check if the next or close button is clicked
                if next_button.collidepoint(event.pos):
                    # set the flag to start the program
                    start_program = True
                    # exit the event loop
                    running = False
                elif close_button.collidepoint(event.pos):
                    # exit the event loop
                    running = False
            elif event.type == pygame.KEYDOWN:
                # check if the 'r' or 'd' key is pressed
                if event.key == pygame.K_r:
                    # set the flag to start the program
                    start_program = True
                    # exit the event loop
                    running = False
                elif event.key == pygame.K_d:
                    # exit the event loop
                    running = False

    # Wait for the main program thread to finish
    main_thread.join()

# Quit pygame
pygame.quit()
