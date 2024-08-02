"""

"""

import re
import pytest

def some_small_utilities(content):
    """
    Collection of various small utilities
    """
    content = re.sub(r'\s*\\text\s*\{\s*([ \.,;:!]*)\s*\}', r'\1', content) # mathpix always introduces \text {, } like this
    content = re.sub(r'\\text\s*\{', r'\\text{', content) # mathpix always introduces \text { some text } like this with a space after text
    content = re.sub(r'\s*\^\s*\{\s*T\s*\}', r'^{\\top}', content) # Transpose symbol uses `\top`
    content = re.sub(r'\s*\^\s*\{\s*[\'`]\s*\}', r'^{\\prime}', content) # `\prime` replaces single quote superscript

    return content

# Test cases
@pytest.mark.parametrize(
    "input_text, expected_output",
    [
        ("A^{T}", "A^{\\top}"),
        ("B^{  T}", "B^{\\top}"),
        ("C^{T  }", "C^{\\top}"),
        ("D^{  T  }", "D^{\\top}"),
        ("E^{T} and F^{T}", "E^{\\top} and F^{\\top}"),
        ("G^{ T } is different from H^{ T}", "G^{\\top} is different from H^{\\top}"),
        ("No transpose here.", "No transpose here."),
    ]
)
def test_some_small_utilities(input_text, expected_output):
    assert some_small_utilities(input_text) == expected_output

# Run tests
if __name__ == "__main__":
    pytest.main(["-v", __file__])