from cryptography.fernet import Fernet

file = open('key.key', 'rb')
key = file.read()
file.close()


def encryption(filename):
    f = open(filename, 'rb')
    data = f.read()
    f.close()
    fernet = Fernet(key)
    encrypted = fernet.encrypt(data)

    f = open(filename, 'wb')
    f.write(encrypted)
    f.close()


def decryption(filename):
    f = open(filename, 'rb')
    data = f.read()
    f.close()
    fernet = Fernet(key)
    decrypted = fernet.decrypt(data)

    f = open(filename, 'wb')
    f.write(decrypted)
    f.close()
