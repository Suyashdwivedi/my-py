from flask import Flask, request, redirect, url_for, send_file, render_template
from PyPDF2 import PdfMerger
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MERGED_FOLDER'] = 'merged'
app.config['ALLOWED_EXTENSIONS'] = {'pdf'}

# Ensure the upload and merged folders exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['MERGED_FOLDER'], exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_files():
    files = request.files.getlist('files')
    if not files or any(not allowed_file(f.filename) for f in files):
        return redirect(url_for('index'))

    filenames = []
    for file in files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            filenames.append(filepath)

    # Merge PDFs
    output_filename = 'merged.pdf'
    output_filepath = os.path.join(app.config['MERGED_FOLDER'], output_filename)

    merger = PdfMerger()
    try:
        for filepath in filenames:
            merger.append(filepath)
        merger.write(output_filepath)
    except Exception as e:
        return f"Error: {e}"
    finally:
        merger.close()

    # Clean up uploaded files
    for filepath in filenames:
        os.remove(filepath)

    # Check if the merged file exists before sending
    if os.path.exists(output_filepath):
        return send_file(output_filepath, as_attachment=True)
    else:
        return "Error: Merged file not found."

if __name__ == '__main__':
    app.run(debug=True)