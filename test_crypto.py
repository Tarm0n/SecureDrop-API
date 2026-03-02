import os
from crypto import encrypt_secret, decrypt_secret

def test():
    password = "password123+"

    encrypted = encrypt_secret(password)
    decrypted = decrypt_secret(encrypted)

    assert password != encrypted
    assert password == decrypted