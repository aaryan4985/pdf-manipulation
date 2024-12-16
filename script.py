import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from pypdf import PdfReader, PdfWriter
import os

class PDFToolApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF Merger and Splitter")
        self.root.geometry("400x300")
        self.root.resizable(False, False)

        # Styling
        self.style = ttk.Style()
        self.style.configure("TButton", font=("Helvetica", 12), padding=10)
        self.style.configure("TLabel", font=("Helvetica", 14), padding=10)

        # Title
        title_label = ttk.Label(root, text="PDF Merger and Splitter", font=("Helvetica", 18, "bold"))
        title_label.pack(pady=20)

        # Buttons
        merge_btn = ttk.Button(root, text="Merge PDFs", command=self.merge_pdfs)
        merge_btn.pack(pady=10)

        split_btn = ttk.Button(root, text="Split PDF", command=self.split_pdf)
        split_btn.pack(pady=10)

        exit_btn = ttk.Button(root, text="Exit", command=root.quit)
        exit_btn.pack(pady=20)

    def merge_pdfs(self):
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

    def split_pdf(self):
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

if __name__ == "__main__":
    root = tk.Tk()
    app = PDFToolApp(root)
    root.mainloop()
