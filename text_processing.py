from latex_linter.add_space_between_cjk_and_english import add_space_between_cjk_and_english
from latex_linter.dollars_to_equations import dollars_to_equations
from latex_linter.equations_to_dollars import equations_to_dollars
from latex_linter.format_math_display import format_equations, format_dollars, format_square_brackets
from latex_linter.format_math_inline import format_single_dollar, format_parentheses
from latex_linter.parentheses_to_single_dollar import parentheses_to_single_dollar
from latex_linter.repair_display_brackets import repair_display_brackets
from latex_linter.repair_inline_parentheses import repair_inline_parentheses, repair_inline_parentheses_aggressive
from latex_linter.remove_extra_newlines import remove_extra_newlines
from latex_linter.square_brackets_to_dollars import square_brackets_to_dollars
from latex_linter.square_brackets_to_equations import square_brackets_to_equations
from latex_linter.format_math_display_multiply_lines import format_aligns
from latex_linter.equations_to_equations_star import equations_to_equations_star 
from latex_linter.replace_fullwidth_punctuation import replace_fullwidth_punctuation
from latex_linter.remove_markdown import remove_markdown
from latex_linter.markdown_to_latex import markdown_to_latex

def replace_text(content, options):
    """
    根据用户选择，执行相应的替换操作。
    """

    # ====================================
    # 通用功能
    # ====================================

    # ---------- 在中日韩字符和英文或数字之间添加空格 ----------
    if options.get('add_space_between_cjk_and_english'):
        content = add_space_between_cjk_and_english(content)

    # ---------- 将多行空行变成单行空行 ----------
    if options.get('remove_extra_newlines'):
        content = remove_extra_newlines(content)

    # ====================================
    # 数学公式
    # ====================================

    # ---------- GPT 缺失斜杠：修复行间 [ ... ] ----------
    if options.get('repair_display_brackets'):
        content = repair_display_brackets(content)

    # ---------- GPT 缺失斜杠：修复行内 ( ... ) ----------
    if options.get('repair_inline_parentheses'):
        content = repair_inline_parentheses(content)

    # ---------- GPT 缺失斜杠：修复行内 ( ... )（激进策略） ----------
    if options.get('repair_inline_parentheses_aggressive'):
        content = repair_inline_parentheses_aggressive(content)

    # ---------- 行内公式：规范 $ ... $ 环境 ----------
    if options.get('format_single_dollar'):
        content = format_single_dollar(content)

    # ---------- 行内公式：规范 \( ... \) 环境 ----------
    if options.get('format_parentheses'):
        content = format_parentheses(content)

    # ---------- 行内公式：替换 \( ... \) 为 $ ... $ 环境 ----------
    if options.get('parentheses_to_single_dollar'):
        content = parentheses_to_single_dollar(content)
        content = format_single_dollar(content)

    # ---------- 行间公式：规范 equation 环境 ----------
    if options.get('format_equations'):
        content = format_equations(content)

    # ---------- 行间公式：规范 $$ ... $$ 环境 ----------
    if options.get('format_dollars'):
        content = format_dollars(content)

    # ---------- 行间公式：规范 \[ ... \] 环境 ----------
    if options.get('format_square_brackets'):
        content = format_square_brackets(content)

    # ---------- 行间公式：替换 \[ ... \] 为 $$ ... $$ 环境 ----------
    if options.get('square_brackets_to_dollars'):
        content = square_brackets_to_dollars(content)
        content = format_dollars(content)

    # ---------- 行间公式：替换 equation 为 $$ ... $$ 环境 ----------
    if options.get('equations_to_dollars'):
        content = equations_to_dollars(content)
        content = format_dollars(content)

    # ---------- 行间公式：替换 \[ ... \] 为 equation 环境 ----------
    if options.get('square_brackets_to_equations'):
        content = square_brackets_to_equations(content)
        content = format_equations(content)

    # ---------- 行间公式：替换 $$ ... $$ 为 equation 环境 ----------
    if options.get('dollars_to_equations'):
        content = dollars_to_equations(content)
        content = format_equations(content)

    # ====================================
    # 其他latex特性
    # ====================================

    # ---------- 规范 align 环境 ----------
    if options.get('format_aligns'):
        content = format_aligns(content)

    if options.get('equations_to_equations_star'):
        content = equations_to_equations_star(content)

    # ====================================
    # 针对 Markdown 特性的功能
    # ====================================

    # ---------- 一键去除 Markdown 标记 ----------
    if options.get('remove_markdown'):
        content = remove_markdown(content)

    # ---------- 一键把 Markdown 标记变成 LaTeX ----------
    if options.get('markdown_to_latex'):
        content = markdown_to_latex(content)

    # ---------- 高数B讲义制作用 ----------
    if options.get('replace_fullwidth_punctuation'):
        content = replace_fullwidth_punctuation(content)

    return content
