"""
Inline formulas: Replace \( ... \) with $ ... $ environment
"""

import re
import pytest

def parentheses_to_single_dollar(content):
    """
    Replace \( and \) in LaTeX documents with $ surrounding.
    
    Args:
        content (str): The document content containing LaTeX inline formulas.
    
    Returns:
        str: The processed document content where \( and \) have been replaced with $.
    """
    content = re.sub(r'\\\(|\\\)', '$', content)
    return content

# Test cases
@pytest.mark.parametrize(
    "input_text, expected_output",
    [
        (r"This is inline math: \(a + b = c\).", "This is inline math: $a + b = c$."),
        (r"Multiple formulas: \(x + y = z\) and \(a^2 + b^2 = c^2\).", "Multiple formulas: $x + y = z$ and $a^2 + b^2 = c^2$."),
        (r"No math content here.", "No math content here."),
        (r"Already $a + b = c$ format.", "Already $a + b = c$ format."),
        (r"Mixed \(a + b = c\) and $x + y = z$ formats.", "Mixed $a + b = c$ and $x + y = z$ formats."),
    ]
)
def test_parentheses_to_single_dollar(input_text, expected_output):
    assert parentheses_to_single_dollar(input_text) == expected_output

# Run tests
if __name__ == "__main__":
    pytest.main(["-v", __file__])