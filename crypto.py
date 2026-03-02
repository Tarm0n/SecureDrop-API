import os, base64
from dotenv import load_dotenv
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

#load var from .env
load_dotenv()

m_b64 = os.getenv("ENCRYPTION_KEY")

MASTER_KEY = base64.b64decode(m_b64)

def encrypt_secret(plain_text: str) -> str:
    p = plain_text.encode("utf-8")

    nonce = os.urandom(12)
    aesgcm = AESGCM(MASTER_KEY)

    cipher_text = aesgcm.encrypt(nonce, p, associated_data=None)
    block = nonce + cipher_text
    return base64.b64encode(block).decode("utf-8")

def decrypt_secret(cipher_text: str) -> str:
    raw = base64.b64decode(cipher_text)

    nonce = raw[:12]
    cipher = raw[12:]

    aesgcm = AESGCM(MASTER_KEY)
    plain_text = aesgcm.decrypt(nonce, cipher, associated_data=None)
    
    return plain_text.decode("utf-8")