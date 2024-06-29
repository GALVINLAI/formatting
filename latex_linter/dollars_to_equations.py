"""
行间公式：替换 $$ ... $$ 为 equation 环境
"""

import re
import pytest

# TODO 下面的核心逻辑有bug，如果注释里面有单个 $$，则会被替换为 equation 环境，需要改进。


def dollars_to_equations(content):
    """
    将 LaTeX 文档中的 $$ 替换为 equation 环境，并自动规范内部格式。
    
    Args:
        content (str): 包含 $$ 行间公式的文档内容。
    
    Returns:
        str: 处理后的文档内容，其中 $$ 行间公式已被替换为 equation 环境。
    """
    def fun_dollars_to_equations(match):
        nonlocal count
        count += 1
        if count % 2 == 1:
            return r'\begin{equation}'
        else:
            return r'\end{equation}'
    
    count = 0
    content = re.sub(r'\$\$', fun_dollars_to_equations, content)
    return content

# 测试用例
@pytest.mark.parametrize(
    "input_text, expected_output",
    [
        ("This is an equation: $$a + b = c$$.", "This is an equation: \\begin{equation}a + b = c\\end{equation}."),
        ("Multiple equations: $$x + y = z$$ and $$a^2 + b^2 = c^2$$.", "Multiple equations: \\begin{equation}x + y = z\\end{equation} and \\begin{equation}a^2 + b^2 = c^2\\end{equation}."),
        ("No equations here.", "No equations here."),
        ("$$Single equation$$", "\\begin{equation}Single equation\\end{equation}"),
        ("Mixed content with $$a + b = c$$ and text.", "Mixed content with \\begin{equation}a + b = c\\end{equation} and text."),
    ]
)
def test_dollars_to_equations(input_text, expected_output):
    assert dollars_to_equations(input_text) == expected_output

# 运行测试
if __name__ == "__main__":
    pytest.main(["-v", __file__])

