"""

"""

import re
import pytest

def some_small_utilities(content):
    """
    将 LaTeX 文档中 ^{T} 的格式替换为 ^{\top}，考虑各种空格情况。
    
    Args:
        content (str): 包含 ^{T} 的文档内容。
    
    Returns:
        str: 处理后的文档内容，其中 ^{T} 的格式已被替换为 ^{\top}。
    """
    content = re.sub(r'\s*\\text\s*\{\s*([ \.,;:!]*)\s*\}', r'\1', content) # mathpix 总是喜欢搞出来  \text {, } 这样
    content = re.sub(r'\\text\s*\{', r'\\text{', content) # mathpix 总是喜欢搞出来  \text { some text } 这样 text后面有一个空格
    content = re.sub(r'\s*\^\s*\{\s*T\s*\}', r'^{\\top}', content) # 转置符号使用 `\top`
    content = re.sub(r'\s*\^\s*\{\s*[\'`]\s*\}', r'^{\\prime}', content) #  `\prime` 代替单引号上标

    return content

# 测试用例
@pytest.mark.parametrize(
    "input_text, expected_output",
    [
        ("A^{T}", "A^{\\top}"),
        ("B^{  T}", "B^{\\top}"),
        ("C^{T  }", "C^{\\top}"),
        ("D^{  T  }", "D^{\\top}"),
        ("E^{T} and F^{T}", "E^{\\top} and F^{\\top}"),
        ("G^{ T } is different from H^{ T}", "G^{\\top} is different from H^{\\top}"),
        ("No transpose here.", "No transpose here."),
    ]
)
def test_some_small_utilities(input_text, expected_output):
    assert some_small_utilities(input_text) == expected_output

# 运行测试
if __name__ == "__main__":
    pytest.main(["-v", __file__])