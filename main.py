import tkinter as tk
from tkinter import messagebox, ttk
import pyperclip
import json
from text_processing import replace_text  # Your custom text processing module
from file_operations import select_files, replace_text_in_files, select_folder, get_files_in_folder  # Your custom file operations module
from datetime import datetime
from functools import partial

# Define metadata
metadata = {
    "title": "LatexFormatting (Latex Math Formula Source Code Formatter) [Under Continuous Development]",
    "author": "Lai Xiaodai",
    "version": "1.4",
    "update_date": "2024-07-30",
    "description": "A utility tool for formatting LaTeX and Markdown files.",
    "resource_url": "https://github.com/GALVINLAI/formatting",
    "email": "lai_zhijian@pku.edu.cn",
}

# Filename to save checkbox states
CHECKBOX_STATE_FILE = "checkbox_states.json"
LAST_STATE_NAME = "Last Closed State"

class ToolTip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip = None
        self.id = None
        widget.bind("<Enter>", self.schedule_tooltip)
        widget.bind("<Leave>", self.hide_tooltip)

    def schedule_tooltip(self, event):
        self.id = self.widget.after(700, self.show_tooltip)

    def show_tooltip(self):
        if self.tooltip or not self.text:
            return
        x, y, _, _ = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 25
        self.tooltip = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")
        label = tk.Label(tw, text=self.text, justify='left',
                         background="#ffffff", relief='solid', borderwidth=1,
                         wraplength=200)
        label.pack(ipadx=1)

    def hide_tooltip(self, event):
        if self.id:
            self.widget.after_cancel(self.id)
            self.id = None
        if self.tooltip:
            self.tooltip.destroy()
            self.tooltip = None

def get_options():
    """
    Get the values of all checkboxes and return a dictionary containing all options.
    """
    return {local_key: var.get() for local_key, var in checkbox_vars.items()}

def save_checkbox_states(state_name=LAST_STATE_NAME):
    """
    Save the states of the checkboxes to a file.
    """
    options = get_options()
    options["auto_copy"] = auto_copy_checkbox_var.get()

    all_states = load_all_states()
    all_states[state_name] = options

    with open(CHECKBOX_STATE_FILE, 'w', encoding='utf-8') as f:
        json.dump(all_states, f, ensure_ascii=False, indent=4)

    update_state_menu()

def load_checkbox_states(state_name=None, show_warning=False):
    """
    Load the checkbox states from a file.
    """
    try:
        with open(CHECKBOX_STATE_FILE, 'r', encoding='utf-8') as f:
            all_states = json.load(f)
            if state_name and state_name in all_states:
                options = all_states[state_name]
                for key, value in options.items():
                    if key in checkbox_vars:
                        checkbox_vars[key].set(value)
                if "auto_copy" in options:
                    auto_copy_checkbox_var.set(options["auto_copy"])
                CURRENT_STATE_VAR.set(state_name)  # Update the current state variable
                update_state_menu()  # Update the menu display
            elif show_warning:
                messagebox.showwarning("Warning", "Invalid or non-existent state name.")
    except FileNotFoundError:
        pass

