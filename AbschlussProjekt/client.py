import socket
from threading import Thread
import sqlite3
import datetime as dt
import sys


class Client:
    """
    A class representing a client in a chat application. This class handles connecting to a server,
    sending and receiving messages, and managing the client's interactions with the server.
    """
    def __init__(self, host: str, port: int, db):
        """
        Initializes the Client by connecting to the server and starting communication.
        Args:
            host: (str) 127.0.0.1
            port: (int) 8095
            db: database
        """
        self.socket = socket.socket()
        self.socket.connect((host, port))
        self.name = input("Enter your name: ")
        self.db = db
        self.socket.send(self.name.encode())

        # Start a thread to listen for incoming messages
        Thread(target=self.receive_messages, daemon=True).start()

        # Start sending messages
        self.send_messages()

    def send_messages(self):
        """
        This method continuously accepts the user's input and sends it to the server.
        Returns:
            None: This method does not return any value.
        """
        while True:
            client_input = input("")
            if client_input.lower() in ["exit", "q"]:
                if self.socket:
                    self.socket.send(f"{self.name} has left the chat!".encode())
                    self.socket.close()
                print("Closing the chat application!")
                sys.exit()

            else:
                if self.socket:
                    client_message = f"{self.name}: {client_input}"
                    self.socket.send(client_message.encode())
                    self.db.save_messages(self.name, client_input)
                else:
                    print("Socket is closed, can't send messages!")
                    break  # Exit if the socket is closed

    def receive_messages(self):
        """
        This method receives messages from the server and prints them to the console.
        If the connection is lost, it prints a disconnect message.
        Returns:
            None: This method does not return; it blocks indefinitely.
        """
        while True:
            try:
                server_message = self.socket.recv(1024).decode()
                if not server_message:
                    print("Disconnected from the server.")
                    break
                print(server_message)
            except Exception as e:
                print(f"Error receiving message: {e}")
                break
class Database:
    """
    This class provides methods for saving messages to a database.
    """
    def __init__(self, db="chat.db"):
        """
        This method initializes the database connection and creates a table for storing the messages if it does not exist.
        Args:
            db: (str) The name of the Database file ("chat.db").
        """
        self.db=db
        self.conn= sqlite3.connect("chat.db")
        self.cursor=self.conn.cursor()
        self.create_table()
    def create_table(self):
        """
        This method creates the table "chat_messages". The table stores the sender's name,
        message content, and timestamp for each chat message.
        Returns:
            None: This method does not return any value.

        """
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS chat_messages(id INTEGER PRIMARY KEY AUTOINCREMENT,sender_name TEXT,
        message TEXT, timestamp TEXT)
        """)
        self.conn.commit()
    def save_messages(self, sender_name, message):
        """
        This method saves the messages to the database with the timestamp.
        Args:
            sender_name: (str) The name of the message sender.
            message: (str) The content of the chat message.

        Returns:
            None; This method does not return any value, it saves the messages into a database.
        """
        timestamp=dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.cursor.execute("""
        INSERT INTO chat_messages(sender_name,message,timestamp)
        VALUES (?,?,?)""", (sender_name,message,timestamp))
        self.conn.commit()
    def get_messages(self):
        """
        This method selects all messages stored in the `chat_messages` table and orders them by
        their timestamp, from the earliest to the most recent message.
        Returns:
            list of tuple: A list of tuples where each tuple contains the `sender_name`,
                       `message`, and `timestamp` of a chat message.
        """
        self.cursor.execute("""SELECT sender_name,message,timestamp FROM chat_messages ORDER BY timestamp""")
        return self.cursor.fetchall()
    def close(self):
        """
        This method closes a SQLite database connection.
        Returns:
            None: This method does not return any value.
        """
        self.conn.close()

# Test
if __name__=="__main__":
    db=Database()
    client=Client("127.0.0.1",8095,db)
