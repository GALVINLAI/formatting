"""
Inline equations: Replace \[ ... \] with equation environment
"""

import re
import pytest

def square_brackets_to_equations(content):
    """
    Replace \\[ and \\] in LaTeX documents with the equation environment and automatically format the content inside.
    
    Args:
        content (str): The document content containing \\[ and \\] inline equations.
    
    Returns:
        str: The processed document content where \\[ and \\] have been replaced with the equation environment.
    """
    content = re.sub(r'\\\[', r'\\begin{equation}', content)
    content = re.sub(r'\\\]', r'\\end{equation}', content)
    return content

# Test cases
@pytest.mark.parametrize(
    "input_text, expected_output",
    [
        (r"This is an equation: \[a + b = c\].", "This is an equation: \\begin{equation}a + b = c\\end{equation}."),
        (r"Multiple equations: \[x + y = z\] and \[a^2 + b^2 = c^2\].", "Multiple equations: \\begin{equation}x + y = z\\end{equation} and \\begin{equation}a^2 + b^2 = c^2\\end{equation}."),
        (r"No equations here.", "No equations here."),
        (r"\[Single equation\]", "\\begin{equation}Single equation\\end{equation}"),
        (r"Mixed content with \[a + b = c\] and text.", "Mixed content with \\begin{equation}a + b = c\\end{equation} and text."),
    ]
)
def test_square_brackets_to_equations(input_text, expected_output):
    assert square_brackets_to_equations(input_text) == expected_output

# Run tests
if __name__ == "__main__":
    pytest.main(["-v", __file__])