#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Application main method

Created by Ellis Shen, New York.
"""
import threading
import os
import time
import logging
from Tkinter import Tk, Toplevel
import tkMessageBox

from gui import Application
from menu.appColor import gui_Dark
from menu.appMsg import QuitApp_Question
from queue.Queues import Queues

# init logging
logger = logging.getLogger(__name__)

# global app version define here.
appVersion = "0.2.0"

# create root window and hide it
root = Tk()
root.withdraw()
# create top level window belong to root
top = Toplevel(root)

# global Queues
playerQueues = Queues()


def appHandler():
    if tkMessageBox.askokcancel("Quit?", QuitApp_Question, icon=tkMessageBox.QUESTION,
                                default=tkMessageBox.CANCEL, parent=top):
        if app.process is not None and app.process.poll() is None:
            app.process.terminate()
            # app.process.kill()
        try:
            os.remove(os.path.join(app.tempDir, "pvIn.gif"))
            os.remove(os.path.join(app.tempDir, "pvOut.gif"))
            os.removedirs(app.tempDir)
        except OSError:
            pass

        root.destroy()


def guiPreInitialize():
    # Disable resize feature
    #top.resizable(width=FALSE, height=FALSE)
    #top.attributes("-topmost", True) # bring window to top

    # get current location and assign TKDND_LIBRARY location
    tkdndPath = os.getcwd() + "/tkdnd2.7"
    os.environ['TKDND_LIBRARY'] = tkdndPath
    top.columnconfigure(0, weight=1)
    top.rowconfigure(0, weight=1)
    top.configure(background=gui_Dark)
    top.minsize(600, 100)
    top.geometry('+400+530')
    top.protocol("WM_DELETE_WINDOW", appHandler)
    top.title('NTD Player')


if __name__ == "__main__":
    try:
        # initialize log
        timestr = time.strftime('%Y-%m%d')
        LOG_FILENAME = timestr + '.log'
        homeLogs = os.path.expanduser("~") + "/Library/Logs/NtdPlayer"
        # create log folder
        if not os.path.exists(homeLogs):
            os.makedirs(homeLogs)
        logging.basicConfig(filename=homeLogs + "/" + LOG_FILENAME, level=logging.DEBUG,
                            format='[%(asctime)s][%(levelname)s] - %(message)s (%(threadName)-10s) (%(module)s)',
                            disable_existing_loggers=False, )
        
        # Gui init
        guiPreInitialize()
        app = Application(parent=root, version=appVersion, master=top, queues=playerQueues)
        top.mainloop()

    except (KeyboardInterrupt, SystemExit):
        if app.process is not None and app.process.poll() is None:
            app.process.terminate()
            # app.process.kill()
        try:
            os.remove(os.path.join(app.tempDir, "pvIn.gif"))
            os.remove(os.path.join(app.tempDir, "pvOut.gif"))
            os.removedirs(app.tempDir)
        except OSError:
            pass
        root.destroy()
    except AttributeError:
        pass
