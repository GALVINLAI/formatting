import re
import pytest

def format_for_zulip(content):
    """
    Ensure line-by-line and inline formulas comply with Zulip syntax.

    Args:
        content (str): The input text content.

    Returns:
        str: The replaced text content.
    """

    # Refer to Zulip's LaTeX syntax https://zulip.com/help/latex#latex

    # Replace all content surrounded by two $$ with a format starting with ```math and ending with ```.
    # Replace all content surrounded by \[ \] with a format starting with ```math and ending with ```.
    # Replace all content surrounded by equation with a format starting with ```math and ending with ```.
    content = re.sub(r'\s*\$\$\s*(.*?)\s*\$\$\s*', r'\n```math\n\1\n```\n', content, flags=re.DOTALL)
    content = re.sub(r'\s*\\\[\s*(.*?)\s*\\\]\s*', r'\n```math\n\1\n```\n', content, flags=re.DOTALL)
    content = re.sub(r'\s*\\begin\{equation\*?\}\s*(.*?)\s*\\end\{equation\*?\}\s*', r'\n```math\n\1\n```\n', content, flags=re.DOTALL)
    
    # In Zulip's markdown syntax, only content between two $$ is recognized as an inline math formula.
    content = re.sub(r'(?<!\$)\$\s*([^\$]+?)\s*\$', r'$$\1$$', content)
    content = re.sub(r'\\\(\s*(.*?)\s*\\\)', r'$$\1$$', content)

    return content

# -- Testing ----------

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

# Run tests
if __name__ == "__main__":
    pytest.main(["-v", __file__])