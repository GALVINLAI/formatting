"""
规范化各级标题
"""

import re
import pytest

def capitalize_titles(content):
    """
    将给定的LaTeX文档内容中的标题（如\\part, \\chapter, \\section等）进行首字母大写处理。
    
    Args:
        content (str): 包含LaTeX标题的文档内容。
    
    Returns:
        str: 处理后的文档内容，其中标题的首字母已大写。
    
    Note:
        - 该函数使用正则表达式对文档中的标题进行匹配和处理。
        - 标题后的内容将被视为一个整体字符串，并去除其首尾空白字符和结尾的标点符号。
        - 标题中的每个单词（除了指定的例外词汇）的首字母将被大写。
        - 特定的缩写词（全大写的且长度至少为2的单词）将保持原样。
        - 标题后的内容将被包裹在{}中，并在其后添加换行符。
    """
    
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
        对匹配的文本进行格式化处理，包括去除首尾空白、将多个空白字符变成一个空格，以及将每个单词的首字母大写（排除特定词汇）。
        
        Args:
            match: 一个匹配对象，该对象包含了原始字符串中的匹配文本。
        
        Returns:
            str: 格式化后的字符串，包括匹配前的文本、处理后的文本和换行符。
        
        """
        text = match.group(2).strip()  # 去掉首尾空白字符
        text = text.rstrip(" .,;:!。，；：！")  # 去掉结尾标点符号
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
        return match.group(1) + '{' + capitalized_text + '}\\n\\n'

    # 注意，此行代码使用贪婪模式。有效的前提是，例如 \section{title} 后面另起一行。
    content = re.sub(r'((?:\\part|\\chapter|\\section|\\subsection|\\subsubsection|\\paragraph|\\subparagraph)\*?)\{(.*)\}', capitalize, content)

    return content

# 测试用例
@pytest.mark.parametrize(
    "input_text, expected_output",
    [
        (r"\section{introduction}", r"\section{Introduction}\n\n"),
        (r"\subsection{related work}", r"\subsection{Related Work}\n\n"),
        (r"\subsubsection{the importance of AI}", r"\subsubsection{The Importance of AI}\n\n"),
        (r"\section*{abstract}", r"\section*{Abstract}\n\n"),
        (r"\chapter{summary and conclusions}", r"\chapter{Summary and Conclusions}\n\n"),
        (r"\paragraph{this is a test}", r"\paragraph{This is a Test}\n\n"),
        (r"\section{A simple test}", r"\section{A Simple Test}\n\n"),
        (r"\section{NASA and the future}", r"\section{NASA and the Future}\n\n"),
#        (r"\subsection{use of iPhones in research}", r"\subsection{Use of iPhones in Research}\n\n"),
    ]
)
def test_capitalize_titles(input_text, expected_output):
    assert capitalize_titles(input_text) == expected_output

# 运行测试
if __name__ == "__main__":
    pytest.main(["-v", __file__])
