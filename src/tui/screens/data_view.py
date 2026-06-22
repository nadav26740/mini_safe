from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Label, Button, Static
from .modify_data import ModifyData
import pyperclip

class DataView(Screen):
    # Styling for a clean, centered box layout with a grid for buttons
    CSS = """
    DataView {
        align: center middle;
    }
    
    #view-container {
        width: 50;
        height: auto;
        padding: 1;
    }
    
    #title-label {
        text-style: bold;
        text-align: center;
        border: round white;  /* Title enclosed in a border */
        width: 100%;
        margin-bottom: 0;
        padding: 0 1;
    }
    
    #data-bar {
        text-style: bold;
        border: round white;  /* Title enclosed in a border */
        width: 100%;
        margin-bottom: 2;
        padding: 0 1;
    }

    #button-grid {
        layout: grid;
        grid-size: 4;       /* 2 columns, 2 rows */
        height: auto;
    }

    Button {
        text-align: center;
        background: transparent;      /* Removes the default solid background */
        border: tall #007bff;         /* Blue border outline by default */
        width: 100%;
        height: 4;
    }
    
    Button:focus {
        text-style: bold;
        background: $accent;
        color: $text;
    }
    
    #status-bar {
        margin-top: 2;
        text-align: center;
        color: $accent;
    }
    """

    # 1. Accept data_name in the constructor
    def __init__(self, data_name: str) -> None:
        super().__init__()  # Crucial: Initialize the base Screen class
        self.data_name = data_name
        self.data = "🔐 Secret"

    def compose(self) -> ComposeResult:
        with Static(id="view-container"):
            # Title enclosed in a rounded border
            yield Label(f"{self.data_name}", id="title-label")
            yield Label(f"{self.data}", id="data-bar")
            
            # The 4 buttons arranged in a grid structure
            with Static(id="button-grid"):
                yield Button("Decrypt", variant="primary", id="btn-decrypt")
                yield Button("Copy to clipboard", variant="default", id="btn-copy")
                yield Button("Modify", variant="success", id="btn-set")
                yield Button("Back", variant="error", id="btn-back")
                
            # Feedback notification area
            yield Static("", id="status-bar")

    # Catch button press events
    def on_button_pressed(self, event: Button.Pressed) -> None:
        status_bar = self.query_one("#status-bar", Static)
        data_bar = self.query_one("#data-bar", Static)
        button_id = event.button.id

        if button_id == "btn-decrypt":
            data_bar.update(self.app.state.actions.get(self.data_name))
            status_bar.update("🔓 Data decrypted successfully!")
            
        elif button_id == "btn-copy":
            # Textual's built-in clipboard copying utility
            pyperclip.copy(self.app.state.actions.get(self.data_name))
            
            status_bar.update("📋 Copied to system clipboard!")
            
        elif button_id == "btn-set":
            self.app.push_screen(ModifyData(self.data_name), callback=self.handle_return)
            
        elif button_id == "btn-back":
            # Returns to the previous screen (ListScreen) on the screen stack
            self.dismiss()

    def handle_return(self, result=None):
        self.dismiss()
