from pynput import keyboard
import time
import os
import pygame

pygame.mixer.init()

cmd_pressed = False
copy_count = 0

def play_sound(filename):
    sound_path = os.path.join(os.path.dirname(__file__), filename)
    sound = pygame.mixer.Sound(sound_path)
    sound.play()

play_sound("copy.mp3")

def on_press(key):
    global cmd_pressed, copy_count
    try:
        if key == keyboard.Key.cmd:
            cmd_pressed = True
        elif cmd_pressed and key.char in ['c', 'v']:
            copy_count += 1
            print(f"CMD+C detected. Total count: {copy_count}")
            if key.char == 'c':
                play_sound("copy.mp3")
            elif key.char == 'v':
                play_sound("paste.mp3")  # Add this line to play a sound
        if copy_count % 10 == 0:  # Write to file every 10 copy/paste actions
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
            with open(os.path.expanduser('~/how-many-times-did-I-press-CMD-C-or-V.gregg'), 'a') as f:
                f.write(f"{timestamp}: CMD+C/V pressed {copy_count} times\n")
    except AttributeError:
        pass

def on_release(key):
    global cmd_pressed
    if key == keyboard.Key.cmd:
        cmd_pressed = False

with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()