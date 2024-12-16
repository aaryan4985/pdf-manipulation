from flask import Flask, render_template, request, redirect, send_file, flash, url_for
from werkzeug.utils import secure_filename
from pypdf import PdfReader, PdfWriter
import os
import tempfile
import zipfile

app = Flask(__name__)
app.secret_key = 'secretkey'  # For flashing messages

UPLOAD_FOLDER = tempfile.gettempdir()
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Home Page
@app.route('/')
def index():
    return render_template('index.html')

# Merge PDFs
@app.route('/merge', methods=['POST'])
def merge_pdfs():
    if 'files' not in request.files:
        flash("No files uploaded!")
        return redirect(url_for('index'))

    files = request.files.getlist('files')
    if not files or files[0].filename == '':
        flash("Please upload at least two PDF files.")
        return redirect(url_for('index'))

    writer = PdfWriter()
    output_path = os.path.join(app.config['UPLOAD_FOLDER'], "merged_output.pdf")
    
    try:
        for file in files:
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            reader = PdfReader(file_path)
            for page in reader.pages:
                writer.add_page(page)
        
        with open(output_path, "wb") as f:
            writer.write(f)

        return send_file(output_path, as_attachment=True, download_name="merged_output.pdf")
    except Exception as e:
        flash(f"Failed to merge PDFs: {str(e)}")
        return redirect(url_for('index'))

# Split PDF
@app.route('/split', methods=['POST'])
def split_pdf():
    if 'file' not in request.files:
        flash("No file uploaded!")
        return redirect(url_for('index'))

    file = request.files['file']
    if file.filename == '':
        flash("Please upload a PDF file to split.")
        return redirect(url_for('index'))

    try:
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        reader = PdfReader(file_path)
        zip_output_path = os.path.join(app.config['UPLOAD_FOLDER'], "split_pages.zip")
        with zipfile.ZipFile(zip_output_path, 'w') as zipf:
            for i, page in enumerate(reader.pages):
                writer = PdfWriter()
                writer.add_page(page)
                page_output = os.path.join(app.config['UPLOAD_FOLDER'], f"page_{i+1}.pdf")
                with open(page_output, "wb") as f:
                    writer.write(f)
                zipf.write(page_output, f"page_{i+1}.pdf")
                os.remove(page_output)

        return send_file(zip_output_path, as_attachment=True, download_name="split_pages.zip")
    except Exception as e:
        flash(f"Failed to split PDF: {str(e)}")
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
