import os
import time
import calendar
import shutil
import sys
from pathlib import Path
from PyPDF2 import PdfMerger

# gets users pdfs from desktop
# iterates ocr over every pdf w/o -ocr
# returns ocr-d pdf in downloads folder
# test --48

def perform_ocr(source_folder, output_folder):
    processed_files = set()  # Track processed files to avoid duplicate OCR

    while True:
        dir_files = [f for f in os.listdir(source_folder) if os.path.isfile(os.path.join(source_folder, f))]
        for file in dir_files:
            if file.endswith('.pdf') and file not in processed_files:
                # Skip files that have already been OCR'd
                if '-ocr' in file:
                    print('Skipping:', file, '- Already OCR\'d')
                    continue

                print('Working on converting:', file)

                # Set up folder and file paths
                file_name = file.replace('.pdf', '')
                folder = str(int(calendar.timegm(time.gmtime()))) + '_' + file_name
                combined = os.path.join(folder, file_name)

                # Create temporary folder
                if not os.path.exists(folder):
                    os.makedirs(folder)

                # Convert PDF to PNG(s)
                magick = f'convert -density 150 "{os.path.join(source_folder, file)}" "{combined}-%04d.png"'
                print(magick)
                os.system(magick)

                # Convert PNG(s) to PDF(s) with OCR data
                pngs = [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]
                for pic in pngs:
                    if pic.endswith('.png'):
                        combined_pic = os.path.join(folder, pic)
                        print(combined_pic)
                        tesseract = f'tesseract "{combined_pic}" "{combined_pic}-ocr" PDF'
                        print(tesseract)
                        os.system(tesseract)

                # Combine OCR'd PDFs into one
                ocr_pdfs = [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]

                merger = PdfMerger()
                for pdf in ocr_pdfs:
                    if pdf.endswith('.pdf'):
                        merger.append(os.path.join(folder, pdf))

                merged_pdf_path = os.path.join(output_folder, file_name + '-ocr.pdf')
                merger.write(merged_pdf_path)
                merger.close()

                # Delete the original PDF file
                os.remove(os.path.join(source_folder, file))
                print("Original PDF file deleted successfully.")

                # Move the OCR'd PDF to the output folder
                shutil.move(merged_pdf_path, os.path.join(output_folder, file_name + '-ocr.pdf'))

                # Delete the temporary folder and its contents
                shutil.rmtree(folder)
                print("Temporary folder deleted successfully.")

                processed_files.add(file)

        time.sleep(1)  # Wait before checking for new PDF files again

if __name__ == "__main__":
    if len(sys.argv) == 1:
        # No command-line arguments provided, use default folders
        source_folder = str(Path.home() / "Desktop")
        output_folder = str(Path.home() / "Downloads")
    elif len(sys.argv) == 3:
        source_folder = sys.argv[1]
        output_folder = sys.argv[2]
    else:
        print("Usage: python ocr_script.py [source_folder] [output_folder]")
        sys.exit(1)

    perform_ocr(source_folder, output_folder)

