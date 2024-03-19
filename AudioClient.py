import socket
import threading
import pyaudio
import tkinter as tk

class AudioClient(tk.Tk):

    def __init__(self, callback):
        super().__init__()


        # Constants
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.RATE = 44100
        self.CHUNK = 1024

        self.threadRunning = True

        self.callback = callback
        self.title(f"Audio Client")    #set title of chat window with nickname

        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.recv_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # Initialize PyAudio
        self.p = pyaudio.PyAudio()

        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def on_closing(self):
        self.threadRunning = False

        if self.client_socket:
            self.client_socket.close()  # Close client socket
        if self.recv_socket:
            self.recv_socket.close()    # Close audio socket


        #execute callback function when the window is closed
        if self.callback:
            self.callback()

        self.destroy()              #destroy window

    def send_audio(self, addressTosend):

        stream_in = self.p.open(format=self.FORMAT,
                           channels=self.CHANNELS,
                           rate=self.RATE,
                           input=True,
                           frames_per_buffer=self.CHUNK)

        server_address = (addressTosend, 12345)

        while self.threadRunning:

            try:
                data = stream_in.read(self.CHUNK)
                self.client_socket.sendto(data, server_address)
            except Exception as e:
                break


    def recv_audio(self):
        stream_out = self.p.open(format=self.FORMAT,
                            channels=self.CHANNELS,
                            rate=self.RATE,
                            output=True)

        self.recv_socket.bind(("0.0.0.0", 12345))


        while self.threadRunning:

            try:
                data, client_address = self.recv_socket.recvfrom(2048)
                stream_out.write(data)
            except Exception as e:
                break


    def run(self):

        send_thread = threading.Thread(target=self.send_audio, args=("localhost",))
        recv_thread = threading.Thread(target=self.recv_audio)

        send_thread.start()
        recv_thread.start()

        self.mainloop()

