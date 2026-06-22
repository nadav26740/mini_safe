from textual.app import App, ComposeResult
from .state import State
from core import DataDB, Actions
from .screens import PasswordScreen


class TuiApp(App):
    CSS = """
    Screen {
        align: center middle;
    }
    """

    def __init__(self, db_path):
        super().__init__()
        self.state = State()
        self.state.db = DataDB(db_path)

    def on_mount(self) -> None:
        self.state.db.Connect()
        if not self.state.db.verify_tables():
            pass
            self.app.notify(
                "PLS run cli with --init to initilize db",
                title="DB missing",
                severity="error",
                timeout=15,
            )
        else:
            self.push_screen(PasswordScreen())
