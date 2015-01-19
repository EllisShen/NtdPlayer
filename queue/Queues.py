#!/usr/bin/env python
"""
Queues Class. It initializes all queues here.

Adapted by Ellis Shen, New York.
"""

import Queue


class Queues(object):
    """docstring for Queues"""

    def __init__(self):
        super(Queues, self).__init__()
        self.stdoutQueue = Queue.Queue()
        self.stderrQueue = Queue.Queue()

    def getStdoutQueue(self):
        return self.stdoutQueue

    def getStderrQueue(self):
        return self.stderrQueue
