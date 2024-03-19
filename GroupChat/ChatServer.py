import socket
import threading
import time

class ChatServer:
    def __init__(self, host, port, runNetworkDiscoverer):
        self.clients = {}   #store connected clients
        if runNetworkDiscoverer:
            NetworkDiscoverer_thread = threading.Thread(target=self.NetworkDiscoverer_connection)
            NetworkDiscoverer_thread.start()

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



    def send_udp_packet(self, msg):
        data = msg.encode()
        while True:
            # Create a UDP socket
            udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            udp_socket.bind(("0.0.0.0", 26868))
            
            try:
                # Send the UDP packet

                #######udp_socket.sendto(data, (server_address, server_port))
                udp_socket.sendto(data, ("255.255.255.255",26767))
                print(msg, "sent")
                
                # Set a timeout for receiving response
                udp_socket.settimeout(3)  # Timeout set to certain seconds
                
                # Listen for response
                response, address = udp_socket.recvfrom(1024)
                print("Response from Client:", response.decode())
                return response
                
                # Break out of the loop if a response is received
                break
                
            except socket.timeout:
                print("No response received. Resending the packet...")
                # Close the socket
                udp_socket.close()



    def NetworkDiscoverer_connection(self):
        while True:
            self.send_udp_packet("Discover Clients")
            self.send_udp_packet("IP address")
            time.sleep(12)





if __name__ == "__main__":                      #instantiate server with chosen socket and start
    server = ChatServer("0.0.0.0", 65432, True)
    server.start()