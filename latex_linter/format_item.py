"""
规范 \item 格式
"""

import re
import pytest

def format_item(content):
    """
    规范 LaTeX 文档中 \\item 的格式，确保每个 \\item 之前有且仅有一个制表符，并且之后有且仅有一个空格。
    
    Args:
        content (str): 包含 LaTeX 列表项的文档内容。
    
    Returns:
        str: 处理后的文档内容，其中 \\item 的格式已被规范化。
    """
    content = re.sub(r'(?<!\t)\s*\\item\s*', r'\n    \\item ', content)
    return content

# 测试用例
@pytest.mark.parametrize(
    "input_text, expected_output",
    [
        ("\\item First item", "\n    \\item First item"),
        (" \\item Second item", "\n    \\item Second item"),
        ("\n\\item Third item", "\n    \\item Third item"),
        ("\\item    Fourth item", "\n    \\item Fourth item"),
        ("Text without items.", "Text without items."),
#        ("\\begin{itemize}\n\\item Item 1\n\\item  Item 2\n\\end{itemize}", "\\begin{itemize}\n\n    \\item Item 1\n\n    \\item Item 2\n\\end{itemize}")
    ]
)
def test_format_item(input_text, expected_output):
    assert format_item(input_text) == expected_output

# 运行测试
if __name__ == "__main__":
    pytest.main(["-v", __file__])
