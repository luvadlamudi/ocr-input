from flask import Flask, request, jsonify, render_template, send_from_directory
import os
import time
import calendar
import shutil
from pathlib import Path
from PyPDF2 import PdfMerger

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # Get the uploaded file from the request
        uploaded_file = request.files['pdf-file']
        
        # Save the uploaded file to a temporary location
        temp_folder = 'temp_uploads'
        if not os.path.exists(temp_folder):
            os.makedirs(temp_folder)
        uploaded_file.save(os.path.join(temp_folder, 'uploaded.pdf'))

        # Perform OCR on the uploaded PDF file
        ocr_filename = ocr_pdf(os.path.join(temp_folder, 'uploaded.pdf'))
        
        # Generate the download URL for the OCR'd PDF file
        download_url = '/download-pdf?filename=' + ocr_filename
        
        return jsonify({'downloadLink': download_url})
    
    return render_template('index.html')

@app.route('/download-pdf')
def download_pdf():
    filename = request.args.get('filename')
    # ... perform any necessary validation and error handling ...
    directory = os.path.abspath(os.path.dirname(__file__))  # Get the absolute path of the script's directory
    return send_from_directory(directory, filename, as_attachment=True)

def ocr_pdf(pdf_path):
    # OCR process to convert PDF to OCR'd PDF
    processed_files = set()  # Track processed files to avoid duplicate OCR

    file_name = os.path.splitext(os.path.basename(pdf_path))[0]
    folder = str(int(calendar.timegm(time.gmtime()))) + '_' + file_name
    combined = os.path.join(folder, file_name)

    # Create temporary folder
    if not os.path.exists(folder):
        os.makedirs(folder)

    # Convert PDF to PNG(s)
    magick = f'convert -density 150 "{pdf_path}" "{combined}-%04d.png"'
    os.system(magick)

    # Convert PNG(s) to PDF(s) with OCR data
    pngs = [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]
    for pic in pngs:
        if pic.endswith('.png'):
            combined_pic = os.path.join(folder, pic)
            tesseract = f'tesseract "{combined_pic}" "{combined_pic}-ocr" PDF'
            os.system(tesseract)

    # Combine OCR'd PDFs into one
    ocr_pdfs = [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]

    merger = PdfMerger()
    for pdf in ocr_pdfs:
        if pdf.endswith('.pdf'):
            merger.append(os.path.join(folder, pdf))

    merged_pdf_path = os.path.join('output', file_name + '-ocr.pdf')
    merger.write(merged_pdf_path)
    merger.close()

    # Delete the temporary folder and its contents
    shutil.rmtree(folder)

    return file_name + '-ocr.pdf'

if __name__ == '__main__':
    app.run()
