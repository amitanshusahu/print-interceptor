import time
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import pdfplumber

# Path where Bullzip saves printed PDFs
WATCH_FOLDER = "C:\\PrintedBills"

class PrintJobHandler(FileSystemEventHandler):
    def on_created(self, event):
        """Triggered when a new file is created in the watched folder."""
        if event.is_directory:
            return  # Ignore directories
        if event.src_path.lower().endswith(".pdf"):
            print(f"New print job detected: {event.src_path}")
            extract_and_log_pdf_text(event.src_path)

def extract_and_log_pdf_text(pdf_path):
    """Extracts text from a PDF and logs it."""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            text = "\n".join(page.extract_text() or "" for page in pdf.pages).strip()
            if text:
                print("\n📄 Extracted Text from PDF:\n", text)
            else:
                print("⚠️ No extractable text found in the PDF.")
    except Exception as e:
        print(f"❌ Error extracting text from {pdf_path}: {e}")

def main():
    """Main function to start the watchdog observer."""
    if not os.path.exists(WATCH_FOLDER):
        print(f"❌ Error: The folder '{WATCH_FOLDER}' does not exist.")
        return

    print(f"👀 Watching folder: {WATCH_FOLDER}")
    event_handler = PrintJobHandler()
    observer = Observer()
    observer.schedule(event_handler, WATCH_FOLDER, recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Stopping watcher...")
        observer.stop()
    observer.join()

if __name__ == "__main__":
    main()
