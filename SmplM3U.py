#!/usr/bin/env python3

# Make a "portable" m3u playlist so ios vlc doesn't break :(

import urllib.parse
import subprocess
import json
import io
import os

def get_duration(filepath):
    """Gets the duration of a video or audio file in seconds."""

    try:
        command = [
            "/usr/bin/ffprobe",
            "-v", "error",
            "-show_entries", "format=duration",
            "-of", "json",
            filepath
        ]
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        
        json_output = json.loads(result.stdout)
        return int(float(json_output["format"]["duration"]))
    except subprocess.CalledProcessError as e:
        print(f"FFprobe error: {e.stderr}")
        return None
    except Exception as e:
        print(f"Error getting duration with FFprobe: {e}")
        return None


def create_playlist(filename, directory="."):
    """Creates an extended m3u playlist from the given directory's contents and saves it to filename.m3u"""

    playlist = io.StringIO("")
    
    playlist.write("#EXTM3U\n") # Extended m3u playlist file
    playlist.write("#PLAYLIST:"+filename+"\n") # Technically not standerd but VLC accepts it so idrc

    for file in sorted(os.listdir(directory)):
        if not file.endswith('.m4a'):
            continue
        print("[SmplM3U] "+"Appending "+file+" to the playlist.")
        playlist.write("#EXTINF:"+str(get_duration(directory+"/"+file))+","+file.removesuffix(".m4a")+"\n")
        playlist.write(urllib.parse.quote(file)+"\n")
    
    print("[SmplM3U] "+"Writing playlist to " + filename+".m3u")
    
    with open(directory+"/"+filename+".m3u", "w") as file:
        file.write(playlist.getvalue())        

    playlist.close()
