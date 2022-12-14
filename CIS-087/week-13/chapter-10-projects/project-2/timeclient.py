"""
File: timeclient.py
Client for obtaining the day and time.
"""

from socket import *
from codecs import decode

HOST = "localhost" 
PORT = 5000
BUFSIZE = 1024
ADDRESS = (HOST, PORT)

try:
    server = socket(AF_INET, SOCK_STREAM)               # Create a socket
    server.connect(ADDRESS)                             # Connect it to a host
    dayAndTime = decode(server.recv(BUFSIZE), "ascii")  # Read a string from it
    print(dayAndTime)

except ConnectionRefusedError:
    print("Unable to connect to day-time server.  Try again later.")
finally:
    server.close()                                      # Close the connection
