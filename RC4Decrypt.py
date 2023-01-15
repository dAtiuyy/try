from Cryptodome.Cipher import ARC4

class Decipher:
    def __init__(self, key1):
        self.key1 = key1

    def decrypt(self, data):
        rc4 = ARC4.new(self.key1)
        decrypted_data = rc4.decrypt(data[5:])
        return decrypted_data