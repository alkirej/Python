"""
File: timeserver2.py
Server for providing the day and time.  Uses client
handlers to handle clients' requests.
"""

from time import sleep
from threading import Thread
from socket import *
from timeclienthandler import TimeClientHandler

HOST = "localhost"
PORT = 5000
ADDRESS = (HOST, PORT)

stop_server = False

class Listener(Thread):
    def __init__(self):
        Thread.__init__(self, name = "Listener" )

    def run(self):
        server = socket(AF_INET, SOCK_STREAM)
        server.bind(ADDRESS)
        server.listen(5)

        # The server now just waits for connections from clients
        # and hands sockets off to client handlers
        while not stop_server:
            print("Waiting for connection . . .")
            client, address = server.accept()
            print("... connected from: ", address)
            handler = TimeClientHandler(client)
            handler.start()

class QuitThread(Thread):
    def __init__(self):
        Thread.__init__(self, name = "QuitThread" )

    def run(self):
        s = input("Press enter to exit:\n")
        print(s)
        global stop_server
        stop_server = True

def main():
    qt = QuitThread()
    qt.start()

    listener = Listener()
    listener.start()

if __name__ == "__main__":
    main()
