"""
Inline equations: Replace equation with $$ ... $$ environment
"""

import re
import pytest

def equations_to_dollars(content):
    """
    Replace equation environment in LaTeX document with $$ environment.
    
    Args:
        content (str): Document content containing equation environment.
    
    Returns:
        str: Processed document content with equation environment replaced by $$ environment.
    """
    content = re.sub(r'\\begin\{equation\}|\\end\{equation\}', '$$', content)
    return content

# Test cases
@pytest.mark.parametrize(
    "input_text, expected_output",
    [
        (r"This is an equation: \begin{equation}a + b = c\end{equation}.", r"This is an equation: $$a + b = c$$."),
        (r"Multiple equations: \begin{equation}x + y = z\end{equation} and \begin{equation}a^2 + b^2 = c^2\end{equation}.", r"Multiple equations: $$x + y = z$$ and $$a^2 + b^2 = c^2$$."),
        (r"No equations here.", r"No equations here."),
        (r"\begin{equation}Single equation\end{equation}", r"$$Single equation$$"),
        (r"Mixed content with \begin{equation}a + b = c\end{equation} and text.", r"Mixed content with $$a + b = c$$ and text."),
    ]
)
def test_equations_to_dollars(input_text, expected_output):
    assert equations_to_dollars(input_text) == expected_output

# Run tests
if __name__ == "__main__":
    pytest.main(["-v", __file__])