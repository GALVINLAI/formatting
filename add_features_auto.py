import os
import argparse
import sys

'''
This code is designed to automate the integration of new features into an existing Python project. It achieves support for new features by inserting necessary code into the text_processing.py and main.py files. The user needs to provide the name and description of the new feature, which must be enclosed in single quotes. The code performs the following actions:

Import the new feature: Add an import statement in text_processing.py.
Function call: Add or update the function call and comments in text_processing.py.
Update options: Add or update the feature description in main.py to display in the GUI.
'''

def update_text_processing_file(feature_name, feature_description, text_processing_file='text_processing.py'):
    # Update the text_processing.py file
    with open(text_processing_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()  # Read all lines in the file
    
    # Check if the new feature is already integrated
    import_statement = f'from latex_linter.{feature_name} import {feature_name}\n'
    function_call = f"    # ---------- {feature_description} ----------\n    if options['{feature_name}']:\n        content = {feature_name}(content)\n\n"
    
    # If the import statement is not added, add it at the beginning of the import statements
    if import_statement not in lines:
        # Find the position of the first non-import statement and insert the import statement there
        for i, line in enumerate(lines):
            if line.startswith('import') or line.startswith('from'):
                continue
            else:
                lines.insert(i, import_statement)
                break
    
    # Check if the new feature's call already exists and update the comment
    feature_updated = False
    for i, line in enumerate(lines):
        if line.strip().startswith(f"# ----------") and f"if options['{feature_name}']:" in lines[i+1]:
            # Update the comment with the new feature description
            lines[i] = f"    # ---------- {feature_description} ----------\n"
            feature_updated = True
            print(f"Updated comment for {feature_name} in {text_processing_file}.")
            break

    # If the function call does not exist, insert the new feature call before the last return
    if not feature_updated:
        for i in reversed(range(len(lines))):
            if lines[i].strip().startswith('return'):
                lines.insert(i, function_call)
                print(f"Added new feature call for {feature_name} in {text_processing_file}.")
                break
    
    # Write the updated content back to the file
    with open(text_processing_file, 'w', encoding='utf-8') as file:
        file.writelines(lines)
    
    print(f"Integrated {feature_name} into {text_processing_file}.")

def update_main_file(feature_name, feature_description, main_file='main.py'):
    # Update the main.py file
    with open(main_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()  # Read all lines in the file

    # Define the option line
    option_line = f'    ("{feature_name}", "{feature_description}", False),\n'
    option_updated = False
    
    # Check and update the feature option
    for i, line in enumerate(lines):
        # Find the line corresponding to the feature name and update the description
        if line.strip().startswith(f'("{feature_name}",'):
            parts = line.split(',')
            if len(parts) >= 3:
                # Update the description
                parts[1] = f' "{feature_description}"'
                lines[i] = ','.join(parts)
                option_updated = True
                print(f"Updated description for {feature_name} in {main_file}.")
            break
    
    # If the option line does not exist, add it to the options list
    if not option_updated:
        for i, line in enumerate(lines):
            if line.strip().startswith('options = ['):
                lines.insert(i+1, option_line)
                print(f"Added new option for {feature_name} in {main_file}.")
                break

    # Write the updated content back to the file
    with open(main_file, 'w', encoding='utf-8') as file:
        file.writelines(lines)

    print(f"Updated options in {main_file}.")

if __name__ == "__main__":
    # Create parser
    parser = argparse.ArgumentParser(description="Integrate new features into existing Python files.")
    
    # Add command line arguments
    parser.add_argument('--name', required=True, help='The name of the new feature to be integrated, must be the name of a py file in the latex_linter folder containing a function of the same name.')
    parser.add_argument('--description', required=True, help='The textual description of the new feature, must be enclosed in single quotes, displayed in the GUI.')

    # Example usage
    # python add_features_auto.py --name new_feature_name --description 'Custom new feature (for demonstration purposes only)'  

    # Parse arguments
    args = parser.parse_args()
    
    # Get command line arguments
    feature_name = args.name
    feature_description = args.description

    # Check if feature_description is enclosed in single quotes
    if not (feature_description.startswith("'") and feature_description.endswith("'")):
        print("Error: The feature description must be enclosed in single quotes.")
        sys.exit(1)

    # Remove single quotes
    feature_description = feature_description[1:-1]
    
    # Call the feature integration functions
    update_text_processing_file(feature_name, feature_description)
    update_main_file(feature_name, feature_description)