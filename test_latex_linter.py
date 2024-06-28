import unittest, re
from text_processing import (
    add_space_between_cjk_and_english,
    remove_extra_newlines,
    format_math_inline,
    format_math_display,
    capitalize_titles,
    replace_stars_with_textbf,
    replace_stars_with_textit,
    convert_markdown_titles_to_latex,
    replace_text
)

class TestLatexLinter(unittest.TestCase):
    def test_add_space_between_cjk_and_english(self):
        text = "你好world"
        expected = "你好 world"
        self.assertEqual(add_space_between_cjk_and_english(text), expected)

    def test_remove_extra_newlines(self):
        text = "Line 1\n\n\nLine 2"
        expected = "Line 1\n\nLine 2"
        self.assertEqual(remove_extra_newlines(text), expected)

    def test_format_math_inline(self):
        text = r"This is a test $a + b = c$."
        match = re.search(r'(?<!\$)(\$)([^\$]+?)(\$)', text)
        expected = r"This is a test $a + b = c$."
        self.assertEqual(format_math_inline(match), expected)

    def test_format_math_display(self):
        text = r"\begin{equation}a + b = c\label{eq1}\end{equation}"
        match = re.search(r'(\s*\\begin\{equation\*?\})(.*?)(\\end\{equation\*?\}\s*)', text, re.DOTALL)
        expected = r"\begin{equation}\label{eq1}\n    a + b = c\n\end{equation}"
        self.assertEqual(format_math_display(match), expected)

    def test_capitalize_titles(self):
        content = r"\section{a test section}"
        expected = r"\section{A Test Section}"
        self.assertEqual(capitalize_titles(content), expected)

    def test_replace_stars_with_textbf(self):
        text = "This is **bold** text."
        expected = "This is \\textbf{bold} text."
        self.assertEqual(replace_stars_with_textbf(text), expected)

    def test_replace_stars_with_textit(self):
        text = "This is *italic* text."
        expected = "This is \\textit{italic} text."
        self.assertEqual(replace_stars_with_textit(text), expected)

    def test_convert_markdown_titles_to_latex(self):
        content = "# Section Title\n## Subsection Title"
        expected = "\\section{Section Title}\n\\subsection{Subsection Title}"
        self.assertEqual(convert_markdown_titles_to_latex(content), expected)

    def test_replace_text(self):
        content = "你好world\n\n\nThis is **bold** text."
        options = {
            'remove_extra_newlines': True,
            'capitalize_titles': False,
            'format_single_dollar': False,
            'parentheses_to_single_dollar': False,
            'format_equations': False,
            'format_dollars': False,
            'square_brackets_to_dollars': False,
            'equations_to_dollars': False,
            'square_brackets_to_equations': False,
            'dollars_to_equations': False,
            'remove_asterisks_tags': False,
            'format_item': False,
            'convert_markdown_to_latex': True,
            'replace_equation_aligned': False,
            'repalce_all_markdown': False,
            'add_space_between_cjk_and_english': True
        }
        expected = "你好 world\n\nThis is \\textbf{bold} text."
        self.assertEqual(replace_text(content, options), expected)

if __name__ == '__main__':
    unittest.main()
