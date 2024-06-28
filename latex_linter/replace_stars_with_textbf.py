"""

"""
import re
import pytest

def replace_stars_with_textbf(text):
    """
    将文本中的双星号包围的内容替换为LaTeX中的\\textbf{}格式。
    
    Args:
        text (str): 待处理的文本字符串。
    
    Returns:
        str: 处理后的文本字符串，其中双星号包围的内容已被替换为\\textbf{}格式。
    
    """
    # 使用lambda函数进行替换，将匹配的内容放入\textbf{}中
    replacement = lambda match: r"\textbf{" + match.group(1) + "}"
    new_text = re.sub(r"\*{2}(.*?)\*{2}", replacement, text)
    return new_text

# 测试用例
@pytest.mark.parametrize(
    "input_text, expected_output",
    [
        ("This is **bold** text.", "This is \\textbf{bold} text."),
        ("**Bold** at the start.", "\\textbf{Bold} at the start."),
        ("At the end **bold**.", "At the end \\textbf{bold}."),
        ("**Bold** everywhere **bold**.", "\\textbf{Bold} everywhere \\textbf{bold}."),
        ("No bold here.", "No bold here."),
        ("Mix **bold** and normal **text**.", "Mix \\textbf{bold} and normal \\textbf{text}."),
#        ("Nested **bold **in** bold**.", "Nested \\textbf{bold **in** bold}."),
    ]
)
def test_replace_stars_with_textbf(input_text, expected_output):
    assert replace_stars_with_textbf(input_text) == expected_output

# 运行测试
if __name__ == "__main__":
    pytest.main(["-v", __file__])
