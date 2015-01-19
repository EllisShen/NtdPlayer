#!/usr/bin/env python
"""
ClipInfo Class. It stores clip info here.

Adapted by Ellis Shen, New York.
"""


class ClipInfo(object):
    """docstring for Queues"""

    def __init__(self):
        super(ClipInfo, self).__init__()
        self.filePath = ''
        self.length = '0'
        self.ptsTime = ''
        self.inPoint = ''
        self.outPoint = ''

    def setFilePath(self, filePath):
        self.filePath = filePath
        return

    def getFilePath(self):
        return self.filePath

    def setLength(self, length):
        self.length = length
        return

    def getLength(self):
        return self.length

    def setPtsTime(self, ptsTime):
        self.ptsTime = ptsTime
        return

    def getPtsTime(self):
        return self.ptsTime

    def setInPoint(self, inPoint):
        self.inPoint = inPoint
        return

    def getInPoint(self):
        return self.inPoint

    def setOutPoint(self, outPoint):
        self.outPoint = outPoint
        return

    def getOutPoint(self):
        return self.outPoint
