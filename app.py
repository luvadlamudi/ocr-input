import streamlit as st # Web interf
import os # Directory func
import time #Temp folder
import calendar # Temp folder
import shutil #Removes Temp folders
from pathlib import Path # Gets Dir Path
from PyPDF2 import PdfMerger # Merge PDFs into one
import base64 # Binary Convert for Dwnl link
from io import BytesIO # Creates Temp zip
import threading # Dwnl all func




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

    # Save the OCR'd PDF in the same location as the uploaded PDF
    output_path = os.path.join(os.path.dirname(pdf_path), file_name + '-ocr.pdf')
    merger.write(output_path)
    merger.close()

    # Delete the temporary folder and its contents
    shutil.rmtree(folder)
    # Sends back file path
    return output_path

# Function to generate download link for a file
def get_download_link(file_path, file_name):
    with open(file_path, 'rb') as f:
        base64_encoded = base64.b64encode(f.read()).decode()
    download_link = f'<a href="data:application/octet-stream;base64,{base64_encoded}" download="{file_name}">Download {file_name}</a>'
    return download_link

# Streamlit 
def main():
    st.title('OCR PDF')






    # Allows it to accept multiple PDF files
    uploaded_files = st.file_uploader('Upload PDFS', type='pdf', accept_multiple_files=True)
    
    # If there are uploaded files ...
    if uploaded_files:
        ocr_files = []

        for uploaded_file in uploaded_files:
            # Read the contents of the uploaded file
            file_contents = uploaded_file.read()

            # Generate a unique filename for each uploaded file
            file_name = f'{str(int(calendar.timegm(time.gmtime())))}_{uploaded_file.name}'

            # Write the file contents to a temporary location
            temp_path = os.path.join(Path.home(), file_name)
            with open(temp_path, 'wb') as f:
                f.write(file_contents)

            # Perform OCR on the uploaded PDF file
            ocr_file_path = ocr_pdf(temp_path)
            ocr_files.append((ocr_file_path, uploaded_file.name))

            # Delete the temporary file
            os.remove(temp_path)

        # Display the download buttons for the OCR'd PDF files
        for ocr_file_path, file_name in ocr_files:
            download_link = get_download_link(ocr_file_path, file_name)
            st.markdown(download_link, unsafe_allow_html=True)

    ##########
        # NEEDS WORK ***  BUTTON TO DOWNLOAD ALL FILES, POP UP BUTTON AFTER OCR RUNS, ADD -OCR TO EACH FILE DWNL THEN ENCODE USING 
        # BASE64
    #####

        def download_all():
            merged_file_path = merge_pdf_files(ocr_files)
            merged_file_name = 'All_OCR_PDFs.zip'
            download_all_link = get_download_link(merged_file_path, merged_file_name)
            st.markdown(f'<a href="{download_all_link}" download="{merged_file_name}"><button>Download All OCR\'d PDFs</button></a>', unsafe_allow_html=True)

        if len(ocr_files) > 1:
            threading.Thread(target=download_all).start()

    ######



# Function to merge OCR'd PDF files into a single zip file
def merge_pdf_files(ocr_files):
    merger = PdfMerger()

    # Merge all the OCR'd PDF files into one
    for ocr_file_path, _ in ocr_files:
        merger.append(ocr_file_path)

    # Save the merged PDF as a BytesIO object
    merged_pdf_stream = BytesIO()
    merger.write(merged_pdf_stream)
    merger.close()

    # Create a temporary zip file to store the merged PDF
    temp_zip_path = os.path.join(Path.home(), 'merged_pdf.zip')

    # Save the BytesIO object as the temporary zip file
    with open(temp_zip_path, 'wb') as f:
        f.write(merged_pdf_stream.getvalue())

    return temp_zip_path

if __name__ == '__main__':
    main()

#if __name__ == '__main__':
#    main(debug=True)
