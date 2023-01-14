import threading
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

    def ServerMonitor(self):
        self.managerSocket.bind((self.localHostAddr, self.localHostPort))
        self.managerSocket.listen(3)
		# always listening for client connect
        while True:
            self.client.gameSocket, addr = self.managerSocket.accept()

    def Start(self):
        self.active = True
		# start up server socket
        self.serverMonitorThread = threading.Thread(target = self.ServerMonitor, daemon = True)
        self.serverMonitorThread.start()
        self.Connect()

    def Connect(self):
		# connect sockets first
        self.client.ConnectRemote(self.client.remoteHostAddr, self.client.remoteHostPort)
        self.client.connected = True

		# listen for packets
        while True:
            self.client.Listen()

    """
    def Restart(self):
		self.client.Disconnect()
		self.client.ResetCipher()
		threading.Thread(target = self.Connect, daemon = False).start()
	"""
					
def main():
	print("[Initializer]: Loading plugins...")
	print("[Initializer]: Starting proxy...")
	client = Client()
	proxy = Proxy(client)

	threading.Thread(target = proxy.Start, daemon = True).start()

	print("[Initializer]: Proxy started!")

	print("[Initializer]: Starting GUI...")
	print("[Initializer]: GUI started!")
	


if __name__ == "__main__":
	main()
        
