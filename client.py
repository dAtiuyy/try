import socket
import importlib
from threading import Thread
import parse
from Cryptodome.Cipher import ARC4
import pickle
from RC4aa import RC4
import turnON
import sys
import time
import select
import struct

class Client:
    def __init__(self):
        self.remoteHostAddr = "51.222.11.213"
        self.remoteHostPort = 2050
        self.objectID = None
        self.charID = None
        self.reconnecting = False
        self.connected = False
        self.clientSendKey = RC4(bytearray.fromhex("BA15DE"))
        self.clientReceiveKey = RC4(bytearray.fromhex("612a806cac78114ba5013cb531"))
        self.serverSendKey = RC4(bytearray.fromhex("612a806cac78114ba5013cb531"))
        self.serverReceiveKey = RC4(bytearray.fromhex("BA15DE"))
        self.gameSocket = None
        self.serverSocket = None
        self.currentMap = "None"
        self.gameIDs = {
			-1 : "Nexus",
			-2 : "Nexus",
			-5 : "Vault",
			-15 : "Marketplace",
			-16 : "Ascension Enclave",
			-17 : "Aspect Hall"
		}

    def Disconnect(self):
        self.connected = False
        if self.serverSocket:
            self.serverSocket.shutdown(socket.SHUT_RDWR)
            self.serverSocket.close()
        if self.gameSocket:
            self.gameSocket.shutdown(socket.SHUT_RDWR)
            self.gameSocket.close()
        self.gameSocket = None
        self.serverSocket = None

	# reset ciphers to default state
    def ResetCipher(self):
        self.clientSendKey.reset()
        self.clientReceiveKey.reset()
        self.serverSendKey.reset()
        self.serverReceiveKey.reset()

	# for now, we can just recon lazily
    def Reconnect(self):
        self.ConnectRemote(self.remoteHostAddr, self.remoteHostPort)
        self.connected = True

	# Connect to remote host. Block until client connected
    def ConnectRemote(self, host, port):
		# the invalid recon key bug is when client doesn't connect to the proxy server's socket
		# reduced sleep time and it seems to be ok now
        while self.gameSocket == None:
            time.sleep(0.005)

        self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serverSocket.connect((host, port))

	# closes both sockets
    def Close(self):
        self.gameSocket.close()
        self.serverSocket.close()

	# restart entire connection
    def reset(self):
        self.internalBulletID = 0
        self.firstBulletTime = None
        self.Disconnect()
        self.ResetCipher()
        self.Reconnect()

	# call this fcn when you reset connection
    def resetMapName(self):
        self.currentMap = "Nexus"


master_server = Proxy('0.0.0.0','51.222.11.213', 2050)
master_server.start()
print("[Initializer]: Deserializing objects...")
with open("bin/BulletDictionary.pkl", "rb") as f:
    bulletDictionary = pickle.load(f)
    print("[Initializer]: Deserialized {} enemies.".format(len(set([x[0] for x in bulletDictionary.keys()]))))            
    print("[Initializer]: Deserialized {} bullets.".format(len(bulletDictionary)))
with open("bin/NameDictionary.pkl", "rb") as f:
    nameDictionary = pickle.load(f)

with open("bin/TileDictionary.pkl", "rb") as f:
    tileDictionary = pickle.load(f)       
    print("[Initializer]: Deserialized {} tiles.".format(len(tileDictionary)))

with open("bin/AoeDictionary.pkl", "rb") as f:
    aoeDictionary = pickle.load(f)
    print("[Initializer]: Deserialized {} AOEs.".format(sum({y: len(aoeDictionary[y]) for y in aoeDictionary}.values())))

class BulletInfo:

	def __init__(self):
		# bulletType in XML
		self.bulletType = 0
		self.damage = 0

	def PrintString(self):
		print("bulletType", self.bulletType, "damage", self.damage)

