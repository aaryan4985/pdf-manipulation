import tkinter as tk
from tkinter import filedialog, messagebox
from pypdf import PdfReader, PdfWriter
import os

def merge_pdfs():
    # Open file dialog to select multiple PDFs
    files = filedialog.askopenfilenames(title="Select PDF files to merge", filetypes=[("PDF files", "*.pdf")])
    if not files:
        messagebox.showwarning("No Files", "No files selected for merging!")
        return
    
    output_file = filedialog.asksaveasfilename(defaultextension=".pdf", title="Save Merged PDF As", filetypes=[("PDF files", "*.pdf")])
    if not output_file:
        messagebox.showwarning("No Output", "No output file selected!")
        return
    
    writer = PdfWriter()
    try:
        for pdf in files:
            reader = PdfReader(pdf)
            for page in reader.pages:
                writer.add_page(page)
        with open(output_file, "wb") as f:
            writer.write(f)
        messagebox.showinfo("Success", f"Merged PDF saved as:\n{output_file}")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to merge PDFs:\n{e}")

def split_pdf():
    # Open file dialog to select a single PDF
    input_file = filedialog.askopenfilename(title="Select PDF file to split", filetypes=[("PDF files", "*.pdf")])
    if not input_file:
        messagebox.showwarning("No File", "No file selected for splitting!")
        return
    
    output_folder = filedialog.askdirectory(title="Select Folder to Save Split Pages")
    if not output_folder:
        messagebox.showwarning("No Folder", "No folder selected for output!")
        return
    
    try:
        reader = PdfReader(input_file)
        for i, page in enumerate(reader.pages):
            writer = PdfWriter()
            writer.add_page(page)
            output_path = os.path.join(output_folder, f"page_{i+1}.pdf")
            with open(output_path, "wb") as output_file:
                writer.write(output_file)
        messagebox.showinfo("Success", f"Split pages saved in folder:\n{output_folder}")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to split PDF:\n{e}")

def main():
    root = tk.Tk()
    root.withdraw()  # Hide the root window

    while True:
        choice = messagebox.askquestion("PDF Merger and Splitter", "Choose an option:\n\nMerge PDFs - Yes\nSplit PDF - No")
        
        if choice == "yes":
            merge_pdfs()
        elif choice == "no":
            split_pdf()
        else:
            break

if __name__ == "__main__":
    main()
