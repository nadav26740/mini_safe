from tui import TuiApp

DB_DEFAULT_PATH = ".temp/mini_cryptodata.db"


if __name__ == "__main__":
    app = TuiApp(DB_DEFAULT_PATH)
    app.run()