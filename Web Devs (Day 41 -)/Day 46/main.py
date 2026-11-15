import requests
import os
from ytmusicapi import YTMusic
from bs4 import BeautifulSoup
from datetime import datetime

header = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/135.0.0.0 Safari/537.36"
    )
}

inp_date = input("What year you would like to travel to? Type the answer in YYY-MM-DD format: ")
url = f"https://appbrewery.github.io/bakeboard-hot-100/{inp_date}/" 
response = requests.get(url, headers=header)
soup = BeautifulSoup(response.text, "html.parser")

titles = soup.find_all(attrs={"data-rank": True})
song_names = [tag.getText().strip() for tag in soup.select("h3.chart-entry__title")]
# print(song_names)

# Upload playlsit to YTMusic

yt = YTMusic("Web Devs (Day 41 -)/Day 46/browser.json")

# Verify auth works
playlists = yt.get_library_playlists()
print(f"Found {len(playlists)} playlists in your library.")

PLAYLIST_NAME = f"{inp_date} Billboard 100"

# Check if playlist already exists
playlist_id = None
playlists = yt.get_library_playlists(limit=100)

for p in playlists:
    if p["title"] == PLAYLIST_NAME:
        playlist_id = p["playlistId"]
        break

if playlist_id:
    print("This playlist already exists.")
else:
    playlist_id = yt.create_playlist(
        PLAYLIST_NAME,
        f"Playlist with the hottest songs from {inp_date}",
        privacy_status="PRIVATE",
    )
    print("Playlist created.")

# Add songs to playlist
for song in song_names:
    try:
        search_results = yt.search(song, filter="songs", limit=1)
        yt.add_playlist_items(playlist_id, [search_results[0]["videoId"]])
        print(f"Added: {song}")
    except Exception as e:
        print(f"Skipped: {song} | Reason: {e}")

# Delete the playlist
status = yt.delete_playlist(playlist_id)