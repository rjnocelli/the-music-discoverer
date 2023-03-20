import urllib
import base64

from app import utils
from app.clients.base import BaseHttpClient

from app.config import settings

import httpx
        
class SpotifyClient(BaseHttpClient):
    def __init__(self):
        self.client_id = settings.spotify_client_id
        self.secret = settings.spotify_client_secret
        self.api_base_url = 'https://api.spotify.com/v1'
        self.account_base_url = 'https://accounts.spotify.com'
        self.redirect_uri = 'http://localhost:80/callback'
    
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
    
    def get_token(self, code: str, state: str):
        url = self.account_base_url + '/api/token'
        
        headers = {
            'Authorization': f"Basic {base64.b64encode(f'{self.client_id}:{self.secret}'.encode()).decode()}",
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        
        data = {
            'client_id': self.client_id,
            'grant_type': 'authorization_code',
            'redirect_uri': self.redirect_uri,
            'code': code,
            'code_verifier': state,
        }
        
        resp = httpx.post(url, headers=headers, data=data)
        
        return resp.json()

    
    
