import time
import os
import pyperclip  # For copying extracted text to clipboard (optional)
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import pdfplumber  # For extracting text from PDF

# Path where Bullzip saves printed PDFs
WATCH_FOLDER = "C:\\PrintedBills"

class PrintJobHandler(FileSystemEventHandler):
    def on_created(self, event):
        """Triggered when a new file is created in the watched folder."""
        if event.src_path.endswith(".pdf"):
            print(f"New print job detected: {event.src_path}")
            extract_and_log_pdf_text(event.src_path)

def extract_and_log_pdf_text(pdf_path):
    """Extracts text from a PDF and logs it."""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            text = "\n".join(page.extract_text() for page in pdf.pages if page.extract_text())
            print("\n📄 Extracted Text from PDF:\n", text)
            pyperclip.copy(text)  # Optional: Copy extracted text to clipboard
    except Exception as e:
        print(f"❌ Error extracting text from {pdf_path}: {e}")

if __name__ == "__main__":
    print(f"👀 Watching folder: {WATCH_FOLDER}")
    event_handler = PrintJobHandler()
    observer = Observer()
    observer.schedule(event_handler, WATCH_FOLDER, recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
