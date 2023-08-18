# import fitz  # PyMuPDF
# import os
# import pytesseract
# from PIL import Image
# import re

# # Define the main title and subtitles
# main_title = "Part B1-Information relating to tax deducted or collected at source"
# subtitles = [
#     "Salary", 
#     "Dividend", 
#     "Interest from deposit", 
#     "Cash payments", 
#     "Outward foreign remittance/purchase of foreign currency"
# ]

# def extract_tables_from_image(image_path):
#     image = Image.open(image_path)
#     extracted_text = pytesseract.image_to_string(image)

#     return extracted_text

# def extract_tables_by_subtitles(extracted_text):
#     tables = []
#     current_subtitle = None
#     current_table = []

#     lines = extracted_text.split('\n')
#     for line in lines:
#         # Check if the line matches a subtitle
#         if line in subtitles:
#             if current_table and current_subtitle:
#                 tables.append((current_subtitle, current_table))
#                 current_table = []
#             current_subtitle = line
#         elif current_subtitle and line.strip():
#             current_table.append(line)

#     if current_table and current_subtitle:
#         tables.append((current_subtitle, current_table))

#     return tables

# def extract_all_pages_to_images(pdf_path, output_folder):
#     pdf_document = fitz.open(pdf_path)

#     for page_number in range(pdf_document.page_count):
#         page = pdf_document[page_number]

#         image = page.get_pixmap(matrix=fitz.Matrix(2, 2))
#         image_path = f"{output_folder}/page_{page_number + 1}.png"
#         image.save(image_path, "png")

#         extracted_text = extract_tables_from_image(image_path)
#         tables = extract_tables_by_subtitles(extracted_text)

#         for subtitle, table_lines in tables:
#             print(f"Subtitle: {subtitle}")
#             for line in table_lines:
#                 print(line)
#             print("=" * 20)

#     pdf_document.close()

# if __name__ == "__main__":
#     pdf_path = '/home/user/Documents/AIS_2.pdf'
#     output_folder = '/home/user/Documents/Outputs'
#     os.makedirs(output_folder, exist_ok=True)

#     extract_all_pages_to_images(pdf_path, output_folder)
#     print(f"All pages extracted and saved in {output_folder}")

# import fitz  # PyMuPDF
# import os
# import pytesseract
# from PIL import Image
# import re
# import tabula

# # Define the main title and subtitles
# main_title = "Part B1-Information relating to tax deducted or collected at source"
# subtitles = [
#     "Salary", 
#     "Dividend", 
#     "Interest from deposit", 
#     "Cash payments", 
#     "Outward foreign remittance/purchase of foreign currency"
# ]

# def extract_tables_from_image(image_path):
#     image = Image.open(image_path)
#     extracted_text = pytesseract.image_to_string(image)

#     return extracted_text

# def extract_tables_by_subtitles(extracted_text):
#     tables = []
#     current_subtitle = None
#     current_table = []

#     lines = extracted_text.split('\n')
#     for line in lines:
#         # Check if the line matches a subtitle
#         if line in subtitles:
#             if current_table and current_subtitle:
#                 tables.append((current_subtitle, current_table))
#                 current_table = []
#             current_subtitle = line
#         elif current_subtitle and line.strip():
#             current_table.append(line)

#     if current_table and current_subtitle:
#         tables.append((current_subtitle, current_table))

#     return tables

# def extract_all_pages_to_images(pdf_path, output_folder):
#     pdf_document = fitz.open(pdf_path)

#     for page_number in range(pdf_document.page_count):
#         page = pdf_document[page_number]

#         image = page.get_pixmap(matrix=fitz.Matrix(2, 2))
#         image_path = f"{output_folder}/page_{page_number + 1}.png"
#         image.save(image_path, "png")

#         extracted_text = extract_tables_from_image(image_path)
#         tables = extract_tables_by_subtitles(extracted_text)

#         for subtitle, _ in tables:
#             print(f"Subtitle: {subtitle}")
#             # Use Tabula to extract tables based on the subtitle
#             tabula_tables = tabula.read_pdf(pdf_path, pages=page_number + 1, multiple_tables=True)
#             for tabula_table in tabula_tables:
#                 print(tabula_table)
#             print("=" * 20)

#     pdf_document.close()

# if __name__ == "__main__":
#     pdf_path = '/home/user/Documents/AIS_2.pdf'
#     output_folder = '/home/user/Documents/Outputs'
#     os.makedirs(output_folder, exist_ok=True)

#     extract_all_pages_to_images(pdf_path, output_folder)
#     print(f"All pages extracted and saved in {output_folder}")


import fitz  # PyMuPDF
import os
import pytesseract
from PIL import Image
import re
import tabula

# Define the main title and subtitles you are interested in
main_title = "Part B1-Information relating to tax deducted or collected at source"
subtitles = [
    "Salary", 
    "Dividend", 
    "Interest from deposit", 
    "Cash payments", 
    "Outward foreign remittance/purchase of foreign currency"
]

def extract_tables_from_image(image_path):
    image = Image.open(image_path)
    extracted_text = pytesseract.image_to_string(image)

    return extracted_text

def extract_tables_by_subtitles(extracted_text):
    tables = []
    current_subtitle = None
    current_table = []

    lines = extracted_text.split('\n')
    for line in lines:
        # Check if the line matches a subtitle
        if line in subtitles:
            if current_table and current_subtitle:
                tables.append((current_subtitle, current_table))
                current_table = []
            current_subtitle = line
        elif current_subtitle and line.strip():
            current_table.append(line)

    if current_table and current_subtitle:
        tables.append((current_subtitle, current_table))

    return tables

def extract_all_pages_to_images(pdf_path, output_folder):
    pdf_document = fitz.open(pdf_path)

    for page_number in range(pdf_document.page_count):
        page = pdf_document[page_number]

        image = page.get_pixmap(matrix=fitz.Matrix(2, 2))
        image_path = f"{output_folder}/page_{page_number + 1}.png"
        image.save(image_path, "png")

        extracted_text = extract_tables_from_image(image_path)
        tables = extract_tables_by_subtitles(extracted_text)

        for subtitle, _ in tables:
            if subtitle == main_title:  # Only process tables for the specified main title
                print(f"Subtitle: {subtitle}")
                # Use Tabula to extract tables based on the subtitle
                tabula_tables = tabula.read_pdf(pdf_path, pages=page_number + 1, multiple_tables=True)
                for tabula_table in tabula_tables:
                    print(tabula_table)
                print("=" * 20)

    pdf_document.close()

if __name__ == "__main__":
    pdf_path = '/home/user/Documents/AIS_2.pdf'
    output_folder = '/home/user/Documents/Outputs'
    os.makedirs(output_folder, exist_ok=True)

    extract_all_pages_to_images(pdf_path, output_folder)
    print(f"All pages extracted and saved in {output_folder}")
