import RC4Decrypt
from Cryptodome.Cipher import ARC4
import struct

def parsing(data, port, origin):
        if origin == 'server':
                return
        decipher = RC4Decrypt.Decipher(key1=bytearray.fromhex("612a806cac78114ba5013cb531"))
        decrypted_data = decipher.decrypt(data)
        print("[{}({})]{}".format(origin, port, decrypted_data))

        # print the header and ID
        print_header(data)
    
def print_header(data):
        header = struct.unpack("!5s", data[:5])[0]
        id = struct.unpack("!B", data[4:5])[0]
        print("Header:", header)
        print("ID:", id)
