import re
import pytest

def format_math_inline(content):
    """
    规范 $ 包围的行内公式的内部格式。
    
    Args:
        content (str): 包含行内公式的文本内容。
    
    Returns:
        str: 处理后的文本内容，行内公式的内部格式已被规范化。
    """
    def format_inline_math(match):
        text = match.group(2).strip()  # 去掉首尾空白字符
        text = re.sub(r'\s+', ' ', text)  # 将内部多个空白字符变成一个空格
        return f'{match.group(1)}{text}{match.group(3)}'

    content = re.sub(r'(?<!\$)(\$)([^\$]+?)(\$)', format_inline_math, content)
    
    return content

# 测试用例
@pytest.mark.parametrize(
    "input_text, expected_output",
    [
        ("This is an inline math: $ a + b  = c $.", "This is an inline math: $a + b = c$."),
        ("Multiple spaces in $  x  +  y  =  z  $ equation.", "Multiple spaces in $x + y = z$ equation."),
        ("No spaces in $x+y=z$ should remain the same.", "No spaces in $x+y=z$ should remain the same."),
        ("Mixed content $a+b=c$ and $  x  +  y  =  z  $.", "Mixed content $a+b=c$ and $x + y = z$."),
        ("No math content here.", "No math content here."),
    ]
)
def test_format_math_inline(input_text, expected_output):
    assert format_math_inline(input_text) == expected_output

# 运行测试
if __name__ == "__main__":
    pytest.main(["-v", __file__])
