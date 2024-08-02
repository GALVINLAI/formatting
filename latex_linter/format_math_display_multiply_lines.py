import re
import pytest


def format_math_display_multiply_lines(match):
    """
    Standardize the internal format of display equations.
    
    Args:
        match (re.Match): Regular expression match object containing the entire matched text.
            Expected match.group(1) to be the content before the equation (i.e., $$, \begin{equation}, \[).
            Expected match.group(2) to be the equation content.
            Expected match.group(3) to be the content after the equation (i.e., $$, \end{equation}, \]).
    
    Returns:
        str: The formatted text, including equation labels (if any), equation content, and surrounding text.
    """
    # Extract equation content
    text = match.group(2)

    # # Extract and remove \label part
    # # .*? is a non-greedy match, meaning it matches any character until it encounters the first }
    # label_text = re.findall(r'\\label\{.*?\}', text)
    # text = re.sub(r'\\label\{.*?\}', '', text)

    # Strip leading and trailing whitespace characters
    text = text.strip()

    # Replace internal consecutive whitespace characters (except \n) with a single space. This implies that internal newlines are allowed.
    text = re.sub(r'[\t\v\f\r \u00a0\u2000-\u200b\u2028-\u2029\u3000]{2,}', ' ', text)

    # Organize existing newline characters, indenting each line with 4 spaces
    text = re.sub(r'\s*\n\s*', '\n    ', text)

    text = f'\n    {text}'
        
    # Combine the result and return
    formatted_text = f'\n{match.group(1).strip()}{text}\n{match.group(3).strip()}\n'

    return formatted_text
    

# ---------- Standardize align environment ----------
def format_aligns(content):
    # Special attention, this match must be flags=re.DOTALL, i.e., single-line mode
    content = re.sub(r'(\s*\\begin\{align\*?\})(.*?)(\\end\{align\*?\}\s*)', format_math_display_multiply_lines, content, flags=re.DOTALL)
    return content