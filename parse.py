import RC4Decrypt
from Cryptodome.Cipher import ARC4

def parsing(data, port, origin):
        if origin == 'client':
                return
        #print("[{}({})]{}".format(origin, port, int.from_bytes(data, "big")))
        decipher = RC4Decrypt.Decipher(key1=bytearray.fromhex("BA15DE"), key2=bytearray.fromhex("612a806cac78114ba5013cb531"))
        decrypted_data = decipher.decrypt(data)
        print("[{}({})]{}".format(origin, port, decrypted_data))

def parseHeader(header, port, origin):
        if origin == 'server':
                return
        print("[{}({})]{}".format(origin, port, header))

