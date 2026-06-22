from textual.app import App, ComposeResult
from textual.screen import ModalScreen
from textual.screen import Screen
from textual.widgets import Label, Button, Static

# 1. Define your reusable Yes/No Modal Dialog Screen
class ConfirmationDialog(ModalScreen[bool]):
    CSS = """
    ConfirmationDialog {
        align: center middle;
        background: rgba(0, 0, 0, 0.5); /* Dim the background application */
    }

    #dialog-box {
        padding: 1 2;
        background: $surface;
        border: thick $primary;
        width: 40;
        height: auto;
    }

    #dialog-message {
        text-align: center;
        margin-bottom: 1;
    }

    #dialog-buttons {
        layout: grid;
        grid-size: 2; /* 2 columns for Yes and No side-by-side */
        grid-gutter: 2;
    }
    
    Button {
        background: transparent;
        width: 40%;
    }
    
    Button.yes {
        border: tall green;
    }
    
    Button.no {
        border: tall red;
    }
    
    Button:focus {
        text-style: bold;
        background: $accent;
        color: $text;
    }
    """

    def __init__(self, message: str) -> None:
        super().__init__()
        self.message = message

    def compose(self) -> ComposeResult:
        with Static(id="dialog-box"):
            yield Label(self.message, id="dialog-message")
            with Static(id="dialog-buttons"):
                yield Button("Yes", variant="success", id="yes")
                yield Button("No", variant="error", id="no")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "yes":
            # Dismiss the modal and return True
            self.dismiss(True)

        else:
            # Dismiss the modal and return False
            self.dismiss(False)