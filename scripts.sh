

pyinstaller --onefile --add-binary "/usr/lib/x86_64-linux-gnu/libpython3.12.so:." main.py

# install
pip install watchdog pdfplumber pyperclip