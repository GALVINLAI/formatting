import re
import pangu

# TODO 处理title的bug
# \subsection{C. Fubini-study Metric Tensor (Quantum natural gradient)}
# -->
# \subsection{C. Fubini-study Metric Tensor (quantum Natural Gradient)}

# ------------------- 此处，用函数自定义各种复杂的规则 ------------------- 

def add_space_between_cjk_and_english(text: str) -> str:
    '''
    在中日韩字符和英文或数字之间添加空格
    '''
    # 定义正则表达式模式
    cjk_pattern = r'[\u4e00-\u9fff\u30a0-\u30ff\u3040-\u309f\uac00-\ud7af]'
    english_pattern = r'[a-zA-Z0-9]'
    
    # 定义中日韩字符后和前的非字母字符
    english_non_letter_after_cjk = r"-+'\"([¥$"
    english_non_letter_before_cjk = r"-+;:'\"°%$)]"

    # 构建头部和尾部的正则表达式
    head_pattern = re.compile(f'({cjk_pattern})( *)({english_pattern}|[{re.escape(english_non_letter_after_cjk)}])')
    tail_pattern = re.compile(f'({english_pattern}|[{re.escape(english_non_letter_before_cjk)}])( *)({cjk_pattern})')

    # 在中日韩字符和英文或数字之间添加空格
    def add_space(text: str) -> str:
        text = head_pattern.sub(r'\1 \3', text)
        text = tail_pattern.sub(r'\1 \3', text)
        return text

    return add_space(text)


def remove_extra_newlines(content):
    # 将多个连续的空行替换为一个空行
    #  表达式参考 cf: line 24 in https://github.com/platers/obsidian-linter/blob/master/src/rules/consecutive-blank-lines.ts
    content = re.sub(r'(\n([\t\v\f\r \u00a0\u2000-\u200b\u2028-\u2029\u3000]+)?){2,}', '\n\n', content)
    return content

# ---------- 规范行内公式（inline math mode）内部格式 ---------- 
def format_math_inline(match):
    text = match.group(2).strip()  # 去掉首尾空白字符
    text = re.sub(r'\s+', ' ', text)  # 将内部多个空白字符变成一个空格
    text = match.group(1) + text + match.group(3)
    return f'{text}'

# ---------- 规范行间公式（display math mode）内部格式 ---------- 
def format_math_display(match):
    # 提取方程内容
    text = match.group(2)
    # 提取并删除 \label 部分
    label_text = re.findall(r'\\label\{.*?\}', text)
    text = re.sub(r'\\label\{.*?\}', '', text)
    # 去掉首尾空白字符
    text = text.strip()  
    # 将内部连续的2个及以上的空白字符变成一个空格。这里暗示了，内部换行是被允许的。
    text = re.sub(r'\s{2,}', ' ', text)  
    # 重组文本，加入标签和格式化
    if label_text:
        label_text = label_text[0]  # 假设只有一个 \label
        text = f'{label_text}\n    {text}\n'
    else:
        text = f'\n    {text}\n'
    # 组合结果并返回
    formatted_text = f'\n{match.group(1).strip()}{text}{match.group(3).strip()}\n'
    return formatted_text
    
