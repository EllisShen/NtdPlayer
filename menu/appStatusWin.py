#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
 status window class for NtdPlayer

"""
from Tkconstants import HORIZONTAL, FALSE
from Tkinter import Toplevel, Frame, Label
import ttk
import logging

# init logging

logger = logging.getLogger(__name__)


class StatusWindow(Toplevel):
    def __init__(self, parent, title, fileName):
        Toplevel.__init__(self, parent)
        self.configure()
        self.minsize(400, 50)
        self.geometry("+%d+%d" % (parent.winfo_rootx() + 500, parent.winfo_rooty() - 90))
        self.createWidgets(parent, fileName)
        self.resizable(height=FALSE, width=FALSE)
        self.title(title)
        self.grab_set()
        self.protocol("WM_DELETE_WINDOW", self.Ok)

        # wait loop
        # self.wait_window()  # widget wait until destroy.

    def Ok(self, event=None):
        self.destroy()

    def createWidgets(self, parent, fileName):
        statusFrame = Frame(parent)
        statusFrame.pack()
        Label(statusFrame, text=fileName).pack()
        self.progress = ttk.Progressbar(statusFrame, orient=HORIZONTAL, length=150, mode='indeterminate')
        self.progress.start()
        self.progress.pack()
        # ttk.Button(rightFrame, text="OK", state=DISABLE).pack()
        pass


# class itemSatusFrame(Frame):
#     def __init__(self, parent, order, fileName):
#         Frame.__init__(self, parent)
#         leftFrame = Frame(self)
#         leftFrame.pack(side=LEFT)
#         rightFrame = Frame(self)
#         rightFrame.pack(side=LEFT)
#         # init widget for leftFrame
#         Label(leftFrame, text=str(order)).pack()
#         # init widgets for rightFrame
#         Label(rightFrame, text=fileName).pack()
#         self.progressBar = ttk.Progressbar(rightFrame, orient=HORIZONTAL, length=150, mode='indeterminate')
#         self.progressBar.pack()



