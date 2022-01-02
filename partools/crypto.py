from cryptography.fernet import Fernet

KEY = b'2vNUuLo_mGMr6oobUmW04HZPTmxsSNTczu2xHsx1cq8='


def encrypt(message):
    fernet = Fernet(KEY)
    encMessage = fernet.encrypt(message.encode())
    print(f"ENCRYPTED[{encMessage.decode()}]")


def gen_key():
    key = Fernet.generate_key()
    print(key)


if __name__ == "__main__":
    encrypt('my_password')
    # gen_key()
