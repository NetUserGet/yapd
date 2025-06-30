#!/usr/bin/env python3

import SmplM3U
import yt_dlp
import json
import csv

ydl_options = {
    "paths": {
        "home": "../Songs"
    },
    "format": "m4a/bestaudio/best",
    "postprocessors": [{
        "key": "FFmpegExtractAudio",
        "preferredcodec": "m4a",
    }],
    "download_archive": "dsongs.txt"
}

if __name__ == "__main__":
    URLS = []
    try:
        with open("urls.csv", "r") as urls:
            if len(urls.readlines()) == 1:
                print("urls.csv must be longer than 1 line!")
                exit(1)
        with open("urls.csv", "r") as urls:
            reader = csv.reader(urls)
            for row in list(reader)[1::]:
                URLS.append(row[0])
    except FileNotFoundError:
        with open("urls.csv", "w") as urls:
            writer = csv.DictWriter(urls, fieldnames=['url'])
            writer.writeheader()
        print("No urls.csv found!\nCreated urls.csv please append your playlists or videos to the it.")
        exit(1)

    with yt_dlp.YoutubeDL(ydl_options) as ydl:
        error_code = ydl.download(URLS)
    SmplM3U.create_playlist("dplaylist", "../Songs")
