from .db import DataDB, ROW_DB_PASSWORD_HASH
from .passwordManager import PasswordManager
from .encryptor import Encryptor

class Actions:
    def __init__(self, db: DataDB, password_hasher: PasswordManager):
        self._db = db
        self._password_hasher = password_hasher
        self.encryptor = Encryptor()
        pass


    def __verify_password(self) -> bool:
        if self._db.is_connected() is False:
            raise RuntimeError("Database is not connected.")
        
        """Verify the password against the hash stored in the database."""
        salty_password_hash = self._db.Get_Metadata()[ROW_DB_PASSWORD_HASH]
        
        if salty_password_hash is None:
            raise RuntimeError("Salty password hash not found in database.")
        
        return self._password_hasher.verify_password(bytes.fromhex(salty_password_hash))


    def verify_password(self) -> bool:
        return self.__verify_password()

    def get(self, name: str):
        """Get data by name."""
        if self.__verify_password() is False:
            raise RuntimeError("Password verification failed.")
                
        encrypted_data = self._db.Get_data(name)
        if encrypted_data is None:
            raise RuntimeError(f"No data found for name: {name}")
                
        return self.encryptor.decrypt(self._password_hasher.decryptPassword(), encrypted_data)


    def insert(self, name: str, data: str):
        """Set data by name"""
        if self.__verify_password() is False:
            raise RuntimeError("Password verification failed.")
        
        encrypted_data = self.encryptor.encrypt(self._password_hasher.decryptPassword(), data)
        self._db.Save_data(name, encrypted_data)


    def init_db(self, force: bool = False):
        """Initialize the database with the password hash."""
        if self._db.is_connected() is False:
            raise RuntimeError("Failed to connect to the database after initialization.")
        
        if self._db.verify_tables() and not force:
            raise RuntimeError("Database tables already exist. Use --force to overwrite.")

        self._db.Create_DB(self._password_hasher.salty_hash_password())
        
        if self._db.verify_tables() is False:
            raise RuntimeError("Failed to create database tables.")

    def get_all(self):
        """Get all stored data names."""
        if self.__verify_password() is False:
            raise RuntimeError("Password verification failed.")
        
        return self._db.Get_All_names_in_DB()

    def get_metadata(self):
        """Get database metadata."""
        if self.__verify_password() is False:
            raise RuntimeError("Password verification failed.")
        
        metadata = self._db.Get_Metadata()
        metadata[ROW_DB_PASSWORD_HASH] = "<hidden>"
        return metadata