import socket
from threading import Thread

class Server:
    """
    Chatserver accepts the connections of the clients and handles the broadcasting of the messages.
    Attributes:
        client_list: (list) of the clients, containing the name of the client(string) and
        the client_socket(socket.socket)-Client`s socket connection
    """
    client_list = []
    def __init__(self,host,port):
        """
        Initializes the chatserver, via host and  port, binds it and start listening.
        Args:
            host: (str) The IP address to bind the server.
            port: (int) The port number to listen on.
        """
        #AF_INET is the Internet address family for IPv4. SOCK_STREAM is the socket type for TCP,
        # protocol used for the transport of the messages.
        self.socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.socket.bind((host,port))
        self.socket.listen(5)
        print("Server waiting for connection.....")

    def startServer(self):
        """
        Continuously accepts the new client connections, handles the client communication via threads.
        Returns:
            None: This method does not return; it blocks indefinitely.
        """
        while True:
            #Accept the connections from outside/other clients
            (client_socket,address)=self.socket.accept()
            print("Connection from:", str(address))

            client_name=client_socket.recv(1024).decode()
            client = {"client_name":client_name,"client_socket": client_socket}

            self.broadcast_message(client_name,f"{client_name} has joined the chat!")
            Server.client_list.append(client)
            Thread(target=self.add_new_client, args=(client,)).start()
    def add_new_client(self, client:dict):
        """
        Handle incoming messages from a specific client.
        Args:
            client:
                (dict) Client descriptor contains a "client_name" and "client_socket".
        Returns:
            None: This method does not return; it blocks indefinitely.
        """
        client_name=client["client_name"]
        client_socket=client["client_socket"]
        while True:
            try:
                client_message=client_socket.recv(1024).decode()
                if client_message.strip() == client_name + "bye" or not client_message.strip():
                    self.broadcast_message(client_name,f"{client_name} has left the chat!")
                    Server.client_list.remove(client)
                    client_socket.close()
                    break
                else:
                    self.broadcast_message(client_name,f"\033[35m{client_message}\033[0m")
            except:
                print(f"Error with client {client_name}. Removing client.")
                Server.client_list.remove(client)
                client_socket.close()
                break
    def broadcast_message(self, sender_name, message):
        """
        This method sends a message to all connected clients except the sender.
        Args:
            sender_name: (str) Name of the client sending the message.
            message: (str) The message to broadcast.

        Returns:
            None: This method does not return any value.
        """

    #Send message to clients except the sender
        for client in Server.client_list:
            client_socket=client["client_socket"]
            client_name=client["client_name"]
            if client_name != sender_name:
                client_socket.send(message.encode())
#Test
if __name__ == "__main__":
    server=Server("127.0.0.1",8095)
    server.startServer()

