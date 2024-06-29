"""
行内公式：替换 \( ... \) 为 $ ... $ 环境
"""

import re
import pytest

def parentheses_to_single_dollar(content):
    """
    替换 LaTeX 文档中的 \( 和 \) 为 $ 包围。
    
    Args:
        content (str): 包含 LaTeX 行内公式的文档内容。
    
    Returns:
        str: 处理后的文档内容，其中 \( 和 \) 已被替换为 $。
    """
    content = re.sub(r'\\\(|\\\)', '$', content)
    return content

# 测试用例
@pytest.mark.parametrize(
    "input_text, expected_output",
    [
        (r"This is inline math: \(a + b = c\).", "This is inline math: $a + b = c$."),
        (r"Multiple formulas: \(x + y = z\) and \(a^2 + b^2 = c^2\).", "Multiple formulas: $x + y = z$ and $a^2 + b^2 = c^2$."),
        (r"No math content here.", "No math content here."),
        (r"Already $a + b = c$ format.", "Already $a + b = c$ format."),
        (r"Mixed \(a + b = c\) and $x + y = z$ formats.", "Mixed $a + b = c$ and $x + y = z$ formats."),
    ]
)
def test_parentheses_to_single_dollar(input_text, expected_output):
    assert parentheses_to_single_dollar(input_text) == expected_output

# 运行测试
if __name__ == "__main__":
    pytest.main(["-v", __file__])