def load_all_states():
    """
    Load all saved states.
    """
    try:
        with open(CHECKBOX_STATE_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def update_output_text(event=None):
    """
    Get the text from the input text box, process it according to the options, and display the modified text in the output text box, also copy to clipboard if the checkbox is checked.
    """
    input_text = input_text_widget.get("1.0", tk.END)  # Get the content of the input text box
    options = get_options()  # Get the options
    modified_text = replace_text(input_text, options)  # Process the text
    output_text_widget.delete("1.0", tk.END)  # Clear the output text box
    output_text_widget.insert(tk.END, modified_text)  # Insert the modified text
    if auto_copy_checkbox_var.get():  # If the auto-copy checkbox is checked
        pyperclip.copy(modified_text)  # Copy the modified text to the clipboard
    check_state_match()  # Check if the current state matches any saved state

def copy_to_clipboard():
    """
    Copy the content of the output text box to the clipboard.
    """
    modified_text = output_text_widget.get("1.0", tk.END)
    pyperclip.copy(modified_text)

def clear_text_boxes():
    """
    Clear the content of the input and output text boxes.
    """
    input_text_widget.delete("1.0", tk.END)
    output_text_widget.delete("1.0", tk.END)

def process_files(file_paths):
    """
    Process the selected files according to the options and display a completion message.
    """
    if file_paths:
        options = get_options()  # Get the options
        replace_text_in_files(file_paths, options)  # Process the files
        messagebox.showinfo("Completed", "All selected files have been modified.")
    else:
        print("No files selected")

def open_and_replace_files():
    """
    Open the file selection dialog and process the selected files.
    """
    file_paths = select_files()
    process_files(file_paths)

def open_and_replace_files_in_folder():
    """
    Open the folder selection dialog and process all files in the folder.
    """
    folder_path = select_folder()
    if folder_path:
        file_paths = get_files_in_folder(folder_path)
        process_files(file_paths)
    else:
        print("No folder selected")

def show_about():
    """
    Show an about information dialog.
    """
    about_message = (
        f"{metadata['title']}\n\n"
        f"Author: {metadata['author']}\n"
        f"Version: {metadata['version']}\n"
        f"Update Date: {metadata['update_date']}\n\n"
        f"{metadata['description']}\n\n"
        f"Resource URL: {metadata['resource_url']}\n"
        f"Contact Email: {metadata['email']}"
    )
    messagebox.showinfo("About", about_message)

def create_button(frame, text, command, tooltip_text):
    """
    Create a button and add it to the specified frame.
    """
    button = ttk.Button(frame, text=text, command=command)
    button.pack(side=tk.LEFT, padx=5, pady=5)
    ToolTip(button, tooltip_text)  # Add tooltip

def create_checkbox(frame, text, var, row, col):
    """
    Create a checkbox and add it to the specified frame, specifying row and column.
    """
    checkbox = ttk.Checkbutton(frame, text=text, variable=var, takefocus=False)
    checkbox.grid(row=row, column=col, sticky='w', padx=5, pady=2)
    var.trace_add('write', on_checkbox_change)  # Add trace method

def update_state_menu():
    """
    Update the dropdown menu to show all saved states.
    """
    state_menu['menu'].delete(0, 'end')
    all_states = load_all_states()
    current_state = CURRENT_STATE_VAR.get()
    for state_name in all_states.keys():
        label = state_name
        if state_name == current_state:
            label = f"✓ {state_name}"  # Add a checkmark before the current state
        state_menu['menu'].add_command(label=label, command=partial(load_checkbox_states, state_name, True))
def open_save_state_popup():
    """
    Open a popup window to input a state name to save the current state.
    """
    popup = tk.Toplevel(root)
    popup.title("Save State")

    tk.Label(popup, text="Enter new state name:").pack(side=tk.LEFT, padx=5, pady=5)
    state_name_entry = ttk.Entry(popup, width=20)
    state_name_entry.pack(side=tk.LEFT, padx=5, pady=5)

    def on_save():
        state_name = state_name_entry.get()
        if state_name:
            all_states = load_all_states()
            if state_name in all_states:
                # Prompt to overwrite existing state
                if messagebox.askyesno("Confirm", f"State '{state_name}' already exists. Overwrite?"):
                    save_checkbox_states(state_name)
                    CURRENT_STATE_VAR.set(state_name)  # Update current state variable
                    popup.destroy()
                else:
                    popup.destroy()
            else:
                save_checkbox_states(state_name)
                CURRENT_STATE_VAR.set(state_name)  # Update current state variable
                popup.destroy()
        else:
            messagebox.showwarning("Warning", "Please provide a state name.")

    save_button = ttk.Button(popup, text="Save", command=on_save)
    save_button.pack(side=tk.LEFT, padx=5, pady=5)

def check_state_match():
    """
    Check if the current checkbox state matches any saved state.
    If not, clear the current state.
    """
    options = get_options()
    options["auto_copy"] = auto_copy_checkbox_var.get()
    all_states = load_all_states()

    for state_name, saved_options in all_states.items():
        if options == saved_options:
            CURRENT_STATE_VAR.set(state_name)
            update_state_menu()
            return

    CURRENT_STATE_VAR.set("")  # No matching state
    update_state_menu()

def on_checkbox_change(*args):
    """
    Function called when the checkbox state changes.
    """
    check_state_match()

# Create main window
root = tk.Tk()
root.title(f"{metadata['title']} Version: {metadata['version']} Update Date: {metadata['update_date']}")
# Set window icon
root.iconbitmap("icon.ico")

# Initialize CURRENT_STATE_VAR after creating the main window
CURRENT_STATE_VAR = tk.StringVar(root)

# Set style
style = ttk.Style()
style.configure("TButton", padding=1, relief="flat", background="#ccc")
style.configure("TCheckbutton", padding=3)
style.configure("TRadiobutton", padding=3)

# Create button frame and add buttons
button_frame = ttk.Frame(root)
button_frame.pack(pady=10)

# Create dropdown menu for bulk modification of files or folders
bulk_menu_button = ttk.Menubutton(button_frame, text="Bulk Modify Files or Folders", direction="below")
bulk_menu = tk.Menu(bulk_menu_button, tearoff=0)
bulk_menu.add_command(label="Select md or tex files and modify", command=open_and_replace_files)
bulk_menu.add_command(label="Select folder and modify all md and tex files", command=open_and_replace_files_in_folder)
bulk_menu_button["menu"] = bulk_menu
bulk_menu_button.pack(side=tk.LEFT, padx=5, pady=5)

# Create state selection dropdown menu
state_var = tk.StringVar(root)
state_menu = ttk.OptionMenu(button_frame, state_var, "Select Task State", *[])
state_menu.pack(side=tk.LEFT, padx=5)
update_state_menu()

# Add save state button
save_button = ttk.Button(button_frame, text="Save and Name Current Task State", command=open_save_state_popup)
save_button.pack(side=tk.LEFT, padx=5)

create_button(button_frame, "About", show_about, "")

# Create a frame with scrollbar
container = ttk.Frame(root)
container.pack(pady=12, fill='both', expand=True)

canvas = tk.Canvas(container, height=300)
scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview, width=20)
options_frame = ttk.Frame(canvas)

