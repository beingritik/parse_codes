import os
import csv
from pdfminer.high_level import extract_text
from tabula import read_pdf

print("execution started for parsing pdf")
# Specify the master folder containing subfolders with PDFs
master_folder = 'D:\\python3\\pdfs'

# Output CSV file
csv_file_path = 'D:\python3\csv\output_table_data.csv'

# Open CSV file for writing
with open(csv_file_path, 'w', newline='', encoding='utf-8') as csv_file:
    csv_writer = csv.writer(csv_file)

    # Write headers to the CSV file
    # csv_writer.writerow(['Filename', 'Page', 'Attribute', 'Value'])

    # Iterate through the master folder and its subfolders
    for root, dirs, files in os.walk(master_folder):
        for filename in files:
            if filename.endswith('.pdf'):
                # Create the full path to the PDF file
                pdf_path = os.path.join(root, filename)

                # Extract text from the first two pages separately
                for page_number in range(2):
                    # Extract tables from the PDF using tabula
                    tables = read_pdf(pdf_path, pages=page_number + 1, multiple_tables=True)

                    # Process the extracted tables
                    for table_index, table_data in enumerate(tables):
                        # Iterate through rows of the table
                        for row_index, row in table_data.iterrows():
                            # Write each attribute and its value as a separate row
                            for col_name, value in row.items():
                                csv_writer.writerow([filename, page_number + 1, col_name, value])

# Print success message
print(f"Table data has been successfully written to {csv_file_path}")
