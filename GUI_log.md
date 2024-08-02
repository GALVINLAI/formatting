# GUI Features Log

The log for version 1.4 is a summary of all previous features. Going forward, new features added in future versions will be documented separately.

## Version 1.X (X>4)

## Version: 1.4
Update Date: 2024-07-30
Author: Lai Xiaodai

### Overview
LatexFormatting is a utility tool for formatting LaTeX and Markdown files with a rich set of GUI features. This log documents all the GUI features of the tool in version 1.4.

### Main Window
- **Title**: Displays the application name and version information.
- **Icon**: Uses a custom icon (`icon.ico`).

### Menus and Buttons
- **Batch Modify Files or Folders Menu**:
  - **Select md or tex files and modify**: Opens a file selection dialog to choose and modify selected files.
  - **Select a folder and modify all md and tex files**: Opens a folder selection dialog to choose and modify all files in the folder.

- **Status Selection Dropdown Menu**: Displays all saved statuses, allowing users to select and load a status.

- **Save Status Button**: Opens a popup window to input a status name and save the current checkbox status.

- **About Button**: Displays an about dialog with basic information about the tool and author contact information.

### Text Boxes and Containers
- **Left Text Box**: Input the original content (e.g., GPT's response).
- **Right Text Box**: Displays the modified content.

### Checkboxes and Options
Provides the following options to format LaTeX and Markdown files:
1. Add spaces between Chinese, Japanese, and Korean characters and English or numbers
2. Convert multiple blank lines into a single blank line
3. Inline formulas: Standardize the `$ ... $` environment
4. Inline formulas: Standardize the `\( ... \)` environment
5. Inline formulas: Replace `\( ... \)` with `$ ... $` environment [suitable for ChatGPT's responses]
6. Display formulas: Standardize the `equation` environment
7. Display formulas: Standardize the `$$ ... $$` environment
8. Display formulas: Standardize the `\[ ... \]` environment
9. Display formulas: Replace `\[ ... \]` with `$$ ... $$` environment [suitable for ChatGPT's responses]
10. Display formulas: Replace `equation` with `$$ ... $$` environment
11. Display formulas: Replace `\[ ... \]` with `equation` environment
12. Display formulas: Replace `$$ ... $$` with `equation` environment
13. Convert `aligned` environments embedded in `equation` into separate `align` environments
14. Remove the * used in `align` and `equation` environments to hide tags
15. Standardize `\item` format
16. Standardize headings at various levels
17. Convert Markdown headings into corresponding LaTeX elements
18. Convert Markdown's `**` enclosure into the `\textbf` environment
19. Convert Markdown's `*` enclosure into the `\textit` environment
20. Remove all Markdown features
21. Standardize the `align` environment
22. some_small_utilities
23. Replace `equation` with `equation*` environment if there is no label
24. Make inline and display formulas conform to zulip syntax

### Other Features
- **Auto Copy**: Automatically copies the modified content to the clipboard.
- **Copy Button**: Copies the content in the output text box to the clipboard.
- **Clear Button**: Clears the content in the input and output text boxes.
- **Input Text Box Modification Listener**: Detects modifications in the input text box and triggers updates in the output text box.

### Status Management
- **Save Checkbox Status**: Saves the current checkbox status to a file.
- **Load Checkbox Status**: Loads the checkbox status from a file.
- **Update Status Menu**: Updates the dropdown menu to display all saved statuses.
- **Check Status Match**: Checks if the current checkbox status matches any saved status.

### Window Close Event
- **Save Status**: Saves the current checkbox status when the window is closed.