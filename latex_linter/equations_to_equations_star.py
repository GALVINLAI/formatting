"""
Inline formulas: Replace the 'equation' environment with the 'equation*' environment if there is no 'label'.
"""

import re
import pytest

def equations_to_equations_star(content):
    """
    Replace the 'equation' environment with the 'equation*' environment in a LaTeX document if there is no 'label'.
    
    Args:
        content (str): The document content containing 'equation' environments.
    
    Returns:
        str: The processed document content, where 'equation' environments without 'label' have been replaced with 'equation*' environments.
    """
    def format_equation_with_label(match):
        text = match.group(2)
        
        if 'label' not in text:
            # If there is no 'label', then it ends as 'equation*'
            begin = re.sub(r'equation\*?', 'equation*', match.group(1))
            end = re.sub(r'equation\*?', 'equation*', match.group(3))
            return begin + text + end
        else:
            # If there is a 'label', then it ends as 'equation'
            begin = re.sub(r'equation\*?', 'equation', match.group(1))
            end = re.sub(r'equation\*?', 'equation', match.group(3))
            return begin + text + end
    
    # Special attention, this match must be flags=re.DOTALL, i.e., single-line mode
    content = re.sub(r'(\s*\\begin\{equation\*?\})(.*?)(\\end\{equation\*?\}\s*)', format_equation_with_label, content, flags=re.DOTALL)
    
    return content

# Test cases
@pytest.mark.parametrize(
    "input_text, expected_output",
    [
        (r"This is an equation: \begin{equation*}\label{eq1}a + b = c\end{equation}.", r"This is an equation: \begin{equation}\label{eq1}a + b = c\end{equation}."),
        (r"This is an equation: \begin{equation}a + b = c\end{equation}.", r"This is an equation: \begin{equation*}a + b = c\end{equation*}."),
        (r"Multiple equations: \begin{equation*}\label{eq2}x + y = z\end{equation*} and \begin{equation}a^2 + b^2 = c^2\end{equation}.", r"Multiple equations: \begin{equation}\label{eq2}x + y = z\end{equation} and \begin{equation*}a^2 + b^2 = c^2\end{equation*}."),
        (r"No equations here.", r"No equations here."),
        (r"\begin{equation}Single equation\end{equation}", r"\begin{equation*}Single equation\end{equation*}"),
        (r"Mixed content with \begin{equation}a + b = c\end{equation} and text.", r"Mixed content with \begin{equation*}a + b = c\end{equation*} and text."),
    ]
)
def test_equations_to_equations_star(input_text, expected_output):
    assert equations_to_equations_star(input_text) == expected_output

# Run tests
if __name__ == "__main__":
    pytest.main(["-v", __file__])