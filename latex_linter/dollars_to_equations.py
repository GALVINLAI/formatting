"""
Inline formulas: Replace $$ ... $$ with the equation environment
"""

import re
import pytest

# TODO The core logic below has a bug. If there is a single $$ in the comments, it will be replaced with the equation environment, which needs to be improved.


def dollars_to_equations(content):
    """
    Replace $$ in LaTeX documents with the equation environment and automatically standardize the internal format.
    
    Args:
        content (str): The document content containing $$ inline formulas.
    
    Returns:
        str: The processed document content, where $$ inline formulas have been replaced with the equation environment.
    """
    def fun_dollars_to_equations(match):
        nonlocal count
        count += 1
        if count % 2 == 1:
            return r'\begin{equation}'
        else:
            return r'\end{equation}'
    
    count = 0
    content = re.sub(r'\$\$', fun_dollars_to_equations, content)
    return content

# Test cases
@pytest.mark.parametrize(
    "input_text, expected_output",
    [
        ("This is an equation: $$a + b = c$$.", "This is an equation: \\begin{equation}a + b = c\\end{equation}."),
        ("Multiple equations: $$x + y = z$$ and $$a^2 + b^2 = c^2$$.", "Multiple equations: \\begin{equation}x + y = z\\end{equation} and \\begin{equation}a^2 + b^2 = c^2\\end{equation}."),
        ("No equations here.", "No equations here."),
        ("$$Single equation$$", "\\begin{equation}Single equation\\end{equation}"),
        ("Mixed content with $$a + b = c$$ and text.", "Mixed content with \\begin{equation}a + b = c\\end{equation} and text."),
    ]
)
def test_dollars_to_equations(input_text, expected_output):
    assert dollars_to_equations(input_text) == expected_output

# Run tests
if __name__ == "__main__":
    pytest.main(["-v", __file__])