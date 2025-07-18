import yt_dlp
from sys import argv

url = argv[1]

ydl_opts = {
    'format': 'bestvideo[height<=1440]+bestaudio/best[height<=1440]',
    'outtmpl': 'D:/youtubedownloads/%(title)s.%(ext)s',
    'merge_output_format': 'mp4',
    'ffmpeg_location': 'D:/ffmpeg-2025-07-07-git-d2828ab284-full_build/bin/ffmpeg.exe',
    'postprocessors': [
        {'key': 'FFmpegVideoConvertor', 'preferedformat': 'mp4'}
    ],
    'quiet': False,
    'noplaylist': True,
    'no_warnings': True,
    'continuedl': True,
}

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    ydl.download([url])
