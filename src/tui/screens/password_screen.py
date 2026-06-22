from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Input, Label, Static

from core import PasswordManager, Actions
from .data_list import DataList


class PasswordScreen(Screen):
    CSS = """
    Screen { align: center middle; }    
    #form-container { width: 40; }
    #password-input { margin-bottom: 1; margin-top: 1; }
    #status-message { border: solid red; padding: 0 1; color: red; display: none; }
    """
    
    def compose(self) -> ComposeResult:
        with Static(id="form-container"):
            yield Label("Password:")
            
            yield Input(password=True, placeholder="Enter password...", id="password-input")
                
            yield Static("", id="status-message")
            
    # This function is automatically called when Enter is pressed in ANY input
    def on_input_submitted(self, event: Input.Submitted) -> None:
        # Check if the event came from our password input field
        if event.control.id == "password-input":
            password_entered = event.value
            self.process_password(password_entered)

    # This runs every single time a key is pressed inside the input box
    def on_input_changed(self, event: Input.Changed) -> None:
        if event.control.id == "password-input":
            # 1. Get the raw keystroke sequence text 
            current_value = event.value
            message_widget = self.query_one("#status-message", Static)
            
            if current_value:
                last_char = current_value[-1]
                
                if last_char.isalpha() and last_char.isupper():
                    message_widget.update("🔒 Caps Lock on")
                    message_widget.styles.border = ("solid", "cyan")
                    message_widget.styles.color = "cyan"
                    message_widget.styles.display = "block"
                    message_widget.styles.text_style = "bold"


                elif last_char.isalpha() and last_char.islower():
                    message_widget.styles.display = "none"
            else:
                message_widget.styles.display = "none"

    # Your custom function to process the password
    def process_password(self, password: str) -> None:
        message_widget = self.query_one("#status-message", Static)
        
        # Simple validation example
        
        self.app.state.passManager = PasswordManager(password.encode('utf-8'))
        self.app.state.actions = Actions(self.app.state.db, self.app.state.passManager)

        if self.app.state.actions.verify_password():
            self.app.notify("✅ Correct Password!")
            # message_widget.styles.border = ("solid", "green")
            # message_widget.styles.color = "green"
            self.app.push_screen(DataList())
        
        else:
            message_widget.update("❌ Wrong Password!")
            message_widget.styles.border = ("solid", "red")
            message_widget.styles.color = "red"
            
        # Make the message visible now that it has content
        message_widget.styles.display = "block"