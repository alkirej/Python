"""
Author:  Jeff Alkire
Date:    Nov 30, 2022
Purpose: Data structure to contain all relevant portions of the server's
         response to a data request.
"""

from season_data import SeasonData

def build_response_from_message(user_request: str):
    """
    Given a comma separated message, build a response object.
    :param user_request:  The message is csv format
    :return: the data as a SeasonData object
    """
    entries = user_request.split(",")
    entries.pop(0)
    message = ",".join(entries)
    if message==",,,,,,,,":
        message="Data,,not,Available,,,,,,"
    return SeasonData(message)

class Response:
    """
    Stores all data about a single season for a single team.
    """
    def __init__(self, season_info: SeasonData):
        self.version = 1
        if season_info == None:
            self.data = SeasonData(",,,,,,,,,")
        else:
            self.data = season_info

    def __str__(self):
        """
        Convert info into a string for easier transference between the
        client and server.
        return: A string representation of the response object.
        """
        return "%d,%s,%s,%s,%s,%s,%s,%s,%s,%s" \
                    % ( self.version,
                        self.data.year,
                        self.data.league_name,
                        self.data.team_name,
                        self.data.wins,
                        self.data.losses,
                        self.data.win_percentage,
                        self.data.playoff_results,
                        self.data.coach_name,
                        self.data.best_player
                       )
