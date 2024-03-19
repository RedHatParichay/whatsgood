import threading
import time
import tkinter as tk
from ChatClient import ChatClient

def create_client():
    client = ChatClient("localhost", 65432, f"Client-{threading.get_ident()}", None)
    client.start()

def main():
    root = tk.Tk()
    root.withdraw()  # Hide the root window

    num_clients = 199   #Number of clients created

    for _ in range(num_clients):
        root.after(0, create_client)  # Schedule creation of client on main thread

    root.mainloop()

if __name__ == "__main__":
    main()
