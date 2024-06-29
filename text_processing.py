# 静态导入
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
from latex_linter.repalce_all_markdown import repalce_all_markdown
from latex_linter.replace_equation_aligned import replace_equation_aligned
from latex_linter.replace_stars_with_textbf import replace_stars_with_textbf
from latex_linter.replace_stars_with_textit import replace_stars_with_textit
from latex_linter.square_brackets_to_dollars import square_brackets_to_dollars
from latex_linter.square_brackets_to_equations import square_brackets_to_equations
from latex_linter.format_math_display_multiply_lines import format_aligns


def replace_text(content, options):
    """
    根据用户选择，执行相应的替换操作。
    """

    # ====================================
    # 通用功能
    # ====================================

    # ---------- 在中日韩字符和英文或数字之间添加空格 ----------
    if options['add_space_between_cjk_and_english']:
        content = add_space_between_cjk_and_english(content)

    # ---------- 将多行空行变成单行空行 ----------
    if options['remove_extra_newlines']:
        content = remove_extra_newlines(content)

    # ====================================
    # 数学公式
    # ====================================

    # ---------- 行内公式：规范 $ ... $ 环境 ----------
    if options['format_single_dollar']:
        content = format_single_dollar(content)

    # ---------- 行内公式：规范 \( ... \) 环境 ----------
    if options['format_parentheses']:
        content = format_parentheses(content)

    # ---------- 行内公式：替换 \( ... \) 为 $ ... $ 环境 ----------
    if options['parentheses_to_single_dollar']:
        content = parentheses_to_single_dollar(content)
        content = format_single_dollar(content)

    # ---------- 行间公式：规范 equation 环境 ----------
    if options['format_equations']:
        content = format_equations(content)

    # ---------- 行间公式：规范 $$ ... $$ 环境 ----------
    if options['format_dollars']:
        content = format_dollars(content)

    # ---------- 行间公式：规范 \[ ... \] 环境 ----------
    if options['format_square_brackets']:
        content = format_square_brackets(content)

    # ---------- 行间公式：替换 \[ ... \] 为 $$ ... $$ 环境 ----------
    if options['square_brackets_to_dollars']:
        content = square_brackets_to_dollars(content)
        content = format_dollars(content)

    # ---------- 行间公式：替换 equation 为 $$ ... $$ 环境 ----------
    if options['equations_to_dollars']:
        content = equations_to_dollars(content)
        content = format_dollars(content)

    # ---------- 行间公式：替换 \[ ... \] 为 equation 环境 ----------
    if options['square_brackets_to_equations']:
        content = square_brackets_to_equations(content)
        content = format_equations(content)

    # ---------- 行间公式：替换 $$ ... $$ 为 equation 环境 ----------
    if options['dollars_to_equations']:
        content = dollars_to_equations(content)
        content = format_equations(content)

    # ---------- 将内嵌在 equation 中的 aligned 环境变成单独的 align 环境 ----------
    if options['replace_equation_aligned']:
        content = replace_equation_aligned(content)

    # ---------- 去掉 align 和 equation 环境中用于不显示tag的 * 号 ----------
    if options['remove_asterisks_tags']:
        content = remove_asterisks_tags(content)

    # ====================================
    # 其他latex特性
    # ====================================

    # ---------- 规范 \item 格式 ----------
    if options['format_item']:
        content = format_item(content)

    # ---------- 将各级标题（例如 \section \subsection 等）的英文首字母大写，并去掉被包围文本的首尾空白字符，同时内部多个空字符变成一个空格 ----------
    if options['capitalize_titles']:
        content = capitalize_titles(content)

    # ---------- 规范 align 环境 ----------
    if options['format_aligns']:
        content = format_aligns(content)

    # ====================================
    # 针对 Markdown 特性的功能
    # ====================================

    # ---------- 将 Markdown 的标题等变成 latex 对应物 ----------
    if options['convert_markdown_titles_to_latex']:
        content = convert_markdown_titles_to_latex(content)

    # ---------- 将 Markdown 的 ** 包围变成 \\textbf 环境 ----------
    if options['replace_stars_with_textbf']:
        content = replace_stars_with_textbf(content)

    # ---------- 将 Markdown 的 * 包围变成 \\textit 环境 ----------
    if options['replace_stars_with_textit']:
        content = replace_stars_with_textit(content)

    # ---------- 去掉所有 Markdown 特征 ----------
    if options['repalce_all_markdown']:
        content = repalce_all_markdown(content)

    return content