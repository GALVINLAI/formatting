import re
import pytest

def replace_stars_with_textit(text):
    """
    将文本中的星号(*)及其包围的内容替换为LaTeX的\\textit{}格式。
    
    Args:
        text (str): 待处理的文本字符串。
    
    Returns:
        str: 处理后的文本字符串，其中星号(*)及其包围的内容被替换为LaTeX的\\textit{}格式。
    
    """
    # 使用lambda函数进行替换，将匹配的内容放入\\textit{}中
    replacement = lambda match: r"\textit{" + match.group(1) + "}"
    new_text = re.sub(r"\*(.*?)\*", replacement, text)
    return new_text

# 测试用例
@pytest.mark.parametrize(
    "input_text, expected_output",
    [
        ("This is *italic* text.", "This is \\textit{italic} text."),
        ("*Italic* at the start.", "\\textit{Italic} at the start."),
        ("At the end *italic*.", "At the end \\textit{italic}."),
        ("*Italic* everywhere *italic*.", "\\textit{Italic} everywhere \\textit{italic}."),
        ("No italic here.", "No italic here."),
        ("Mix *italic* and normal *text*.", "Mix \\textit{italic} and normal \\textit{text}."),
#        ("Nested *italic *in* italic*.", "Nested \\textit{italic *in* italic}."),
    ]
)
def test_replace_stars_with_textit(input_text, expected_output):
    assert replace_stars_with_textit(input_text) == expected_output

# 运行测试
if __name__ == "__main__":
    pytest.main(["-v", __file__])
