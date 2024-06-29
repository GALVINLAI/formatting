import re
import pytest


def format_math_inline(match):
    """
    规范行内公式的内部格式。
    
    Args:
        match (re.Match): 正则表达式匹配对象，包含整个匹配文本。
            预期 match.group(1) 为方程前的内容。
            预期 match.group(2) 为方程内容。
            预期 match.group(3) 为方程后的内容。
    
    Returns:
        str: 格式化后的文本。
    """

    # 提取数学内容，并去掉首尾空白字符
    text = match.group(2).strip()

    # 将内部多个空白字符变成一个空格
    text = re.sub(r'\s+', ' ', text)

    # 组合结果并返回
    formatted_text = f'{match.group(1)}{text}{match.group(3)}'

    return formatted_text


# ---------- 规范 $ ... $ 环境 ----------
def format_single_dollar(content):
    # 使用 (?<!\$) 避免匹配到 $$ 环境
    content = re.sub(r'(?<!\$)(\$)([^\$]+?)(\$)', format_math_inline, content)
    return content


# ---------- 规范 \( ... \) 环境 ----------
def format_parentheses(content):
    content = re.sub(r'(\\\()(.+?)(\\\))', format_math_inline, content)
    return content


@pytest.mark.parametrize(
    "input_text, expected_output",
    [
        ("This is an inline math: $ a + b       = c $.", "This is an inline math: $a + b = c$."),
        ("Multiple spaces in $  x  +  y  =  z  $ equation.", "Multiple spaces in $x + y = z$ equation."),
        ("No spaces in $x+y=z$ should remain the same.", "No spaces in $x+y=z$ should remain the same."),
        ("Mixed content $a+b=c$ and $  x  +  y  =  z  $.", "Mixed content $a+b=c$ and $x + y = z$."),
        ("No math content here.", "No math content here."),
    ]
)
def test_format_single_dollar(input_text, expected_output):
    assert format_single_dollar(input_text) == expected_output

if __name__ == "__main__":
    pytest.main(["-v", __file__])


@pytest.mark.parametrize(
    "input_text, expected_output",
    [
        ("This is an inline math: \( a + b  = c \).", "This is an inline math: \(a + b = c\)."),
        ("Multiple spaces in \(  x  +  y  =  z  \) equation.", "Multiple spaces in \(x + y = z\) equation."),
        ("No spaces in \(x+y=z\) should remain the same.", "No spaces in \(x+y=z\) should remain the same."),
        ("Mixed content \(a+b=c\) and \(  x  +  y  =  z  \).", "Mixed content \(a+b=c\) and \(x + y = z\)."),
        ("No math content here.", "No math content here."),
    ]
)
def test_format_parentheses(input_text, expected_output):
    assert format_parentheses(input_text) == expected_output


# Run tests
if __name__ == "__main__":
    pytest.main(["-v", __file__])