from cryptography.fernet import Fernet
key = Fernet.generate_key()

file = open('password.key', 'wb')
file.write(key)
file.close
