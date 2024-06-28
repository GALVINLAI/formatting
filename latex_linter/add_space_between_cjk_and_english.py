"""
在中日韩字符和英文或数字之间添加空格
"""

import re
import pytest

def add_space_between_cjk_and_english(text: str) -> str:
    """
    在中日韩字符和英文或数字之间添加空格
    
    Args:
        text (str): 需要处理的字符串
    
    Returns:
        str: 处理后的字符串，中日韩字符和英文或数字之间添加了空格
    
    """
    # 定义正则表达式模式
    cjk_pattern = r'[\u4e00-\u9fff\u30a0-\u30ff\u3040-\u309f\uac00-\ud7af]'
    english_pattern = r'[a-zA-Z0-9]'
    
    # 定义中日韩字符后和前的非字母字符
    english_non_letter_after_cjk = r"-+'\"([¥$"
    english_non_letter_before_cjk = r"-+;:'\"°%$)]"

    # 构建头部和尾部的正则表达式
    head_pattern = re.compile(f'({cjk_pattern})( *)({english_pattern}|[{re.escape(english_non_letter_after_cjk)}])')
    tail_pattern = re.compile(f'({english_pattern}|[{re.escape(english_non_letter_before_cjk)}])( *)({cjk_pattern})')

    # 在中日韩字符和英文或数字之间添加空格
    def add_space(text: str) -> str:
        text = head_pattern.sub(r'\1 \3', text)
        text = tail_pattern.sub(r'\1 \3', text)
        return text

    return add_space(text)


# 测试用例
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

# 运行测试
if __name__ == "__main__":
    pytest.main(["-v", __file__])