#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
GUI mainloop

Created by Ellis Shen, New York.
"""
from Tkconstants import LEFT
import os
import subprocess
import sys
import threading
import time
import logging
from Tkinter import Tk, Toplevel, StringVar, Label, Frame, PhotoImage, Canvas
import tkFileDialog
import tkMessageBox
import ttk
import tempfile

from Queue import Empty, Full
from menu.appColor import gui_Dark, gui_White, gui_pink
from menu.appMsg import QuitApp_Question, Trim_ConfirmMsg, FileExtension_Error, \
    FFmpeg_Preview_Error, Trim_TimingErrorMsg
from menu.appProgressWindow import ProgressWindow
from parser.Parser import Parser
from tkDnD.tkdnd_wrapper import TkDND
from clipInfo import ClipInfo


logger = logging.getLogger(__name__)
VIDEO_EXTENTIOM_LIST = ['.mov', '.mpg', '.mpeg', '.mp4', '.avi']
FFPLAY_WIDTH = "640"
FFPLAY_HEIGHT = "360"
CANVAS_WIDTH = 400
CANVAS_HEIGHT = 10


class Application(object):
    def __init__(self, parent, version="0.0.0", master=None, queues=None):

        self.itemList = []  # reference to all ttk label items in statusWindow.
        self.imageReference = {}  # reference to all icon images.
        self.queues = queues
        self.clipInfo = ClipInfo()
        self.process = None
        self.tempDir = tempfile.mkdtemp()

        global top
        top = master

        # initialize tkdnd
        logger.info('Initialize TkDnD library')
        # since we cx_Freeze for distribution on PC, it will put all resource files at the same directory.
        # set the TKDND_LIBRARY environment variable to point to the location of tkdnd2.7 dylib folder.
        if sys.platform == 'win32':
            if getattr(sys, 'frozen', False):
                os.environ['TKDND_LIBRARY'] = os.path.join(os.path.dirname(sys.executable), 'tkdnd2.7')
        self.dnd = TkDND(top)

        # init widget
        self.initWidget()

    def initWidget(self):

        # def renderPreviewImage(ptsTime, filePath, outPut):
        # try:
        # subprocess.check_call(
        #             ['ffmpeg', '-y', '-i', filePath, '-ss', ptsTime, '-vframes', '1', '-vf', 'scale=-1:min(80\,
        # iw)', outPut])
        #         pvIn_obj = PhotoImage(file=outPut)
        #         pvIn_Label = ttk.Label(self.sndLeftFrame, image=pvIn_obj)
        #         pvIn_Label.image = pvIn_obj
        #         pvIn_Label.pack()
        #     except subprocess.CalledProcessError:
        #         logger.error("ffmpeg render inPoint frame failed! ptsTime = %s" % ptsTime)
        #     pass

        def setInPoint():
            ptsTime = self.clipInfo.getPtsTime()
            logger.info("Set In point = %s" % ptsTime)
            self.clipInfo.setInPoint(ptsTime)
            filePath = self.clipInfo.getFilePath()
            try:
                ffmpegReturn = subprocess.check_call(
                    ['bin/ffmpeg', '-ss', ptsTime, '-y', '-i', filePath, '-vframes', '1', '-vf',
                     'scale=-1:min(120\, iw)', os.path.join(self.tempDir, 'pvIn.gif')])
                if ffmpegReturn != 0:
                    tkMessageBox.showwarning("Error", FFmpeg_Preview_Error, icon=tkMessageBox.ERROR, parent=top)
                    return
                pvIn_obj = PhotoImage(file=os.path.join(self.tempDir, 'pvIn.gif'))
                if self.pvIn_Label is None:
                    self.pvInText.set(ptsTime + 's')
                    Label(self.sndLeftFrame, textvariable=self.pvInText, font=("Arial Bold", 14),
                          fg=gui_White, bg=gui_Dark, pady=0).pack()
                    self.pvIn_Label = ttk.Label(self.sndLeftFrame, image=pvIn_obj)
                    self.pvIn_Label.image = pvIn_obj
                    self.pvIn_Label.pack()

                    if self.pvOut_Label is None:
                        self.pvOutText.set('0s')
                        Label(self.sndRightFrame, textvariable=self.pvOutText, font=("Arial Bold", 14),
                              fg=gui_White, bg=gui_Dark, pady=0).pack()
                        self.pvOut_Label = ttk.Label(self.sndRightFrame, image=self.pvBlack_Obj)
                        self.pvOut_Label.image = self.pvBlack_Obj
                        self.pvOut_Label.pack()
                else:
                    self.pvInText.set(ptsTime + 's')
                    self.pvIn_Label.configure(image=pvIn_obj)
                    self.pvIn_Label.image = pvIn_obj
            except subprocess.CalledProcessError:
                logger.error("ffmpeg render inPoint frame failed! ptsTime = %s" % ptsTime)
            pass

        def setOutPoint():
            ptsTime = self.clipInfo.getPtsTime()
            logger.info("Set Out point = %s" % ptsTime)
            self.clipInfo.setOutPoint(ptsTime)
            filePath = self.clipInfo.getFilePath()
            try:
                ffmpegReturn = subprocess.check_call(
                    ['bin/ffmpeg', '-ss', ptsTime, '-y', '-i', filePath, '-vframes', '1', '-vf',
                     'scale=-1:min(120\, iw)', os.path.join(self.tempDir, 'pvOut.gif')])
                if ffmpegReturn != 0:
                    tkMessageBox.showwarning("Error", FFmpeg_Preview_Error, icon=tkMessageBox.ERROR, parent=top)
                    return
                pvOut_obj = PhotoImage(file=os.path.join(self.tempDir, 'pvOut.gif'))
                if self.pvOut_Label is None:
                    self.pvOutText.set(ptsTime + 's')
                    Label(self.sndRightFrame, textvariable=self.pvOutText, font=("Arial Bold", 14),
                          fg=gui_White, bg=gui_Dark, pady=0).pack()
                    self.pvOut_Label = ttk.Label(self.sndRightFrame, image=pvOut_obj)
                    self.pvOut_Label.image = pvOut_obj
                    self.pvOut_Label.pack()

                    if self.pvIn_Label is None:
                        self.pvInText.set('0s')
                        Label(self.sndLeftFrame, textvariable=self.pvInText, font=("Arial Bold", 14),
                              fg=gui_White, bg=gui_Dark, pady=0).pack()
                        self.pvIn_Label = ttk.Label(self.sndLeftFrame, image=self.pvBlack_Obj)
                        self.pvIn_Label.image = self.pvBlack_Obj
                        self.pvIn_Label.pack()
                else:
                    self.pvOutText.set(ptsTime + 's')
                    self.pvOut_Label.configure(image=pvOut_obj)
                    self.pvOut_Label.image = pvOut_obj
            except subprocess.CalledProcessError:
                logger.error("ffmpeg render OutPoint frame failed! ptsTime = %s" % ptsTime)
            pass

        def trimVideo():
            answer = tkMessageBox.askyesno("Confirm?", Trim_ConfirmMsg, icon=tkMessageBox.QUESTION, parent=top)
            if answer:
                inPoint = float(self.clipInfo.getInPoint())
                outPoint = float(self.clipInfo.getOutPoint())

                # check if outPoint is later than inPoint
                if outPoint < inPoint:
                    tkMessageBox.showerror("Error!", Trim_TimingErrorMsg, icon=tkMessageBox.ERROR, parent=top)
                    return

                logger.info("Confirmed to trim video from In = %f to Out = %f", inPoint, outPoint)
                home = os.path.expanduser("~")
                savePath = tkFileDialog.asksaveasfilename(
                    title="Set filename and save location",
                    defaultextension=".mov",
                    initialdir=os.path.join(home, "Desktop"),
                    parent=top
                )
                logger.info("File saved path = %s" % savePath)
                if savePath is not "":
                    pWin = ProgressWindow(top, "Attention", "Background Processing...")
                    pWin.geometry("+%d+%d" % (top.winfo_rootx() + 50, top.winfo_rooty() + 50))
                    pWin.after(1000, lambda: ffmpegTrim(pWin, inPoint, outPoint, savePath))
            pass

        def ffmpegTrim(progressBar, inPoint, outPoint, savePath):
            ffmpegReturn = subprocess.check_call(
                ['bin/ffmpeg', '-ss', str(inPoint), '-y', '-i', self.clipInfo.getFilePath(), '-t',
                 str(outPoint - inPoint),
                 '-c', 'copy', savePath])
            if ffmpegReturn == 0:
                progressBar.stopProgress()
                progressBar.closeWindow()
                tkMessageBox.showinfo("Info", "Trim Video Successfully!", icon=tkMessageBox.INFO, parent=top)
            else:
                logger.error("FFmpeg trim video fails! Error code = %d", ffmpegReturn)
                progressBar.closeWindow()
                tkMessageBox.showerror("Error", "Trim Video Failed!!", icon=tkMessageBox.ERROR, parent=top)
            pass

        # init custom Style
        gui_style = ttk.Style()
        gui_style.configure("TButton", relief="flat", bd=gui_Dark)

        #
        # init main frame and second frame
        #
        mainFrame = Frame(top, bg=gui_Dark)
        mainFrame.pack()
        sendFrame = Frame(top, bg=gui_Dark)
        sendFrame.pack()
        thirdFrame = Frame(top, bg=gui_Dark)
        thirdFrame.pack()
        # init frames inside main frame
        leftFrame = Frame(mainFrame, bg=gui_Dark, padx=48)
        leftFrame.pack(side=LEFT)
        middleFrame = Frame(mainFrame, bg=gui_Dark, padx=16)
        middleFrame.pack(side=LEFT)
        rightFrame = Frame(mainFrame, bg=gui_Dark, padx=48)
        rightFrame.pack(side=LEFT)
        self.labelText = StringVar()
        self.labelText.set("0:00:00.00")
        # InPoint Button
        inPoint_Obj = PhotoImage(file=Application.find_data_file(os.path.join("icons", "InButton.gif")))
        outPoint_Obj = PhotoImage(file=Application.find_data_file(os.path.join("icons", "OutButton.gif")))
        self.pvBlack_Obj = PhotoImage(file=Application.find_data_file(os.path.join("icons", "pvBlack.gif")))
        self.imageReference['InPoint'] = inPoint_Obj
        self.imageReference['OutPoint'] = outPoint_Obj
        self.imageReference['pvBlack'] = self.pvBlack_Obj

        ttk.Button(leftFrame, image=inPoint_Obj, command=lambda: setInPoint()).pack()
        # Timecode label
        Label(middleFrame, textvariable=self.labelText, font=("Arial Bold", 36),
              fg=gui_White, bg=gui_Dark, pady=0).pack()
        Label(middleFrame, text="HR           MIN                            SEC", font=("Arial", 10),
              fg=gui_White, bg=gui_Dark, pady=0).pack()
        # OutPoint Button
        ttk.Button(rightFrame, image=outPoint_Obj, command=lambda: setOutPoint()).pack()

        #
        # init frames inside second frames
        #
        self.sndLeftFrame = Frame(sendFrame, bg=gui_Dark, pady=16)
        self.sndLeftFrame.pack(side=LEFT)
        self.pvIn_Label = None
        self.pvInText = StringVar()
        sndMiddleFrame = Frame(sendFrame, bg=gui_Dark, padx=30, pady=16)
        sndMiddleFrame.pack(side=LEFT)
        # ttk.Button(sndMiddleFrame, text="Trim Video", command=lambda: trimVideo()).pack()
        self.sndRightFrame = Frame(sendFrame, bg=gui_Dark, pady=16)
        self.sndRightFrame.pack(side=LEFT)
        self.pvOut_Label = None
        self.pvOutText = StringVar()
        # progressBar and Button
        # thirdLeftFrame = Frame(thirdFrame, bg=gui_Dark, padx=30, pady=16)
        # thirdLeftFrame.pack(side=LEFT)
        thirdMiddleFrame = Frame(thirdFrame, bg=gui_Dark, padx=15, pady=16)
        thirdMiddleFrame.pack(side=LEFT)
        thirdRightFrame = Frame(thirdFrame, bg=gui_Dark, padx=15, pady=16)
        thirdRightFrame.pack(side=LEFT)

        # self.clipProgress = ttk.Progressbar(thirdMiddleFrame,  orient=HORIZONTAL, length=320, mode='indeterminate')
        # self.clipProgress.pack()
        self.w = Canvas(thirdMiddleFrame, width=CANVAS_WIDTH, height=CANVAS_HEIGHT, bg=gui_Dark, bd=0)
        self.w.pack()
        self.pin = self.w.create_rectangle(2, 0, 6, 15, fill=gui_pink, outline=gui_Dark)
        self.pinCurX = 2
        # print "coords = " + str(self.w.coords(self.pin))

        ttk.Button(thirdRightFrame, text="Trim", command=lambda: trimVideo()).pack()
        # register top as Tkdnd drag zone
        self.dnd.bindtarget(mainFrame, self.videoHandler, 'text/uri-list')
        pass

    def videoHandler(self, event):
        # get file path and file extension
        logging.info('video = %s' % event.data)
        path = event.data
        path = path.replace("{", "")
        path = path.replace("}", "")
        # path = path.translate(None, '{}')  # remove {} from path
        filePath = os.path.abspath(path)
        fileExtension = os.path.splitext(filePath)[1]
        logging.debug('filePath = %s', filePath)
        logging.debug('fileExtension = %s', fileExtension)
        # save filePath to clipInfo class
        self.clipInfo.setFilePath(filePath)
        # check file extension first
        if fileExtension in VIDEO_EXTENTIOM_LIST:
            if self.process is None:
                self.process = subprocess.Popen(
                    ['bin/ffplay', '-x', FFPLAY_WIDTH, '-y', FFPLAY_HEIGHT, filePath],
                    stderr=subprocess.PIPE)
                self.thread = threading.Thread(target=self.readlines, args=(self.process, self.queues.stderrQueue))
                self.thread.setDaemon(True)
                self.thread.start()
                # retrieve queue data
                self.updateGui()
            elif self.process.poll() is None:
                # last process is not terminated yet, terminate it!
                self.process.terminate()
                self.process = None
                self.videoHandler(event)
                pass
            else:  # last process is terminated, clear process and re-enter the procedure.
                self.process = None
                self.videoHandler(event)
                pass
        else:
            tkMessageBox.showwarning("Error", FileExtension_Error, icon=tkMessageBox.ERROR, parent=top)

    def readlines(self, process, queue):
        line = ''
        durationInspected = False
        while process.poll() is None:
            out = process.stderr.read(1)
            if out != '':
                if (out == '\n') or (out == '\r'):
                    logger.debug(line + '\n')
                    # print line
                    # Inspect duration
                    if not durationInspected:
                        m = Parser.FFMPEG_DURATION_PATTERN.search(line)
                        if m:
                            hour = int(m.group(1))
                            minute = int(m.group(2))
                            second = int(m.group(3))
                            onePerSecond = int(m.group(4))
                            totalSeconds = str(hour * 3600 + minute * 60 + second) + '.' + str(onePerSecond)
                            logger.info("total seconds = %s", totalSeconds)
                            # set clipLength
                            self.clipInfo.setLength(totalSeconds)
                            durationInspected = True
                    # Inspect playback info
                    ptsTime = Parser.ffmpegStderrParser(line)
                    if ptsTime is not None:
                        try:
                            queue.put_nowait(ptsTime)
                        except Full:
                            logger.error("queue full error!")
                            pass
                    line = ''
                else:
                    line = line + out

            if out == '':
                break

    def updateGui(self):

        def _checkDigits(string):
            if len(string) < 2:
                string = '0' + string
            return string

        try:
            ptsTime = self.queues.stderrQueue.get_nowait()
            negative = False
            # ffplay may throw out "nan" output, ignore it!
            if ptsTime != "nan":
                # make sure the ptsTime is not longer then clip length
                if float(ptsTime) <= float(self.clipInfo.getLength()):
                    self.clipInfo.setPtsTime(ptsTime)
                    # convert ptsTime to HR:MIN:SEC format
                    integer, decimal = ptsTime.split('.')
                    # Is it a negative number?
                    if '-' in integer:
                        integer = integer.replace('-', '')
                        negative = True
                    integer = int(integer)
                    hour = integer / 3600
                    integer %= 3600
                    minute = integer / 60
                    second = integer % 60
                    hour = str(hour)
                    minute = str(minute)
                    minute = _checkDigits(minute)  # make it as double digits
                    second = str(second)
                    # put negative '-' in string if it's negative number
                    if negative:
                        second = '-' + second
                    second = _checkDigits(second)  # make it as double digits
                    self.labelText.set(str(hour) + ':' + str(minute) + ':' + str(second) + '.' + decimal)

                    # update video indicator location
                    pinLocation = int((float(ptsTime) / float(self.clipInfo.getLength())) * CANVAS_WIDTH)
                    if pinLocation > 0:
                        self.w.coords(self.pin, (pinLocation, 0, pinLocation + 4, 15))
        except Empty:
            pass

        if self.process.poll() is None:
            top.after(10, self.updateGui)

    @staticmethod
    def find_data_file(filename):
        if sys.platform == 'win32':
            if getattr(sys, 'frozen', False):
                # The application is frozen
                datadir = os.path.dirname(sys.executable)

            else:
                # The application is not frozen
                # Change this bit to match where you store your data files:
                datadir = os.path.dirname(__file__)

            return os.path.join(datadir, filename)
        else:
            return filename


# ------------------------------------------------------------------------------
# Function Test
# ------------------------------------------------------------------------------

def appHandler():
    if tkMessageBox.askokcancel("Quit?", QuitApp_Question,
                                icon=tkMessageBox.QUESTION, default=tkMessageBox.CANCEL, parent=top):
        os.removedirs(app.tempDir)
        root.destroy()


if __name__ == "__main__":
    try:
        # initialize log
        timestr = time.strftime('%Y-%m%d')
        LOG_FILENAME = timestr + '.log'
        logging.basicConfig(filename=LOG_FILENAME, level=logging.DEBUG,
                            format='[%(levelname)s] (%(threadName)-10s) (%(module)s) %(message)s', )

        # create root window and hide it
        root = Tk()
        root.withdraw()
        # create top level window belong to root
        top = Toplevel(root, bg=gui_Dark)
        # Disable resize feature
        # top.resizable(width=FALSE, height=FALSE)
        # top.attributes("-topmost", True) # bring window to top
        top.columnconfigure(0, weight=1)
        top.rowconfigure(0, weight=1)
        top.minsize(600, 100)
        top.geometry('+400+500')
        top.protocol("WM_DELETE_WINDOW", appHandler)
        # Make the window being focused
        # Create App obj
        app = Application(parent=root, master=top)
        top.title('NTD Player')

        top.mainloop()
        root.destroy()

    # entry = Entry()
    # entry.pack()

    except (KeyboardInterrupt, SystemExit):
        pass
