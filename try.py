import socket
import importlib
from threading import Thread
import parse
from Cryptodome.Cipher import ARC4
import time


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
                try:
                    data = self.server.recv(4096)
                    if data:
                        self.game.sendall(data)
                except (ConnectionResetError, OSError):
                        self.server.close()
                        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        self.server.connect((self.host, self.port))

class Game2Proxy(Thread):
    def __init__(self, host, port):
        super(Game2Proxy, self).__init__()
        self.game = None
        self.port = port
        self.host = host
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((host, port))
        self.sock.listen(1)
        self.game, addr = self.sock.accept()

    def run(self):
        while True:
            try:
                data = self.game.recv(4096)
                if data:
                    importlib.reload(parse)
                    parse.parsing(data, self.port, 'client')
                    self.server.sendall(data)
            except (ConnectionResetError, OSError):
                    self.game.close()
                    self.sock.close()
                    self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                    self.sock.bind((self.host, self.port))
                    self.sock.listen(1)
                    self.game,addr = self.sock.accept()

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