def capitalize_titles(content):
    
    exceptions = {
        "a", "an", "the", "aboard", "about", "abt.", "above", "abreast", "absent", "across", "after", "against", "along",
        "aloft", "alongside", "amid", "amidst", "mid", "midst", "among", "amongst", "anti", "apropos", "around", "round",
        "as", "aslant", "astride", "at", "atop", "ontop", "bar", "barring", "before", "B4", "behind", "below", "beneath",
        "neath", "beside", "besides", "between", "'tween", "beyond", "but", "by", "chez", "circa", "c.", "ca.", "come",
        "concerning", "contra", "counting", "cum", "despite", "spite", "down", "during", "effective", "ere", "except",
        "excepting", "excluding", "failing", "following", "for", "from", "in", "including", "inside", "into", "less",
        "like", "minus", "modulo", "mod", "near", "nearer", "nearest", "next", "notwithstanding", "of", "o'", "off",
        "offshore", "on", "onto", "opposite", "out", "outside", "over", "o'er", "pace", "past", "pending", "per", "plus",
        "post", "pre", "pro", "qua", "re", "regarding", "respecting", "sans", "save", "saving", "short", "since", "sub",
        "than", "through", "thru", "throughout", "thruout", "till", "times", "to", "t'", "touching", "toward", "towards",
        "under", "underneath", "unlike", "until", "unto", "up", "upon", "versus", "vs.", "v.", "via", "vice", "vis-à-vis",
        "wanting", "with", "w/", "w.", "c̄", "within", "w/i", "without", "'thout", "w/o", "abroad", "adrift", "aft",
        "afterward", "afterwards", "ahead", "apart", "ashore", "aside", "away", "back", "backward", "backwards",
        "beforehand", "downhill", "downstage", "downstairs", "downstream", "downward", "downwards", "downwind", "east",
        "eastward", "eastwards", "forth", "forward", "forwards", "heavenward", "heavenwards", "hence", "henceforth",
        "here", "hereby", "herein", "hereof", "hereto", "herewith", "home", "homeward", "homewards", "indoors", "inward",
        "inwards", "leftward", "leftwards", "north", "northeast", "northward", "northwards", "northwest", "now", "onward",
        "onwards", "outdoors", "outward", "outwards", "overboard", "overhead", "overland", "overseas", "rightward",
        "rightwards", "seaward", "seawards", "skywards", "skyward", "south", "southeast", "southwards", "southward",
        "southwest", "then", "thence", "thenceforth", "there", "thereby", "therein", "thereof", "thereto", "therewith",
        "together", "underfoot", "underground", "uphill", "upstage", "upstairs", "upstream", "upward", "upwards", "upwind",
        "west", "westward", "westwards", "when", "whence", "where", "whereby", "wherein", "whereto", "wherewith", "although",
        "because", "considering", "given", "granted", "if", "lest", "once", "provided", "providing", "seeing", "so", "supposing",
        "though", "unless", "whenever", "whereas", "wherever", "while", "whilst", "ago", "according to", "as regards", "counter to",
        "instead of", "owing to", "pertaining to", "at the behest of", "at the expense of", "at the hands of", "at risk of",
        "at the risk of", "at variance with", "by dint of", "by means of", "by virtue of", "by way of", "for the sake of", "for sake of",
        "for lack of", "for want of", "from want of", "in accordance with", "in addition to", "in case of", "in charge of", "in compliance with",
        "in conformity with", "in contact with", "in exchange for", "in favor of", "in front of", "in lieu of", "in light of", "in the light of",
        "in line with", "in place of", "in point of", "in quest of", "in relation to", "in regard to", "with regard to", "in respect to",
        "with respect to", "in return for", "in search of", "in step with", "in touch with", "in terms of", "in the name of", "in view of",
        "on account of", "on behalf of", "on grounds of", "on the grounds of", "on the part of", "on top of", "with a view to", "with the exception of",
        "à la", "a la", "as soon as", "as well as", "close to", "due to", "far from", "in case", "other than", "prior to", "pursuant to",
        "regardless of", "subsequent to", "as long as", "as much as", "as far as", "by the time", "in as much as", "inasmuch", "in order to",
        "in order that", "even", "provide that", "if only", "whether", "whose", "whoever", "why", "how", "or not", "whatever", "what", "both",
        "and", "or", "not only", "but also", "either", "neither", "nor", "just", "rather", "no sooner", "such", "that", "yet", "is", "it"
    }
    
    def capitalize(match):
        """
        对匹配的文本进行一些格式化处理，包括去除首尾空白、将多个空白字符变成一个空格，以及将每个单词的首字母大写（排除特定词汇）
        """
        text = match.group(2).strip()  # 去掉首尾空白字符
        text = text.rstrip(" .,;:!。，；：！") # 去掉结尾标点符号
        text = re.sub(r'\s+', ' ', text)  # 将内部多个空白字符变成一个空格

        # 将内容的每个单词首字母大写
        words = text.split()
        capitalized_words = [
            # 处理第一个单词，如果它已经全大写，则保持不变；否则，将其首字母大写。重点是，不排除exceptions。
            words[0] if words[0].isupper() else words[0].capitalize() 
        ] + [
            # 处理后续的单词。如果单词在 exceptions 列表中，或者全大写，或者是全大写的缩写词（由正则表达式 ^[A-Z]{2,}$ 匹配），则保持不变；否则，将其首字母大写。
            word if word.lower() in exceptions or word.isupper() or re.match(r'^[A-Z]{2,}$', word) else word.capitalize() for word in words[1:]
        ]
        capitalized_text = ' '.join(capitalized_words)
        return match.group(1) + '{' + capitalized_text + '}\n\n'

    # 注意，此行代码使用贪婪模式。有效的前提是，例如 \section{title} 后面另起一行。
    content = re.sub(r'((?:\\part|\\chapter|\\section|\\subsection|\\subsubsection|\\paragraph|\\subparagraph)\*?)\{(.*)\}', capitalize, content)

    return content

