

import os
import fitz  # PyMuPDF
import langid
from tabula import read_pdf
import numpy as np
import pandas as pd  # Import pandas library for handling np.nan values
import csv
import io
import re
from os import environ as env
from dotenv import load_dotenv
load_dotenv()

master_folder = env['DOWNLOAD_PDF_31000']
csv_file_path = env['OUTPUT_CSV_31000']

def extract_text_from_pdf(pdf_path):
    try:
        # print("called extract from pdf then this")
        doc = fitz.open(pdf_path)
        text = ""
        for page_num in range(2):
            page = doc[page_num]
            text += page.get_text()
        doc.close()
        return text
    except Exception as e:
        error_message = str(e)
        if "no objects found" in error_message:
            print(f"Error opening PDF file {pdf_path}: {error_message}")
        else:
            # Handle other exceptions if needed
            print(f"Unexpected error: {error_message}")
        return " broken document - {pdf_path}"

def extract_table_fields(pdf_path):
    try:
        
       tables = read_pdf(pdf_path, pages=[1, 2], lattice=True, multiple_tables=True)  # Extract tables from the first two pages
       table_data = {}

       for index, table in enumerate(tables):
           table_name = f"Table_{index + 1}"
           table_data[table_name] = table.to_dict(orient='records')

       return table_data
   
    except Exception as e:
        print(f"Error extracting tables from {pdf_path}: {e}")
        return {}        

def identify_language(text):
    lang, _ = langid.classify(text)
    return lang

def process_pdfs(master_folder):
    data_dict = {}

    for root, dirs, files in os.walk(master_folder):
        for file in files:      
            if file.endswith(".pdf"):
                pdf_path = os.path.join(root, file)
                # print(f"Processing PDF: {pdf_path}")
                text = extract_text_from_pdf(pdf_path)
                # print("text",text)
                language = identify_language(text)
                # print("lan",language)

                # You can modify this condition based on your specific case
                if language in ['en', 'hi']:
                    table_data = extract_table_fields(pdf_path)
                    key = f"{file}_{language}"
                    data_dict[key] = table_data
                    # print("data_dict[key]",data_dict[key])
                else:
                    key = f"{file}_{language}"
                    data_dict[key] =  {'Table_1': [{"Broken pdf and parsing failed for this document"}]}
    return data_dict

if __name__ == "__main__":
    # master_folder = r"F:\harshit_bid_project\scrapping_pdfs"
    # master_folder = r"F:\ritik_project\temp"
    # master_folder = r"F:\ritik_project\expdf"
    # master_folder = r"F:\ritik_project\poster"
    extracted_data = process_pdfs(master_folder)
    # print("extracted data--",extracted_data)

    final_dict = {}
    # # # Print the extracted data
 
    for pdf_name, value in extracted_data.items():
        output_dict = {}

        if isinstance(value, str):
            # Handle the case where the value is a string (broken PDF)
            print(f"Broken pdf and parsing failed for this document: {pdf_name}")
        elif 'Table_1' in value:
            table_1_data = value['Table_1']

            if isinstance(table_1_data, set):
                # Handle the case where 'Table_1' is a set
                print(f"Unexpected data type for {pdf_name}: 'Table_1' is a set.")
                # You can choose to store the set itself or any other representation in final_dict
                final_dict[pdf_name] = {'Table_1': table_1_data}
            elif isinstance(table_1_data, list):
                # print("!!!!22222")
                # Process the list of dictionaries
                for item in table_1_data: 
                    # print("tabl;e inside = ",item)
                    if isinstance(item, dict):
                        key = item.get('Bid Details/ बड ववरण') 
                        # print("key",key)
                        parsed_1_value = item.get('Unnamed: 4')  
                        
                        if key and parsed_1_value and not pd.isna(parsed_1_value):  # Check for non-NaN parsed_1_values
                           output_dict[key] = parsed_1_value
                    else:
                        output_dict[pdf_name] =item
       
                # Extract the first 9 key-value pairs
                first_9_pairs = dict(list(output_dict.items())[:9])
                final_dict[pdf_name] = first_9_pairs
            else:
                print(f"Unexpected data type for {pdf_name}: 'Table_1' is neither a set nor a list.")
                # You can choose to store the data itself or any other representation in final_dict
                final_dict[pdf_name] = {'Table_1': table_1_data}
        else:
            print(f"Unexpected value type for {pdf_name}: {type(value)}")
            # You can choose to store the value itself or any other representation in final_dict
            final_dict[pdf_name] = {'Value': value}

print("final_dict:", final_dict)

with open(csv_file_path, 'w', newline='', encoding='utf-8') as csv_file:
    csv_writer = csv.writer(csv_file)

    # Write header (column names)
    if final_dict:
        header = list(next(iter(final_dict.values())).keys())
        header.insert(0, 'Bid pdf name:')  # Add 'Key' column to the beginning
        csv_writer.writerow(header)

    # Write final_dict rows
        for key, inner_dict in final_dict.items():
            row = [key] + list(inner_dict.values())
            csv_writer.writerow(row)
    else:
        print("no oer corrupt data for this pdf:{pdf_name}")

print(f"Data has been written to {csv_file_path}")


    # for pdf_name, value in extracted_data.items():
    #     output_dict = {}

    #     if isinstance(value, str):
    #         # Handle the case where the value is a string (broken PDF)
    #         print(f"Broken pdf and parsing failed for this document: {pdf_name}")
    #     elif 'Table_1' in value and isinstance(value['Table_1'], list):
    #         # Process the dictionary only if 'Table_1' is present and is a list
    #         for item in value['Table_1']:
    #             key = item.get('Bid Details/ बड ववरण') 
    #             value = item.get('Unnamed: 4')
    #             if key and value and not pd.isna(value):  # Check for non-NaN values
    #                 output_dict[key] = value

    #         # Extract the first 9 key-value pairs
    #         first_9_pairs = dict(list(output_dict.items())[:9])
    #         final_dict[pdf_name] = first_9_pairs
    #     else:
    #         print(f"Unexpected value type for {pdf_name}: {type(value)}")

    # print("9pairs", final_dict)



