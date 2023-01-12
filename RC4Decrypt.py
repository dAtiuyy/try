from Cryptodome.Cipher import ARC4

class Decipher:
    def __init__(self, key1, key2):
        self.key1 = key1
        self.key2 = key2

    def decrypt(self, data):
        rc4 = ARC4.new(self.key1)
        decrypted_data = rc4.decrypt(data)
        rc4 = ARC4.new(self.key2)
        decrypted_data = rc4.decrypt(decrypted_data)
        return decrypted_data