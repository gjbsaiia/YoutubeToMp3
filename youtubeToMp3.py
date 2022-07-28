from __future__ import unicode_literals
import os
import string
import sys
import youtube_dl
import argparse

class ProgressLogger(object):
    def __init__(self, debugMode = False):
        self.debugMode = debugMode
    def debug(self, msg):
        if not self.debugMode:
            pass
        else:
            print(msg)
    def warning(self, msg):
        if not self.debugMode:
            pass
        else:
            print(msg)
    def error(self, msg):
        print(msg)

def main(args: argparse.Namespace):
    urls = []
    if(os.path.isfile(args.config)):
        url = getOptionsFromFile(args.config)
    else:
        url = input("Input youtube link: ")
    urls.append(url)
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download(urls)

def check_complete(d):
    if d['status'] == 'finished':
        print('Done downloading, now converting ...')

def getOptionsFromFile(path: string):
    args = []
    with open(path, 'r', encoding=sys.getfilesystemencoding()) as argFile:
        args = argFile.readlines()
    options = { 'playlistStart': None, 'playlistEnd': None, 'url': None }
    for line in args:
        line = line.replace(" ", "")
        for option in options.keys():
            i = line.find(option)
            if(i >= 0):
                i += len(option)+1
                end_i = int(line.find(",", i))
                arg = line[i : end_i] if end_i > 0 else line[i:]
                options[option] = arg
    
    if(options["playlistStart"]):
        try:
            ydl_opts.update({'playlistStart', int(options["playlistStart"])})
        except ValueError:
            print("playlist start not a valid number")
    if(options["playlistEnd"]):
        try:
            ydl_opts.update({'playlistEnd', int(options["playlistEnd"])})
        except ValueError:
            print("playlist end not a valid number")

    return options["url"]

ydl_opts = {
    'format': 'bestaudio/best',
    'restrictfilenames': True,
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192'
    }],
    'logger': ProgressLogger(True),
    'progress_hooks': [check_complete]
}

# Execute the wrapper
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config')
    args = parser.parse_args()
    try:
        main(args)
    except KeyboardInterrupt:
        print()
        print('Interrupted \_[o_0]_/')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)