"""
Convert the aligned environment embedded in equation to a separate align environment.
"""

import re
import pytest

def replace_equation_aligned(content):
    """
    Convert the aligned environment embedded in equation to a separate align environment.
    
    Args:
        content (str): The document content containing LaTeX environments.
    
    Returns:
        str: The processed document content, where the aligned environment embedded in equation has been replaced with a separate align environment.
    """
    content = re.sub(r'\\begin{equation(\*?)}\s*\\begin{aligned(\*?)}', r'\\begin{align\2}', content)
    content = re.sub(r'\\end{aligned(\*?)}\s*\\end{equation(\*?)}', r'\\end{align\1}', content)
    return content

# Test cases
@pytest.mark.parametrize(
    "input_text, expected_output",
    [
        (r"\begin{equation}\begin{aligned} x + y = z \end{aligned}\end{equation}", r"\begin{align} x + y = z \end{align}"),
        (r"\begin{equation*}\begin{aligned*} a^2 + b^2 = c^2 \end{aligned*}\end{equation*}", r"\begin{align*} a^2 + b^2 = c^2 \end{align*}"),
        (r"No LaTeX content here.", "No LaTeX content here."),
        (r"Mixed content \begin{equation}\begin{aligned} a = b \end{aligned}\end{equation} and text.", r"Mixed content \begin{align} a = b \end{align} and text."),
    ]
)
def test_replace_equation_aligned(input_text, expected_output):
    assert replace_equation_aligned(input_text) == expected_output

# Run tests
if __name__ == "__main__":
    pytest.main(["-v", __file__])