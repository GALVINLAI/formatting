"""
Description of the new feature
"""

import re
import pytest

def new_feature_name(content):
    # Implementation code
    return content

# Test cases
@pytest.mark.parametrize(
    "input_text, expected_output",
    [
        ("This is an equation: $$a + b = c$$.", "This is an equation: \\begin{equation}a + b = c\\end{equation}."),
        ("Multiple equations: $$x + y = z$$ and $$a^2 + b^2 = c^2$$.", "Multiple equations: \\begin{equation}x + y = z\\end{equation} and \\begin{equation}a^2 + b^2 = c^2\\end{equation}."),
    ]
)
def test_new_feature_name(input_text, expected_output):
    assert new_feature_name(input_text) == expected_output

# Run tests
if __name__ == "__main__":
    pytest.main(["-v", __file__])