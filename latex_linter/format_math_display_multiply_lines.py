import re
import pytest


def format_math_display_multiply_lines(match):
    """
    规范行间公式的内部格式。
    
    Args:
        match (re.Match): 正则表达式匹配对象，包含整个匹配文本。
            预期 match.group(1) 为方程前的内容（即，$$, \begin{equation}, \[）。
            预期 match.group(2) 为方程内容。
            预期 match.group(3) 为方程后的内容（即，$$, \end{equation}, \]）。
    
    Returns:
        str: 格式化后的文本，包含方程标签（如果有）、方程内容和前后文本。
    """
    # 提取方程内容
    text = match.group(2)

    # # 提取并删除 \label 部分
    # # .*? 是一个非贪婪匹配，表示匹配任意字符直到遇到后面的第一个 }
    # label_text = re.findall(r'\\label\{.*?\}', text)
    # text = re.sub(r'\\label\{.*?\}', '', text)

    # 去掉首尾空白字符
    text = text.strip()

    # 将内部连续的2个及以上的空白字符(除了\n)变成一个空格。这里暗示了，内部换行是被允许的。
    text = re.sub(r'[\t\v\f\r \u00a0\u2000-\u200b\u2028-\u2029\u3000]{2,}', ' ', text)

    # 整理已有的换行符，让每一行前面缩进4个空格
    text = re.sub(r'\s*\n\s*', '\n    ', text)

    text = f'\n    {text}'
        
    # 组合结果并返回
    formatted_text = f'\n{match.group(1).strip()}{text}\n{match.group(3).strip()}\n'

    return formatted_text
    

# ---------- 规范 align 环境 ----------
def format_aligns(content):
    # 特别注意，该匹配必须是 flags=re.DOTALL，即单行模式
    content = re.sub(r'(\s*\\begin\{align\*?\})(.*?)(\\end\{align\*?\}\s*)', format_math_display_multiply_lines, content, flags=re.DOTALL)
    return content



@pytest.mark.parametrize(
    "input_text, expected_output",
    [
        (
            "\\begin{align} x + y = z \\end{align}",
            "\n\\begin{align}\n    x + y = z\n\\end{align}\n"
        ),
        (
            "\\begin{align*} a^2 + b^2 = c^2 \\end{align*}",
            "\n\\begin{align*}\n    a^2 + b^2 = c^2\n\\end{align*}\n"
        ),
        (
            "\\begin{align*}\n    x + y = z \\end{align*}",
            "\n\\begin{align*}\n    x + y = z\n\\end{align*}\n"
        ),
        (
            "No aligns here.",
            "No aligns here."
        ),
    ]
)
def test_format_aligns(input_text, expected_output):
    assert format_aligns(input_text) == expected_output


# 运行测试
if __name__ == "__main__":
    pytest.main(["-v", __file__])
