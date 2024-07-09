"""
行间公式：替换 equation 为 equation* 环境，如果没有 label
"""

import re
import pytest

def equations_to_equations_star(content):
    """
    将 LaTeX 文档中的 equation 环境替换为 equation* 环境，如果没有 label。
    
    Args:
        content (str): 包含 equation 环境的文档内容。
    
    Returns:
        str: 处理后的文档内容，其中无 label 的 equation 环境已被替换为 equation* 环境。
    """
    def format_equation_with_label(match):
        text = match.group(2)
        
        if 'label' not in text:
            # 如果没有 label，则最后为 equation*
            begin = re.sub(r'equation\*?', 'equation*', match.group(1))
            end = re.sub(r'equation\*?', 'equation*', match.group(3))
            return begin + text + end
        else:
            # 如果有 label，则最后为 equation
            begin = re.sub(r'equation\*?', 'equation', match.group(1))
            end = re.sub(r'equation\*?', 'equation', match.group(3))
            return begin + text + end
    
    # 特别注意，该匹配必须是 flags=re.DOTALL，即单行模式
    content = re.sub(r'(\s*\\begin\{equation\*?\})(.*?)(\\end\{equation\*?\}\s*)', format_equation_with_label, content, flags=re.DOTALL)
    
    return content

# 测试用例
@pytest.mark.parametrize(
    "input_text, expected_output",
    [
        (r"This is an equation: \begin{equation*}\label{eq1}a + b = c\end{equation}.", r"This is an equation: \begin{equation}\label{eq1}a + b = c\end{equation}."),
        (r"This is an equation: \begin{equation}a + b = c\end{equation}.", r"This is an equation: \begin{equation*}a + b = c\end{equation*}."),
        (r"Multiple equations: \begin{equation*}\label{eq2}x + y = z\end{equation*} and \begin{equation}a^2 + b^2 = c^2\end{equation}.", r"Multiple equations: \begin{equation}\label{eq2}x + y = z\end{equation} and \begin{equation*}a^2 + b^2 = c^2\end{equation*}."),
        (r"No equations here.", r"No equations here."),
        (r"\begin{equation}Single equation\end{equation}", r"\begin{equation*}Single equation\end{equation*}"),
        (r"Mixed content with \begin{equation}a + b = c\end{equation} and text.", r"Mixed content with \begin{equation*}a + b = c\end{equation*} and text."),
    ]
)
def test_equations_to_equations_star(input_text, expected_output):
    assert equations_to_equations_star(input_text) == expected_output

# 运行测试
if __name__ == "__main__":
    pytest.main(["-v", __file__])
