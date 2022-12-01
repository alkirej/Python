
from season_data import SeasonData

class Request:
    """
    Stores all data about a single season for a single team.
    """
    def __init__(self, user_request: str):
        entries = user_request.split(",")
        self.init_data( entries[0],entries[1],entries[2])

    def init_data(self,
                  protocol_version,
                  team_name,
                  year
                  ):
        self.version = protocol_version
        self.team = team_name
        self.year = year

    def __eq__(self,other):
        if type(other) == Request:
            return self.protocol_version == other.protocol_version and \
                   self.team_name == other.team_name and \
                   self.year == other.year

        elif type(other) == SeasonData:
            return other.year == self.year

        else:
            return False