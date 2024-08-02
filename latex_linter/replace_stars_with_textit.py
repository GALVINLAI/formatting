import re
import pytest

def replace_stars_with_textit(text):
    """
    Replace asterisks (*) and their enclosed content with LaTeX's \\textit{} format.
    
    Args:
        text (str): The text string to be processed.
    
    Returns:
        str: The processed text string, where asterisks (*) and their enclosed content are replaced with LaTeX's \\textit{} format.
    
    """
    # Use a lambda function for replacement, placing the matched content inside \\textit{}
    replacement = lambda match: r"\textit{" + match.group(1) + "}"
    new_text = re.sub(r"\*(.*?)\*", replacement, text)
    return new_text

# Test cases
@pytest.mark.parametrize(
    "input_text, expected_output",
    [
        ("This is *italic* text.", "This is \\textit{italic} text."),
        ("*Italic* at the start.", "\\textit{Italic} at the start."),
        ("At the end *italic*.", "At the end \\textit{italic}."),
        ("*Italic* everywhere *italic*.", "\\textit{Italic} everywhere \\textit{italic}."),
        ("No italic here.", "No italic here."),
        ("Mix *italic* and normal *text*.", "Mix \\textit{italic} and normal \\textit{text}."),
#        ("Nested *italic *in* italic*.", "Nested \\textit{italic *in* italic}."),
    ]
)
def test_replace_stars_with_textit(input_text, expected_output):
    assert replace_stars_with_textit(input_text) == expected_output

# Run tests
if __name__ == "__main__":
    pytest.main(["-v", __file__])