import yt_dlp
import os
from gui import GUI
import imageio_ffmpeg as ffmpeg


class App:
    def __init__(self):
        self.gui = GUI()
        self.ffmpeg_path = ffmpeg.get_ffmpeg_exe()
        self.downloads_path = os.path.join(os.path.expanduser('~'), 'Downloads')

    def download_from_youtube(self, url, format='mp3'):
        ydl_input = {
            'add_metadata': True,
            'writethumbnail': True,
            'updatetime': False,
            'format': 'bestaudio/best' if format == 'mp3' else 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            'outtmpl': self.downloads_path + '/%(title)s.%(ext)s',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
                # 'add_metadata': True
            }] if format == 'mp3' else [],
            'ffmpeg_location': self.ffmpeg_path,
        }

        with yt_dlp.YoutubeDL(ydl_input) as ydl:
            ydl.download([url])


    def download_from_soundcloud(self, url):
        ydl_input = {
            'format': 'bestaudio/best',
            'outtmpl': 'downloads/%(title)s.%(ext)s',
            'postprocessors': [{
                'key': 'FFMpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }] if format == 'mp3' else []
        }

        with yt_dlp.YoutubeDL(ydl_input) as ydl:
            ydl.download([url])


    def check_format_of_url(self, url):
        print('HI!!!!!')


if __name__ == '__main__':
    run = App()
    run.download_from_youtube(url='insert https link here')

