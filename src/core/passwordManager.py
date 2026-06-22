import bcrypt
from cryptography.fernet import Fernet

class PasswordManager:
    def __init__(self, password: bytes):
        self.memkey = Fernet.generate_key()
        self.cipher = Fernet(self.memkey)
        self.password = bytearray(self.cipher.encrypt(password))

    def decryptPassword(self) -> bytes:
        """# PRIVATE METHOD:
        Decrypt a password using Fernet symmetric encryption."""
        if self.password is None:
            raise ValueError("Password is not set.")
        return self.cipher.decrypt(bytes(self.password))

    def salty_hash_password(self) -> bytes:
        """
        Hash a password using bcrypt with a fixed salt and clear the input buffer afterwards.

        Args:
            password: Password as a bytearray.

        Returns:
            bcrypt hash as bytes.
        """
        salt = bcrypt.gensalt(rounds=12)
        password_hash = bcrypt.hashpw(bytes(self.decryptPassword()), salt)        
        return password_hash


    def verify_password(self, salty_password_hash: bytes) -> bool:
        """
        Verify a password against a bcrypt hash and clear the input buffer afterwards.

        Args:
            password: Password as a bytearray.
            password_hash: bcrypt hash to verify against.
        Returns:
            True if the password matches the hash, False otherwise.
        """
        return bcrypt.checkpw(self.decryptPassword(), salty_password_hash)


    def _wipe_password(self) -> None:
        """Clear the password from memory by overwriting the bytearray."""
        for i in range(len(self.password)):
            self.password[i] = 0


    def __del__(self):
        """Destructor to ensure password is wiped from memory when the object is destroyed."""
        self._wipe_password()