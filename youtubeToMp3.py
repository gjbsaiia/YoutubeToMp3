from __future__ import unicode_literals
import os
import sys
import youtube_dl

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

def main():
    urls = []
    url = input("Input youtube link: ")
    urls.append(url)
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download(urls)

def check_complete(d):
    if d['status'] == 'finished':
        print('Done downloading, now converting ...')

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
	try:
		main()
	except KeyboardInterrupt:
		print()
		print('Interrupted \_[o_0]_/')
		try:
			sys.exit(0)
		except SystemExit:
			os._exit(0)