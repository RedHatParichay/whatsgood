
import threading
import time
import tkinter as tk
from AudioClient import AudioClient

def create_Audio():
    client = AudioClient(callback = None)
    client.run()

def main():
    root = tk.Tk()
    root.withdraw()  # Hide the root window

    num_clients = 1     #Number of audio clients made

    for _ in range(num_clients):
        root.after(0, create_Audio)  # Schedule creation of client on main thread

    root.mainloop()

if __name__ == "__main__":
    main()