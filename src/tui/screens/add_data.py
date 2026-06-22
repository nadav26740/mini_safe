from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Label, Button, Static, Input


from .components.confirm_dialog import ConfirmationDialog

class AddData(Screen):
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
    
    Input {
        margin-bottom: 1;
    }
    
    #title-label {
        text-style: bold;
        text-align: center;
        border: round white;  /* Title enclosed in a border */
        width: 100%;
        margin-bottom: 2;
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
        width: 40%;
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
    def __init__(self) -> None:
        super().__init__()  # Crucial: Initialize the base Screen class
        self.data = "Encrypted..."

    def compose(self) -> ComposeResult:
        with Static(id="view-container"):
            # Title enclosed in a rounded border
            yield Label(f"Add data", id="title-label")

            yield Label("Name:")
            yield Input(password=False, placeholder="Enter name...", id="name-input")

            yield Label("Data:")
            yield Input(password=True, placeholder="Enter secret...", id="data-input")

            # The 4 buttons arranged in a grid structure
            with Static(id="button-grid"):
                yield Button("Set", variant="success", id="btn-set")
                yield Button("Back", variant="error", id="btn-back")
                
            # Feedback notification area
            yield Static("", id="status-bar")

    # Catch button press events
    def on_button_pressed(self, event: Button.Pressed) -> None:
        button_id = event.button.id

        if button_id == "btn-set":
            self.handle_set()

        elif button_id == "btn-back":
            # Returns to the previous screen (ListScreen) on the screen stack
            self.dismiss()

    def handle_set(self):
        status_bar = self.query_one("#status-bar", Static)
        data_input = self.query_one("#data-input", Input).value
        name_input = self.query_one("#name-input", Input).value
        
        if name_input == '':
            status_bar.update("❌ Name missing");
            return

        elif data_input == '':
            status_bar.update("❌ Data missing");
            return

        if self.app.state.actions.insert(name_input, data_input):
            self.app.notify(
                "New Data has been added",
                title="Adding Data",
                severity="information",
                timeout=5
            )
            self.dismiss()
            return
        
        # if failed
        self.app.push_screen(
            ConfirmationDialog("Data already exists\nOverwrite?"),
            callback=self.handle_overwrite
        )
        
        pass
    
    def handle_overwrite(self, confirmed: bool):
        data_input = self.query_one("#data-input", Input).value
        name_input = self.query_one("#name-input", Input).value

        if (confirmed):
            self.app.notify(
                    "Data has been overwriten",
                    title="Adding Data",
                    severity="warning",
                    timeout=5
                )
            self.app.state.actions.insert(name_input, data_input, True)
            self.dismiss()
        
        else:
            self.app.notify(
                "🛡️ Overwrite canceled",
                title="Overwrite Data",
                severity="warning",
                timeout=5)
            
        pass