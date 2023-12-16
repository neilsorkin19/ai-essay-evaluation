import os
import sys
import csv
import docx2txt
import fitz  # PyMuPDF
from PyPDF2 import PdfFileReader
import hashlib
import shutil

# Global index to track the order of processed documents
global_index = 1

def get_word_count(file_path):
    if file_path.endswith('.docx'):
        try:
            text = docx2txt.process(file_path)
            word_count = len(text.split())
        except Exception as e:
            word_count = 0
    elif file_path.endswith('.pdf'):
        try:
            pdf = fitz.open(file_path)
            word_count = 0
            for page_num in range(len(pdf)):
                page = pdf[page_num]
                text = page.get_text()
                word_count += len(text.split())
            pdf.close()
        except Exception as e:
            word_count = 0
    elif file_path.endswith('.txt'):
        try:
            with open(file_path, 'r', encoding='utf-8') as txt_file:
                text = txt_file.read()
                word_count = len(text.split())
        except Exception as e:
            word_count = 0
    else:
        word_count = 0
    return word_count

def generate_hashed_filename(foldername, index, file_extension):
    unique_identifier = f'{foldername}_{index}'.encode('utf-8')
    md5_hash = hashlib.md5(unique_identifier).hexdigest()
    return f'{md5_hash}{file_extension}'

def list_folders_and_files(root_folder, output_csv, copy_to_folder):
    global global_index
    try:
        hashed_filenames = set()
        with open(output_csv, 'w', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(['Global Index', 'Index', 'Old File Name', 'AI/Human', 'Parent Folder', 'File Extension', 'Word Count', 'Hashed Filename'])

            for foldername, subfolders, filenames in os.walk(root_folder):
                for index, filename in enumerate(filenames, start=1):
                    file_path = os.path.join(foldername, filename)
                    parent_folder = os.path.basename(os.path.normpath(foldername))
                    file_extension = os.path.splitext(filename)[1]
                    is_ai = "AI/Human"
                    word_count = get_word_count(file_path)
                    if "ai" in filename.lower():
                        is_ai = "AI"
                    elif "human" in filename.lower():
                        is_ai = "Human"

                    hashed_filename = generate_hashed_filename(parent_folder, index, file_extension)

                    # Ensure uniqueness of hashed filenames
                    if hashed_filename in hashed_filenames:
                        print(f"Error: Duplicate hashed filename '{hashed_filename}' found.")
                        continue
                    hashed_filenames.add(hashed_filename)

                    # Copy the file to the specified folder
                    destination_path = os.path.join(copy_to_folder, hashed_filename)
                    shutil.copy(file_path, destination_path)

                    csv_writer.writerow([global_index, index, filename, is_ai, parent_folder, file_extension, word_count, hashed_filename])

                    print(f'Global Index: {global_index}, Index: {index}, Old File Name: {filename}, AI/Human: {is_ai}, Parent Folder: {parent_folder}, File Extension: {file_extension}, Word Count: {word_count}, Hashed Filename: {hashed_filename}')
                    
                    global_index += 1

    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python parse_folders.py <path_to_folder> <output_csv> <copy_to_folder>")
        sys.exit(1)

    root_folder = sys.argv[1]
    if not os.path.isdir(root_folder):
        print(f"'{root_folder}' is not a valid directory.")
        sys.exit(1)

    output_csv = sys.argv[2]
    copy_to_folder = sys.argv[3]
    if not os.path.exists(copy_to_folder):
        os.makedirs(copy_to_folder)

    list_folders_and_files(root_folder, output_csv, copy_to_folder)
