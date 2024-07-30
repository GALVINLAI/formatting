@echo off
pyinstaller --onefile --noconsole --name formatting --icon=icon.ico --distpath .\ main.py
