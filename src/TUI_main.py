from tui import TuiApp
from pathlib import Path

# Automatically finds the cross-platform home directory
default_dir = Path.home()
DB_DEFAULT_PATH = default_dir / ".mini_dataSafe.db"

def main():
    app = TuiApp(DB_DEFAULT_PATH)
    app.run()

if __name__ == "__main__":
    main()