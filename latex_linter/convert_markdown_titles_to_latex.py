"""
Convert Markdown titles to their LaTeX equivalents.
"""

import re
import pytest

def convert_markdown_titles_to_latex(content):
    """
    Convert Markdown-formatted titles to LaTeX-formatted titles.
    
    Args:
        content (str): A string containing Markdown titles.
    
    Returns:
        str: A string containing LaTeX titles after conversion.
    
    """
    # Handle # title -> \section{title}
    content = re.sub(r'^# (.+)$', r'\\section{\1}', content, flags=re.MULTILINE)
    # Handle ## title -> \subsection{title}
    content = re.sub(r'^## (.+)$', r'\\subsection{\1}', content, flags=re.MULTILINE)  
    # Handle ### title -> \subsubsection{title}
    content = re.sub(r'^### (.+)$', r'\\subsubsection{\1}', content, flags=re.MULTILINE)
    # Handle #### title -> normal text
    content = re.sub(r'^#{4,} (.+)$', r'\1', content, flags=re.MULTILINE)
    return content

# Test cases
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

# Run tests
if __name__ == "__main__":
    pytest.main(["-v", __file__])