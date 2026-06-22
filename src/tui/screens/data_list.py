from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Input, Label, Static, ListView, ListItem, Button

from .data_view import DataView
from .add_data import AddData

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
    
    #password-list {
        border: cyan;
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
    
    #button-grid {
        layout: horizontal;
        grid-size: 4;       /* 2 columns, 2 rows */
        grid-gutter: 1 2;     /* Vertical and horizontal spacing between buttons */
        height: auto;
    }
    
    Button {
        text-align: center;
        background: transparent;      /* Removes the default solid background */
        border: tall #007bff;         /* Blue border outline by default */
        width: 50%;
        height: 3;
    }
    
    Button:focus {
        text-style: bold;
        background: $accent;
        color: $text;
    }
    
    #search-bar {
        width: 50%;
        height: 3;
        margin-bottom: 1;
        background: transparent;
    }
    """

    def compose(self) -> ComposeResult:
        with Static(id="list-container"):
            # Labeled centered title
            yield Label("Secrets", id="screen-title")
            
            # The List View containing our items
            yield Input(placeholder="search..", id="search-bar")
            yield ListView(id="password-list")
            
            # Place to show which item was clicked
            yield Static("", id="action-status")
        
            with Static(id="button-grid"):
                    yield Button("Add", variant="primary", id="btn-add")
                    yield Button("Exit", variant="error", id="btn-exit")
        
        return


    def on_mount(self) -> None:
        # Load initial data when screen first mounts
        self.db_items: list[str] = []
        self.reload_data()
        list_view = self.query_one("#password-list", ListView).focus()
        list_view.border_title = "Secrets"

        return


    # This handles whenever a user presses 'Enter' or clicks a list item
    def on_list_view_selected(self, event: ListView.Selected) -> None:
        # Extract the label text from inside the selected ListItem
        selected_text = getattr(event.item, "name", "Unknown")        
        # Trigger your function
        self.app.push_screen(
            DataView(selected_text),
            callback=self.handle_return)
        return

    # This runs every single time a key is pressed inside the input box
    def on_input_changed(self, event: Input.Changed) -> None:
        if event.control.id == "search-bar":
            self.filter_data(event.value)


    # Catch button press events
    def on_button_pressed(self, event: Button.Pressed) -> None:
        button_id = event.button.id

        if button_id == "btn-add":
            self.app.push_screen(
                AddData(),
                callback=self.handle_return)
            
        elif button_id == "btn-exit":
            self.app.exit()
        return


    # Your custom on-press function
    def handle_item_selection(self, item_name: str) -> None:
        status = self.query_one("#action-status", Static)
        status.update(f"Selected: {item_name}")
        return


    def filter_data(self, filter: str):
        items = [element for element in self.db_items if filter in element]
        self.rerender_list(items)
        return


    def reload_data(self):
        elements = self.app.state.actions.get_all()
        if (elements == self.db_items):
            return

        self.db_items = elements
        self.rerender_list(self.db_items)
        return


    def rerender_list(self, elements):
        if (len(elements) == 0):
            return

        list_view = self.query_one("#password-list", ListView)
        list_view.clear()

        for item in elements:
            item: str
            list_item = ListItem(Label(item), name=item)
            list_view.append(list_item)
        list_view.index = 0        
        return


    def handle_return(self, result=None):
        """reloading the window on returning to it
        """
        self.reload_data();
        return