import re
import pytest


def format_math_display(match):
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

    # 提取并删除 \label 部分
    # .*? 是一个非贪婪匹配，表示匹配任意字符直到遇到后面的第一个 }
    label_text = re.findall(r'\\label\{.*?\}', text)
    text = re.sub(r'\\label\{.*?\}', '', text)

    # 去掉首尾空白字符
    text = text.strip()

    # 将内部连续的2个及以上的空白字符(除了\n)变成一个空格。这里暗示了，内部换行是被允许的。
    text = re.sub(r'[\t\v\f\r \u00a0\u2000-\u200b\u2028-\u2029\u3000]{2,}', ' ', text)

    # 整理已有的换行符，让每一行前面缩进4个空格
    text = re.sub(r'\s*\n\s*', '\n    ', text)

    # 重组文本，加入标签和格式化
    # TODO 不能处理 align 环境中存在多个label的情况
    if label_text:
        label_text = label_text[0]  # 假设只有一个 \label
        # label 放在开头部分
        text = f'{label_text}\n    {text}'
    else:
        text = f'\n    {text}'
        
    # 组合结果并返回
    formatted_text = f'\n{match.group(1).strip()}{text}\n{match.group(3).strip()}\n'

    return formatted_text
    

# ---------- 规范 equation 环境 ----------
def format_equations(content):
    # 特别注意，该匹配必须是 flags=re.DOTALL，即单行模式
    content = re.sub(r'(\s*\\begin\{equation\*?\})(.*?)(\\end\{equation\*?\}\s*)', format_math_display, content, flags=re.DOTALL)
    return content


# ---------- 规范 $$ ... $$ 环境 ----------
def format_dollars(content):
    # 特别注意，该匹配必须是 flags=re.DOTALL，即单行模式
    content = re.sub(r'(\s*\$\$)(.*?)(\$\$\s*)', format_math_display, content, flags=re.DOTALL)
    return content


# ---------- 规范 \[ ... \ ] 环境 ----------
def format_square_brackets(content):
    # 特别注意，该匹配必须是 flags=re.DOTALL，即单行模式
    content = re.sub(r'(\s*\\\[)(.*?)(\\\]\s*)', format_math_display, content, flags=re.DOTALL)
    return content

# -- 测试 ----------

@pytest.mark.parametrize(
    "input_text, expected_output",
    [
        (
            "$$ x + y = z $$",
            "\n$$\n    x + y = z\n$$\n"
        ),
        (
            "$$ a^2 + b^2 = c^2 $$",
            "\n$$\n    a^2 + b^2 = c^2\n$$\n"
        ),
        (
            "$$\n    x + y = z $$",
            "\n$$\n    x + y = z\n$$\n"
        ),
        (
            "No equations here.",
            "No equations here."
        ),
        (
            "Multiple equations: $$ x + y = z $$ and $$ a^2 + b^2 = c^2 $$.",
            "Multiple equations:\n$$\n    x + y = z\n$$\nand\n$$\n    a^2 + b^2 = c^2\n$$\n."
        ),
    ]
)
def test_format_dollars(input_text, expected_output):
    assert format_dollars(input_text) == expected_output



@pytest.mark.parametrize(
    "input_text, expected_output",
    [
        (
            "\\begin{equation} x + y = z \\end{equation}",
            "\n\\begin{equation}\n    x + y = z\n\\end{equation}\n"
        ),
        (
            "\\begin{equation*} a^2 + b^2 = c^2 \\end{equation*}",
            "\n\\begin{equation*}\n    a^2 + b^2 = c^2\n\\end{equation*}\n"
        ),
        (
            "\\begin{equation*}\n    x + y = z \\end{equation*}",
            "\n\\begin{equation*}\n    x + y = z\n\\end{equation*}\n"
        ),
        (
            "No equations here.",
            "No equations here."
        ),
    ]
)
def test_format_equations(input_text, expected_output):
    assert format_equations(input_text) == expected_output

@pytest.mark.parametrize(
    "input_text, expected_output",
    [
        (
            "\\[ x + y = z \\]",
            "\n\\[\n    x + y = z\n\\]\n"
        ),
        (
            "\\[ a^2 + b^2 = c^2 \\]",
            "\n\\[\n    a^2 + b^2 = c^2\n\\]\n"
        ),
        (
            "\\[\n    x + y = z \\]",
            "\n\\[\n    x + y = z\n\\]\n"
        ),
        (
            "No equations here.",
            "No equations here."
        ),
    ]
)
def test_format_square_brackets(input_text, expected_output):
    assert format_square_brackets(input_text) == expected_output










# 运行测试
if __name__ == "__main__":
    pytest.main(["-v", __file__])
