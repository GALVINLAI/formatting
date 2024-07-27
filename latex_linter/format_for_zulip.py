import re
import pytest

def format_for_zulip(content):
    """
    让行间，行内公式符合zulip语法

    Args:
        content (str): 输入文本内容。

    Returns:
        str: 替换后的文本内容。
    """

    # 参考 zulip 的 latex 语法 https://zulip.com/help/latex#latex

    # 将所有被两个 $$ 包围的内容替换成用 ```math 开头和 ``` 结尾的包围形式。
    # 将所有被 \[ \] 包围的内容替换成用 ```math 开头和 ``` 结尾的包围形式。
    # 将所有被 equation 包围的内容替换成用 ```math 开头和 ``` 结尾的包围形式。
    content = re.sub(r'\s*\$\$\s*(.*?)\s*\$\$\s*', r'\n```math\n\1\n```\n', content, flags=re.DOTALL)
    content = re.sub(r'\s*\\\[\s*(.*?)\s*\\\]\s*', r'\n```math\n\1\n```\n', content, flags=re.DOTALL)
    content = re.sub(r'\s*\\begin\{equation\*?\}\s*(.*?)\s*\\end\{equation\*?\}\s*', r'\n```math\n\1\n```\n', content, flags=re.DOTALL)
    
    # zulip 的 markdown 语法中，只有两个 $$ 之间的内容会被识别为inline数学公式。
    content = re.sub(r'(?<!\$)\$\s*([^\$]+?)\s*\$', r'$$\1$$', content)
    content = re.sub(r'\\\(\s*(.*?)\s*\\\)', r'$$\1$$', content)

    return content

# -- 测试 ----------

@pytest.mark.parametrize(
    "input_text, expected_output",
    [
        (
            "$$ x + y = z $$",
            "```math\nx + y = z\n```"
        ),
        (
            "\\begin{equation} x + y = z \\end{equation}",
            "```math\nx + y = z\n```"
        ),
        (
            "\\[ x + y = z \\]",
            "```math\nx + y = z\n```"
        ),
        (
            "This is inline math: \(  a + b = c\).",
            "This is inline math: $$a + b = c$$.",
        ),
        (
            "Multiple spaces in $  x  +  y  =  z  $ equation.", 
            "Multiple spaces in $$x  +  y  =  z$$ equation."
        ),
    ]
)
def test_format_for_zulip(input_text, expected_output):
    assert format_for_zulip(input_text) == expected_output

# 运行测试
if __name__ == "__main__":
    pytest.main(["-v", __file__])
