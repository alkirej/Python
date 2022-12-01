"""
Author:  Jeff Alkire
Date:    Nov 30, 2022
Purpose: Show the gui used by the client.  It accepts a team and a season.
         When the lookup information button is pressed, a message is sent to the
         server process via a socket.  The server's response is populated into
         the appropriate fields.
"""

import datetime

from breezypythongui import EasyFrame
from codecs import decode
from socket import *

from nba_record_server import ADDRESS
from request import Request
from response import build_response_from_message

BUFSIZE = 1024

FROM_YEAR=1947
today=datetime.date.today()
TO_YEAR=today.year

# list of the fields retreived from the server.
RESULT_FIELDS = ["League", "Season", "Team Name", "Won", "Lost", "Win %",
                 "Playoff Results", "Coach(es)", "Best Player"
                ]

def build_year_list(start_year, end_year):
    """
    Build a list of seasons in the correct format.  For example, 1980-81 or 1999-00.
    param start_year: first part of the first year to include
    param end_year: last part of the last season to include.
    return: list of years in the range
    """
    season_list = []
    for yr in range(end_year-1,start_year-1,-1):
        next = str( (yr+1) % 100 )
        if (len(next)==1):
            next = "0" + next
        current_season = "%s-%s" % (yr,next)
        season_list.append(current_season)

    return season_list

SEASONS=build_year_list(FROM_YEAR, TO_YEAR)

def establish_connection_to_server():
    """
    Connect to the lookup server.
    return: the socket to communite with.
    """
    server_socket = socket(AF_INET, SOCK_STREAM)               # Create a socket
    server_socket.connect(ADDRESS)                             # Connect it to a host
    return server_socket

def send_request(server_socket, request):
    """
    Send the request to the server for a given team and year.
    param server_socket: communication channel
    param request: request object (contains team and year info)
    """
    text_response = str(request) + "\n"
    server_socket.send(bytes(text_response,"ascii"))

def get_response( server_socket ):
    """
    Get the server's response and store it into a season data object.
    param server_socket: Communication channel
    return: Information from the server.
    """
    server_response = decode(server_socket.recv(BUFSIZE), "ascii").split("\n")
    season_data = build_response_from_message(server_response[0]+"\n")
    return season_data



class NbaRecordClientGui(EasyFrame):
    """
    Main class for this module.

    Displays the window and dispatches button clicks.
    """

    def add_gui_line( self, label_text, row_num):
        """
        Add a label <-> text box pair to display the season information.
        param label_text: Label identifying the text
        param row_num: What row on the screen to display the pair in
        return: the textfield object so the value can be updated later.
        """
        self.addLabel(text=label_text,
                      row=row_num,
                      column=0,
                      sticky="NW"
                      )

        return self.addTextField(text="",
                                 row=row_num,
                                 column=1,
                                 sticky="NW"
                                 )

    def add_result_fields(self, fields, start_at_row ):
        """
        Add a group of fields that will be populated with data from the server.
        :param fields:  The list of fields to be added.  This is a list of
                        strings that are used as the labels.
        :param start_at_row: The first row to use.  Each field gets its own
                             row.
        :return: a list of the textbox objects so the screen can be updated.
        """
        result_field_objects = []
        current_row = start_at_row
        for fld in fields:
            current_field = self.add_gui_line( fld, current_row )
            result_field_objects.append(current_field)
            current_row += 1
        return result_field_objects

    def __init__(self):
        """
        Setup widgets on window
        """
        EasyFrame.__init__(self)
        self.setTitle("NBA Season Record Lookup Utility")

        # NBA Team Row (0)
        self.addLabel(text="NBA Team:",
                      row=0,
                      column=0,
                      sticky="NW"
                      )
        team_list = ["Lakers","Pelicans"]
        self.team = self.addCombobox \
            (row = 0,
             column = 1,
             values=team_list,
             text=""
             )
        self.team.set(team_list[0])

        self.addLabel(text="",
                      row=0,
                      column=2,
                      sticky="NW"
                      )

        # Season Row (1)
        self.addLabel(text="Season",
                      row=1,
                      column=0,
                      sticky="NW"
                      )
        self.season = self.addCombobox \
            (row = 1,
             column = 1,
             text=SEASONS[len(SEASONS)-1],
             values=SEASONS
             )

        # Button Row (2)
        self.addButton(text = "Lookup Season Information",
                       row = 2,
                       column = 0,
                       columnspan = 2,
                       command = self.lookup_info
                       )

        self.result_fields = self.add_result_fields(RESULT_FIELDS,3)

    def fill_results(self, season_data):
        """
        Given the data, fill in the page.
        :param season_data: Data to populate the screen with
        """
        self.result_fields[0].setValue( season_data.league_name )
        self.result_fields[1].setValue( season_data.year )
        self.result_fields[2].setValue( season_data.team_name )
        self.result_fields[3].setValue( season_data.wins )
        self.result_fields[4].setValue( season_data.losses )
        self.result_fields[5].setValue( season_data.win_percentage )
        self.result_fields[6].setValue( season_data.playoff_results )
        self.result_fields[7].setValue( season_data.coach_name )
        self.result_fields[8].setValue( season_data.best_player )

    # Methods to handle user events.
    def lookup_info(self):
        """
        Read the year and team from the form, send a request to the information
        server, wait for the response, and then populate the results form with
        the supplied data.
        """
        request = Request(self.team.getText(),self.season.getText())
        socket = establish_connection_to_server()
        send_request( socket, request )
        season_data = get_response( socket )

        self.fill_results( season_data )
        socket.close()

def main():
    """ Instantiate window and start gui loop. """
    NbaRecordClientGui().mainloop()

if __name__ == "__main__":
    main()