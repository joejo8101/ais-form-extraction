from tabula import read_pdf
from tabulate import tabulate
import re
import PyPDF2

data_dict = {
    'AIS_Form': {
        'name_of_assessee': None,
        'date_of_birth': None,
        'mobile_number': None,
        'email_address': None,
        'address_of_assignee': None,
        'pan_employee': None,
        'assessment_year': None,
    },
    'SalaryAISForm': {
        'information_code': None,
        'information_description': None,
        'information_source': None,
        'count': None,
        'amount': None,
        'salary_quater': None,
        'salary_dop_credit': None,
        'salary_amount_paid_credited': None,
        'salary_tds_deducted': None,
        'salary_tds_deposited': None,
        'salary_status': None,
    },
    'DividenAISForm': {
        'information_code': None,
        'information_description': None,
        'information_source': None,
        'count': None,
        'amount': None,
        'dividend_data': []
        # 'dividend_reported_on': None,
        # 'dividend_amount': None,
        # 'dividend_status': None,
    },
    'InterestAISForm': {
        'information_code': None,
        'information_description': None,
        'information_source': None,
        'count': None,
        'amount': None,
        'interest_reported_on': None,
        'interest_acct_no': None,
        'interest_acct_type': None,
        'interest_amount': None,
        'interest_status': None,
    },
    'PurchaseAISForm': {
        'information_code': None,
        'information_description': None,
        'information_source': None,
        'count': None,
        'amount': None,
        'purchase_client_id': None,
        'purchase_amc_name': None,
        'purchase_holder_flag': None,
        'purchase_total_purchase_amount': None,
        'purchase_total_sales_value': None,
        'purchase_status': None,
    },
    'SalesSecuritiesUnitMutualFund': {
        'information_code': None,
        'information_description': None,
        'information_source': None,
        'count': None,
        'amount': None,
        'sales_amc_name': None,
        'sales_date_of_sale_transfer': None,
        'sales_security_class': None,
        'sales_security_name': None,
        'sales_debit_type': None,
        'sales_credit_type': None,
        'sales_asset_type': None,
        'sales_quantity': None,
        'sales_sales_price_per_unit': None,
        'sales_sales_consideration': None,
        'sales_status': None,
    },
    'PurchaseSecuritiesUnitMutualFund': {
        'information_code': None,
        'information_description': None,
        'information_source': None,
        'count': None,
        'amount': None,
        'purchase_client_id': None,
        'purchase_amc_name': None,
        'purchase_holder_flag': None,
        'purchase_total_amount': None,
        'purchase_total_sales_value': None,
        'purchase_status': None,
    },
    'B7': {
        'information_code': None,
        'information_description': None,
        'information_source': None,
        'count': None,
        'amount': None,
    },
    'B3': {
        'assessment_year': None,
        'major_head': None,
        'minor_head': None,
        'tax_a': None,
        'surcharge_b': None,
        'education_cess_c': None,
        'others_d': None,
        'total': None,
        'bsr_code': None,
        'date_of_deposit': None,
        'challan_serial_no': None,
        'challan_identification_no': None,
    },
}

search_patterns = {
    r'Assessment Year\s*(\d{4}-\d{2})': ('AIS_Form', 'assessment_year'),
    r'Permanent Account Number \(PAN\)\s*([A-Z0-9]{10})': ('AIS_Form', 'pan_employee'),
    r'Name of Assessee\s*([A-Z\s]+)\s*Aadhaar': ('AIS_Form', 'name_of_assessee'),
    r'Date of Birth\s*(\d{2}/\d{2}/\d{4})': ('AIS_Form', 'date_of_birth'),
    r'Mobile Number\s*(\d{10})': ('AIS_Form', 'mobile_number'),
    r'E-mail Address\s*([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)\s*Mobile': ('AIS_Form', 'email_address'),
    r'ActiveAddress\s*([\w\s,/-]+)\s*E-mail Address': ('AIS_Form', 'address_of_assignee'),
    r'Q\d+\(([A-Za-z]+-[A-Za-z]+)\)\s*(\d{2}/\d{2}/\d{4})\s*([\d,]+)\s*([\d,]+)\s*([\d,]+)\s*(Active|Inactive)': ('SalaryAISForm', 'salary_quarter_info'),
}
def is_table_relevant(table):
    """
    Check if the table is relevant based on the master keywords.
    Returns a tuple (bool, keyword/title)
    """
    # Convert the initial rows of the table to a single string
    initial_text = ' '.join([' '.join(map(str, row)) for row in table[:3]])  # checking first 3 rows, adjust as needed
    for keyword in master_keywords:
        if keyword.lower() in initial_text.lower():
            return True, keyword  # Return True and the detected keyword
    return False, None
