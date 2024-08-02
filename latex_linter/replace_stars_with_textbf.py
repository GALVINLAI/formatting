"""

"""
import re
import pytest

def replace_stars_with_textbf(text):
    """
    Replace content surrounded by double asterisks with \\textbf{} format in LaTeX.
    
    Args:
        text (str): The input text string to be processed.
    
    Returns:
        str: The processed text string with content surrounded by double asterisks replaced with \\textbf{} format.
    
    """
    # Use a lambda function for replacement, placing the matched content inside \textbf{}
    replacement = lambda match: r"\textbf{" + match.group(1) + "}"
    new_text = re.sub(r"\*{2}(.*?)\*{2}", replacement, text)
    return new_text

# Test cases
@pytest.mark.parametrize(
    "input_text, expected_output",
    [
        ("This is **bold** text.", "This is \\textbf{bold} text."),
        ("**Bold** at the start.", "\\textbf{Bold} at the start."),
        ("At the end **bold**.", "At the end \\textbf{bold}."),
        ("**Bold** everywhere **bold**.", "\\textbf{Bold} everywhere \\textbf{bold}."),
        ("No bold here.", "No bold here."),
        ("Mix **bold** and normal **text**.", "Mix \\textbf{bold} and normal \\textbf{text}."),
#        ("Nested **bold **in** bold**.", "Nested \\textbf{bold **in** bold}."),
    ]
)
def test_replace_stars_with_textbf(input_text, expected_output):
    assert replace_stars_with_textbf(input_text) == expected_output

# Run tests
if __name__ == "__main__":
    pytest.main(["-v", __file__])