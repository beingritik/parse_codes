import os
import fitz  # PyMuPDF
import langid
from tabula import read_pdf
import numpy as np
import pandas as pd  # Import pandas library for handling np.nan values
import csv
import io
import re

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page_num in range(2):  # Extract text from the first two pages
        page = doc[page_num]
        text += page.get_text()

    doc.close()
    return text

def extract_table_fields(pdf_path):
    tables = read_pdf(pdf_path, pages=[1, 2])  # Extract tables from the first two pages
    # print("tables",tables)
    table_data = {}

    for index, table in enumerate(tables):
        table_name = f"Table_{index + 1}"
        table_data[table_name] = table.to_dict(orient='records')

    return table_data

def identify_language(text):
    lang, _ = langid.classify(text)
    return lang

def process_pdfs(master_folder):
    data_dict = {}

    for root, dirs, files in os.walk(master_folder):
        for file in files:
            if file.endswith(".pdf"):
                pdf_path = os.path.join(root, file)
                text = extract_text_from_pdf(pdf_path)
                language = identify_language(text)

                # You can modify this condition based on your specific case
                if language in ['en', 'hi']:
                    table_data = extract_table_fields(pdf_path)
                    key = f"{file}_{language}"
                    data_dict[key] = table_data
    return data_dict

if __name__ == "__main__":
    # D:\python3\n
    # master_folder = r"D:\python3\pdfs"
    master_folder = r"D:\python3\poster"
    extracted_data = process_pdfs(master_folder)
    print("extracted data--",extracted_data)

    formatted_data = {}
    final_dict = {}
    # # # Print the extracted data
    for pdf_name, value in extracted_data.items():
        output_dict = {}
        for item in value['Table_1']:
            # print("value--------,",item)
            key = item.get('Bid Details/ बड ववरण')
            value = item.get('Unnamed: 4')
            # if key and value and not pd.isna(value):  # Check for non-NaN values
            #     output_dict[key] = value
            # else:
            #     bid_info = {}
            #     entry_text = item.get('Bid Details/ बड ववरण', '')
            #     if '/' in entry_text:
            # # Splitting key and value based on '/'
            #         key_value_pair = re.split(r'/', entry_text)
            #         key = key_value_pair[0].strip()
            #         value = key_value_pair[1].strip()
            #         bid_info[key] = value
            #     elif ':' in entry_text:
            # # Handling other key-value pairs with colon
            #         key, value = entry_text.split(':', 1)
            #         bid_info[key.strip()] = value.strip()
            #     else:
            # # Handle the case where no colon or slash is present
            # # You may want to customize this part based on your specific requirements
            #         bid_info['UnknownKey'] = entry_text.strip()

            #     output_dict[pdf_name] = bid_info

            #     print("output=====",output_dict)

            if key and value and not pd.isna(value):  # Check for non-NaN values
                # print("output dict",value)
                output_dict[key] = value

            else:
                bid_info = {}
                entry_text = item['Bid Details/ बड ववरण']
                if '/' in entry_text:
                # Splitting key and value based on '/'
                    key_value_pair = re.split(r'/', entry_text)
                    key = key_value_pair[0].strip()
                    value = key_value_pair[1].strip()
                    bid_info[key] = value
                else:
                # Handling other key-value pairs
                     pdf_name, value = entry_text.split(':', 1)
                     bid_info[key.strip()] = value.strip()

                output_dict[pdf_name] = bid_info


                print('item----',item)
                bid_detail = item.get('Bid Details/ बड ववरण', '')
                if 'बड खलने क' in bid_detail:
                
                # Skip rows with 'बड खलने क' as it seems incomplete in the provided data
                   continue
                bid_detail_parts = bid_detail.split(':')
                if len(bid_detail_parts) == 2:
                    key = bid_detail_parts[0].strip()
                    value = bid_detail_parts[1].strip()
                    output_dict[pdf_name][key] = value

        # first_9_pairs = dict(list(output_dict.items()))

        # Extract the first 9 key-value pairs
        first_9_pairs = dict(list(output_dict.items())[:9])
        final_dict[pdf_name] = first_9_pairs
     
    print("9pairs",final_dict)

    csv_file_path = r'D:\python3\csv\output.csv'

# Write data to CSV

with open(csv_file_path, 'w', newline='', encoding='utf-8') as csv_file:
    csv_writer = csv.writer(csv_file)

    # Write header (column names)
    header = list(next(iter(final_dict.values())).keys())
    header.insert(0, 'Bid pdf name:')  # Add 'Key' column to the beginning
    csv_writer.writerow(header)

    # Write final_dict rows
    for key, inner_dict in final_dict.items():
        row = [key] + list(inner_dict.values())
        csv_writer.writerow(row)

print(f"Data has been written to {csv_file_path}")
    








































#     # Detect the delimiter using Sniffer
# delimiter = csv.Sniffer().sniff(str(next(iter(final_dict.values())).values())).delimiter

# # Write final_dict to CSV with quoting and delimiter auto-detected
# with open(csv_file_path, 'w', newline='', encoding='utf-8') as csv_file:
#     csv_writer = csv.writer(csv_file, quoting=csv.QUOTE_MINIMAL, delimiter=delimiter)

#     # Write header (column names)
#     header = list(next(iter(final_dict.values())).keys())
#     header.insert(0, 'Key')  # Add 'Key' column to the beginning
#     csv_writer.writerow(header)

#     # Write final_dict rows
#     for key, inner_dict in final_dict.items():
#         row = [key] + list(inner_dict.values())
#         csv_writer.writerow(row)

# print(f"Data has been written to {csv_file_path}")