# def is_table_relevant(table):
#     """
#     Check if the table is relevant based on the master keywords.
#     """
#     # Convert the initial rows of the table to a single string
#     initial_text = ' '.join([' '.join(map(str, row)) for row in table[:3]])  # checking first 3 rows, adjust as needed
#     for keyword in master_keywords:
#         if keyword.lower() in initial_text.lower():
#             return True
#     return False
def process_salary_table(table):
    # Extracting Information
    info_row = table[0]
    data_dict['SalaryAISForm']['information_code'] = info_row[1]
    data_dict['SalaryAISForm']['information_description'] = info_row[2]
    data_dict['SalaryAISForm']['information_source'] = info_row[3]
    data_dict['SalaryAISForm']['count'] = info_row[4]
    data_dict['SalaryAISForm']['amount'] = info_row[5]

    # Creating a list for quarter data
    data_dict['SalaryAISForm']['salary_quarters'] = []

    # Extracting salary information for each quarter
    salary_data = table[2:]  # Skipping the header rows

    for row in salary_data:
        quarter_data = {
            'salary_quater': row[1],
            'salary_dop_credit': row[2],
            'salary_amount_paid_credited': row[3],
            'salary_tds_deducted': row[4],
            'salary_tds_deposited': row[6],
            'salary_status': row[7]
        }
        data_dict['SalaryAISForm']['salary_quarters'].append(quarter_data)
def process_dividend_table(table):
    # Extracting Information
    info_row = table[0]
    data_dict['DividenAISForm']['information_code'] = info_row[1]
    data_dict['DividenAISForm']['information_description'] = info_row[2]
    data_dict['DividenAISForm']['information_source'] = info_row[3]
    data_dict['DividenAISForm']['count'] = info_row[4]
    data_dict['DividenAISForm']['amount'] = info_row[5]

    # Extracting dividend data
    for dividend_data in table[2:]:
        dividend_row = {
            'dividend_quarter': dividend_data[1],
            'dividend_reported_on': dividend_data[2],
            'dividend_amount': dividend_data[3],
            'dividend_tds_deducted': dividend_data[4],
            'dividend_tds_deposited': dividend_data[5],
            'dividend_status': dividend_data[6]
        }
        data_dict['DividenAISForm']['dividend_data'].append(dividend_row)

master_keywords = ["Salary", "Dividend", "Interest from deposit", "Cash payments", "Outward foreign remittance/purchase of foreign currency"]

pdf_path = '/home/user/Documents/AIS_2.pdf'

# Open the PDF file
with open(pdf_path, "rb") as f:
    reader = PyPDF2.PdfReader(f)

    # Extract text from each page of the PDF
    extracted_text = ""
    for page in reader.pages:
        extracted_text += page.extract_text()
    print("EXTRACTED TEXT", extracted_text)

# Iterate over the search_patterns dictionary
for pattern, (dict_key, field) in search_patterns.items():
    match = re.search(pattern, extracted_text, re.IGNORECASE)
    if match:
        value = match.group(1).strip()
        data_dict[dict_key][field] = value

# Reads table from PDF file
df_list = read_pdf(pdf_path, pages="all", multiple_tables=True, lattice=True, stream=True)

# Convert each DataFrame to a list of lists
table_data = [df.values.tolist() for df in df_list]

# Process and display tables
for data in table_data:
    # Check if table is relevant
    is_relevant, table_title = is_table_relevant(data)  # Get boolean and title
    if not is_relevant:
        continue

    if table_title == "Salary":
        process_salary_table(data)
    elif table_title == "Dividend":
        process_dividend_table(data)


    # Print table title
    print(f"\n{table_title}\n{'=' * len(table_title)}")  # This will print the title underlined with '='

    # Print table data
    print(tabulate(data))
    table_text = '\n'.join(' '.join(str(cell) for cell in row) for row in data)
    
    # Search for the patterns and extract the values
    for pattern, (dict_key, field) in search_patterns.items():
        if data_dict[dict_key][field] is not None:
            continue  # Skip fields already extracted using PdfReader

        match = re.search(pattern, table_text, re.IGNORECASE)
        if match:
            value = match.group(1).strip()
            data_dict[dict_key][field] = value

# Print the dictionary
for key, value in data_dict.items():
    print(f"{key}: {value}")
    print("\n")





