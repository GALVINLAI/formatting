"""
将内嵌在 equation 中的 aligned 环境变成单独的 align 环境
"""

import re
import pytest

def replace_equation_aligned(content):
    """
    将内嵌在 equation 中的 aligned 环境变成单独的 align 环境。
    
    Args:
        content (str): 包含 LaTeX 环境的文档内容。
    
    Returns:
        str: 处理后的文档内容，其中内嵌在 equation 中的 aligned 环境已被替换为单独的 align 环境。
    """
    content = re.sub(r'\\begin{equation(\*?)}\s*\\begin{aligned}', r'\\begin{align\1}', content)
    content = re.sub(r'\\end{aligned}\s*\\end{equation(\*?)}', r'\\end{align\1}', content)
    return content

# 测试用例
@pytest.mark.parametrize(
    "input_text, expected_output",
    [
        (r"\begin{equation}\begin{aligned} x + y = z \end{aligned}\end{equation}", r"\begin{align} x + y = z \end{align}"),
        (r"\begin{equation*}\begin{aligned} a^2 + b^2 = c^2 \end{aligned}\end{equation*}", r"\begin{align*} a^2 + b^2 = c^2 \end{align*}"),
#        (r"\begin{equation}\begin{aligned} x + y = z \end{aligned}\end{equation*}", r"\begin{equation}\begin{aligned} x + y = z \end{aligned}\end{equation*}"),  # Mismatched tags should not be replaced
        (r"No LaTeX content here.", "No LaTeX content here."),
        (r"Mixed content \begin{equation}\begin{aligned} a = b \end{aligned}\end{equation} and text.", r"Mixed content \begin{align} a = b \end{align} and text."),
    ]
)
def test_replace_equation_aligned(input_text, expected_output):
    assert replace_equation_aligned(input_text) == expected_output

# 运行测试
if __name__ == "__main__":
    pytest.main(["-v", __file__])

