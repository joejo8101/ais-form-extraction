# This script takes in PNG files with multiple tables in them and converts the items in the second column into individual PNGs, using the text from the first column as the file name.
import cv2
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import csv
try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract
import string
import os
import re


def convert_BGR_to_gray(img):
    bgr = img[:,:,:3] # Channels 0..2
    gray_img = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
    return gray_img


def sort_contours(cnts, method="left-to-right"):
    # initialize the reverse flag and sort index
    reverse = False
    i = 0
    # handle if we need to sort in reverse
    if method == "right-to-left" or method == "bottom-to-top":
        reverse = True
    # handle if we are sorting against the y-coordinate rather than
    # the x-coordinate of the bounding box
    if method == "top-to-bottom" or method == "bottom-to-top":
        i = 1
    # construct the list of bounding boxes and sort them from top to
    # bottom
    boundingBoxes = [cv2.boundingRect(c) for c in cnts]
    (cnts, boundingBoxes) = zip(*sorted(zip(cnts, boundingBoxes),
    key=lambda b:b[1][i], reverse=reverse))
    # return the list of sorted contours and bounding boxes
    return (cnts, boundingBoxes)


def get_line_kernels(img):
    kernel_len = np.array(img).shape[1]//100
    ver_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, kernel_len))
    hor_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_len, 1))
    return ver_kernel, hor_kernel


def threshold_and_invert(img):
    #thresholding the image to a binary image
    thresh,img_bin = cv2.threshold(img,128,255,cv2.THRESH_BINARY |cv2.THRESH_OTSU)
    #inverting the image 
    img_bin = 255-img_bin

    return img_bin

def filter_contours_by_width(contours):

    filtered_contours = []
    # get first line
    x, y, w, h = cv2.boundingRect(contours[0])
    # set min lenth of the  all lines as 95% of first line
    min_line_length = w * 0.95

    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        if w > min_line_length:  # Set your own thresholds for length
            filtered_contours.append(cnt)

    return filtered_contours

def filter_contours_by_height(contours):

    filtered_contours = []
    # get first line
    x, y, w, h = cv2.boundingRect(contours[0])
    # set min lenth of the  all lines as 95% of first line
    min_line_length = h * 0.95

    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        if h > min_line_length:  # Set your own thresholds for length
            filtered_contours.append(cnt)

    return filtered_contours


def get_rows(filtered_contours, table_img):
    rows = []
    # Iterate over the sorted contours and crop the rows of the table
    for i in range(1, len(filtered_contours)):
        top_cnt = filtered_contours[i-1]
        bottom_cnt = filtered_contours[i]
        
        # Get the bounding rectangle coordinates for the two contours
        x_top, y_top, w_top, h_top = cv2.boundingRect(top_cnt)
        x_bottom, y_bottom, w_bottom, h_bottom = cv2.boundingRect(bottom_cnt)
        
        # Calculate the top and bottom y-coordinates for the cropped region
        top_y = y_top + h_top
        bottom_y = y_bottom
        
        # Calculate the current row height
        current_height = bottom_y - top_y

        cropped_region = table_img[top_y:bottom_y, x_top:x_top+w_top,:]

        rows.append(cropped_region)

    return rows




def remove_special_characters(file_name):

    # Define the pattern to match special characters
    pattern = r"[^\w.\"#*/]"
    print(file_name)

    # Remove special characters except '/'
    clean_file_name = re.sub(pattern, "", file_name)
    print(clean_file_name)

    # Replace '/' with '++'
    clean_file_name = clean_file_name.replace("/", "++")

    print(clean_file_name)
    return clean_file_name



def extract_text(image):

    # Create a PIL image from the grayscale image
    pil_image = Image.fromarray(image)

    text = pytesseract.image_to_string(pil_image)

    return remove_special_characters(text)



