import tkinter as tk
from tkinter import filedialog, messagebox
from PyPDF2 import PdfMerger
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import io
import os
import tempfile

class PDFMergerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF & Image Merger")
        self.root.geometry("700x500")
        self.root.resizable(True, True)
        
        # Set color scheme
        self.bg_color = "#f0f0f0"
        self.accent_color = "#4CAF50"
        self.button_color = "#2196F3"
        self.root.configure(bg=self.bg_color)

        # Store file paths separately from display names
        self.file_paths = []

        # Create main container
        main_container = tk.Frame(root, bg=self.bg_color)
        main_container.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)

        # Title label
        title_label = tk.Label(
            main_container, 
            text="PDF & Image Merger", 
            font=("Arial", 18, "bold"),
            bg=self.bg_color,
            fg="#333333"
        )
        title_label.pack(pady=(0, 10))

        # Subtitle
        subtitle_label = tk.Label(
            main_container,
            text="Merge PDF files and images (JPG, PNG, GIF) into a single PDF",
            font=("Arial", 10),
            bg=self.bg_color,
            fg="#666666"
        )
        subtitle_label.pack(pady=(0, 15))

        # Create frame for listbox and scrollbar
        list_frame = tk.Frame(main_container, bg=self.bg_color)
        list_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15))

        # Scrollbar
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Listbox with custom styling
        self.listbox = tk.Listbox(
            list_frame,
            selectmode=tk.MULTIPLE,
            font=("Arial", 10),
            bg="white",
            fg="#333333",
            selectbackground=self.accent_color,
            selectforeground="white",
            yscrollcommand=scrollbar.set,
            relief=tk.FLAT,
            borderwidth=2,
            highlightthickness=1,
            highlightbackground="#cccccc"
        )
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.listbox.yview)

        # Button frame
        button_frame = tk.Frame(main_container, bg=self.bg_color)
        button_frame.pack(fill=tk.X)

        # Create styled buttons
        button_style = {
            "font": ("Arial", 10, "bold"),
            "relief": tk.FLAT,
            "cursor": "hand2",
            "borderwidth": 0,
            "pady": 10
        }

        self.add_button = tk.Button(
            button_frame,
            text="➕ Add Files",
            command=self.browse_files,
            bg=self.accent_color,
            fg="white",
            activebackground="#45a049",
            activeforeground="white",
            **button_style
        )
        self.add_button.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))

        self.remove_button = tk.Button(
            button_frame,
            text="🗑️ Remove Selected",
            command=self.remove_selected,
            bg="#FF9800",
            fg="white",
            activebackground="#e68900",
            activeforeground="white",
            **button_style
        )
        self.remove_button.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

        self.clear_button = tk.Button(
            button_frame,
            text="✖️ Clear All",
            command=self.clear_all,
            bg="#F44336",
            fg="white",
            activebackground="#da190b",
            activeforeground="white",
            **button_style
        )
        self.clear_button.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

        self.merge_button = tk.Button(
            button_frame,
            text="📄 Merge & Save",
            command=self.save_as,
            bg=self.button_color,
            fg="white",
            activebackground="#0b7dda",
            activeforeground="white",
            **button_style
        )
        self.merge_button.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 0))

        # Options frame
        options_frame = tk.Frame(main_container, bg=self.bg_color)
        options_frame.pack(fill=tk.X, pady=(10, 0))

        # Compression checkbox
        self.compress_var = tk.BooleanVar(value=True)
        self.compress_check = tk.Checkbutton(
            options_frame,
            text="📦 Compress images for A4 print quality (reduces file size)",
            variable=self.compress_var,
            font=("Arial", 9),
            bg=self.bg_color,
            fg="#333333",
            selectcolor=self.bg_color,
            activebackground=self.bg_color
        )
        self.compress_check.pack(anchor=tk.W, pady=(0, 5))

        # Image width selection frame
        width_frame = tk.Frame(options_frame, bg=self.bg_color)
        width_frame.pack(fill=tk.X, pady=(0, 5))

        width_label = tk.Label(
            width_frame,
            text="📏 Image width:",
            font=("Arial", 9),
            bg=self.bg_color,
            fg="#333333"
        )
        width_label.pack(side=tk.LEFT, padx=(0, 10))

        # Width dropdown
        self.width_var = tk.StringVar(value="Fit to Page")
        width_options = [
            "Fit to Page",
            "Half Size of Page",
            "Quarter Size",
            "Custom Width"
        ]
        self.width_dropdown = tk.OptionMenu(
            width_frame,
            self.width_var,
            *width_options,
            command=self.on_width_change
        )
        self.width_dropdown.config(
            font=("Arial", 9),
            bg="white",
            fg="#333333",
            relief=tk.FLAT,
            highlightthickness=1
        )
        self.width_dropdown.pack(side=tk.LEFT)

        # Custom width entry (initially hidden)
        self.custom_width_frame = tk.Frame(width_frame, bg=self.bg_color)
        self.custom_width_frame.pack(side=tk.LEFT, padx=(10, 0))

        self.custom_width_entry = tk.Entry(
            self.custom_width_frame,
            width=8,
            font=("Arial", 9)
        )
        self.custom_width_entry.pack(side=tk.LEFT, padx=(0, 5))

        custom_width_label = tk.Label(
            self.custom_width_frame,
            text="mm",
            font=("Arial", 9),
            bg=self.bg_color,
            fg="#666666"
        )
        custom_width_label.pack(side=tk.LEFT)

        # Hide custom width initially
        self.custom_width_frame.pack_forget()

        # Status label at the bottom
        self.status_label = tk.Label(
            main_container,
            text="Ready to merge files",
            font=("Arial", 9),
            bg=self.bg_color,
            fg="#666666"
        )
        self.status_label.pack(pady=(10, 5))

        # Credit line with hyperlink
        credit_frame = tk.Frame(main_container, bg=self.bg_color)
        credit_frame.pack(pady=(0, 5))

        credit_label = tk.Label(
            credit_frame,
            text="Created by ",
            font=("Arial", 8),
            bg=self.bg_color,
            fg="#999999"
        )
        credit_label.pack(side=tk.LEFT)

        # Hyperlinked name
        self.link_label = tk.Label(
            credit_frame,
            text="Suyash Dwivedi",
            font=("Arial", 8, "underline"),
            bg=self.bg_color,
            fg="#2196F3",
            cursor="hand2"
        )
        self.link_label.pack(side=tk.LEFT)
        self.link_label.bind("<Button-1>", lambda e: self.open_link("https://meta.wikimedia.org/wiki/User:Suyash.dwivedi"))

    def open_link(self, url):
        """Open URL in default web browser"""
        import webbrowser
        webbrowser.open(url)

    def on_width_change(self, selection):
        """Show/hide custom width entry based on selection"""
        if selection == "Custom Width":
            self.custom_width_frame.pack(side=tk.LEFT, padx=(10, 0))
        else:
            self.custom_width_frame.pack_forget()

    def browse_files(self):
        """Open file dialog to select PDF and image files"""
        files = filedialog.askopenfilenames(
            title="Select PDF or Image files",
            filetypes=[
                ("All supported", "*.pdf *.jpg *.jpeg *.png *.gif"),
                ("PDF files", "*.pdf"),
                ("Image files", "*.jpg *.jpeg *.png *.gif"),
                ("All files", "*.*")
            ]
        )
        
        for file in files:
            # Store the full file path
            self.file_paths.append(file)
            
            file_name = os.path.basename(file)
            file_ext = os.path.splitext(file)[1].lower()
            
            # Add file type indicator
            if file_ext == '.pdf':
                display_name = f"📄 {file_name}"
            else:
                display_name = f"🖼️ {file_name}"
            
            self.listbox.insert(tk.END, display_name)
            
        self.update_status(f"Added {len(files)} file(s) - Total: {len(self.file_paths)} file(s)")

    def remove_selected(self):
        """Remove selected files from the listbox"""
        selected_indices = self.listbox.curselection()
        if not selected_indices:
            messagebox.showwarning("Warning", "No files selected to remove!")
            return

        count = len(selected_indices)
        # Remove in reverse order to maintain correct indices
        for index in reversed(selected_indices):
            self.listbox.delete(index)
            del self.file_paths[index]
        
        self.update_status(f"Removed {count} file(s) - Total: {len(self.file_paths)} file(s)")

    def clear_all(self):
        """Clear all files from the listbox"""
        if self.listbox.size() == 0:
            return
        
        result = messagebox.askyesno("Confirm", "Clear all files from the list?")
        if result:
            self.listbox.delete(0, tk.END)
            self.file_paths = []
            self.update_status("List cleared")

    def update_status(self, message):
        """Update the status label"""
        self.status_label.config(text=message)
        self.root.update_idletasks()

    def image_to_pdf(self, image_path):
        """Convert an image to PDF with proper sizing and centering"""
        # Create a temporary PDF in memory
        packet = io.BytesIO()
        
        # Open the image
        img = Image.open(image_path)
        
        # Apply compression if enabled
        if self.compress_var.get():
            # Calculate optimal size for printing at 150 DPI (good quality)
            # A4 at 150 DPI = 1240 x 1754 pixels
            max_print_width = 1240
            max_print_height = 1754
            
            # Resize if image is larger than print size
            if img.width > max_print_width or img.height > max_print_height:
                img.thumbnail((max_print_width, max_print_height), Image.Resampling.LANCZOS)
        
        # Convert RGBA to RGB if necessary
        if img.mode == 'RGBA':
            background = Image.new('RGB', img.size, (255, 255, 255))
            background.paste(img, mask=img.split()[3])
            img = background
        elif img.mode != 'RGB':
            img = img.convert('RGB')
        
        # Save compressed image to temporary file if compression is enabled
        if self.compress_var.get():
            temp_img_path = tempfile.NamedTemporaryFile(delete=False, suffix='.jpg').name
            img.save(temp_img_path, 'JPEG', quality=90, optimize=True)
            image_to_use = temp_img_path
        else:
            image_to_use = image_path
        
        # Get image dimensions (after potential compression)
        img_width, img_height = img.size
        
        # Use A4 size as default page size (210mm x 297mm)
        from reportlab.lib.units import mm
        page_width = 210 * mm
        page_height = 297 * mm
        
        # Add margins (10mm on each side)
        margin = 10 * mm
        usable_width = page_width - (2 * margin)
        usable_height = page_height - (2 * margin)
        
        # Determine target width based on selection
        width_option = self.width_var.get()
        
        if width_option == "Half Size of Page":
            target_width = usable_width / 2
        elif width_option == "Quarter Size":
            target_width = usable_width / 4
        elif width_option == "Custom Width":
            try:
                custom_mm = float(self.custom_width_entry.get())
                target_width = custom_mm * mm
            except:
                target_width = usable_width  # Fallback to full width
        else:  # Fit to Page
            target_width = usable_width
        
        # Calculate scaling
        if width_option == "Fit to Page":
            # Fit to width or height, whichever is limiting
            scale = min(usable_width / img_width, usable_height / img_height)
        else:
            # Fit to specified width, maintaining aspect ratio
            scale = target_width / img_width
            # But ensure it doesn't exceed page height
            if (img_height * scale) > usable_height:
                scale = usable_height / img_height
        
        # Don't scale up images, only scale down if necessary
        if scale > 1:
            scale = 1
        
        new_width = img_width * scale
        new_height = img_height * scale
        
        # Calculate position to center the image
        x_offset = (page_width - new_width) / 2
        y_offset = (page_height - new_height) / 2
        
        # Create PDF with reportlab
        c = canvas.Canvas(packet, pagesize=(page_width, page_height))
        
        # Draw the image centered on the page
        c.drawImage(
            image_to_use,
            x_offset,
            y_offset,
            width=new_width,
            height=new_height,
            preserveAspectRatio=True
        )
        
        c.save()
        
        # Clean up temporary compressed image if created
        if self.compress_var.get() and image_to_use != image_path:
            try:
                os.unlink(image_to_use)
            except:
                pass
        
        # Move to the beginning of the BytesIO buffer
        packet.seek(0)
        
        return packet

    def save_as(self):
        """Open a file dialog to choose the output file name and location"""
        if len(self.file_paths) == 0:
            messagebox.showwarning("Warning", "No files to merge!")
            return
            
        output_file = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")],
            title="Save merged PDF as"
        )
        
        if not output_file:
            return  # User canceled the save dialog

        self.merge_files(output_file)

    def merge_files(self, output_file):
        """Merge PDF and image files into a single PDF"""
        if len(self.file_paths) == 0:
            messagebox.showwarning("Warning", "No files to merge!")
            return

        try:
            self.update_status("Merging files... Please wait")
            self.root.update()
            
            merger = PdfMerger()
            temp_files = []  # Keep track of temporary files
            
            # Process all files in order
            for idx, file_path in enumerate(self.file_paths):
                self.update_status(f"Processing file {idx + 1}/{len(self.file_paths)}...")
                self.root.update()
                
                file_ext = os.path.splitext(file_path)[1].lower()
                
                if file_ext == '.pdf':
                    # Directly append PDF files
                    merger.append(file_path)
                elif file_ext in ['.jpg', '.jpeg', '.png', '.gif']:
                    # Convert image to PDF first
                    pdf_buffer = self.image_to_pdf(file_path)
                    
                    # Create a temporary file for the converted PDF
                    temp_pdf = tempfile.NamedTemporaryFile(delete=False, suffix='.pdf')
                    temp_pdf.write(pdf_buffer.read())
                    temp_pdf.close()
                    temp_files.append(temp_pdf.name)
                    
                    # Append the temporary PDF
                    merger.append(temp_pdf.name)
                else:
                    messagebox.showwarning(
                        "Unsupported File",
                        f"Skipping unsupported file: {os.path.basename(file_path)}"
                    )
                    continue

            # Write out the merged PDF
            self.update_status("Saving merged PDF...")
            self.root.update()
            
            merger.write(output_file)
            merger.close()
            
            # Clean up temporary files
            for temp_file in temp_files:
                try:
                    os.unlink(temp_file)
                except:
                    pass

            self.update_status(f"Success! Merged {len(self.file_paths)} file(s)")
            messagebox.showinfo("Success", f"Merged PDF saved as:\n{output_file}")
            
            # Clear the list after successful merge
            self.listbox.delete(0, tk.END)
            self.file_paths = []
            self.update_status("Ready to merge files")
            
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while merging:\n{str(e)}")
            self.update_status("Error during merge")
            
            # Clean up temporary files in case of error
            for temp_file in temp_files:
                try:
                    os.unlink(temp_file)
                except:
                    pass

if __name__ == "__main__":
    root = tk.Tk()
    app = PDFMergerApp(root)
    root.mainloop()
