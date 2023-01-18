import RC4Decrypt
from Cryptodome.Cipher import ARC4
import struct

def parsing(data, port, origin):
        if origin == 'server':
                return
        decipher = RC4Decrypt.Decipher(key1=bytearray.fromhex("612a806cac78114ba5013cb531"))
        decrypted_data = decipher.decrypt(data)
        #print("[{}({})]{}".format(origin, port, decrypted_data))

        # print the header, length and ID
        print_header(data)
    
def print_header(data):
        header = struct.unpack("!5s", data[:5])[0]
        id = struct.unpack("!B", data[4:5])[0]
        length = struct.unpack("!i", data[:4])[0]
        #"""
        id_to_name = {9: 'Hello', 91: 'UPDATEACK', 16: 'MOVE', 64: 'PONG', 112: 'QUEUEPONG', 66: 'PLAYERSHOOT', 1: 'USEITEM', 25: 'INVSWAP', 26: 'LOAD', 47: 'PLAYERTEXT', 174: 'POTIONSTORAGEINTERACTION', 35: 'SHOOTACK', 57: 'OTHERHIT', 79: 'GOTOACK', 19: 'ENEMYHIT', 77: 'AOEACK', 45: 'TELEPORT', 6: 'USEPORTAL', 98: 'GROUNDDAMAGE', 13: 'SQUAREHIT', 12: 'CREATE', 18: 'INVDROP', 60: 'SETCONDITION', 93: 'BUY', 178: 'GROUNDTELEPORTER', 0: 'FAILURE', 161: 'UNBOXREQUEST'}
        if id in id_to_name:
                print(id_to_name[id],'ID =' , id, 'Length =' , length)
        #"""
        if id not in {1, 9, 91, 112, 25, 16, 66, 26, 64, 47, 174, 79, 35, 19, 57, 45, 98, 6, 77, 13, 12, 18, 60, 93, 178, 0, 161}:
                print('UNKNOWN', id, header, length)
