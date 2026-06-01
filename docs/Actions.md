# Actions.py Documentation

## Overview

The `Actions` class serves as the main orchestrator for all core operations in the mini_safe cryptographic data storage system. It provides a high-level interface for encrypting, decrypting, and managing sensitive data while handling password verification and database interactions.

## Location

`src/core/actions.py`

## Class: Actions

### Purpose

The `Actions` class coordinates three core components:
- **Database Management** (`DataDB`) - Handles data persistence
- **Password Handling** (`PasswordManager`) - Manages password hashing and decryption
- **Encryption/Decryption** (`Encryptor`) - Handles cryptographic operations

---

## Constructor

### `__init__(self, db: DataDB, password_hasher: PasswordManager)`

Initializes the Actions instance with required dependencies.

**Parameters:**
- `db: DataDB` - Database instance for storing and retrieving encrypted data
- `password_hasher: PasswordManager` - Password manager for handling hash verification and password decryption

**Attributes:**
- `self._db` - Stores the database instance (private)
- `self._password_hasher` - Stores the password hasher instance (private)
- `self.encryptor` - Creates and stores an Encryptor instance for encryption/decryption operations

**Example:**
```python
from src.core.db import DataDB
from src.core.passwordManager import PasswordManager
from src.core.actions import Actions

db = DataDB()
password_hasher = PasswordManager()
actions = Actions(db, password_hasher)
```

---

## Private Methods

### `__verify_password(self) -> bool`

Verifies the user's password against the stored hash in the database. This is a security check performed before any data access operation.

**Returns:**
- `bool` - True if password verification succeeds

**Raises:**
- `RuntimeError` - If database is not connected
- `RuntimeError` - If password hash is not found in database
- `RuntimeError` - If password verification fails

**Security Note:** This method is private (name mangled with `__`) to prevent accidental external calls and ensure password verification happens through the public methods only.

**Logic:**
1. Checks if database is connected
2. Retrieves the stored password hash from database metadata
3. Verifies the current password against the stored hash
4. Returns verification result

---

## Public Methods

### `get(self, name: str) -> str`

Retrieves and decrypts data stored under the given name.

**Parameters:**
- `name: str` - The identifier/key for the stored data

**Returns:**
- `str` - The decrypted data

**Raises:**
- `RuntimeError` - If password verification fails
- `RuntimeError` - If no data exists for the given name

**Process:**
1. Verifies password
2. Retrieves encrypted data from database
3. Decrypts data using password
4. Returns decrypted data

**Example:**
```python
secret = actions.get("api_key")
print(secret)  # Prints the decrypted API key
```

---

### `insert(self, name: str, data: str) -> None`

Encrypts and stores data under the given name.

**Parameters:**
- `name: str` - The identifier/key for storing the data
- `data: str` - The sensitive data to encrypt and store

**Raises:**
- `RuntimeError` - If password verification fails

**Process:**
1. Verifies password
2. Encrypts data using password
3. Saves encrypted data to database

**Example:**
```python
actions.insert("api_key", "sk-1234567890abcdef")
actions.insert("password", "MySecurePassword123!")
```

---

### `init_db(self, force: bool = False) -> None`

Initializes the database by creating tables and storing the password hash.

**Parameters:**
- `force: bool` - If True, overwrites existing database tables. Default: False

**Raises:**
- `RuntimeError` - If database is not connected
- `RuntimeError` - If tables already exist and force is False
- `RuntimeError` - If database table creation fails

**Process:**
1. Checks database connection
2. Verifies if tables already exist
3. Creates database tables with password hash
4. Validates table creation

**Important:** This should be called once during initial setup. Using `force=True` will delete all existing data.

**Example:**
```python
# First time setup
actions.init_db()

# Reinitialize (destructive)
actions.init_db(force=True)
```

---

### `get_all(self) -> list`

Retrieves all stored data names/keys in the database.

**Returns:**
- `list` - List of all stored data identifiers

