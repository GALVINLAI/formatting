"""
Standardize \item formatting
"""

import re
import pytest

def format_item(content):
    """
    Standardize the formatting of \\item in LaTeX documents to ensure each \\item is preceded by exactly one tab and followed by exactly one space.
    
    Args:
        content (str): The document content containing LaTeX list items.
    
    Returns:
        str: The processed document content with the \\item formatting standardized.
    """
    content = re.sub(r'(?<!\t)\s*\\item\s*', r'\n    \\item ', content)
    return content

      
# Test cases
@pytest.mark.parametrize(
    "input_text, expected_output",
    [
        ("\\item First item", "\n    \\item First item"),
        (" \\item Second item", "\n    \\item Second item"),
        ("\n\\item Third item", "\n    \\item Third item"),
        ("\\item    Fourth item", "\n    \\item Fourth item"),
        ("Text without items.", "Text without items."),
        ("\\begin{itemize}\n\\item Item 1\n\\item  Item 2\n\\end{itemize}", "\\begin{itemize}\n    \\item Item 1\n    \\item Item 2\n\\end{itemize}")
    ]
)
def test_format_item(input_text, expected_output):
    assert format_item(input_text) == expected_output

# Run tests
if __name__ == "__main__":
    pytest.main(["-v", __file__])