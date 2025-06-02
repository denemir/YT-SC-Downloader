import queue
import yt_dlp
import os
import threading
from gui import GUI
import imageio_ffmpeg as ffmpeg


class App:
    def __init__(self):
        self.gui = GUI()
        self.ffmpeg_path = ffmpeg.get_ffmpeg_exe()
        self.downloads_path = os.path.join(os.path.expanduser('~'), 'Downloads')
        self.status_queue = queue.Queue()
        self.download_thread = None
        self.is_downloading = False

    def start_download_thread(self, url, format, quality):
        if self.download_thread and self.download_thread.is_alive():
            return

        self.download_thread = threading.Thread(
            target=self._download_worker,
            args=(url, format, quality),
            daemon=True
        )
        self.download_thread.start()

        # Start checking for status updates
        self._check_status_queue()

    def _download_worker(self, url, format, quality):
        try:
            self.is_downloading = True
            self.status_queue.put("Starting download...")

            # performing the download
            self.download_from_youtube(url, format, quality)

            self.status_queue.put("✓ Download complete!")
        except Exception as e:
            if url == '':
                self.status_queue.put("Error: Please input a link.")
            elif 'is not a valid URL.' in str(e):
                self.status_queue.put("Error: Invalid link.")
            else: self.status_queue.put(f"Error: {str(e)}")
        finally:
            self.is_downloading = False

    def _check_status_queue(self):
        try:
            if not self.status_queue.empty():
                status = self.status_queue.get_nowait()
                if status == "✓ Download complete!":
                    self.gui.set_status(f"✓ Download complete! @{self.downloads_path}")
                    return
                else:
                    self.gui.set_status(status)
        except queue.Empty:
            pass

        if self.is_downloading or not self.status_queue.empty():
            self.gui.root.after(1, self._check_status_queue)

    def download_from_youtube(self, url, format='mp3', quality='bestaudio/best'):
        def progress_hook(d):
            if d['status'] == 'downloading':
                percent = d.get('_percent_str', 'Unknown')
                speed = d.get('_speed_str', '')
                eta = d.get('_eta_str', '')

                status_msg = f"Downloading: {percent}"
                if speed:
                    status_msg += f" | Speed: {speed}"
                if eta:
                    status_msg += f" | ETA: {eta}"

                self.status_queue.put(status_msg)

            elif d['status'] == 'finished':
                filename = os.path.basename(d['filename'])
                self.status_queue.put(f"Processing: {filename}")

        try:
            with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
                info_dict = ydl.extract_info(url, download=False)
        except Exception as e:
            raise Exception(f"Failed to extract video: {str(e)}")

        ydl_input = {
            'updatetime': False,
            'format': quality if format == 'mp3' else 'bestvideo[ext=mp4]+bestaudio[ext=mp3]/best[ext=mp4]/best',
            'outtmpl': self.downloads_path + '/%(title)s.%(ext)s',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
                # 'add_metadata': True
            }] if format == 'mp3' else [],
            'ffmpeg_location': self.ffmpeg_path,
            'progress_hooks': [progress_hook]
        }

        with yt_dlp.YoutubeDL(ydl_input) as ydl:
            ydl.download([url])


    def run(self):
        self.gui.initialize_gui(self)

if __name__ == '__main__':
    run = App()
    run.run()

