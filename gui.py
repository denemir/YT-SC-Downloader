import tkinter
from os import truncate
from tkinter import ttk
# from tktooltip import ToolTip
import sv_ttk

class GUI:
    def __init__(self, prog=None):
        self.prog = prog
        self.options = None
        self.current_option = None
        self.url = None
        self.root = tkinter.Tk()
        self.selected_tab = None
        self.media_type_dropdown = None

        # frames
        self.input_frame = None
        self.status_frame = None

        # buttons
        self.download_button = None

        # status field
        self.status_field = None
        self.status_message = ' '
        self.marquee_tracker = None
        self.is_initialized = False
        self.is_destroyed = False

    def initialize_gui(self, prog):
        # setup window
        self.prog = prog
        self.root.title('YT-SC Downloader')
        self.root.minsize(width=250, height=0)
        self.root.resizable(False, False)
        self.url = tkinter.StringVar()

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        # add menu options & buttons
        menu_bar = tkinter.Menu(self.root)
        file_menu = tkinter.Menu(menu_bar, tearoff=0)
        # file_menu.add_cascade(label="Version: " + self.current_version, state="disabled")
        # menu_bar.add_cascade(label="File", menu=file_menu)

        # setting up the frames
        self.input_frame = ttk.Frame(self.root)
        self.input_frame.pack(padx=10, pady=(10, 0), side="top", fill="x")

        self.status_frame = ttk.Frame(self.root)
        self.status_frame.pack(side="top", fill="x", pady=0, ipady=0)

        # url text box
        text_box_label = ttk.Label(self.input_frame, text="URL")
        text_box_label.pack(side="left", padx=5, pady=0)
        text_box = ttk.Entry(self.input_frame, textvariable=self.url)
        text_box.pack(side="left", pady=0)

        # download button
        download_button = ttk.Button(self.input_frame, text='Download', command=self.download, state='enabled')
        download_button.pack(side="right", padx=5, pady=0) #, pady=3

        self.root.config(menu=menu_bar)
        sv_ttk.set_theme("dark")

        self.root.mainloop()

    def download(self):
        url = self.url.get().strip()
        format = 'mp3'
        quality = 'bestaudio/best'
        self.prog.start_download_thread(url=url, format=format, quality=quality)

    def initialize_status(self):
        # status message
        self.status_field = ttk.Label(self.status_frame, text=self.status_message, font=("Segoe UI", 10), padding=0)
        self.status_field.pack(side="bottom", fill="x", ipadx=20, pady=0)
        self.is_initialized = True

    def set_status(self, status):
        if not self.is_initialized:
            self.initialize_status()

        if self.marquee_tracker:
            self.root.after_cancel(self.marquee_tracker)
            self.marquee_tracker = None

        self.status_message = status
        color = None

        # setting the color
        if 'Download complete' in status:
            color = "green"
        elif 'Error' in status:
            color = "red"
        else: color = "white"

        if self.status_field and self.status_field.winfo_exists():
            self.status_field.config(text=self.status_message, foreground=color)

            if len(self.status_message) > 56:
                status = self.truncate(status, max_length=50)
                self.status_message = status +  '   |   '
                self.marquee(self.status_field, self.status_message)

    def marquee(self, widget, text, delay=100):
        def shift():
            nonlocal text
            if widget.winfo_exists():
                text = text[1:] + text[0]
                widget.config(text=text)
                self.marquee_tracker = widget.after(delay, shift)
            else:
                self.marquee_tracker = None

        if self.marquee_tracker:
            widget.after_cancel(self.marquee_tracker)

        shift()

    def truncate(self, text, max_length=40):
        if len(text) > max_length:
            return text[:max_length-3] + "..."
        return text

    def on_closing(self):
        self.is_destroyed = True

        # cancel any pending marquee animation
        if self.marquee_tracker:
            self.root.after_cancel(self.marquee_tracker)
            self.marquee_tracker = None

        if hasattr(self.prog, 'is_downloading'):
            self.prog.is_downloading = False

        self.root.destroy()