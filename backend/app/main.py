
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from .clients.spotify import SpotifyClient

app = FastAPI()

spotify_client = SpotifyClient()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/auth", response_class=RedirectResponse)
def auth():
    return spotify_client.make_authorize_url()