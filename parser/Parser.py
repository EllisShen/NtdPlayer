#!/usr/bin/env python
"""
Parser Class. This class testify ffplay stderr message.

Adapted by Ellis Shen, New York.
"""

import logging
import re

# init logging
logger = logging.getLogger(__name__)


class Parser(object):
    """ Parsing
    """
    FFMPEG_DURATION_PATTERN = re.compile("Duration: (\\d\\d):(\\d\\d):(\\d\\d)\\.(\\d\\d)")
    FFPLAY_PLAYBACK_PATTERN = re.compile("^\s(.+) A-V: .+")

    def __init__(self):
        super(Parser, self).__init__()

    @staticmethod
    def ffmpegStderrParser(line):
        m = Parser.FFPLAY_PLAYBACK_PATTERN.match(line)
        if m:
            ptsTime = m.group(1).strip()
            return ptsTime
        else:
            return None
