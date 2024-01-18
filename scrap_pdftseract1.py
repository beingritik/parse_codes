import os
import camelot
import pytesseract
from PIL import Image
from pdf2image import convert_from_path
from PyPDF2 import PdfFileReader

def extract_text_from_pdf(pdf_path):
    images = convert_from_path(pdf_path)
    text = ""
    for page_image in images:
        text += pytesseract.image_to_string(page_image, lang='eng+hin')
    return text

def extract_table_from_pdf(pdf_path):
    # Use camelot to extract tables from the first two pages
    tables = camelot.read_pdf(pdf_path, flavor='stream', pages='1,2')

    if tables:
        return tables[0].df  # Use the first table from the list of tables
    else:
        return None

def process_pdf_folder(master_folder):
    data_dict = {}

    # Iterate through subfolders
    for subdir, _, files in os.walk(master_folder):
        for file in files:
            if file.lower().endswith('.pdf'):
                pdf_path = os.path.join(subdir, file)

                # Check if the PDF is encrypted
                with open(pdf_path, 'rb') as file_handle:
                    reader = PdfFileReader(file_handle)
                    if reader.isEncrypted:
                        raise Exception(f"The PDF file '{pdf_path}' is encrypted. Decryption is not supported.")

                # Extract text from the PDF using Tesseract OCR
                text = extract_text_from_pdf(pdf_path)

                # Process the extracted text (you may need to customize this based on your PDF content)
                # Here, we are just printing the extracted text
                print(text)

    return data_dict

# Replace 'your_master_folder_path' with the path to your master folder
master_folder_path = r'D:\python3\pdfs'
result_dict = process_pdf_folder(master_folder_path)

# Print the resulting dictionary
print("RESULT====", result_dict)
