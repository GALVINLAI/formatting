"""
Convert multiple blank lines into a single blank line
"""

import re
import pytest

def remove_extra_newlines(content):
    """
    Remove extra blank lines from the text content, preserving a single blank line.
    
    Args:
        content (str): The text content to be processed.
    
    Returns:
        str: The processed text content with extra blank lines replaced by a single blank line.
    
    """
    # Expression reference cf: line 24 in https://github.com/platers/obsidian-linter/blob/master/src/rules/consecutive-blank-lines.ts
    content = re.sub(r'(\n([\t\v\f\r \u00a0\u2000-\u200b\u2028-\u2029\u3000]+)?){2,}', '\n\n', content)
    return content

# Test cases
@pytest.mark.parametrize(
    "input_text, expected_output",
    [
        ("Line1\n\n\nLine2", "Line1\n\nLine2"),
        ("Line1\n\n\n\nLine2", "Line1\n\nLine2"),
        ("Line1\n\n\n\n\nLine2", "Line1\n\nLine2"),
        ("Line1\n\nLine2", "Line1\n\nLine2"),
        ("Line1\n\n   \nLine2", "Line1\n\nLine2"),
        ("Line1\n \n    \n  Line2", "Line1\n\nLine2"),
    ]
)
def test_remove_extra_newlines(input_text, expected_output):
    assert remove_extra_newlines(input_text) == expected_output

# Run tests
if __name__ == "__main__":
    pytest.main(["-v", __file__])