import re
import pytest


def format_math_display(match):
    """
    规范行间公式的内部格式。
    
    Args:
        match (re.Match): 正则表达式匹配对象，包含整个匹配文本。
            预期 match.group(1) 为方程前的内容（可能为空）。
            预期 match.group(2) 为方程内容。
            预期 match.group(3) 为方程后的内容（可能为空）。
    
    Returns:
        str: 格式化后的文本，包含方程标签（如果有）、方程内容和前后文本。
    """
    # 提取方程内容
    text = match.group(2)

    # 提取并删除 \label 部分
    label_text = re.findall(r'\\label\{.*?\}', text)
    text = re.sub(r'\\label\{.*?\}', '', text)

    # 去掉首尾空白字符
    text = text.strip()

    # 将内部连续的2个及以上的空白字符(除了\n)变成一个空格。这里暗示了，内部换行是被允许的。
    text = re.sub(r'[\t\v\f\r \u00a0\u2000-\u200b\u2028-\u2029\u3000]{2,}', ' ', text)

    # 整理已有的换行符
    text = re.sub(r'\s*\n\s*', '\n    ', text)

    # 重组文本，加入标签和格式化
    if label_text:
        label_text = label_text[0]  # 假设只有一个 \label
        text = f'{label_text}\n    {text}\n'
    else:
        text = f'\n    {text}\n'
        
    # 组合结果并返回
    formatted_text = f'{match.group(1).strip()}{text}{match.group(3).strip()}\n'

    return formatted_text
    

# ---------- 规范 equation 环境 ----------
def format_equations(content):
    # 特别注意，该匹配必须是 flags=re.DOTALL，即单行模式
    content = re.sub(r'(\s*\\begin\{equation\*?\})(.*?)(\\end\{equation\*?\}\s*)', format_math_display, content, flags=re.DOTALL)
    return content


# ---------- 规范 $$ ... $$ 环境 ----------
def format_dollars(content):
    # 特别注意，该匹配必须是 flags=re.DOTALL，即单行模式
    content = re.sub(r'(\$\$)(.*?)(\$\$)', format_math_display, content, flags=re.DOTALL)
    return content


# ---------- 规范 \[ ... \ ] 环境 ----------
def format_square_brackets(content):
    # 特别注意，该匹配必须是 flags=re.DOTALL，即单行模式
    content = re.sub(r'(\\\[)(.*?)(\\\])', format_math_display, content, flags=re.DOTALL)
    return content


# 测试用例
@pytest.mark.parametrize(
    "input_text, expected_output",
    [
        # (
        #     r"\begin{equation} x + y = z \end{equation}",
        #     r"\begin{equation}\n    x + y = z\n\end{equation}\n"
        # ),
        # (
        #     r"\begin{equation} a^2 + b^2 = c^2 \end{equation}",
        #     r"\begin{equation}\n    a^2 + b^2 = c^2\n\end{equation}\n"
        # ),
        # (
        #     r"\begin{equation}\n    x + y = z \end{equation}",
        #     r"\begin{equation}\n    x + y = z\n\end{equation}\n"
        # ),
        # (
        #     r"No equations here.",
        #     r"No equations here."
        # ),
        # (
        #     r"Multiple equations: \begin{equation} x + y = z \end{equation} and \begin{equation} a^2 + b^2 = c^2 \end{equation}.",
        #     r"Multiple equations: \begin{equation}\n    x + y = z\n\end{equation}\n and \begin{equation}\n    a^2 + b^2 = c^2\n\end{equation}\n."
        # ),
    ]
)
def test_format_equations(input_text, expected_output):
    assert format_equations(input_text) == expected_output


@pytest.mark.parametrize(
    "input_text, expected_output",
    [
        # (
        #     r"$$ x + y = z $$",
        #     r"$$\n    x + y = z\n$$\n"
        # ),
        # (
        #     r"$$ a^2 + b^2 = c^2 $$",
        #     r"$$\n    a^2 + b^2 = c^2\n$$\n"
        # ),
        # (
        #     r"$$\n    x + y = z $$",
        #     r"$$\n    x + y = z\n$$\n"
        # ),
        # (
        #     r"No equations here.",
        #     r"No equations here."
        # ),
        # (
        #     r"Multiple equations: $$ x + y = z $$ and $$ a^2 + b^2 = c^2 $$.",
        #     r"Multiple equations: $$\n    x + y = z\n$$\n and $$\n    a^2 + b^2 = c^2\n$$\n."
        # ),
    ]
)
def test_format_dollars(input_text, expected_output):
    assert format_dollars(input_text) == expected_output

# 运行测试
if __name__ == "__main__":
    pytest.main(["-v", __file__])
