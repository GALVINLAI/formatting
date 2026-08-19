from PySide6.QtWidgets import QFileDialog
import os
from text_processing import replace_text


def select_files():
    """打开文件选择对话框，返回选中的文件路径列表。"""
    file_paths, _ = QFileDialog.getOpenFileNames(
        None,
        "选择文件",
        "",
        "Markdown files (*.md);;LaTeX files (*.tex);;All files (*.*)"
    )
    return file_paths


def replace_text_in_files(file_paths, options):
    """对选中的文件批量执行文本替换。"""
    for file_path in file_paths:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()

        modified_content = replace_text(content, options)

        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(modified_content)
        print(f"Text replaced in {file_path}")


def select_folder():
    """打开文件夹选择对话框，返回选中的文件夹路径。"""
    folder_path = QFileDialog.getExistingDirectory(
        None,
        "选择文件夹",
        ""
    )
    return folder_path


def get_files_in_folder(folder_path):
    """递归获取文件夹中所有 .md 和 .tex 文件的路径。"""
    file_paths = []
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.tex') or file.endswith('.md'):
                file_paths.append(os.path.join(root, file))
    return file_paths
