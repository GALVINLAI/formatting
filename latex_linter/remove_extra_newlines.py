"""
将多行空行变成单行空行
"""

import re
import pytest

def remove_extra_newlines(content):
    """
    将文本内容中的多余空行去除，保留一个空行。
    
    Args:
        content (str): 待处理的文本内容。
    
    Returns:
        str: 处理后的文本内容，多余的空行被替换为一个空行。
    
    """
    # 表达式参考 cf: line 24 in https://github.com/platers/obsidian-linter/blob/master/src/rules/consecutive-blank-lines.ts
    content = re.sub(r'(\n([\t\v\f\r \u00a0\u2000-\u200b\u2028-\u2029\u3000]+)?){2,}', '\n\n', content)
    return content

# 测试用例
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

# 运行测试
if __name__ == "__main__":
    pytest.main(["-v", __file__])
