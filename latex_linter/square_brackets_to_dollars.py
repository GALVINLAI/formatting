"""
行间公式 3：替换 \[ 和 \] 为 $$ 环境，并自动规范内部格式【特别针对ChatGPT的回答】
"""

import re
import pytest

def square_brackets_to_dollars(content):
    """
    将 LaTeX 文档中的 \\[ 和 \\] 替换为 $$ 环境。
    
    Args:
        content (str): 包含 \\[ 和 \\] 的文档内容。
    
    Returns:
        str: 处理后的文档内容，其中 \\[ 和 \\] 已被替换为 $$。
    """
    content = re.sub(r'\\\[|\\\]', '$$', content)
    return content

# 测试用例
@pytest.mark.parametrize(
    "input_text, expected_output",
    [
        (r"This is an equation: \[a + b = c\].", "This is an equation: $$a + b = c$$."),
        (r"Multiple equations: \[x + y = z\] and \[a^2 + b^2 = c^2\].", "Multiple equations: $$x + y = z$$ and $$a^2 + b^2 = c^2$$."),
        (r"No equations here.", "No equations here."),
        (r"\[Single equation\]", "$$Single equation$$"),
        (r"Mixed content with \[a + b = c\] and text.", "Mixed content with $$a + b = c$$ and text."),
    ]
)
def test_square_brackets_to_dollars(input_text, expected_output):
    assert square_brackets_to_dollars(input_text) == expected_output

# 运行测试
if __name__ == "__main__":
    pytest.main(["-v", __file__])

