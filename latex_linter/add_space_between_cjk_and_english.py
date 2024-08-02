"""
Add space between CJK characters and English or digits
"""

import re
import pytest

def add_space_between_cjk_and_english(text: str) -> str:
    """
    Add space between CJK characters and English or digits
    
    Args:
        text (str): The string to be processed
    
    Returns:
        str: The processed string with spaces added between CJK characters and English or digits
    
    """
    # Define regex patterns
    cjk_pattern = r'[\u4e00-\u9fff\u30a0-\u30ff\u3040-\u309f\uac00-\ud7af]'
    english_pattern = r'[a-zA-Z0-9]'
    
    # Define non-letter characters after and before CJK characters
    english_non_letter_after_cjk = r"-+'\"([¥$"
    english_non_letter_before_cjk = r"-+;:'\"°%$)]"

    # Construct head and tail regex patterns
    head_pattern = re.compile(f'({cjk_pattern})( *)({english_pattern}|[{re.escape(english_non_letter_after_cjk)}])')
    tail_pattern = re.compile(f'({english_pattern}|[{re.escape(english_non_letter_before_cjk)}])( *)({cjk_pattern})')

    # Add space between CJK characters and English or digits
    def add_space(text: str) -> str:
        text = head_pattern.sub(r'\1 \3', text)
        text = tail_pattern.sub(r'\1 \3', text)
        return text

    return add_space(text)


# Test cases
@pytest.mark.parametrize(
    "input_text, expected_output",
    [
        ("hello世界", "hello 世界"),
        ("你好123", "你好 123"),
        ("123世界456", "123 世界 456"),
        ("hello世界hello", "hello 世界 hello"),
        ("你好world", "你好 world"),
        ("你好 world", "你好 world"),
        ("hello 世界", "hello 世界"),
        ("hello+世界", "hello+ 世界"),
        ("世界(hello)", "世界 (hello)"),
        ("hello\"世界", "hello\" 世界"),
        ("世界\"hello", "世界 \"hello"),
    ]
)
def test_add_space_between_cjk_and_english(input_text, expected_output):
    assert add_space_between_cjk_and_english(input_text) == expected_output

# Run tests
if __name__ == "__main__":
    pytest.main(["-v", __file__])