import time
import os
import fitz  # PyMuPDF for extracting text
import tkinter as tk
from tkinter import scrolledtext
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import platform

# Change to the folder where PDFs are saved
if platform.system() == "Windows":
    PDF_DIR = r"C:\Bills"  # Windows path
else:
    PDF_DIR = "/home/amitanshu/Bills"  # Linux path

def extract_text_from_pdf(pdf_path):
    """Extract text from a PDF file."""
    doc = fitz.open(pdf_path)
    text = "\n".join(page.get_text() for page in doc)
    return text

def show_bill_popup(bill_text):
    root = tk.Tk()
    root.title("Nexus Print Interceptor - Bill Details")
    
    # Set window size and position (center of screen)
    window_width, window_height = 500, 400
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width // 2) - (window_width // 2)
    y = (screen_height // 2) - (window_height // 2)
    root.geometry(f"{window_width}x{window_height}+{x}+{y}")

    tk.Label(root, text="Nexus Print Interceptor", font=("Arial", 12, "bold")).pack(pady=10)
    tk.Label(root, text="Extracted Bill Details:", font=("Arial", 12, "bold")).pack(pady=10)
    
    text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=60, height=15, font=("Arial", 10))
    text_area.insert(tk.END, bill_text)
    text_area.config(state=tk.DISABLED)
    text_area.pack(padx=10, pady=5)

    tk.Button(root, text="Want to save in db ? OK", command=root.destroy, font=("Arial", 12)).pack(pady=10)

    root.mainloop()

class PDFHandler(FileSystemEventHandler):
    """Handles new PDFs in the directory."""
    def on_created(self, event):
        if event.src_path.endswith(".pdf"):
            time.sleep(2)  # Ensure the file is fully written
            print(f"New bill detected: {event.src_path}")
            extracted_text = extract_text_from_pdf(event.src_path)
            print("\n--- Extracted Bill Details ---\n")
            print(extracted_text)
            print("\n-------------------------------\n")

            # Show bill details in a popup window
            show_bill_popup(extracted_text)

def monitor_folder():
    """Monitors the folder for new print files."""
    event_handler = PDFHandler()
    observer = Observer()
    observer.schedule(event_handler, PDF_DIR, recursive=False)
    observer.start()
    print(f"Monitoring {PDF_DIR} for new bills...")

    try:
        while True:
            time.sleep(5)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

monitor_folder()
