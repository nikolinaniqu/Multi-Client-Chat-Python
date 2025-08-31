from server import Server
from client import Client,Database
from threading import Thread
import time

class Menu:
    """

    The Menu class manages the overall interaction flow of the chat application.
    It provides options to start the server, start a client, or exit the program.

    """
    def __init__(self):
        """
        Initializes the Menu object by setting up attributes to store the server instance
        and a list of connected client instances.
         Attributes:
            server (Server or None): The chat server instance, default is None.
            clients (list): A list of client instances that are connected to the server.
        """
        self.server=None
        self.clients=[]

    def main_menu(self):
        """
        Displays the main menu in the console and allows the user to choose an option:
        - Start the server
        - Start a client
        - Exit the application

        The loop continues until the user selects to exit the program. It ensures the user
        is prompted until a valid option is entered.
        Returns:
            None
        """
        while True:
            print("Chat Application Menu:")
            print("a) Start the Server")
            print("b) Start the client")
            print("q) Exit the program")

            choice= input("Please select an option(a/b/q):").strip().lower()

            if choice=="a":
                Menu.start_server(self)
            elif choice=="b":
                Menu.start_client(self)
            elif choice== "q":
                self.close_application()
                print("Closing the application!")
                break
            else:
                print("Please choose a valid option!")
                self.main_menu()
                time.sleep(2)

    def start_server(self):
        """
        Starts the chat server if it is not already running.
        If the server is already running, it notifies the user.
        A new thread is created to handle the server's tasks concurrently.


        Returns:
            This method does not return anything.
        """
        if self.server:
            print("Server is already running!")
        else:
            self.server=Server("127.0.0.1",8095)
            server_thread= Thread(target=self.server.startServer, daemon=True)
            server_thread.start()
    def start_client(self):
        """
        Starts a new client, connects it to the server, and manages its message
        sending and receiving processes.

        A new instance of the `Client` class is created and added to the `clients` list.
        The client will automatically send and receive messages in the background.

        This method also interacts with the database to store and retrieve chat messages.
        Returns:
            This method does not return anything.
        """
        db=Database()
        client=Client("127.0.0.1",8095,db)
        self.clients.append(client)
        client.send_messages()
        client.receive_messages()
        db.get_messages()
        db.save_messages()
        print("Client started and connected to the server")

    def close_application(self):
        """
        Stops the server (if running) and disconnects all clients from the chat application.
        This method closes all active client connections and prints a final message indicating
        the application has been closed.


        Returns:
            This method does not return anything.
        """
        if self.server:
            print("Stopping the server.")
        for client in self.clients:
            print(f"Disconnecting the {client.name} form the chat application!")
            client.client_socket.close()
        print("All client connections are disconnected")

        print("The application closed!")

if __name__== "__main__":
    menu= Menu()
    menu.main_menu()