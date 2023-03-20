
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from .clients.spotify import SpotifyClient

app = FastAPI()

spotify_client = SpotifyClient()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/authorize", response_class=RedirectResponse)
async def auth():
    return spotify_client.make_authorize_url()

@app.get("/callback")
async def get_token(code: str, state: str):
    payload = spotify_client.get_token(code, state)
    return payload   