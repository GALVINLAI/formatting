import os
import importlib

# 动态导入 latex_linter 文件夹中的所有函数
module_path = "latex_linter"

# 获取 latex_linter 文件夹中的所有 Python 文件
module_files = [f for f in os.listdir(module_path) if f.endswith('.py') and f != '__init__.py']

# 动态导入所有函数到当前命名空间
for module_file in module_files:
    module_name = module_file[:-3]  # 去掉 .py 扩展名
    module = importlib.import_module(f"{module_path}.{module_name}")
    globals()[module_name] = getattr(module, module_name)

def replace_text(content, options):
    """
    根据用户选择，执行相应的替换操作。
    """
    # ---------- 将多行空行变成单行空行 ----------
    if options['remove_extra_newlines']:
        content = remove_extra_newlines(content)

    # ---------- 将各级标题（例如 \section \subsection 等）的英文首字母大写，并去掉被包围文本的首尾空白字符，同时内部多个空字符变成一个空格 ----------
    if options['capitalize_titles']:
        content = capitalize_titles(content)

    # ---------- 将 Markdown 的加粗/斜体/标题等变成 latex 对应物 ----------
    if options['convert_markdown_to_latex']:
        content = convert_markdown_titles_to_latex(content)

    # ---------- 去掉 align 和 equation 环境中用于不显示tag的 * 号 ----------
    if options['remove_asterisks_tags']:
        content = remove_asterisks_tags(content)

    # ---------- 行内公式 1：规范 $ 包围的内部格式 ----------
    if options['format_single_dollar']:
        content = re.sub(r'(?<!\$)(\$)([^\$]+?)(\$)', format_math_inline, content)

    # ---------- 行内公式 2：替换 \( 和 \) 为 $ 包围，并自动规范内部格式 ----------
    if options['parentheses_to_single_dollar']:
        content = parentheses_to_single_dollar(content)

    # ---------- 行间公式 1：规范 equation 环境内部格式 ----------
    if options['format_equations']:
        content = format_equations(content)

    # ---------- 行间公式 2：规范 $$ 环境内部格式 ----------
    if options['format_dollars']:
        content = format_dollars(content)

    # ---------- 行间公式 3：替换 \[ 和 \] 为 $$ 环境，并自动规范内部格式 ----------
    if options['square_brackets_to_dollars']:
        content = square_brackets_to_dollars(content)

    # ---------- 行间公式 4：替换 equation 为 $$ 环境，并自动规范内部格式 ----------
    if options['equations_to_dollars']:
        content = equations_to_dollars(content)

    # ---------- 行间公式 5：替换 \[ 和 \] 为 equation 环境，并自动规范内部格式 ----------
    if options['square_brackets_to_equations']:
        content = square_brackets_to_equations(content)

    # ---------- 行间公式 6：替换 $$ 为 equation 环境，并自动规范内部格式 ----------
    if options['dollars_to_equations']:
        content = dollars_to_equations(content)

    # ---------- 规范 \item 格式 ----------
    if options['format_item']:
        content = format_item(content)

    # ---------- 将内嵌在 equation 中的 aligned 环境变成单独的 align 环境 ----------
    if options['replace_equation_aligned']:
        content = replace_aligned_with_align(content)

    # ---------- 去掉所有Markdown特征 ----------
    if options['repalce_all_markdown']:
        content = repalce_all_markdown(content)

    # ---------- 在中日韩字符和英文或数字之间添加空格 ----------
    if options['add_space_between_cjk_and_english']:
        content = add_space_between_cjk_and_english(content)

    return content