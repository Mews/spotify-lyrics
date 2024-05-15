:: To build the debug mode exe just remove the "--windowed" option
:: And optionally change the "--name" option to something else
pyinstaller src/main.py --clean --onedir --name spotify-lyrics --windowed --icon assets/icon.ico
pause