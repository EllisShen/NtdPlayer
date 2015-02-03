#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
 message window for NtdPlayer

"""
from Tkconstants import HORIZONTAL, FALSE
from Tkinter import Toplevel
import ttk
from menu.appColor import gui_White


class ProgressWindow(Toplevel):
    def __init__(self, parent, title, message):
        Toplevel.__init__(self, parent)
        self.configure(background=gui_White)
        self.minsize(400, 50)
        # self.geometry("+%d+%d" % (parent.winfo_rootx(), parent.winfo_rooty()))
        # self.geometry("+400+530")
        self.resizable(height=FALSE, width=FALSE)
        self.title(title)
        self.grab_set()

        ttk.Label(self, text=message, font=("Lucida Grande", 16)).pack(pady=5)
        self.pBar = ttk.Progressbar(self, orient=HORIZONTAL, length=320, mode='indeterminate')
        self.pBar.pack(pady=5)
        self.pBar.start()

    def stopProgress(self):
        self.pBar.stop()

    def closeWindow(self):
        self.destroy()

# if __name__ == "__main__":
#     master = Tk()
#     master.geometry("+400+400")
#     test = ProgressWindow(master, "test", "Background Progressing...")
#     test.mainloop()