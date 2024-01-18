import os
import csv
from pdfminer.high_level import extract_text
from tabula import read_pdf

print("execution started for parsing pdf")
# Specify the master folder containing subfolders with PDFs
master_folder = 'D:\\python3\\pdfs'

# Output CSV file
csv_file_path = 'D:\python3\csv\output_table_data.csv'

# Header row
header_row = ['Filename', 'Page', 'Bid End Date/Time', 'Bid Opening Date/Time', 'Bid Document', 'Bid Details', 'Bid Offer Validity', 'Ministry/State Name', 'Department Name', 'Organisation Name', 'Office Name', 'Total Quantity', 'Item Category', 'BOQ Title', 'Minimum Average Annual Turnover', 'OEM Average Turnover', 'Years of Past Experience', 'MSE Exemption', 'Startup Exemption', 'Document required from seller', 'Past Performance', 'Bid to RA enabled', 'RA Qualification Rule', 'Type of Bid', 'Primary product category', 'Time allowed for Technical Clarifications', 'Estimated Bid Value', 'Evaluation Method', 'EMD Detail', 'Group wise evaluation']

# Open CSV file for writing
with open(csv_file_path, 'w', newline='', encoding='utf-8') as csv_file:
    csv_writer = csv.writer(csv_file)

    # Write the header row to the CSV file
    csv_writer.writerow(header_row)

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
                    print("tables==========", tables)

                    # Process the extracted tables
                    for table_index, table_data in enumerate(tables):
                        # Extract specific row based on header row
                        extracted_row = [filename, page_number + 1] + [table_data[table_data.columns[table_data.columns.str.contains(header)]] for header in header_row[2:]]
                        
                        # Write row to the CSV file
                        csv_writer.writerow(extracted_row)

# Print success message
print(f"Table data has been successfully written to {csv_file_path}")
