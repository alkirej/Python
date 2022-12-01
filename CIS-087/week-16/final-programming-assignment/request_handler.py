from codecs import decode
from threading import Thread

from request import Request
from response import Response

BUFSIZE = 1024

class RequestHandler(Thread):
    """Handles a client request."""
    def __init__(self, client, cache):
        Thread.__init__(self)
        self.client = client
        self.cache = cache

    def run(self):
        user_request = decode(self.client.recv(BUFSIZE), "ascii").split()
        request = Request(user_request[0])
        season_data = self.process(request)
        text_response = str(Response(season_data)) + "\n"
        self.client.send(bytes(text_response,"ascii"))

        self.client.close()

    def process(self,req):
        team_data = self.cache[req.team]
        matches = (x for x in team_data if req==x)
        try:
            return next(matches)
        except StopIteration:
            return None
