#!/usr/bin/env/ python
import os
import subprocess
import yt_dlp

# /usr/bin/env python3 downloader.py

# Class for handling an output log of activity.
class MyLogger:
    # Debug 
    def debug(self, msg):
        # For compatibility with youtube-dl, both debug and info are passed into debug
        # You can distinguish them by the prefix '[debug] '
        if msg.startswith('[debug] '):
            print(msg)
        else:
            self.info(msg)
    # Info
    def info(self, msg):
        print(msg)
    # Warning
    def warning(self, msg):
        print(msg)
    # Error
    def error(self, msg):
        print(msg)

# See "progress_hooks" in help(yt_dlp.YoutubeDL)
def my_hook(d):
    if d['status'] == 'finished':
        print('Done downloading, now post-processing ...')
    elif d['status'] == 'downloading':
        print('Time spent: {0}'.format(d['elapsed']))
        pass
    else:
        print('STATUS: ' + d['status'])

# Selects the best video format avaiable.
def format_selector(ctx):
    formats = ctx.get('formats')[::-1]
    best_video = next(f for f in formats if f['vcodec'] != 'none' and f['acodec'] == 'none')
    audio_ext = {'mp4': 'm4a', 'webm': 'webm'}[best_video['ext']]
    best_audio = next(f for f in formats if (f['acodec'] != 'none' and f['vcodec'] == 'none' and f['ext'] == audio_ext))
    yield {
        'format_id': f'{best_video["format_id"]}+{best_audio["format_id"]}',
        'ext': best_video['ext'],
        'requested_formats': [best_video, best_audio],
        'protocol': f'{best_video["protocol"]}+{best_audio["protocol"]}'
    }

# Download best possible video format.
def download_video_best(url):
    ydl_opts = {
        'format': format_selector,
        #'format': 'webm/bestvideo+bestaudio/best',
        'outtmpl': './Videos/%(title)s.%(ext)s',
        'logger': MyLogger(),
        'progress_hooks': [my_hook],
        'thumbnails': '--list-thumbnails',
        'download-archive': True,
        'split-chapters': True,
        'verbose': True,
        'writedescription': False,
        'list-formats': True,
        'embed-metadata': True,
        #'embed-thumbnail': True,
        'embed-chapters': True,
    }
    with yt_dlp.YoutubeDL(params=ydl_opts) as ydl:        
        ydl.download(url_list=url)
    try:
        with yt_dlp.YoutubeDL(params=ydl_opts) as ydl:
            result = ydl.download(url)
            print('downloaded video')
    except(Exception):
            # Print the excetion trace upon error.
            print(Exception.__traceback__)

# WEBM Video
def download_webm(url):
    download_command = [
        "yt-dlp",
        ### Download Options
        "--limit-rate","10.0M",
        "--throttled-rate","100K",
        ### Filesystem Options
        "--output","./Videos/%(title)s.%(ext)s",        
        "--restrict-filenames",
        "--force-overwrites",
        ### Thumbnail Options:
        "--list-thumbnails",
        ### Verbosity and Simulation Options
        "--no-simulate",
        "--progress",
        "--verbose",
        #"--print-traffic",
        ### Video Format Options:
        "--format","webm/bestvideo+bestaudio/best",
        "--list-formats",
        ### Post-Processing Options
        "--embed-subs",
        #"--embed-thumbnail", # WEBM does not support thumbnail?
        "--embed-metadata",
        "--embed-chapters",        
        url
    ]    
    subprocess.run(download_command)
    print('Downloaded WEBM')

# Webm sectioned into embedded chapters.(download an album video into songs.)
def download_webm_album(url):
# Need to edit output to be named.
# https://github.com/yt-dlp/yt-dlp?tab=readme-ov-file#output-template
    download_command = [
        "yt-dlp",
        ### Download Options
        "--limit-rate","10.0M",
        "--throttled-rate","100K",
        ### Filesystem Options
        "--output","./Videos/%(title)s.%(ext)s",        
        "--restrict-filenames",
        "--force-overwrites",
        ### Thumbnail Options:
        "--list-thumbnails",
        ### Verbosity and Simulation Options
        "--no-simulate",
        "--progress",
        "--verbose",
        #"--print-traffic",
        ### Video Format Options:
        "--format","webm/bestvideo+bestaudio/best",
        "--list-formats",
        ### Post-Processing Options
        "--embed-subs",
        #"--embed-thumbnail", # WEBM does not support thumbnail?
        "--embed-metadata",
        "--embed-chapters",
        "--split-chapters",
        url
    ]    
    subprocess.run(download_command)
    print('Downloaded WEBM')

# MP4 Video
def download_mp4(url):
    download_command = [
        "yt-dlp",
        ### Download Options
        "--limit-rate","10.0M",
        "--throttled-rate","100K",
        ### Filesystem Options
        "--output","./Videos/%(title)s.%(ext)s",        
        "--restrict-filenames",
        "--force-overwrites",
        ### Thumbnail Options:
        "--list-thumbnails",
        ### Verbosity and Simulation Options
        "--no-simulate",
        "--progress",
        "--verbose",
        #"--print-traffic",
        ### Video Format Options:
        "--format","mp4/bestvideo+bestaudio/best",
        "--list-formats",
        ### Post-Processing Options
        "--embed-subs",
        "--embed-thumbnail",
        "--embed-metadata",
        "--embed-chapters",
        url
    ]    
    subprocess.run(download_command)
    print('Downloaded MP4')

