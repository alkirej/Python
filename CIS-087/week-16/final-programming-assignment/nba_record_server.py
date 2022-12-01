"""
Author:  Jeff Alkire
Date:    11-30-2022
Purpose: Class to implement nba record server that will listen on a particular
         port and return the record of the given team in the given year.
"""

import os
from socket import *
from threading import Thread
from time import ctime

from season_data import SeasonData
from request_handler import RequestHandler

DATA_DIR = "data-dir"
HOST = "localhost"
PORT = 32124
ADDRESS = (HOST, PORT)
BACKLOG_ALLOWED = 25

STOP_SERVER = False

def team_from_filename(filename: str):
    """
    Record data is stored in the data directory in the format <team name>.csv
    :param filename: Name of file found in data directory.
    :return:
    """
    dot_idx = filename.index(".")
    teamname = filename[0:dot_idx].lower().capitalize()
    return teamname

class NbaRecordServerListener(Thread):
    """
    Implements the listener thread for the server.
    """
    def load_data(self,data_dir=DATA_DIR):
        # move into the data directory to read the files there.
        os.chdir(data_dir)
        # Process all files in the data directory.
        for file in os.scandir("."):
            try:
                print("Reading data from: %s" % file.name)

                with open(file.name, "r") as f:
                    # read entire file (they are relatively short)
                    lines = f.readlines()
                    # Skip first line (header info)
                    lines.pop(0)

                    # all data for this team.
                    team_data = []
                    # Store each entry into a SeasonData object and store in a list.
                    for l in lines:
                        team_data.append( SeasonData(l) )

                    # Get team's name from the filename
                    teamname = team_from_filename(file.name)
                    # Cache all tead data for each team.
                    self.DATA_CACHE[teamname] = team_data

            except:
                # Handle errors by ignore them which will cause the file being
                # read to be ignored.
                print("ERROR PROCESSING: %s (ignoring file)" % file.name)
                pass

    def __init__(self):
        Thread.__init__(self)

        # Read data from disk into memory.
        self.DATA_CACHE = {}
        self.load_data()

    def run(self) -> None:
        svr_socket = socket(AF_INET, SOCK_STREAM)
        svr_socket.bind(ADDRESS)
        svr_socket.listen( BACKLOG_ALLOWED )

        while not STOP_SERVER:
            print("Listening for connections on port %d . . ." % PORT)
            client, address = svr_socket.accept()
            print("... connected from: %s at %s" % (address,ctime()))
            req_handler = RequestHandler(client, self.DATA_CACHE)
            req_handler.start()

class QuitThread(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        input("Press enter to exit:\n")
        global STOP_SERVER
        STOP_SERVER = True

def main():
    qt = QuitThread()
    qt.start()

    listener = NbaRecordServerListener()
    listener.start()

if __name__ == "__main__":
    main()