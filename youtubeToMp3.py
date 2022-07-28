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
        print(msg)
    def warning(self, msg):
        if not self.debugMode:
            pass
        else:
            print("warning: " + msg)
    def error(self, msg):
        updateSettingsFile()
        print(msg)
    
playListCount: int = 0
settingsFile: string = None

def main(args: argparse.Namespace):
    global playListCount, settingsFile
    playListCount = 0
    urls = []
    if(args.config and os.path.isfile(args.config)):
        url = getOptionsFromFile(args.config)
        settingsFile = args.config
    else:
        url = input("Input youtube link: ")
    urls.append(url)
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download(urls)

def updateSettingsFile():
    global playListCount, settingsFile
    if(playListCount == 0):
        return
    if(not settingsFile):
        print("job failed to complete.\r\nrelaunch playlist link with option 'playliststart' set to "+playListCount+".")
        return
    print("updating settings file: "+settingsFile)
    lines = []
    with open(settingsFile, 'r', encoding=sys.getfilesystemencoding()) as argFile:
        lines = argFile.readlines()
    rewrite = []
    for line in lines:
        i = line.find('playliststart')
        if(i >= 0):
            i += len('playliststart')+1
            end_i = line.find(",", i)
            arg = (line[i : end_i] if end_i > 0 else line[i:]).strip()
            rewrite.append('playliststart: '+str(playListCount + int(arg) if arg.isdigit() else playListCount)+",")
        else:
            rewrite.append(line)
    with open(settingsFile, "w", encoding=sys.getfilesystemencoding()) as argFile:
        argFile.writelines(rewrite)

def check_complete(d):
    global playListCount
    if d['status'] == 'finished':
        print('Done downloading, now converting ...')
        playListCount += 1

def getOptionsFromFile(path: string):
    args = []
    with open(path, 'r', encoding=sys.getfilesystemencoding()) as argFile:
        args = argFile.readlines()
    options = { 'playliststart': None, 'playlistend': None, 'url': None, 'sleep_interval': None }
    for line in args:
        for option in options.keys():
            i = line.find(option)
            if(i >= 0):
                i += len(option)+1
                end_i = line.find(",", i)
                arg = (line[i : end_i] if end_i > 0 else line[i:]).strip()
                options[option] = arg
    if(options["playliststart"]):
        try:
            ydl_opts.update({'playliststart': int(options["playliststart"])})
        except ValueError:
            print("playlist start not a valid number")
    if(options["playlistend"]):
        try:
            ydl_opts.update({'playlistend': int(options["playlistend"])})
        except ValueError:
            print("playlist end not a valid number")
    if(options["sleep_interval"]):
        try:
            ydl_opts.update({'sleep_interval': int(options["sleep_interval"])})
        except ValueError:
            print("sleep_interval not a valid number")

    return options["url"]

ydl_opts = {
    'format': 'bestaudio/best',
    'restrictfilenames': True,
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192'
    }],
    'logger': ProgressLogger(False),
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
        updateSettingsFile()
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)