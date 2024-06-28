"""
去掉所有Markdown特征
"""

import re
import pytest

def repalce_all_markdown(content):
    """
    删除 LaTeX 文档中的 Markdown 格式，包括删除所有 ** 和 ## 之类的标题。
    
    Args:
        content (str): 包含 Markdown 格式的文档内容。
    
    Returns:
        str: 处理后的文档内容，其中所有 ** 和 ## 之类的标题已被删除。
    """
    content = re.sub(r'\*\*', '', content)  # 删除所有 **
    content = re.sub(r'\#+ ', '', content)  # 删除所有 ## 之类的标题
    return content

# 测试用例
@pytest.mark.parametrize(
    "input_text, expected_output",
    [
        ("This is **bold** text.", "This is bold text."),
        ("## This is a title", "This is a title"),
        ("### Another title", "Another title"),
        ("Normal text without formatting.", "Normal text without formatting."),
        ("Mixed **bold** and ## title", "Mixed bold and title"),
        ("### **Bold title**", "Bold title"),
    ]
)
def test_repalce_all_markdown(input_text, expected_output):
    assert repalce_all_markdown(input_text) == expected_output

# 运行测试
if __name__ == "__main__":
    pytest.main(["-v", __file__])

