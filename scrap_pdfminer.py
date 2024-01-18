from pdfminer.high_level import extract_text
import os

print("execution started for parsing pdf")
# Specify the master folder containing subfolders with PDFs
master_folder = 'D:\\python3\\pdfs'

# Iterate through the master folder and its subfolders
for root, dirs, files in os.walk(master_folder):
    for filename in files:
        if filename.endswith('.pdf'):
            # Create the full path to the PDF file
            pdf_path = os.path.join(root, filename)

            # Extract text from the first two pages separately
            for page_number in range(2):
                text = extract_text(pdf_path, page_numbers=[page_number])

                # Do something with the extracted text
                print(f"Text from {filename}, Page {page_number + 1}:\n{text}\n")
