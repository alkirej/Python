


class SeasonData:
    """
    Stores all data about a single season for a single team.
    """
    def __init__(self, line_from_csv_file):
        entries = line_from_csv_file.split(",")
        # Prune /n off end of each line
        entries[8] = entries[8][:-1]
        # Store each entry into a SeasonData object and store in a list.
        self.init_data( entries[0], # year
                        entries[1], # league
                        entries[2], # team name
                        entries[3], # wins
                        entries[4], # losses
                        entries[5], # win %
                        entries[6], # playoff results
                        entries[7], # coach(es)
                        entries[8]  # best player
                      )

    def init_data(self, year,
                        league_name,
                        team_name,
                        wins,
                        losses,
                        win_percentage,
                        playoff_results,
                        coach_name,
                        best_player
                 ):
        self.year = year
        self.league_name = league_name
        self.team_name = team_name
        self.wins = wins
        self.losses = losses
        self.win_percentage = win_percentage
        self.playoff_results = playoff_results
        self.coach_name = coach_name
        self.best_player = best_player