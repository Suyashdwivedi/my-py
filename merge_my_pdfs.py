import tkinter as tk
from tkinter import filedialog, messagebox
from PyPDF2 import PdfMerger  # Use PdfMerger instead of PdfFileMerger

class PDFMergerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF Merger")
        self.root.geometry("500x400")  # Set the initial window size
        self.root.resizable(True, True)  # Allow resizing of the window

        self.file_list = []

        # Create a frame to hold buttons and place it on the left side
        self.button_frame = tk.Frame(root)
        self.button_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

        # Create UI components
        self.label = tk.Label(root, text="Select PDF files to merge:")
        self.label.pack(pady=10)

        self.listbox = tk.Listbox(root, selectmode=tk.MULTIPLE, width=50, height=15)
        self.listbox.pack(pady=10)

        # Create buttons and pack them vertically inside the frame
        self.browse_button = tk.Button(self.button_frame, text="Browse", command=self.browse_files)
        self.browse_button.pack(fill=tk.X, pady=5)

        self.remove_button = tk.Button(self.button_frame, text="Remove Selected", command=self.remove_selected)
        self.remove_button.pack(fill=tk.X, pady=5)

        self.merge_button = tk.Button(self.button_frame, text="Merge PDFs", command=self.save_as)
        self.merge_button.pack(fill=tk.X, pady=5)

        self.close_button = tk.Button(self.button_frame, text="Close", command=root.quit)
        self.close_button.pack(fill=tk.X, pady=5)

    def browse_files(self):
        # Open file dialog to select multiple PDF files
        files = filedialog.askopenfilenames(filetypes=[("PDF files", "*.pdf")])
        for file in files:
            self.listbox.insert(tk.END, file)

    def remove_selected(self):
        # Remove selected files from the listbox
        selected_indices = self.listbox.curselection()
        if not selected_indices:
            messagebox.showwarning("Warning", "No files selected to remove!")
            return

        for index in reversed(selected_indices):
            self.listbox.delete(index)

    def save_as(self):
        # Open a file dialog to choose the output file name and location
        output_file = filedialog.asksaveasfilename(defaultextension=".pdf",
                                                     filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")])
        if not output_file:
            return  # User canceled the save dialog

        self.merge_pdfs(output_file)

    def merge_pdfs(self, output_file):
        # Get selected files from the listbox
        selected_files = self.listbox.curselection()
        if not selected_files:
            messagebox.showwarning("Warning", "No files selected!")
            return

        merger = PdfMerger()  # Use PdfMerger instead of PdfFileMerger
        for index in selected_files:
            file_path = self.listbox.get(index)
            merger.append(file_path)

        # Write out the merged PDF
        merger.write(output_file)
        merger.close()

        messagebox.showinfo("Success", f"Merged PDF saved as: {output_file}")
        self.listbox.delete(0, tk.END)  # Clear the listbox

if __name__ == "__main__":
    root = tk.Tk()
    app = PDFMergerApp(root)
    root.mainloop()
