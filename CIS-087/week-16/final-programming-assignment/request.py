"""
Author:  Jeff Alkire
Date:    Nov 30, 2022
Purpose: Data structure to contain all relevant portions of a information request.
"""

from season_data import SeasonData

def build_request_from_message(user_request: str):
    """
    Given a user request in comma separated value format, build a request object.
    :param user_request: string version
    :return: request object version
    """
    entries = user_request.split(",")
    return Request( entries[1],entries[2])

class Request:
    """
    Stores all data about a single season for a single team.
    """
    def __init__(self,team,year):
        self.init_data(1,team,year)

    def init_data(self,
                  protocol_version,
                  team_name,
                  year
                  ):
        self.version = protocol_version
        self.team = team_name
        self.year = year

    def __str__(self):
        """ Convert request to a csv string """
        return "%d,%s,%s" % (1,self.team,self.year)

    def __eq__(self,other):
        """
        Allows equality check between a user's request and the data in
        a SeasonData object.
        param other: item to compare myself to.
        return: True if there is a match, false if not.
        """
        if type(other) == Request:
            return self.protocol_version == other.protocol_version and \
                   self.team_name == other.team_name and \
                   self.year == other.year

        elif type(other) == SeasonData:
            return other.year == self.year

        else:
            return False