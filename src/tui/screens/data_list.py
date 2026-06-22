from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Input, Label, Static, ListView, ListItem

from .data_view import DataView

from core import PasswordManager, Actions

class DataList(Screen):
    # 1. The List Screen pulls data from the app's database
    # CSS to center the entire container and style the list + title
    CSS = """
    ListScreen {
        align: center middle;
    }
    
    #list-container {
        width: 44;
        height: auto;
    }
    
    #screen-title {
        text-style: bold;
        text-align: center;  /* Centers the text horizontally */
        margin-bottom: 1;
        background: $accent;
        color: $text;
        padding: 0 1;
    }

    ListView {
        border: heavy blue;
        height: auto;
        max-height: 10;
    }
    
    #action-status {
        margin-top: 1;
        text-align: center;
        color: $accent;
    }
    """

    def compose(self) -> ComposeResult:
        db_items = self.app.state.actions.get_all()
        
        with Static(id="list-container"):
            # Labeled centered title
            yield Label("Passwords", id="screen-title")
            
            # The List View containing our items
            with ListView(id="password-list"):
                for item in db_items:
                    item: str
                    yield ListItem(Label(item.capitalize()), id=item)
            
            # Place to show which item was clicked
            yield Static("", id="action-status")

    # This handles whenever a user presses 'Enter' or clicks a list item
    def on_list_view_selected(self, event: ListView.Selected) -> None:
        # Extract the label text from inside the selected ListItem
        selected_text = getattr(event.item, "id", "Unknown")        
        # Trigger your function
        self.app.push_screen(DataView(selected_text))

    # Your custom on-press function
    def handle_item_selection(self, item_name: str) -> None:
        status = self.query_one("#action-status", Static)
        status.update(f"Selected: {item_name}")