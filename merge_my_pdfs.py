gitimport tkinter as tk
from tkinter import filedialog, messagebox
from PyPDF2 import PdfFileMerger

class PDFMergerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF Merger")
        self.root.geometry("400x300")

        self.file_list = []

        # Create UI components
        self.label = tk.Label(root, text="Select PDF files to merge:")
        self.label.pack(pady=10)

        self.listbox = tk.Listbox(root, selectmode=tk.MULTIPLE, width=50, height=10)
        self.listbox.pack(pady=10)

        self.browse_button = tk.Button(root, text="Browse", command=self.browse_files)
        self.browse_button.pack(pady=5)

        self.merge_button = tk.Button(root, text="Merge PDFs", command=self.merge_pdfs)
        self.merge_button.pack(pady=5)

        self.close_button = tk.Button(root, text="Close", command=root.quit)
        self.close_button.pack(pady=5)

    def browse_files(self):
        # Open file dialog to select multiple PDF files
        files = filedialog.askopenfilenames(filetypes=[("PDF files", "*.pdf")])
        for file in files:
            self.listbox.insert(tk.END, file)

    def merge_pdfs(self):
        # Get selected files from the listbox
        selected_files = self.listbox.curselection()
        if not selected_files:
            messagebox.showwarning("Warning", "No files selected!")
            return

        merger = PdfFileMerger()
        for index in selected_files:
            file_path = self.listbox.get(index)
            merger.append(file_path)

        # Write out the merged PDF
        output_file = "merged_all_pages.pdf"
        merger.write(output_file)
        merger.close()

        messagebox.showinfo("Success", f"Merged PDF saved as: {output_file}")
        self.listbox.delete(0, tk.END)  # Clear the listbox

if __name__ == "__main__":
    root = tk.Tk()
    app = PDFMergerApp(root)
    root.mainloop()
