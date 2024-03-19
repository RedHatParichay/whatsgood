import socket
import threading

class ChatServer:

    def __init__(self, host, port):
      self.clients = {}   #store connected clients

      try:
          #AF_INET = Address format for IPv4
          #SOCK_STREAM = Socket type for TCP connection
          self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
          self.server_socket.bind((host, port))       #assign port and ip to socket instance
          self.server_socket.listen()                 #listen for incoming connections
          print(f"Server listening on {host}:{port}") #output what socket server is listening on
      except socket.error as e:
          print(f"Socket error: {e}")
          self.server_socket.close()
          return
      except Exception as e:
          print(f"Error: {e}")
          self.server_socket.close()
          return

    def handle_client(self, client_socket, client_address):
        nickname = "Unknown"  # Default value in case an exception occurs

        try:
            nickname = client_socket.recv(1024).decode("utf-8")             #receive and decode nickname from client
            self.clients[client_socket] = nickname                          #associate nickname to its client connection
            print(f"{client_address} connected with nickname: {nickname}")  #output which user connected

            while True:
                message = client_socket.recv(1024).decode("utf-8")          #recieve and decode message
                if not message:     #if there is no message, don't print anything
                    break
                print(f"{nickname}: {message}")                             #print nickname and message

                #encode and send(broadcast) the message to all connected clients within chat except sender
                for other_client, other_nickname in list(self.clients.items()):
                    if other_client != client_socket:
                        try:
                            other_client.send(f"{nickname}: {message}".encode("utf-8"))
                        except socket.error as send_error:
                            print(f"Error sending message to {other_nickname}: {send_error}")

        except socket.error as receive_error:
            print(f"Socket error receiving data: {receive_error}")
        except Exception as e:
            print(f"Error: {e}")

        finally:
            #remove the client on disconnection
            if client_socket in self.clients:
                del self.clients[client_socket]

            try:
                client_socket.shutdown(socket.SHUT_RDWR)        #initiate graceful shutdown
            except socket.error as shutdown_error:
                print(f"Error shutting down socket for {nickname}: {shutdown_error}")

            try:
                client_socket.close()                           #close client socket
                print(f"{nickname} disconnected")               #output which client disconnected
            except socket.error as close_error:
                print(f"Error closing socket for {nickname}: {close_error}")

    def start(self):
        while True:
            try:
                client_socket, addr = self.server_socket.accept()    #accept connection
                print(f"Accepted connection from {addr}")
                #start a new thread to handle the client
                client_thread = threading.Thread(target=self.handle_client, args=(client_socket, addr))
                client_thread.start()
            except socket.error as e:
                print(f"Socket error: {e}")
                break
            except Exception as e:
                print(f"Error: {e}")
                break

        self.server_socket.close()
