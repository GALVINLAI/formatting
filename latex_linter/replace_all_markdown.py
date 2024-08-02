"""
Remove all Markdown features
"""

import re
import pytest

def replace_all_markdown(content):
    """
    Remove Markdown formatting from LaTeX documents, including removing all ** and ##-like headings.
    
    Args:
        content (str): The document content containing Markdown formatting.
    
    Returns:
        str: The processed document content with all ** and ##-like headings removed.
    """
    content = re.sub(r'\*\*', '', content)  # Remove all **
    content = re.sub(r'\#+ ', '', content)  # Remove all ##-like headings
    
    return content

# Test cases
@pytest.mark.parametrize(
    "input_text, expected_output",
    [
        ("This is **bold** text.", "This is bold text."),
        ("## This is a title", "This is a title"),
        ("### Another title", "Another title"),
        ("Normal text without formatting.", "Normal text without formatting."),
        ("Mixed **bold** and ## title", "Mixed bold and title"),
        ("### **Bold title**", "Bold title"),
    ]
)
def test_replace_all_markdown(input_text, expected_output):
    assert replace_all_markdown(input_text) == expected_output

# Run tests
if __name__ == "__main__":
    pytest.main(["-v", __file__])