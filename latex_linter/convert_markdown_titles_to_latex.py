"""
将 Markdown 的标题等变成 latex 对应物
"""

import re
import pytest

def convert_markdown_titles_to_latex(content):
    """
    将Markdown格式的标题转换为LaTeX格式的标题。
    
    Args:
        content (str): 包含Markdown标题的字符串。
    
    Returns:
        str: 转换后包含LaTeX标题的字符串。
    
    """
    # 处理 # title -> \section{title}
    content = re.sub(r'^# (.+)$', r'\\section{\1}', content, flags=re.MULTILINE)
    # 处理 ## title -> \subsection{title}
    content = re.sub(r'^## (.+)$', r'\\subsection{\1}', content, flags=re.MULTILINE)  
    # 处理 ### title -> \subsubsection{title}
    content = re.sub(r'^### (.+)$', r'\\subsubsection{\1}', content, flags=re.MULTILINE)
    # 处理 #### title -> normal text
    content = re.sub(r'^#{4,} (.+)$', r'\1', content, flags=re.MULTILINE)
    return content

# 测试用例
@pytest.mark.parametrize(
    "input_text, expected_output",
    [
        ("# Title", r"\section{Title}"),
        ("## Subtitle", r"\subsection{Subtitle}"),
        ("### Subsubtitle", r"\subsubsection{Subsubtitle}"),
        ("#### Normal text", "Normal text"),
        ("# Title\n## Subtitle\n### Subsubtitle\n#### Normal text", "\section{Title}\n\subsection{Subtitle}\n\subsubsection{Subsubtitle}\nNormal text"),
        ("Some text\n# Title\nMore text", "Some text\n\section{Title}\nMore text"),
        ("####### Too many hashes", "Too many hashes"),
    ]
)
def test_convert_markdown_titles_to_latex(input_text, expected_output):
    assert convert_markdown_titles_to_latex(input_text) == expected_output

# 运行测试
if __name__ == "__main__":
    pytest.main(["-v", __file__])
