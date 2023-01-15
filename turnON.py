from threading import Thread
import sys

from client import *

"""
i hate myself and i hate python i hope yall suffer.
this this gonna be the MAIn CLASS or whatver it is. i use C++ not fuckin python
simpilar to swrllys proxy.py
"""

class turnON:
    def __init__(self, client: Client):
        self.localHostAddr = "127.0.0.1"
        self.localHostPort = 2050 # look up 843 and flash
        self.managerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client = client

        self.active = False
        self.serverMonitorThread = None
        
