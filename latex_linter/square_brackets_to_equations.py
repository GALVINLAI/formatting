"""
行间公式 5：替换 \[ 和 \] 为 equation 环境，并自动规范内部格式
"""

import re
import pytest

def square_brackets_to_equations(content):
    """
    将 LaTeX 文档中的 \\[ 和 \\] 替换为 equation 环境，并自动规范内部格式。
    
    Args:
        content (str): 包含 \\[ 和 \\] 行间公式的文档内容。
    
    Returns:
        str: 处理后的文档内容，其中 \\[ 和 \\] 已被替换为 equation 环境。
    """
    content = re.sub(r'\\\[', r'\\begin{equation}', content)
    content = re.sub(r'\\\]', r'\\end{equation}', content)
    return content

# 测试用例
@pytest.mark.parametrize(
    "input_text, expected_output",
    [
        (r"This is an equation: \[a + b = c\].", "This is an equation: \\begin{equation}a + b = c\\end{equation}."),
        (r"Multiple equations: \[x + y = z\] and \[a^2 + b^2 = c^2\].", "Multiple equations: \\begin{equation}x + y = z\\end{equation} and \\begin{equation}a^2 + b^2 = c^2\\end{equation}."),
        (r"No equations here.", "No equations here."),
        (r"\[Single equation\]", "\\begin{equation}Single equation\\end{equation}"),
        (r"Mixed content with \[a + b = c\] and text.", "Mixed content with \\begin{equation}a + b = c\\end{equation} and text."),
    ]
)
def test_square_brackets_to_equations(input_text, expected_output):
    assert square_brackets_to_equations(input_text) == expected_output

# 运行测试
if __name__ == "__main__":
    pytest.main(["-v", __file__])

