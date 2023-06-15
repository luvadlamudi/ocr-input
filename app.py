import streamlit as st
import os
import time
import calendar
import shutil
from pathlib import Path
from PyPDF2 import PdfMerger
import base64

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

    return merged_pdf_path


# Streamlit app
def main():
    st.title('OCR PDF')

    uploaded_files = st.file_uploader('Upload PDF', type='pdf', accept_multiple_files=True)

    if uploaded_files is not None:
        # Create a temporary folder to store the uploaded PDFs
        temp_folder = 'temp_uploads'
        if not os.path.exists(temp_folder):
            os.makedirs(temp_folder)

        ocr_filenames = []

        for uploaded_file in uploaded_files:
            # Read the contents of the uploaded file
            file_contents = uploaded_file.read()

            # Generate a unique filename for each uploaded file
            file_name = f'{str(int(calendar.timegm(time.gmtime())))}_{uploaded_file.name}'

            # Write the file contents to the temporary location
            file_path = os.path.join(temp_folder, file_name)
            with open(file_path, 'wb') as f:
                f.write(file_contents)

            # Perform OCR on the uploaded PDF file
            ocr_filename = ocr_pdf(file_path)
            ocr_filenames.append(ocr_filename)

        # Generate the download URLs for the OCR'd PDF files
        download_urls = []
        for ocr_filename in ocr_filenames:
            with open(ocr_filename, 'rb') as f:
                contents = f.read()
                b64_pdf = base64.b64encode(contents).decode('utf-8')
                download_url = f'<a href="data:application/pdf;base64,{b64_pdf}" download="{ocr_filename}">Download OCR\'d PDF</a>'
                download_urls.append(download_url)

        # Display the download links for the OCR'd PDF files
        for download_url in download_urls:
            st.markdown(download_url, unsafe_allow_html=True)

if __name__ == '__main__':
    main()
