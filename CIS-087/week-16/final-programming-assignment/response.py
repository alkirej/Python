
from season_data import SeasonData

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