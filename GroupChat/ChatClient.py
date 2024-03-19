import socket
import threading
import tkinter as tk
from tkinter import scrolledtext

class ChatClient(tk.Tk):
    def __init__(self, host, port, nickname, callback):
        super().__init__()

        self.nickname = nickname        #store nickname of current client
        self.callback = callback        #perform function when chat closed

        self.title(f"Chat Client - {self.nickname}")    #set title of chat window with nickname

        #AF_INET = Address format for IPv4
        #SOCK_STREAM = Socket type for TCP connection
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((host, port))            #connect to socket instance
        self.client_socket.send(nickname.encode("utf-8"))   #send nickname to server

        #display viewable and scrollable chat history area
        self.chat_display = scrolledtext.ScrolledText(self, wrap=tk.WORD, state=tk.DISABLED)
        self.chat_display.pack(expand=True, fill="both")

        #area to type messages
        self.message_entry = tk.Entry(self)
        self.message_entry.pack(expand=True, fill="x")

        #button when clicked will send the message
        self.send_button = tk.Button(self, text="Send", command=self.send_message)
        self.send_button.pack()

        #start thread to receive messages
        self.receive_thread = threading.Thread(target=self.receive_messages)
        self.receive_thread.start()

        #bind the window closing event to the on_closing method
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def on_closing(self):
        #notify the server about client leaving
        self.client_socket.send("[DISCONNECT]".encode("utf-8"))

        self.client_socket.close()  #close client socket

        #execute callback function when the window is closed
        if self.callback:
            self.callback()

        self.destroy()              #destroy window

    def send_message(self):
        message = self.message_entry.get()                  #get message from message typing area
        if message:                                             #if it contains a message
            self.client_socket.send(message.encode("utf-8"))    #encode and send message
            self.display_message(f"{self.nickname}: {message}") #display sent message
            self.message_entry.delete(0, tk.END)           #delete message from message typing area

    def receive_messages(self):
        while True:
            try:
                message = self.client_socket.recv(1024).decode("utf-8") #receive and decode message
                if not message: #if it does not contains a message, don't do anything
                    break
                self.display_message(message)   #or else display message
            except ConnectionResetError:
                break
            except Exception as e:
                print(f"Error: {e}")
                break

    def display_message(self, message):
        self.chat_display.config(state=tk.NORMAL)           #set state to normal to enable editing
        self.chat_display.insert(tk.END, f"{message}\n")    #display received/sent message
        self.chat_display.config(state=tk.DISABLED)      #set state back to disabled to disable editing
        self.chat_display.yview(tk.END)         #scroll to the end to show the latest messages

    def start(self):        #start tkinter mainloop
        self.mainloop()

