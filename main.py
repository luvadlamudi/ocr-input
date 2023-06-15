import streamlit as st
import os
import time
import calendar
import shutil
from pathlib import Path
from PyPDF2 import PdfMerger

# OCR PDF function
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

# Streamlit app
def main():
    st.title('OCR PDF')

    uploaded_file = st.file_uploader('Upload PDF', type='pdf', accept_multiple_files=True)

    if uploaded_file is not None:
        # Save the uploaded file to a temporary location
        temp_folder = 'temp_uploads'
        if not os.path.exists(temp_folder):
            os.makedirs(temp_folder)
        uploaded_file.save(os.path.join(temp_folder, 'uploaded.pdf'))

        # Perform OCR on the uploaded PDF file
        ocr_filename = ocr_pdf(os.path.join(temp_folder, 'uploaded.pdf'))

        # Generate the download URL for the OCR'd PDF file
        download_url = '/download-pdf?filename=' + ocr_filename

        # Display the download link
        st.markdown(f'[Download OCR\'d PDF]({download_url})')

if __name__ == '__main__':
    main()
