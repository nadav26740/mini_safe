from core import PasswordManager, DataDB, Actions

class State:
    """Contain the states for the app
    """
    def __init__(self):
        self.db: DataDB
        self.passManager: PasswordManager
        self.actions: Actions