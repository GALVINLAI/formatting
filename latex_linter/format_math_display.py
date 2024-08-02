import re
import pytest


def format_math_display(match):
    """
    Standardize the internal format of displayed equations.
    
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

    # Extract and remove \label part
    # .*? is a non-greedy match, meaning it matches any character until it encounters the first }
    label_text = re.findall(r'\\label\{.*?\}', text)
    text = re.sub(r'\\label\{.*?\}', '', text)

    # Strip leading and trailing whitespace characters
    text = text.strip()

    # Replace internal consecutive whitespace characters (except \n) with a single space. This implies that internal newlines are allowed.
    text = re.sub(r'[\t\v\f\r \u00a0\u2000-\u200b\u2028-\u2029\u3000]{2,}', ' ', text)

    # Organize existing newline characters, indenting each line with 4 spaces
    text = re.sub(r'\s*\n\s*', '\n    ', text)

    # Reassemble text, adding labels and formatting
    # TODO Cannot handle multiple labels in align environment
    if label_text:
        label_text = label_text[0]  # Assume there is only one \label
        # Place label at the beginning
        text = f'{label_text}\n    {text}'
    else:
        text = f'\n    {text}'
        
    # Combine results and return
    formatted_text = f'\n{match.group(1).strip()}{text}\n{match.group(3).strip()}\n'

    return formatted_text
    

# ---------- Standardize equation environment ----------
def format_equations(content):
    # Special attention: this match must be flags=re.DOTALL, i.e., single-line mode
    content = re.sub(r'(\s*\\begin\{equation\*?\})(.*?)(\\end\{equation\*?\}\s*)', format_math_display, content, flags=re.DOTALL)
    return content


# ---------- Standardize $$ ... $$ environment ----------
def format_dollars(content):
    # Special attention: this match must be flags=re.DOTALL, i.e., single-line mode
    content = re.sub(r'(\s*\$\$)(.*?)(\$\$\s*)', format_math_display, content, flags=re.DOTALL)
    return content


# ---------- Standardize \[ ... \ ] environment ----------
def format_square_brackets(content):
    # Special attention: this match must be flags=re.DOTALL, i.e., single-line mode
    content = re.sub(r'(\s*\\\[)(.*?)(\\\]\s*)', format_math_display, content, flags=re.DOTALL)
    return content

# -- Testing ----------

@pytest.mark.parametrize(
    "input_text, expected_output",
    [
        (
            "$$ x + y = z $$",
            "\n$$\n    x + y = z\n$$\n"
        ),
        (
            "$$ a^2 + b^2 = c^2 $$",
            "\n$$\n    a^2 + b^2 = c^2\n$$\n"
        ),
        (
            "$$\n    x + y = z $$",
            "\n$$\n    x + y = z\n$$\n"
        ),
        (
            "No equations here.",
            "No equations here."
        ),
        (
            "Multiple equations: $$ x + y = z $$ and $$ a^2 + b^2 = c^2 $$.",
            "Multiple equations:\n$$\n    x + y = z\n$$\nand\n$$\n    a^2 + b^2 = c^2\n$$\n."
        ),
    ]
)
def test_format_dollars(input_text, expected_output):
    assert format_dollars(input_text) == expected_output