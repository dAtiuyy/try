import socket
import importlib
from threading import Thread
import parse
from Cryptodome.Cipher import ARC4
import pickle
from RC4aa import RC4

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

class Proxy2server(Thread):
    def __init__(self, host, port):
        super(Proxy2server, self).__init__()
        self.game = None
        self.port = port
        self.host = host
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.connect((host, port))

    def run(self):
        while True:
            data = self.server.recv(4096)
            if data:
                #print( "[{}] <- {}".format(self.port, data))
                try:
                   importlib.reload(parse)
                   parse.parsing(data, self.port, 'server')
                except Exception as e:
                    print('server[{}]'.format(self.port), e)
                # do sum
                self.game.sendall(data)

class Game2Proxy(Thread):
    def __init__(self, host, port):
        super(Game2Proxy, self).__init__()
        self.game = None
        self.port = port
        self.host = host
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((host, port))
        sock.listen(1)
        self.game, addr = sock.accept()

    def run(self):
        while True:
            data = self.game.recv(4096)
            if data:
                #print( "[{}] -> {}".format(self.port, data))
                importlib.reload(parse)
                parse.parsing(data, self.port, 'client')
                #does shit dude
                self.server.sendall(data)

class Proxy(Thread):
    def __init__(self, from_host, to_host, port):
        super(Proxy, self).__init__()
        self.from_host = from_host
        self.to_host = to_host
        self.port = port

    def run(self):
        while(True):
            print( "[proxy({})] is setting up".format(self.port))
            self.g2p = Game2Proxy(self.from_host, self.port)
            self.p2s = Proxy2server(self.to_host, self.port)
            print( "[proxy({})] connection established".format(self.port))
            self.g2p.server = self.p2s.server
            self.p2s.game = self.g2p.game

            self.g2p.start()
            self.p2s.start()

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

