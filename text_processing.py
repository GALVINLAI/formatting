from latex_linter.add_space_between_cjk_and_english import add_space_between_cjk_and_english
from latex_linter.capitalize_titles import capitalize_titles
from latex_linter.convert_markdown_titles_to_latex import convert_markdown_titles_to_latex
from latex_linter.dollars_to_equations import dollars_to_equations
from latex_linter.equations_to_dollars import equations_to_dollars
from latex_linter.format_item import format_item
from latex_linter.format_math_display import format_equations, format_dollars, format_square_brackets
from latex_linter.format_math_inline import format_single_dollar, format_parentheses
from latex_linter.parentheses_to_single_dollar import parentheses_to_single_dollar
from latex_linter.remove_asterisks_tags import remove_asterisks_tags
from latex_linter.remove_extra_newlines import remove_extra_newlines
from latex_linter.replace_all_markdown import replace_all_markdown
from latex_linter.replace_equation_aligned import replace_equation_aligned
from latex_linter.replace_stars_with_textbf import replace_stars_with_textbf
from latex_linter.replace_stars_with_textit import replace_stars_with_textit
from latex_linter.square_brackets_to_dollars import square_brackets_to_dollars
from latex_linter.square_brackets_to_equations import square_brackets_to_equations
from latex_linter.format_math_display_multiply_lines import format_aligns
from latex_linter.some_small_utilities import some_small_utilities 
from latex_linter.equations_to_equations_star import equations_to_equations_star 
from latex_linter.format_for_zulip import format_for_zulip
from latex_linter.new_feature_name import new_feature_name

def replace_text(content, options):
    """
    Perform corresponding replacement operations based on user choices.
    """

    # ====================================
    # General Features
    # ====================================

    # ---------- Add space between CJK characters and English or digits ----------
    if options['add_space_between_cjk_and_english']:
        content = add_space_between_cjk_and_english(content)

    # ---------- Convert multiple blank lines into single blank lines ----------
    if options['remove_extra_newlines']:
        content = remove_extra_newlines(content)

    # ====================================
    # Mathematical Formulas
    # ====================================

    # ---------- Inline formulas: Standardize $ ... $ environment ----------
    if options['format_single_dollar']:
        content = format_single_dollar(content)

    # ---------- Inline formulas: Standardize \( ... \) environment ----------
    if options['format_parentheses']:
        content = format_parentheses(content)

    # ---------- Inline formulas: Replace \( ... \) with $ ... $ environment ----------
    if options['parentheses_to_single_dollar']:
        content = parentheses_to_single_dollar(content)
        content = format_single_dollar(content)

    # ---------- Display formulas: Standardize equation environment ----------
    if options['format_equations']:
        content = format_equations(content)

    # ---------- Display formulas: Standardize $$ ... $$ environment ----------
    if options['format_dollars']:
        content = format_dollars(content)

    # ---------- Display formulas: Standardize \[ ... \] environment ----------
    if options['format_square_brackets']:
        content = format_square_brackets(content)

    # ---------- Display formulas: Replace \[ ... \] with $$ ... $$ environment ----------
    if options['square_brackets_to_dollars']:
        content = square_brackets_to_dollars(content)
        content = format_dollars(content)

    # ---------- Display formulas: Replace equation with $$ ... $$ environment ----------
    if options['equations_to_dollars']:
        content = equations_to_dollars(content)
        content = format_dollars(content)

    # ---------- Display formulas: Replace \[ ... \] with equation environment ----------
    if options['square_brackets_to_equations']:
        content = square_brackets_to_equations(content)
        content = format_equations(content)

    # ---------- Display formulas: Replace $$ ... $$ with equation environment ----------
    if options['dollars_to_equations']:
        content = dollars_to_equations(content)
        content = format_equations(content)

    # ---------- Convert embedded aligned environment within equation to separate align environment ----------
    if options['replace_equation_aligned']:
        content = replace_equation_aligned(content)

    # ---------- Remove asterisks used for not displaying tags in align and equation environments ----------
    if options['remove_asterisks_tags']:
        content = remove_asterisks_tags(content)

    # ====================================
    # Other LaTeX Features
    # ====================================

    # ---------- Standardize \item format ----------
    if options['format_item']:
        content = format_item(content)

    # ---------- Capitalize the first letter of English titles (e.g., \section, \subsection, etc.), trim surrounding whitespace, and convert multiple internal spaces to a single space ----------
    if options['capitalize_titles']:
        content = capitalize_titles(content)

    # ---------- Standardize align environment ----------
    if options['format_aligns']:
        content = format_aligns(content)

    if options['some_small_utilities']:
        content = some_small_utilities(content)

    if options['equations_to_equations_star']:
        content = equations_to_equations_star(content)

    # ---------- Make display and inline formulas conform to Zulip syntax ----------
    if options['format_for_zulip']:
        content = format_for_zulip(content)

    # ====================================
    # Features for Markdown
    # ====================================

    # ---------- Convert Markdown titles, etc., to corresponding LaTeX elements ----------
    if options['convert_markdown_titles_to_latex']:
        content = convert_markdown_titles_to_latex(content)

    # ---------- Convert Markdown's ** enclosure to \textbf environment ----------
    if options['replace_stars_with_textbf']:
        content = replace_stars_with_textbf(content)

    # ---------- Convert Markdown's * enclosure to \textit environment ----------
    if options['replace_stars_with_textit']:
        content = replace_stars_with_textit(content)

    # ---------- Remove all Markdown features ----------
    if options['replace_all_markdown']:
        content = replace_all_markdown(content)

    # ---------- Custom new feature (for demonstration purposes only) ----------
    if options['new_feature_name']:
        content = new_feature_name(content)

    return content