options_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(
        scrollregion=canvas.bbox("all")
    )
)

canvas.create_window((0, 0), window=options_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

# Add mouse wheel support
def on_mouse_wheel(event):
    canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

canvas.bind("<Enter>", lambda event: canvas.bind_all("<MouseWheel>", on_mouse_wheel))
canvas.bind("<Leave>", lambda event: canvas.unbind_all("<MouseWheel>"))

options = [
    ("new_feature_name", "Custom New Feature (for demonstration only)", False),
    ("add_space_between_cjk_and_english", "Add space between CJK characters and English or numbers", True),
    ("remove_extra_newlines", "Turn multiple blank lines into single blank lines", True),
    ("format_single_dollar", "Inline formulas: Standardize $ ... $ environment", False),
    ("format_parentheses", "Inline formulas: Standardize \\( ... \\) environment", False),
    ("parentheses_to_single_dollar", "Inline formulas: Replace \\( ... \\) with $ ... $ environment [suitable for ChatGPT's responses]", False),
    ("format_equations", "Block formulas: Standardize equation environment", False),
    ("format_dollars", "Block formulas: Standardize $$ ... $$ environment", False),
    ("format_square_brackets", "Block formulas: Standardize \\[ ... \\] environment", False),
    ("square_brackets_to_dollars", "Block formulas: Replace \\[ ... \\] with $$ ... $$ environment [suitable for ChatGPT's responses]", False),
    ("equations_to_dollars", "Block formulas: Replace equation with $$ ... $$ environment", False),
    ("square_brackets_to_equations", "Block formulas: Replace \\[ ... \\] with equation environment", False),
    ("dollars_to_equations", "Block formulas: Replace $$ ... $$ with equation environment", False),
    ("replace_equation_aligned", "Replace aligned environment embedded in equation with separate align environment", False),
    ("remove_asterisks_tags", "Remove * for no display tags in align and equation environments", False),
    ("format_item", "Standardize \\item format", False),
    ("capitalize_titles", "Standardize titles at all levels", True),
    ("convert_markdown_titles_to_latex", "Convert Markdown titles to corresponding LaTeX elements", False),
    ("replace_stars_with_textbf", "Replace Markdown's ** enclosure with \\textbf environment", False),
    ("replace_stars_with_textit", "Replace Markdown's * enclosure with \\textit environment", False),
    ("replace_all_markdown", "Remove all Markdown features", False),
    ("format_aligns", "Standardize align environment", False),
    ("some_small_utilities", "some_small_utilities", False),
    ("equations_to_equations_star", "Replace equation with equation* environment if no label", False),
    ("format_for_zulip", "Make inline and block formulas conform to Zulip syntax", False)
]

checkbox_vars = {option[0]: tk.BooleanVar(value=option[2]) for option in options}

# Determine if the length of options is odd or even to decide if padding is needed.
half = len(options) // 2 if len(options) % 2 == 0 else len(options) // 2 + 1

for idx, (key, text, _) in enumerate(options):
    col = 0 if idx < half else 1
    row = idx % half
    create_checkbox(options_frame, text, checkbox_vars[key], row, col)

# Create container for text boxes and labels
text_frame = ttk.Frame(root)
text_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=10)

# Create left text box and label
left_frame = ttk.LabelFrame(text_frame, text="Original Content (e.g., GPT's response)", padding=10)
left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
input_text_widget = tk.Text(left_frame, wrap="word", width=50, height=10, font=("Consolas", 10))
input_text_widget.pack(fill=tk.BOTH, expand=True)

# Create right text box and label
right_frame = ttk.LabelFrame(text_frame, text="Modified Content", padding=10)
right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)
output_text_widget = tk.Text(right_frame, wrap="word", width=50, height=10, font=("Consolas", 10))
output_text_widget.pack(fill=tk.BOTH, expand=True)

# Add checkboxes and buttons to the right text box container
auto_copy_checkbox_var = tk.BooleanVar()
auto_copy_checkbox = ttk.Checkbutton(right_frame, text="Automatically copy modified content", variable=auto_copy_checkbox_var)
auto_copy_checkbox.pack(side=tk.LEFT, padx=5, pady=5)

copy_button = ttk.Button(right_frame, text="Copy to Clipboard", command=copy_to_clipboard)
copy_button.pack(side=tk.LEFT, padx=5, pady=5)

clear_button = ttk.Button(right_frame, text="Clear Text Boxes", command=clear_text_boxes)
clear_button.pack(side=tk.LEFT, padx=5, pady=5)

def on_input_text_change(event):
    """
    Detect changes in the input text box and trigger updates in the output text box.
    """
    input_text_widget.edit_modified(False)
    update_output_text()

input_text_widget.bind("<<Modified>>", on_input_text_change)

# Load checkbox states before starting the main loop
load_checkbox_states(LAST_STATE_NAME)

# Save state when window is closed
def on_closing():
    save_checkbox_states(LAST_STATE_NAME)
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)

# Start the main loop
root.mainloop()