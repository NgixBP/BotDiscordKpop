import os

from dotenv import load_dotenv


load_dotenv()


# Discord
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")


# MusicBrainz
MUSICBRAINZ_API_URL = os.getenv(
    "MUSICBRAINZ_API_URL",
    "https://musicbrainz.org/ws/2"
)