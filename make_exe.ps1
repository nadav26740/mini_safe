python -m venv .exe.venv
"%~dp0.exe.venv/Scripts/pip.exe" install -r requirements.txt
"%~dp0.exe.venv/Scripts/pip.exe" install pyinstaller
"%~dp0.exe.venv/Scripts/pyinstaller.exe" --onefile ./src/TUI_main.py
"%~dp0.exe.venv/Scripts/pyinstaller.exe" --onefile ./src/CLI_main.py
