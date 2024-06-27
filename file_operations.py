from tkinter import filedialog
import os
from text_processing import replace_text


def select_files():
    file_paths = filedialog.askopenfilenames(
        filetypes=[("Markdown files", "*.md"), ("LaTeX files", "*.tex"), ("All files", "*.*")])
    return file_paths


def replace_text_in_files(file_paths, options):
    for file_path in file_paths:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()

        modified_content = replace_text(content, options)

        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(modified_content)
        print(f"Text replaced in {file_path}")


def select_folder():
    folder_path = filedialog.askdirectory()
    return folder_path


def get_files_in_folder(folder_path):
    file_paths = []
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.tex') or file.endswith('.md'):
                file_paths.append(os.path.join(root, file))
    return file_paths
