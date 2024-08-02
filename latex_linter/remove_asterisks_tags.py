"""
Remove the * character in align and equation environments to display tags
"""

import re
import pytest

def remove_asterisks_tags(content):
    """
    Remove the * character in align and equation environments in a LaTeX document to display tags.
    
    Args:
        content (str): The document content containing LaTeX environments.
    
    Returns:
        str: The processed document content with the * character removed from align and equation environments.
    """
    content = re.sub(r'\\(begin|end)\{(align|equation)\*\}', r'\\\1{\2}', content)
    return content

# Test cases
@pytest.mark.parametrize(
    "input_text, expected_output",
    [
        (r"\begin{align*} x + y = z \end{align*}", r"\begin{align} x + y = z \end{align}"),
        (r"\begin{equation*} a^2 + b^2 = c^2 \end{equation*}", r"\begin{equation} a^2 + b^2 = c^2 \end{equation}"),
        (r"\begin{align} x + y = z \end{align}", r"\begin{align} x + y = z \end{align}"),
        (r"\begin{equation} a^2 + b^2 = c^2 \end{equation}", r"\begin{equation} a^2 + b^2 = c^2 \end{equation}"),
        (r"Some text without environment.", r"Some text without environment."),
    ]
)
def test_remove_asterisks_tags(input_text, expected_output):
    assert remove_asterisks_tags(input_text) == expected_output

# Run tests
if __name__ == "__main__":
    pytest.main(["-v", __file__])