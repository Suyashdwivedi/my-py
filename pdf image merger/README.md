# PDF & Image Merger

A powerful Python application to merge PDF files and images (JPG, PNG, GIF) into a single PDF document with advanced compression and sizing options.

## Features

### ✨ Core Features
- **Merge PDFs and Images** - Combine multiple PDF files and images into one PDF
- **Image Compression** - Reduce file size while maintaining print quality
- **Flexible Image Sizing** - Multiple width options for image placement
- **Smart Centering** - All images are automatically centered on the page
- **Modern UI** - Clean, intuitive interface with color-coded buttons

### 📦 Compression Options
When "Compress images for A4 print quality" is enabled:
- Images are resized to optimal print resolution (150 DPI)
- JPEG compression with 90% quality (excellent for printing)
- Reduces file size by 60-80% while maintaining visual quality
- Perfect for sharing via email or web

**When to use compression:**
- ✅ Sharing documents via email
- ✅ Uploading to websites
- ✅ Standard office printing
- ❌ Professional photo printing
- ❌ Large format prints

### 📏 Image Width Options

1. **Fit to Page** (Default)
   - Images scale to fit the entire page (width or height, whichever is limiting)
   - Best for mixed content (portraits and landscapes)
   - Maximum size while staying within page boundaries

2. **Half Size of Page**
   - Images scale to 50% of the page width
   - Good for creating documents with multiple images per page
   - Useful for before/after comparisons

3. **Quarter Size**
   - Images scale to 25% of the page width
   - Perfect for thumbnail galleries
   - Ideal for contact sheets or image catalogs

4. **Custom Width**
   - Enter your own width in millimeters
   - Images will scale to your specified width
   - Useful for specific layout requirements
   - Example: Enter "100" for 100mm wide images

## Installation

### Required Libraries
```bash
pip install PyPDF2 Pillow reportlab
```

### Running the Application
```bash
python pdf_image_merger.py
```

## How to Use

1. **Add Files**
   - Click "➕ Add Files" button
   - Select PDF files, images, or both
   - Files appear in the list with icons (📄 for PDF, 🖼️ for images)

2. **Configure Options**
   - Check/uncheck compression option
   - Select image width from dropdown
   - Enter custom width if needed

3. **Manage Files**
   - Select files to remove and click "🗑️ Remove Selected"
   - Click "✖️ Clear All" to remove all files
   - Files are merged in the order they appear

4. **Merge and Save**
   - Click "📄 Merge & Save"
   - Choose output location and filename
   - Wait for processing to complete

## Technical Details

### Supported Formats
- **PDFs**: `.pdf`
- **Images**: `.jpg`, `.jpeg`, `.png`, `.gif`

### Image Processing
- **Page Size**: A4 (210mm × 297mm)
- **Margins**: 10mm on all sides
- **Compression DPI**: 150 (when enabled)
- **JPEG Quality**: 90% (when enabled)
- **Aspect Ratio**: Always preserved

### File Size Comparison
Example with 5 high-resolution photos (4000×3000 px each):

| Setting | Output Size | Quality |
|---------|-------------|---------|
| No compression | ~15 MB | Maximum |
| With compression | ~3 MB | Excellent for print |

## Tips for Best Results

### For Full-Page Photos
- ✅ Enable compression
- ✅ Use "Fit to Page" width
- Result: Small file size, great for sharing

### For Professional Documents
- ❌ Disable compression
- ✅ Use "Fit to Page"
- Result: Maximum quality, larger files

### For Image Galleries/Catalogs
- ✅ Enable compression
- ✅ Use "Half Size of Page" or "Quarter Size"
- Result: Multiple images visible per page

### For Custom Layouts
- ✅ Use "Custom Width" option
- ✅ Enter exact width in millimeters
- Result: Precise control over image sizing

## Troubleshooting

### Images appear too small
- Solution: Use "Fit to Page" instead of "Half Size" or "Quarter Size"

### Want multiple images per page
- Solution: Use "Half Size of Page" or "Quarter Size" option

### File size too large
- Solution: Enable compression option

### Image quality degraded
- Solution: Disable compression for maximum quality

### Custom width not working
- Solution: Make sure to enter only numbers in millimeters

## System Requirements
- Python 3.7 or higher
- Tkinter (usually included with Python)
- 50MB free disk space for temporary files

## License
Free to use and modify for personal and commercial projects.

## Support
For issues or questions, please check:
1. Required libraries are installed
2. Image files are not corrupted
3. Sufficient disk space available
4. Valid numeric values in custom width field
