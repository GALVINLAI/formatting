import re
import pytest


def format_math_inline(match):
    """
    Standardize the internal format of inline equations.
    
    Args:
        match (re.Match): The regex match object containing the entire matched text.
            Expected match.group(1) to be the content before the equation.
            Expected match.group(2) to be the equation content.
            Expected match.group(3) to be the content after the equation.
    
    Returns:
        str: The formatted text.
    """

    # Extract the math content and strip leading and trailing whitespace characters
    text = match.group(2).strip()

    # Replace multiple internal whitespace characters with a single space
    text = re.sub(r'\s+', ' ', text)

    # Combine the result and return
    formatted_text = f'{match.group(1)}{text}{match.group(3)}'

    return formatted_text


# ---------- Standardize $ ... $ environment ----------
def format_single_dollar(content):
    # Use (?<!\$) to avoid matching the $$ environment
    content = re.sub(r'(?<!\$)(\$)([^\$]+?)(\$)', format_math_inline, content)
    return content


# ---------- Standardize \( ... \) environment ----------
def format_parentheses(content):
    content = re.sub(r'(\\\()(.+?)(\\\))', format_math_inline, content)
    return content


@pytest.mark.parametrize(
    "input_text, expected_output",
    [
        ("This is an inline math: $ a + b       = c $.", "This is an inline math: $a + b = c$."),
        ("Multiple spaces in $  x  +  y  =  z  $ equation.", "Multiple spaces in $x + y = z$ equation."),
        ("No spaces in $x+y=z$ should remain the same.", "No spaces in $x+y=z$ should remain the same."),
        ("Mixed content $a+b=c$ and $  x  +  y  =  z  $.", "Mixed content $a+b=c$ and $x + y = z$."),
        ("No math content here.", "No math content here."),
    ]
)
def test_format_single_dollar(input_text, expected_output):
    assert format_single_dollar(input_text) == expected_output

if __name__ == "__main__":
    pytest.main(["-v", __file__])


@pytest.mark.parametrize(
    "input_text, expected_output",
    [
        ("This is an inline math: \( a + b  = c \).", "This is an inline math: \(a + b = c\)."),
        ("Multiple spaces in \(  x  +  y  =  z  \) equation.", "Multiple spaces in \(x + y = z\) equation."),
        ("No spaces in \(x+y=z\) should remain the same.", "No spaces in \(x+y=z\) should remain the same."),
        ("Mixed content \(a+b=c\) and \(  x  +  y  =  z  \).", "Mixed content \(a+b=c\) and \(x + y = z\)."),
        ("No math content here.", "No math content here."),
    ]
)
def test_format_parentheses(input_text, expected_output):
    assert format_parentheses(input_text) == expected_output


# Run tests
if __name__ == "__main__":
    pytest.main(["-v", __file__])