# Write data to Csv 
# print(f"Data has been written to {csv_file_path}")








































# import os
# import fitz  # PyMuPDF
# import langid
# from tabula import read_pdf
# import numpy as np
# import pandas as pd  # Import pandas library for handling np.nan values
# import csv
# import io
# import re

# def extract_text_from_pdf(pdf_path):
#     doc = fitz.open(pdf_path)
#     text = ""
#     for page_num in range(2):  # Extract text from the first two pages
#         page = doc[page_num]
#         text += page.get_text()

#     doc.close()
#     return text

# def extract_table_fields(pdf_path):
#     tables = read_pdf(pdf_path, pages=[1, 2])  # Extract tables from the first two pages
#     # print("tables",tables)
#     table_data = {}

#     for index, table in enumerate(tables):
#         table_name = f"Table_{index + 1}"
#         table_data[table_name] = table.to_dict(orient='records')

#     return table_data

# def identify_language(text):
#     lang, _ = langid.classify(text)
#     return lang

# def process_pdfs(master_folder):
#     data_dict = {}

#     for root, dirs, files in os.walk(master_folder):
#         for file in files:
#             if file.endswith(".pdf"):
#                 pdf_path = os.path.join(root, file)
#                 text = extract_text_from_pdf(pdf_path)
#                 language = identify_language(text)

#                 # You can modify this condition based on your specific case
#                 if language in ['en', 'hi']:
#                     table_data = extract_table_fields(pdf_path)
#                     key = f"{file}_{language}"
#                     data_dict[key] = table_data
#     return data_dict

# if __name__ == "__main__":
#     # D:\python3\n
#     # master_folder = r"D:\python3\pdfs"
#     master_folder = r"D:\python3\poster"
#     extracted_data = process_pdfs(master_folder)
#     print("extracted data--",extracted_data)

#     formatted_data = {}
#     final_dict = {}
#     # # # Print the extracted data
#     for pdf_name, value in extracted_data.items():
#         output_dict = {}
#         for item in value['Table_1']:
#             # print("value--------,",item)
#             key = item.get('Bid Details/ बड ववरण')
#             value = item.get('Unnamed: 4')
#             if key and value and not pd.isna(value):  # Check for non-NaN values
#                 # print("output dict",value)
#                 output_dict[key] = value

#             # else:
#             #     bid_info = {}
#             #     entry_text = item['Bid Details/ बड ववरण']
#             #     if '/' in entry_text:
#             #     # Splitting key and value based on '/'
#             #         key_value_pair = re.split(r'/', entry_text)
#             #         key = key_value_pair[0].strip()
#             #         value = key_value_pair[1].strip()
#             #         bid_info[key] = value
#             #     else:
#             #     # Handling other key-value pairs
#             #          pdf_name, value = entry_text.split(':', 1)
#             #          bid_info[key.strip()] = value.strip()

#             #     output_dict[pdf_name] = bid_info


#             #     print('item----',item)
#             #     bid_detail = item.get('Bid Details/ बड ववरण', '')
#             #     if 'बड खलने क' in bid_detail:
                
#             #     # Skip rows with 'बड खलने क' as it seems incomplete in the provided data
#             #        continue
#             #     bid_detail_parts = bid_detail.split(':')
#             #     if len(bid_detail_parts) == 2:
#             #         key = bid_detail_parts[0].strip()
#             #         value = bid_detail_parts[1].strip()
#             #         output_dict[pdf_name][key] = value

#         # first_9_pairs = dict(list(output_dict.items()))

#         # Extract the first 9 key-value pairs
#         first_9_pairs = dict(list(output_dict.items())[:9])
#         final_dict[pdf_name] = first_9_pairs
     
#     print("9pairs",final_dict)

#     csv_file_path = r'D:\python3\csv\output.csv'

# # Write data to CSV

# with open(csv_file_path, 'w', newline='', encoding='utf-8') as csv_file:
#     csv_writer = csv.writer(csv_file)

#     # Write header (column names)
#     header = list(next(iter(final_dict.values())).keys())
#     header.insert(0, 'Bid pdf name:')  # Add 'Key' column to the beginning
#     csv_writer.writerow(header)

#     # Write final_dict rows
#     for key, inner_dict in final_dict.items():
#         row = [key] + list(inner_dict.values())
#         csv_writer.writerow(row)

# print(f"Data has been written to {csv_file_path}")
    








































# #     # Detect the delimiter using Sniffer
# # delimiter = csv.Sniffer().sniff(str(next(iter(final_dict.values())).values())).delimiter

# # # Write final_dict to CSV with quoting and delimiter auto-detected
# # with open(csv_file_path, 'w', newline='', encoding='utf-8') as csv_file:
# #     csv_writer = csv.writer(csv_file, quoting=csv.QUOTE_MINIMAL, delimiter=delimiter)

# #     # Write header (column names)
# #     header = list(next(iter(final_dict.values())).keys())
# #     header.insert(0, 'Key')  # Add 'Key' column to the beginning
# #     csv_writer.writerow(header)

# #     # Write final_dict rows
# #     for key, inner_dict in final_dict.items():
# #         row = [key] + list(inner_dict.values())
# #         csv_writer.writerow(row)

# # print(f"Data has been written to {csv_file_path}")







