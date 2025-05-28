import tkinter
from tkinter import ttk
# from tktooltip import ToolTip
import sv_ttk

class GUI:
    def __init__(self):
        self.options = None
        self.current_option = None
        self.root = tkinter.Tk()
        self.selected_tab = None
        self.media_type_dropdown = None

    def initialize_gui(self):
        # setup window
        self.root.title('Auto-Play Bot')
        self.root.minsize(250, 75)
        self.root.resizable(False, False)

        # add menu options & buttons
        menu_bar = tkinter.Menu(self.root)
        file_menu = tkinter.Menu(menu_bar, tearoff=0)
        # file_menu.add_cascade(label="Version: " + self.current_version, state="disabled")
        # menu_bar.add_cascade(label="File", menu=file_menu)

        # url text box
        text_box_label = ttk.Label(text="URL")
        text_box_label.pack(side="left")
        text_box = ttk.Entry(self.root, textvariable=self.selected_tab)
        text_box.pack(side="left")

        self.root.config(menu=menu_bar)
        sv_ttk.set_theme("dark")

        self.root.bind('<Return>', self.start_bot)
        self.root.mainloop()