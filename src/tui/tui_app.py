from textual.app import App, ComposeResult
from .state import State
from core import DataDB, Actions
from .screens import PasswordScreen

DB_DEFAULT_PATH = ".temp/mini_cryptodata.db"

class TuiApp(App):
    CSS = """
    Screen {
        align: center middle;
    }
    """
    
    def __init__(self):
        super().__init__()
        self.state = State()

    def on_mount(self) -> None:
        self.state.db = DataDB(DB_DEFAULT_PATH);
        self.state.db.Connect()
        self.push_screen(PasswordScreen())