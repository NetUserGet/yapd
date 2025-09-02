#!/usr/bin/env python3

# A simple library to make extended m3u playlists.

import urllib.parse
import subprocess
import hashlib
import json
import io
import os

def printm3u(s):
    print("[SmplM3U] " + s)

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
        printm3u(f"FFprobe error: {e.stderr}")
        return None
    except Exception as e:
        printm3u(f"Error getting duration with FFprobe: {e}")
        return None


def create_playlist(filename, extension=".m4a", directory=".", cache=True, tracks=[]):
    """Creates an extended m3u playlist from the given directory's contents and saves it to filename.m3u"""
    
    # mirror mirror on the wall whos the hackiest of them all?
    tracks = tracks if tracks else sorted(os.listdir(directory))

    if cache:
        if __create_cache(directory, extension, tracks):
            return

    playlist = io.StringIO("")
    
    playlist.write("#EXTM3U\n") # Extended m3u playlist file
    playlist.write("#PLAYLIST:"+filename+"\n") # Technically not standerd but VLC accepts it so idrc
    
    
    for file in tracks:
        if not file.endswith(extension):
            continue
        
        printm3u("Appending "+file+" to the playlist.")
        
        playlist.write("#EXTINF:"+str(get_duration(directory+"/"+file))+","+file.removesuffix(extension)+"\n")
        playlist.write(urllib.parse.quote(file)+"\n")
    
    printm3u("Writing playlist to " + filename+".m3u")
    
    with open(directory+"/"+filename+".m3u", "w") as file:
        file.write(playlist.getvalue())        

    playlist.close()

def __create_cache(directory, extension, tracks):
        h = hashlib.sha256()
        for file in tracks:
                if not file.endswith(extension):
                    continue
                h.update(file.encode("utf-8"))
        try:
            with open(directory+"/"+"m3ucache.txt", "rb") as cache:
                    c = cache.read()
                    if c == h.digest():
                        printm3u("Contents of directory have not changed!")
                        printm3u("Skipping creation of m3u playlist!")
                        return True # Since nothing changed we just return
        except FileNotFoundError:
            printm3u("Didn't find a m3ucache.txt, creating m3ucache.txt.")

        with open(directory+"/"+"m3ucache.txt", "wb") as cache:
                # Since we didn't return it is likely that the cache file either doesn't exist or is there are new files.
                cache.write(h.digest())
        return False
