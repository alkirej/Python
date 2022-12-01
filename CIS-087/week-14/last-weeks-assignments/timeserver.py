"""
File: timeserver.py
Project 10.3

Server for providing the day and time.
Allows the server to be shut down gracefully.
Uses a thread for the server and waits for user
input to shut down.
"""

from socket import *
from timeclienthandler import TimeClientHandler
from threading import Thread

class TimeServer(Thread):
    """Server for the day and time."""
    
    def __init__(self):
        """Includes Boolean flag to shut down."""
        Thread.__init__(self)
        self.done = False

    def run(self):
        """Runs until signaled to shut down.  At least
        one client must connect after the signal is sent."""
        HOST = 'localhost'
        PORT = 5000
        ADDRESS = (HOST, PORT)

        server = socket(AF_INET, SOCK_STREAM)
        server.bind(ADDRESS)
        server.listen(5)

        while not self.done:
            print('Waiting for connection . . .')
            client, address = server.accept()
            print('... connected from:', address)
            handler = TimeClientHandler(client)
            handler.start()

    def quit(self):
        """The server is signaled to shut down."""
        self.done = True

def main():
    """Starts the server thread and waits for the user to
    signal to quit."""
    server = TimeServer()
    server.start()
    input("Press enter to shut the server down.\n")
    server.quit()
    print("Server shutting down.")

    
if __name__ == "__main__":
    main()


