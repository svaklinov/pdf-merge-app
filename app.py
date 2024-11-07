# app.py

from flask import Flask, render_template, request, send_file, redirect, url_for, flash
from PyPDF2 import PdfMerger
import os
from werkzeug.utils import secure_filename
import uuid

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a secure key in production

# Configure upload folder and allowed extensions
UPLOAD_FOLDER = 'uploads'
MERGED_FOLDER = 'merged'
ALLOWED_EXTENSIONS = {'pdf'}

# Ensure upload and merged directories exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(MERGED_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Check if the post request has the files
        if 'pdf1' not in request.files or 'pdf2' not in request.files:
            flash('No file part')
            return redirect(request.url)
        
        file1 = request.files['pdf1']
        file2 = request.files['pdf2']
        
        # If user does not select files, browser may submit empty files
        if file1.filename == '' or file2.filename == '':
            flash('No selected file')
            return redirect(request.url)
        
        if file1 and allowed_file(file1.filename) and file2 and allowed_file(file2.filename):
            filename1 = secure_filename(file1.filename)
            filename2 = secure_filename(file2.filename)
            
            # Create a unique directory for this merge job
            job_id = str(uuid.uuid4())
            job_folder = os.path.join(app.config['UPLOAD_FOLDER'], job_id)
            os.makedirs(job_folder, exist_ok=True)
            
            file1_path = os.path.join(job_folder, filename1)
            file2_path = os.path.join(job_folder, filename2)
            
            file1.save(file1_path)
            file2.save(file2_path)
            
            # Merge PDFs
            merger = PdfMerger()
            merger.append(file1_path)
            merger.append(file2_path)
            
            merged_filename = f'merged_{job_id}.pdf'
            merged_path = os.path.join(MERGED_FOLDER, merged_filename)
            merger.write(merged_path)
            merger.close()
            
            return redirect(url_for('download_file', filename=merged_filename))
        else:
            flash('Allowed file types are PDF')
            return redirect(request.url)
    return render_template('index.html')

@app.route('/download/<filename>')
def download_file(filename):
    return send_file(os.path.join(MERGED_FOLDER, filename), as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
