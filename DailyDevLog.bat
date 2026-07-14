@echo off
cd /d "%~dp0"
call env\Scripts\activate.bat
python -m desktop_ui.main
