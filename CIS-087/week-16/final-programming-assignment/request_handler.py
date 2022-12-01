from codecs import decode
from threading import Thread

from request import Request
from response import Response

BUFSIZE = 1024

class RequestHandler(Thread):
    """
    Thread to handles a client request. One thread per request.
    """
    def __init__(self, client, cache):
        """initialize object's connection and data cache."""
        Thread.__init__(self)
        self.client = client
        self.cache = cache

    def run(self):
        """Process single request and send response."""
        user_request = decode(self.client.recv(BUFSIZE), "ascii").split()
        request = Request(user_request[0])
        season_data = self.process(request)
        text_response = str(Response(season_data)) + "\n"
        self.client.send(bytes(text_response,"ascii"))

        self.client.close()

    def process(self,req):
        """
        Routine to process the request.  Search through the cache for the team
        supplied in the request.  The search all data for this team for the data
        for the specified year.
        param req: Request object with the user's request.
        return: The data for the given team in the given year.  If no data is
                found, None is returned.
        """
        try:
            team_data = self.cache[req.team]
            matches = (x for x in team_data if req==x)
            return next(matches)
        except:
            return None
