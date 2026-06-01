import os
import base64
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM


class Encryptor:
    def _derive_key(self, password: bytes, salt: bytes) -> bytes:
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,              # AES-256 key
            salt=salt,
            iterations=200_000,
        )
        return kdf.derive(password)

    def encrypt(self, password: bytes, data: str) -> str:
        """Encrypting data

        Args:
            password (str): The password to derive the key.
            data (str): The plaintext data to encrypt.

        Returns:
            str: Base64-encoded string containing salt + nonce + ciphertext.
        """
        
        salt = os.urandom(16)
        key = self._derive_key(password, salt)

        aesgcm = AESGCM(key)
        nonce = os.urandom(12)

        ciphertext = aesgcm.encrypt(nonce, data.encode(), None)

        # store: salt + nonce + ciphertext
        result = salt + nonce + ciphertext
        return base64.b64encode(result).decode()

    def decrypt(self, password: bytes, token: str) -> str:
        """Decrypt data using AES-GCM with a key derived from the password.

        Args:
            password (str): The password to derive the key.
            token (str): Base64-encoded string containing salt + nonce + ciphertext.

        Returns:
            str: The decrypted plaintext.
        """
        
        raw = base64.b64decode(token)

        salt = raw[:16]
        nonce = raw[16:28]
        ciphertext = raw[28:]

        key = self._derive_key(password, salt)

        aesgcm = AESGCM(key)
        plaintext = aesgcm.decrypt(nonce, ciphertext, None)

        return plaintext.decode()