def replace_stars_with_textbf(text):
    # 使用lambda函数进行替换，将匹配的内容放入\textbf{}中
    replacement = lambda match: r"\textbf{" + match.group(1) + "}"
    new_text = re.sub(r"\*{2}(.*?)\*{2}", replacement, text)
    return new_text

def replace_stars_with_textit(text):
    # 使用lambda函数进行替换，将匹配的内容放入\textit{}中
    replacement = lambda match: r"\textit{" + match.group(1) + "}"
    new_text = re.sub(r"\*(.*?)\*", replacement, text)
    return new_text

def convert_markdown_titles_to_latex(content):
    # 处理 # title -> \section{title}
    content = re.sub(r'^# (.+)$', r'\\section{\1}', content, flags=re.MULTILINE)
    # 处理 ## title -> \subsection{title}
    content = re.sub(r'^## (.+)$', r'\\subsection{\1}', content, flags=re.MULTILINE)  
    # 处理 ### title -> \subsubsection{title}
    content = re.sub(r'^### (.+)$', r'\\subsubsection{\1}', content, flags=re.MULTILINE)
    # 处理 #### title -> normal text
    content = re.sub(r'^#{4,} (.+)$', r'\1', content, flags=re.MULTILINE)
    return content

# ------------------- 此处，replace_text 汇总各种规则到一个函数中 ------------------- 

