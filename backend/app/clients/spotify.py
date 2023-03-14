import os
import urllib

from app import utils
from app.clients.base import BaseHttpClient
        
class SpotifyClient(BaseHttpClient):
    def __init__(self):
        self.secret = os.getenv('SPOTIFY_CLIENT_STECRET')
        self.client_id = os.getenv('SPOTIFY_CLIENT_ID')
        self.api_base_url = 'https://api.spotify.com/v1'
        self.account_base_url = 'https://accounts.spotify.com'
        self.redirect_uri = 'http://localhost:80/'

    def make_authorize_url(self):
        url = self.account_base_url + '/authorize'
        verifier, challenge = utils.gen_code_verifier()

        params = {
            'client_id': self.client_id,
            'response_type': 'code',
            'redirect_uri': self.redirect_uri,
            'state': verifier,
            'scope': 'playlist-modify-public',
            'code_challenge_method': 'S256',
            'code_challenge': challenge,
        }

        return url + '?' + urllib.parse.urlencode(params)

    
    