**Raises:**
- `RuntimeError` - If password verification fails

**Use Case:** Useful for listing all stored secrets or getting an inventory of what's stored.

**Example:**
```python
all_keys = actions.get_all()
print(all_keys)  # ['api_key', 'password', 'ssh_key']
```

---

### `get_metadata(self) -> dict`

Retrieves database metadata while hiding the password hash for security.

**Returns:**
- `dict` - Database metadata with password hash replaced with `<hidden>`

**Raises:**
- `RuntimeError` - If password verification fails

**Security Feature:** The password hash is automatically masked in the returned metadata to prevent accidental exposure.

**Example:**
```python
metadata = actions.get_metadata()
print(metadata)
# Output might include creation date, modification date, etc.
# But password hash will show as "<hidden>"
```

---

## Dependencies

### Imported Modules

1. **DataDB** - From `src.core.db`
   - Handles database operations (Create, Read, Update)
   - Stores encrypted data and metadata

2. **PasswordManager** - From `src.core.passwordManager`
   - Hashes passwords with salt
   - Verifies passwords
   - Manages encrypted password storage

3. **Encryptor** - From `src.core.encryptor`
   - Encrypts data
   - Decrypts data
   - Uses cryptographic algorithms

4. **ROW_DB_PASSWORD_HASH** - Constant from `src.core.db`
   - Defines the database column/key for password hash metadata

---

## Error Handling

The Actions class implements comprehensive error handling:

| Error Type | Scenario | Recovery |
|-----------|----------|----------|
| `RuntimeError` (DB not connected) | Database connection lost | Reconnect to database |
| `RuntimeError` (Password verification failed) | Wrong password or tampered data | Verify correct password |
| `RuntimeError` (Data not found) | Requested key doesn't exist | Check key name or create new entry |
| `RuntimeError` (Hash not found) | Corrupted database metadata | Reinitialize database with `force=True` |
| `RuntimeError` (Tables exist) | Attempting to re-initialize | Use `force=True` or connect to existing DB |

---

## Usage Example

### Complete Workflow

```python
from src.core.db import DataDB
from src.core.passwordManager import PasswordManager
from src.core.actions import Actions

# Initialize components
db = DataDB("safe.db")
password_hasher = PasswordManager("my_secure_password")
actions = Actions(db, password_hasher)

# First time: Initialize database
actions.init_db()

# Store secrets
actions.insert("github_token", "ghp_xxxxxxxxxxxxxxxxxxxxx")
actions.insert("api_key", "sk_live_xxxxx")

# Retrieve secrets
github_token = actions.get("github_token")
print(f"GitHub Token: {github_token}")

# List all stored secrets
all_keys = actions.get_all()
print(f"Stored secrets: {all_keys}")

# Get metadata
metadata = actions.get_metadata()
print(f"DB Info: {metadata}")
```

---

## Security Considerations

1. **Password Verification** - Every data access operation requires password verification
2. **Password Hiding** - Password hashes are never exposed in metadata
3. **Encryption** - All stored data is encrypted before persistence
4. **Private Methods** - Internal methods are marked private to prevent misuse
5. **Database Connection Check** - Operations verify database connectivity before execution

---

## Design Patterns

- **Dependency Injection** - Dependencies passed via constructor for flexibility
- **Encapsulation** - Private methods hide implementation details
- **Composition** - Uses composition to leverage specialized classes
- **Error-First** - Early validation and error checking
- **Security-First** - Password verification before all data operations

---

## Related Files

- `src/core/db.py` - Database management
- `src/core/passwordManager.py` - Password hashing and management
- `src/core/encryptor.py` - Encryption/decryption operations
- `src/CLI_Main.py` - Command-line interface that uses Actions

---

## Future Enhancements

- Add batch operations for efficiency
- Implement data versioning/history
- Add search functionality for stored data
- Implement encryption key rotation
- Add audit logging for access attempts
