# Project Introduction

**LatexFormatting** is a utility tool designed for formatting LaTeX and Markdown files. This tool offers multiple options to standardize mathematical formulas and text formatting, particularly for LaTeX formulas generated by ChatGPT.

## Main Features

1. **Add spaces between Chinese, Japanese, Korean characters and English or numbers**  
   Default enabled: ✅

2. **Convert multiple blank lines into a single blank line**  
   Default enabled: ✅

3. **Inline formulas: Standardize `$ ... $` environment**  
   Default enabled: ❌

4. **Inline formulas: Standardize `\( ... \)` environment**  
   Default enabled: ❌

5. **Inline formulas: Replace `\( ... \)` with `$ ... $` environment [Suitable for ChatGPT responses]**  
   Default enabled: ❌

6. **Display formulas: Standardize `equation` environment**  
   Default enabled: ❌

7. **Display formulas: Standardize `$$ ... $$` environment**  
   Default enabled: ❌

8. **Display formulas: Standardize `\[ ... \]` environment**  
   Default enabled: ❌

9. **Display formulas: Replace `\[ ... \]` with `$$ ... $$` environment [Suitable for ChatGPT responses]**  
   Default enabled: ❌

10. **Display formulas: Replace `equation` with `$$ ... $$` environment**  
    Default enabled: ❌

11. **Display formulas: Replace `\[ ... \]` with `equation` environment**  
    Default enabled: ❌

12. **Display formulas: Replace `$$ ... $$` with `equation` environment**  
    Default enabled: ❌

13. **Convert `aligned` environment embedded in `equation` into separate `align` environment**  
    Default enabled: ❌

14. **Remove `*` in `align` and `equation` environments for not displaying tags**  
    Default enabled: ❌

15. **Standardize `\item` format**  
    Default enabled: ❌

16. **Standardize headings at various levels**  
    Default enabled: ✅

17. **Convert Markdown headings into corresponding LaTeX elements**  
    Default enabled: ❌

18. **Convert Markdown's `**` enclosure into `\textbf` environment**  
    Default enabled: ❌

19. **Convert Markdown's `*` enclosure into `\textit` environment**  
    Default enabled: ❌

20. **Remove all Markdown features**  
    Default enabled: ❌

21. **Standardize `align` environment**  
    Default enabled: ❌

22. **Some small utility functions**  
    Default enabled: ❌

23. **Replace `equation` with `equation*` environment if there is no `label`**  
    Default enabled: ❌

## Additional Notes

1. The current checkbox status can be saved and automatically restored the next time it is opened.
2. Batch processing of all `.md` or `.tex` files in a folder is supported.
3. You can choose to automatically or manually copy the modified content.

# Usage

## Method 1: Open from Terminal (MAC or WINDOWS systems)

Ensure the `pyperclip` library is installed:
```sh
pip install pyperclip
```
Run `main.py` in the root directory to automatically open the user interface:
```sh
python main.py
```

## Method 2: Package into an executable file `formatting.exe` for use. Supports multiple instances. (WINDOWS systems only)

For specific packaging methods, see the development instructions below. [Warning] This software may be identified and removed by antivirus software, so please add it to the whitelist. For details, refer to [What to do if the exe packaged by PyInstaller is flagged by antivirus software](https://blog.csdn.net/cclbanana/article/details/136010033)

## ⚠️ Important Notes

If the output box on the right does not respond when the input box on the left changes, it indicates a bug. Please close and restart.

## If Typora cannot compile formulas normally

In `Typora` preferences, check if the `Markdown` settings.
# Development Instructions

## Environment Requirements

- Python 3.x
- Required Python libraries:
  - `tkinter` (`tk` is part of the Python standard library)
  - `pyperclip`
  - `pyinstaller` (if you need to generate an exe file separately)
  - Continuous development, add what's missing as needed

## Project Structure

```plaintext
project/
│
├── main.py                      # Main program file
├── icon.ico                     # Program icon
├── text_processing.py           # Text processing module
├── file_operations.py           # File operations module
└── README.md                    # Development instructions (this file)
```

## Code Structure Explanation

**`main.py`**: Main program file, containing the GUI interface and main logic.

**`text_processing.py`** and **`file_operations.py`** files contain specific text processing and file operation functions, to be defined according to project needs.

## How to Add Custom New Features

See the `how_add_new_features.md` file in the root directory for details.

## Building the Executable File `formatting.exe` (WINDOWS systems only)

Run the following in the directory where `main.py` is located to create an executable exe file using `PyInstaller`:
```sh
pyinstaller --onefile --noconsole --name formatting --icon=icon.ico --distpath ./ main.py
```
Or simply double-click `get_exe.bat`.

## Contribution Guide

1. Fork this project.
2. Create your feature branch (`git checkout -b feature/AmazingFeature`).
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`).
4. Push to the branch (`git push origin feature/AmazingFeature`).
5. Create a new Pull Request.

## Contact Information

For any questions or suggestions, please contact the author:

- Email: galvin.lai@outlook.com
- GitHub: [GALVINLAI](https://github.com/GALVINLAI/formatting)