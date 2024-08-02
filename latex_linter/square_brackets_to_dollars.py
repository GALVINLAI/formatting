"""
Inline equations: Replace \[ ... \] with $$ ... $$ environment
"""

import re
import pytest

def square_brackets_to_dollars(content):
    """
    Replace \\[ and \\] in a LaTeX document with $$ environment.
    
    Args:
        content (str): The document content containing \\[ and \\].
    
    Returns:
        str: The processed document content with \\[ and \\] replaced by $$.
    """
    content = re.sub(r'\\\[|\\\]', '$$', content)
    return content

# Test cases
@pytest.mark.parametrize(
    "input_text, expected_output",
    [
        (r"This is an equation: \[a + b = c\].", "This is an equation: $$a + b = c$$."),
        (r"Multiple equations: \[x + y = z\] and \[a^2 + b^2 = c^2\].", "Multiple equations: $$x + y = z$$ and $$a^2 + b^2 = c^2$$."),
        (r"No equations here.", "No equations here."),
        (r"\[Single equation\]", "$$Single equation$$"),
        (r"Mixed content with \[a + b = c\] and text.", "Mixed content with $$a + b = c$$ and text."),
    ]
)
def test_square_brackets_to_dollars(input_text, expected_output):
    assert square_brackets_to_dollars(input_text) == expected_output

# Run tests
if __name__ == "__main__":
    pytest.main(["-v", __file__])