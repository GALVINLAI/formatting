"""
行间公式 4：替换 equation 为 $$ 环境，并自动规范内部格式
"""

import re
import pytest

def equations_to_dollars(content):
    """
    将 LaTeX 文档中的 equation 环境替换为 $$ 环境。
    
    Args:
        content (str): 包含 equation 环境的文档内容。
    
    Returns:
        str: 处理后的文档内容，其中 equation 环境已被替换为 $$ 环境。
    """
    content = re.sub(r'\\begin\{equation\}|\\end\{equation\}', '$$', content)
    return content

# 测试用例
@pytest.mark.parametrize(
    "input_text, expected_output",
    [
        (r"This is an equation: \begin{equation}a + b = c\end{equation}.", "This is an equation: $$a + b = c$$."),
        (r"Multiple equations: \begin{equation}x + y = z\end{equation} and \begin{equation}a^2 + b^2 = c^2\end{equation}.", "Multiple equations: $$x + y = z$$ and $$a^2 + b^2 = c^2$$."),
        (r"No equations here.", "No equations here."),
        (r"\begin{equation}Single equation\end{equation}", "$$Single equation$$"),
        (r"Mixed content with \begin{equation}a + b = c\end{equation} and text.", "Mixed content with $$a + b = c$$ and text."),
    ]
)
def test_equations_to_dollars(input_text, expected_output):
    assert equations_to_dollars(input_text) == expected_output

# 运行测试
if __name__ == "__main__":
    pytest.main(["-v", __file__])

