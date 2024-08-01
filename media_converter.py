#!/usr/bin/env python3
import os
import os.path
import sys
import glob
from enum import Enum

# Uses ffmpeg
# https://ffmpeg.org/ffmpeg.html
# http://doc.gnu-darwin.org/ffmpeg/ffmpeg-doc.html

# Enum of possible file extensions.
class Extentions(Enum):
    WEBM = '.webm'
    MKV = '.mkv'
    MP4 = '.mp4'
    WAV = '.wav'
    M4A = '.m4a'
    MP3 = '.mp3'

# Convert a webm file to mp3.(video -> audio)
def webm_to_mp3(webmFile):
    print(Extentions.WEBM.value + ' ---> ' + Extentions.MP3.value)
    mp3File = webmFile.replace(Extentions.WEBM.value, Extentions.MP3.value)
    command = 'ffmpeg -i "{0}" -vn -n "{1}"'.format(webmFile, mp3File)
    try:
        os.system(command=command)
        print('File Created:', mp3File)
    except Exception:
        mp3File = ''
        print('MP3 Error!')
    return mp3File

# Convert webm file to wav.(video -> audio)
def webm_to_wav(webmFile):
    print(Extentions.WEBM.value + ' ---> ' + Extentions.WAV.value)
    wavFile = webmFile.replace(Extentions.WEBM.value, Extentions.WAV.value)
    command = 'ffmpeg -i "{0}" -vn -n "{1}"'.format(webmFile, wavFile)
    try:
        os.system(command=command)
        print('File Created:', wavFile)
    except Exception:
        wavFile = ''
        print('WAV Error!')
    return wavFile

# Convert webm file to mp4.(video -> video)
def webm_to_mp4(webmFile):
    print(Extentions.WEBM.value + ' ---> ' + Extentions.MP4.value)
    mp4File = webmFile.replace(Extentions.WEBM.value, Extentions.MP4.value)
    command = 'ffmpeg -i "{0}" -r 30 -n "{1}"'.format(webmFile, mp4File)
    os.system(command=command)
    return mp4File

# Convert mp4 file to mp3.(video -> audio)
def mp4_to_mp3(mp4File):
    print(Extentions.MP4.value + ' ---> ' + Extentions.MP3.value)
    mp3File = mp4File.replace(Extentions.MP4.value, Extentions.MP3.value)
    command = 'ffmpeg -i "{0}" -vn -n "{1}"'.format(mp4File, mp3File)
    os.system(command=command)
    return mp3File

# Main
if __name__ == "__main__":
    videoPath = None
    if sys.platform == 'linux':
        videoPath = '/home/tom/Downloads/'
    elif sys.platform == 'windows' or 'win32':
        videoPath = 'C:\\videos\\'
    
    # Empty list for holding created file results.
    createdFiles = []
    
    # For every webm file in the videos directory, convert to new formats and add to list.
    for webmFile in glob.glob(pathname=videoPath + '*' + Extentions.WEBM.value):
        print('webm file:', webmFile)
        createdFiles.append(webm_to_mp3(webmFile=webmFile))
        #createdFiles.append(webm_to_wav(webmFile=webmFile))
        #createdFiles.append(webm_to_mp4(webmFile=webmFile))
    
    # Same for mp4 files if needed.
    for mp4File in glob.glob(pathname=videoPath + '*' + Extentions.MP4.value):
        print('mp4 file:', mp4File)
        createdFiles.append(mp4_to_mp3(mp4File=mp4File))

    # Get a list of each type of media file worked on.
    webmList = list(filter(lambda x: '.webm' in x, createdFiles))
    mp4List = list(filter(lambda x: '.mp4' in x, createdFiles))
    wavList = list(filter(lambda x: '.wav' in x, createdFiles))
    m4aList = list(filter(lambda x: '.m4a' in x, createdFiles))
    mp3List = list(filter(lambda x: '.mp3' in x, createdFiles))
    
    # Move into sub directories based on their file extension.
    # TO DO
    print('done!')
# end