def replace_text(content, options):
    """
    这个函数的功能是对文本内容进行以下几种文本替换操作：
    根据用户选择，执行相应的替换操作。
    """

    # 较为简单的规则直接写出

    #############################
    # 以下是处理好的
    #############################

    # ---------- 将多行空行变成单行空行 ----------
    if options['remove_extra_newlines']:
        content = remove_extra_newlines(content)

    # ---------- 将各级标题（例如 \section \subsection 等）的英文首字母大写，并去掉被包围文本的首尾空白字符，同时内部多个空字符变成一个空格 ----------
    if options['capitalize_titles']:
        content = capitalize_titles(content)

    # ---------- 行内公式 1：规范 $ 包围的内部格式 ----------
    # 匹配行内公式
    if options['format_single_dollar']:
        content = re.sub(r'(?<!\$)(\$)([^\$]+?)(\$)', format_math_inline, content)

    # ---------- 行内公式 2：替换 \( 和 \) 为 $ 包围，并自动规范内部格式 ----------
    if options['parentheses_to_single_dollar']:
        # 替换 \( 和 \) 为 $
        content = re.sub(r'\\\(|\\\)', '$', content)
        content = re.sub(r'(?<!\$)(\$)([^\$]+?)(\$)', format_math_inline, content)

    # ---------- 行间公式 1：规范 equation 环境内部格式 ----------
    if options['format_equations']:
        # 特别注意，该匹配必须是 flags=re.DOTALL，即单行模式
        content = re.sub(r'(\s*\\begin\{equation\*?\})(.*?)(\\end\{equation\*?\}\s*)', format_math_display, content, flags=re.DOTALL)

    # ---------- 行间公式 2：规范 $$ 环境内部格式 ----------
    if options['format_dollars']:
        content = re.sub(r'(\s*\$\$)([^\$\$]*?)(\$\$\s*)', format_math_display, content)

    # ---------- 行间公式 3：替换 \[ 和 \] 为 $$ 环境，并自动规范内部格式 ----------
    if options['square_brackets_to_dollars']:
        content = re.sub(r'\\\[|\\\]', '$$', content)
        content = re.sub(r'(\s*\$\$)([^\$\$]*?)(\$\$\s*)', format_math_display, content)

    # ---------- 行间公式 4：替换 equation 为 $$ 环境，并自动规范内部格式 ----------
    if options['equations_to_dollars']:
        content = re.sub(r'\\begin\{equation\}|\\end\{equation\}', '$$', content)
        content = re.sub(r'(\s*\$\$)([^\$\$]*?)(\$\$\s*)', format_math_display, content)

    # ---------- 行间公式 5：替换 \[ 和 \] 为 equation 环境，并自动规范内部格式 ----------
    if options['square_brackets_to_equations']:
        content = re.sub(r'\\\[', r'\\begin{equation}', content)
        content = re.sub(r'\\\]', r'\\end{equation}', content)
        content = re.sub(r'(\s*\\begin\{equation\*?\})(.*?)(\\end\{equation\*?\}\s*)', format_math_display, content, flags=re.DOTALL)

    # ---------- 行间公式 6：替换 $$ 为 equation 环境，并自动规范内部格式 ----------
    if options['dollars_to_equations']:
        def fun_dollars_to_equations(match):
            nonlocal count
            count += 1
            if count % 2 == 1:
                return r'\begin{equation}'
            else:
                return r'\end{equation}'
        count = 0
        content = re.sub(r'\$\$', fun_dollars_to_equations, content)
        content = re.sub(r'(\s*\\begin\{equation\*?\})(.*?)(\\end\{equation\*?\}\s*)', format_math_display, content, flags=re.DOTALL)

    # ---------- 去掉 align 和 equation 环境中用于不显示tag的 * 号 ----------
    if options['remove_asterisks_tags']:
        content = re.sub(r'\\(begin|end)\{(align|equation)\*\}', r'\\\1{\2}', content)
    
    if options['format_item']:
    # ---------- 规范 \item 格式 ----------
        # 确保每个 \item 之前有且仅有一个制表符，并且之后有且仅有一个空格
        content = re.sub(r'(?<!\t)\s*\\item\s*', r'\n    \\item ', content)

    # ---------- 将 Markdown 的加粗/斜体/标题等变成 latex 对应物 ----------
    if options['convert_markdown_to_latex']:
        content = replace_stars_with_textbf(content) # 被两个星号（**）包围的内容，并将其替换为在\textbf{}里
        content = replace_stars_with_textit(content) # 被1个星号（*）包围的内容，并将其替换为在\textit{}里
        content = convert_markdown_titles_to_latex(content) # 被两个星号（**）包围的内容，并将其替换为在\textbf{}里
        content = capitalize_titles(content)

    # ---------- 将内嵌在 equation 中的 aligned 环境变成单独的 align 环境 ---------- 
    if options['replace_equation_aligned']:
        content = re.sub(r'\\begin{equation(\*?)}\s*\\begin{aligned}', r'\\begin{align\1}', content)
        content = re.sub(r'\\end{aligned}\s*\\end{equation(\*?)}', r'\\end{align\1}', content)
    
    if options['repalce_all_markdown']:
        content = re.sub(r"\*\*", '', content) # 删除所有 **
        content = re.sub(r'\#+ ', '', content) # 删除所有##之类的title
        return content       

    if options['add_space_between_cjk_and_english']:
        content = add_space_between_cjk_and_english(content)
        
    # ---------- [以防万一] 将多行空行变成单行空行 ----------
    if options['remove_extra_newlines']:
        content = remove_extra_newlines(content)

    return content

    #############################
    # 以下是待处理的
    #############################