def extract_from_rows(rows):

    # skip first three lines as its not needed in the current use case
    for row in rows[3:]:

        gray_row = convert_BGR_to_gray(row)

        img_bin = threshold_and_invert(gray_row)

        ver_kernel, hor_kernel = get_line_kernels(gray_row)

        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))


        #Use vertical kernel to detect and save the vertical lines in a jpg
        image_1 = cv2.erode(img_bin, ver_kernel, iterations=3)
        vertical_lines = cv2.dilate(image_1, ver_kernel, iterations=3)

        contours, _ = cv2.findContours(vertical_lines, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        # Sort all the contours by left to right.
        contours, boundingBoxes = sort_contours(contours, 'left-to-right')


        # filter the contours to remove lines that are not the part of the table
        filtered_vertical_contours = filter_contours_by_height(contours)
        # Initialize a list to store cropped columns
        columns = []

        # Iterate over the sorted contours and crop the columns of the table
        for i in range(1, len(filtered_vertical_contours)):
            left_cnt = filtered_vertical_contours[i-1]
            right_cnt = filtered_vertical_contours[i]
            
            # Get the bounding rectangle coordinates for the two contours
            x_left, y_left, w_left, h_left = cv2.boundingRect(left_cnt)
            x_right, y_right, w_right, h_right = cv2.boundingRect(right_cnt)
            
            # Calculate the left and right x-coordinates for the cropped region
            left_x = x_left + w_left
            right_x = x_right


            # Crop the region between the two lines, ':' takes the alpha channel
            cropped_column = row[y_left:y_left+h_left, left_x:right_x, :]
        
            columns.append(cropped_column)
        # Now, for the given requirement, we assume that there are at least two columns 
        if len(columns) >= 2:


            # Call the function extract_text on the first column
            file_name = extract_text(columns[0])


            # Skip rows with no part name or only white spaces
            if file_name is None or file_name.strip() == '':
                continue

            
            # convert the image to black and save
            columns[1][:,:,:3] = 0
            cv2.imwrite('/home/nev/cad_may12/output/' + file_name + '_black.png', columns[1])

            # convert the image to white and save
            columns[1][:,:,:3] = 255
            cv2.imwrite('/home/nev/cad_may12/output/' + file_name + '_white.png', columns[1])


def extract_table_data(table_img):

    gray_img = convert_BGR_to_gray(table_img)

    img_bin = threshold_and_invert(gray_img)

    ver_kernel, hor_kernel = get_line_kernels(gray_img)

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))

    #Use horizontal kernel to detect and save the horizontal lines in a jpg
    image_1 = cv2.erode(img_bin, hor_kernel, iterations=3)
    horizontal_lines = cv2.dilate(image_1, hor_kernel, iterations=3)

    contours, _ = cv2.findContours(horizontal_lines, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Sort all the contours by top to bottom.
    contours, boundingBoxes = sort_contours(contours, method='top-to-bottom')

    #filter the contours to remove lines that are not the part of the table
    filtered_contours = filter_contours_by_width(contours)

    # get each rows
    rows = get_rows(filtered_contours, table_img)
    
    extract_from_rows(rows)



def find_tables_from_img(og_src):

    gray_img = convert_BGR_to_gray(og_src)
    img_bin = threshold_and_invert(gray_img)

    kernel = np.ones((5, 5), np.uint8)
    dilated_value = cv2.dilate(img_bin, kernel, iterations=3)

    contours, hierarchy = cv2.findContours(dilated_value, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    coordinates = []
    areas = []  # List to store the areas of rectangles
    for cnt in contours:
        x,y,w,h = cv2.boundingRect(cnt)
        area = w * h
        areas.append(area)
        coordinates.append((x,y,w,h))

    # Find the index of the largest area in the areas list
    largest_area_index = max(range(len(areas)), key=lambda k: areas[k])
    largest_area = areas[largest_area_index]

    # Calculate the minimum area threshold
    min_table_area = largest_area * 0.5

    tables = []  # List to store the cropped table images

    for i in range(len(areas)):
        if areas[i] > min_table_area:  # Filter tables by checking if area is greater than the threshold
            x, y, w, h = coordinates[i]
            cropped_image = og_src[y:y+h, x:x+w]
            tables.append(cropped_image)
    return tables


# Specify the directory containing the files
directory = r'/home/nev/cad_may12'

# Iterate over all files in the directory
for filename in os.listdir(directory):

    # Check if the file is a PNG image file
    if filename.endswith('.png'):

         # Construct the full file path
        file_path = os.path.join(directory, filename)

        og_src = cv2.imread(file_path, cv2.IMREAD_UNCHANGED)

        tables = find_tables_from_img(og_src)

        for table in tables:
            extract_table_data(table)
