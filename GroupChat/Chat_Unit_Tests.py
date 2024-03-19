import unittest
import socket
import threading
import time
from ChatServer import ChatServer

class TestChatServer(unittest.TestCase):
    def setUp(self):
        self.server = ChatServer("localhost", 65432, False)
        self.server_thread = threading.Thread(target=self.server.start)
        self.server_thread.start()
        time.sleep(1)  # Give some time for the server to start

    def tearDown(self):
        self.server.server_socket.close()  # Close server socket
        self.server_thread.join()  # Wait for the server thread to finish

    def test_message_transmission(self):
        # Mock client
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(("localhost", 65432))
        secndClient_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        secndClient_socket.connect(("localhost", 65432))

        try:
            # Send nickname
            client_socket.send(b"TestClient")
            secndClient_socket.send(b"SecondClient")

            # Send message
            client_socket.send(b"Hello, this is a test message")

            # Receive message from server
            received_message = secndClient_socket.recv(1024).decode("utf-8").strip()
            expected_message = "TestClient: Hello, this is a test message"

            self.assertEqual(received_message, expected_message)

        finally:
            client_socket.close()
            secndClient_socket.close()


    def test_client_disconnection(self):
        # Mock client
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(("localhost", 65432))

        try:
            # Send nickname
            client_socket.send(b"TestClient")

            # Disconnect client
            client_socket.close()

            # Give some time for server to process disconnection
            time.sleep(1)

            # Verify that client is removed from the server's client list
            self.assertNotIn(client_socket, self.server.clients.values())

        finally:
            client_socket.close()


    def test_bi_directional_message_transmission(self):
        # Mock client 1
        client_socket1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket1.connect(("localhost", 65432))

        # Mock client 2
        client_socket2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket2.connect(("localhost", 65432))

        try:
            # Send nickname for client 1
            client_socket1.send(b"TestClient1")

            # Send nickname for client 2
            client_socket2.send(b"TestClient2")

            # Send message from client 1
            client_socket1.send(b"Hello from client 1")

            # Receive message from server for client 2
            received_message2 = client_socket2.recv(1024).decode("utf-8").strip()
            expected_message2 = "TestClient1: Hello from client 1"

            # Send message from client 1
            client_socket2.send(b"Hello from client 2")

            # Receive message from server for client 1
            received_message1 = client_socket1.recv(1024).decode("utf-8").strip()
            expected_message1 = "TestClient2: Hello from client 2"

            self.assertEqual(received_message1, expected_message1)
            self.assertEqual(received_message2, expected_message2)

        finally:
            client_socket1.close()
            client_socket2.close()






if __name__ == "__main__":
    unittest.main()