# MP4 Video - Some of the split-sections are broken. Unreliable.
def download_mp4_sections(url):
    download_command = [
        "yt-dlp",
        ### Download Options
        #"--limit-rate","5.0M",
        ### Filesystem Options
        "--paths","./Videos/",
        "--output","chapter:Chapters/%(section_number)s_%(section_title)s.%(ext)s",
        "--output","%(title)s.%(ext)s",        
        "--restrict-filenames",
        "--force-overwrites",
        ### Thumbnail Options:
        "--list-thumbnails",
        ### Verbosity and Simulation Options
        "--no-simulate",
        "--progress",
        "--verbose",
        #"--print-traffic",
        ### Video Format Options:
        "--format","mp4/bestvideo+bestaudio/best",
        "--list-formats",
        ### Post-Processing Options
        "--embed-subs",
        "--embed-thumbnail",
        "--embed-metadata",
        "--split-chapters",
        url
    ]    
    subprocess.run(download_command)
    print('Downloaded MP4 Sections')

# MP3 Audio
def download_mp3(url):
    download_command = [
        "yt-dlp",
        ### Download Options
        "--limit-rate","10.0M",
        "--throttled-rate","100K",
        ### Filesystem Options
        "--output","./Audio/%(title)s.%(ext)s",
        "--restrict-filenames",        
        "--force-overwrites",
        #"--trim-filenames", "32", # This option poofs for admin perms.
        ### Thumbnail Options:
        "--list-thumbnails",
        ### Verbosity and Simulation Options
        "--no-simulate",
        "--progress",
        "--verbose",
        #"--print-traffic",
        ### Video Format Options:
        "--format","bestaudio", # mp3/bestaudio/best
        "--list-formats",
        ### Post-Processing Options
        "--extract-audio",
        "--audio-format","mp3",
        "--audio-quality","320k",
        "--no-keep-video",
        "--embed-thumbnail",
        "--embed-metadata",
        "--embed-chapters",
        url
    ]
    subprocess.run(download_command)
    print('Downloaded MP3')

# WAV Audio
def download_wav(url):
    download_command = [
        "yt-dlp",
        ### Download Options
        "--limit-rate","10.0M",
        "--throttled-rate","100K",
        ### Filesystem Options
        "--output","./Audio/%(title)s.%(ext)s",
        "--restrict-filenames",        
        "--force-overwrites",
        #"--trim-filenames", "32", # This option poofs for admin perms.
        ### Thumbnail Options:
        "--list-thumbnails",
        ### Verbosity and Simulation Options
        "--no-simulate",
        "--progress",
        "--verbose",
        #"--print-traffic",
        ### Video Format Options:
        "--format","bestaudio", # mp3/bestaudio/best
        "--list-formats",
        ### Post-Processing Options
        "--extract-audio",
        "--audio-format","wav",
        "--audio-quality","320k",
        "--no-keep-video",
        "--embed-thumbnail",
        "--embed-metadata",
        "--embed-chapters",
        url
    ]
    subprocess.run(download_command)
    print('Downloaded wav')

# OGG Audio
def download_ogg(url):
    # package needed:
    # python -m pip install mutagen
    download_command = [
        "yt-dlp",
        ### Download Options
        "--limit-rate","10.0M",
        "--throttled-rate","100K",
        ### Filesystem Options
        "--output","./Audio/%(title)s.%(ext)s",
        "--restrict-filenames",        
        "--force-overwrites",
        #"--trim-filenames", "32", # This option poofs for admin perms.
        ### Thumbnail Options:
        "--list-thumbnails",
        ### Verbosity and Simulation Options
        "--no-simulate",
        "--progress",
        "--verbose",
        #"--print-traffic",
        ### Video Format Options:
        "--format","ogg/bestaudio", # mp3/bestaudio/best
        "--list-formats",
        ### Post-Processing Options
        "--extract-audio",
        #"--audio-format","ogg",
        "--audio-quality","320k",
        "--no-keep-video",
        "--embed-thumbnail",
        "--embed-metadata",
        "--embed-chapters",
        url
    ]
    subprocess.run(download_command)
    print('Downloaded ogg')

# Main
def main():
    # loop prompt user for input
    while True:
        # User input youtube url.
        url = input("Enter YouTube URL (type 'q' to quit): ")
        if url.lower() == 'q':
            break 
        
        # debug
        #url = 'https://www.youtube.com/watch?v=8_UGZKRgZGo'
                
        # dictionary of download options.
        formatOptions = {
            '0': 'All',
            '1': 'MP3',
            '2': 'MP4',
            '3': 'WEBM',
            '4': 'WAV',
            '5': 'OGG',
        }
        # display options.
        print("Choose the format.")
        for option,fileFormat in formatOptions.copy().items():
            print(option+":"+fileFormat)
        # User input for download options.
        formatChoice = input("Format choice: ")
        # route the choice.
        match formatChoice:
            case '0':
                print("All")
                download_mp3(url=url)
                download_wav(url=url)
                download_ogg(url=url)
                download_mp4(url=url)
                download_webm(url=url)
                download_video_best(url=url)
            case '1':
                print("MP3")
                download_mp3(url=url)
            case '2':
                print("MP4")
                download_mp4(url=url)
                #download_mp4_sections(url=url)
            case '3':
                print("WEBM")
                download_webm(url=url)
            case '4':
                print("WAV")
                download_wav(url=url)                
            case '5':
                print("OGG")
                download_ogg(url=url)
            case _:
                print("Invalid")
        print("job has been jobbed.")
    print('Exiting...')

# main if ran as script.
if __name__ == "__main__":
    main()

