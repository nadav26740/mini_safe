from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Label, Button, Static, Input


from .components.confirm_dialog import ConfirmationDialog

class ModifyData(Screen):
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
    
    #name-bar {
        text-style: bold;
        border: round white;  /* Title enclosed in a border */
        width: 100%;
        margin-bottom: 1;
    }
    
    Input {
        margin-bottom: 1;
    }
    
    #title-label {
        text-style: bold;
        text-align: center;
        border: round white;  /* Title enclosed in a border */
        width: 100%;
        margin-bottom: 1;
        padding: 0 1;
    }
    
    #data-bar {
        text-style: bold;
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
        width: 80%;
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
    def __init__(self, name) -> None:
        super().__init__()  # Crucial: Initialize the base Screen class
        self.data_name = name

    def compose(self) -> ComposeResult:
        with Static(id="view-container"):
            # Title enclosed in a rounded border
            yield Label(f"Add data", id="title-label")

            # yield Label("Name:")
            yield Label(f" {self.data_name}", id="name-bar")

            yield Label("Data:")
            yield Input(password=True, placeholder="Enter secret...", id="data-input")

            # The 4 buttons arranged in a grid structure
            with Static(id="button-grid"):
                yield Button("Set", variant="success", id="btn-set")
                yield Button("Delete", variant="error", id="btn-delete")
                yield Button("Back", variant="warning", id="btn-back")
                
            # Feedback notification area
            yield Static("", id="status-bar")

    def _on_mount(self) -> None:
        widget = self.query_one("#name-bar", Label)
        widget.border_title = "Name:"

    # Catch button press events
    def on_button_pressed(self, event: Button.Pressed) -> None:
        button_id = event.button.id

        if button_id == "btn-set":
            self.handle_set()

        elif button_id == "btn-back":
            # Returns to the previous screen (ListScreen) on the screen stack
            self.dismiss()
        
        elif button_id == "btn-delete":
            self.app.push_screen(
            ConfirmationDialog("Are you sure\nyou want to delete?"),
            callback=self.handle_delete
            )


    def handle_set(self):
        status_bar = self.query_one("#status-bar", Static)
        data_input = self.query_one("#data-input", Input).value
        
        if data_input == '':
            status_bar.update("❌ Data missing");
            return

        self.app.push_screen(
            ConfirmationDialog("Data already exists\nOverwrite?"),
            callback=self.handle_overwrite
        )
        return

    
    def handle_delete(self, confirmed: bool):
        if (confirmed):
            try:
                self.app.state.actions.delete(self.data_name)
            
            except Exception as err:
                self.app.notify(
                    str(err),
                    title="Modifing Data",
                    severity="error",
                    timeout=5)
                return

            self.app.notify(
                    "🗑️ Data Removed",
                    title="Modifing Data",
                    severity="error",
                    timeout=5
                )
            
            self.dismiss()
            
        else:
            self.app.notify(
                "🛡️ Overwrite canceled",
                title="Overwrite Data",
                severity="warning",
                timeout=5)
        return

    
    def handle_overwrite(self, confirmed: bool):
        data_input = self.query_one("#data-input", Input).value

        if (confirmed):
            self.app.notify(
                    "📝 Data has been overwriten",
                    title="Modifing Data",
                    severity="warning",
                    timeout=5
                )
            self.app.state.actions.insert(self.data_name, data_input, True)
            self.dismiss()
        
        else:
            self.app.notify(
                "🛡️ Overwrite canceled",
                title="Overwrite Data",
                severity="warning",
                timeout=5)
            
        return