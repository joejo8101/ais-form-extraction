# import tabula

# # Path to the PDF file you want to extract tables from
# pdf_path = '/home/user/Documents/AIS_2.pdf'

# # Use tabula.read_pdf() to extract tables from the PDF
# tables = tabula.read_pdf(pdf_path, pages='all', multiple_tables=True)

# # Loop through the extracted tables and process them as needed
# for table_num, table in enumerate(tables, start=1):
#     # Process the table data here
#     print(f"Table {table_num}:\n{table}\n")

# import PyPDF2
# import tabula

# # Function to extract text from a PDF
# def extract_text(pdf_path):
#     text = ""
#     with open(pdf_path, "rb") as pdf_file:
#         pdf_reader = PyPDF2.PdfReader(pdf_file)
#         for page in pdf_reader.pages:
#             text += page.extract_text()
#     return text

# # Function to extract tables from a PDF
# def extract_tables(pdf_path):
#     tables = tabula.read_pdf(pdf_path, pages="all", multiple_tables=True)
#     return tables

# # Path to the PDF file
# # pdf_path = "path/to/your/pdf/file.pdf"
# pdf_path = '/home/user/Documents/AIS_2.pdf'


# # Extract text
# # extracted_text = extract_text(pdf_path)
# # print("Extracted Text:")
# # print(extracted_text)

# # # Extract tables
# extracted_tables = extract_tables(pdf_path)
# for idx, table in enumerate(extracted_tables):
#     print(f"Table {idx + 1}:")
#     print(table)
#     print("-" * 40)


# import tabula

# # Path to the PDF file
# pdf_path = '/home/user/Documents/AIS_2.pdf'

# # Extract tables with coordinates using spreadsheet format
# tables_with_coordinates = tabula.read_pdf(pdf_path, pages="all", output_format="json")

# # Print the entire JSON structure for investigation
# print(tables_with_coordinates)

import tabula
import PyPDF2

# Set the PDF path
pdf_path = '/home/user/Documents/AIS_2.pdf'

# Extract text from the PDF using PyPDF2
def extract_text_from_pdf(pdf_path):
    text = ''
    with open(pdf_path, 'rb') as pdf_file:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            text += page.extract_text()
    return text

# Call the function to extract text
pdf_text = extract_text_from_pdf(pdf_path)

# Print the extracted text
print("Extracted Text:")
print(pdf_text)

# Extract tables from the PDF using Tabula
tables = tabula.read_pdf(pdf_path, pages='all', multiple_tables=True)

# Iterate through the extracted tables
for i, table in enumerate(tables, start=1):
    print(f"Table {i}:\n{table}\n")




