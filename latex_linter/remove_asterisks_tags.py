"""
去掉 align 和 equation 环境中用于不显示tag的 * 号
"""

import re
import pytest

def remove_asterisks_tags(content):
    """
    去掉 LaTeX 文档中 align 和 equation 环境中的 * 号，以便显示标签。
    
    Args:
        content (str): 包含 LaTeX 环境的文档内容。
    
    Returns:
        str: 处理后的文档内容，其中 align 和 equation 环境中的 * 号已被去掉。
    """
    content = re.sub(r'\\(begin|end)\{(align|equation)\*\}', r'\\\1{\2}', content)
    return content

# 测试用例
@pytest.mark.parametrize(
    "input_text, expected_output",
    [
        (r"\begin{align*} x + y = z \end{align*}", r"\begin{align} x + y = z \end{align}"),
        (r"\begin{equation*} a^2 + b^2 = c^2 \end{equation*}", r"\begin{equation} a^2 + b^2 = c^2 \end{equation}"),
        (r"\begin{align} x + y = z \end{align}", r"\begin{align} x + y = z \end{align}"),
        (r"\begin{equation} a^2 + b^2 = c^2 \end{equation}", r"\begin{equation} a^2 + b^2 = c^2 \end{equation}"),
        (r"Some text without environment.", r"Some text without environment."),
    ]
)
def test_remove_asterisks_tags(input_text, expected_output):
    assert remove_asterisks_tags(input_text) == expected_output

# 运行测试
if __name__ == "__main__":
    pytest.main(["-v", __file__])

