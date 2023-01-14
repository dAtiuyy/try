import RC4Decrypt
from Cryptodome.Cipher import ARC4
import struct
from RC4aa import RC4

def parsing(data, port, origin):
        clientSendKey = RC4(bytearray.fromhex("BA15DE"))
        clientReceiveKey = RC4(bytearray.fromhex("612a806cac78114ba5013cb531"))
        serverSendKey = RC4(bytearray.fromhex("612a806cac78114ba5013cb531"))
        serverReceiveKey = RC4(bytearray.fromhex("BA15DE"))
        if origin == 'server':
                return
        decipher = RC4Decrypt.Decipher(key1=bytearray.fromhex("612a806cac78114ba5013cb531"))
        decrypted_data = decipher.decrypt(data)
        #print("[{}({})]{}".format(origin, port, decrypted_data[4:6]))
        print("[{}({})]{}".format(origin, port, decrypted_data))


def parseHeader(header, port, origin):
        if origin == 'server':
                return
        print("[{}({})]{}".format(origin, port, header))

