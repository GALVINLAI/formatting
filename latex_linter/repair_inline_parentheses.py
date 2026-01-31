r"""
将 GPT 输出中疑似数学的 ( ... ) 识别为行内公式并改为 \( ... \)
"""

import re
import pytest

# 跳过已有数学环境，避免在数学块内部再次替换括号
_MATH_SPAN_RE = re.compile(
    r'('
    r'\$\$.*?\$\$'
    r'|\\\[.*?\\\]'
    r'|\\begin\{equation\*?\}.*?\\end\{equation\*?\}'
    r'|\\begin\{align\*?\}.*?\\end\{align\*?\}'
    r'|\\\(.*?\\\)'
    r'|(?<!\$)\$[^$\n]+?\$(?!\$)'
    r')',
    flags=re.DOTALL
)

# 仅匹配非嵌套括号，且括号两侧不是字母/数字/下划线或反斜杠
def _is_mathish(text: str) -> bool:
    stripped = text.strip()
    if not stripped:
        return False
    if re.search(r'[\u4e00-\u9fff\u30a0-\u30ff\u3040-\u309f\uac00-\ud7af]', stripped):
        return False
    if re.search(r'\\[a-zA-Z]+', stripped):
        return True
    if re.search(r'[\^_]', stripped):
        return True
    if re.search(r'[=<>]', stripped):
        return True
    if re.search(r'[A-Za-z0-9]\s*[+\-*/]\s*[A-Za-z0-9]', stripped):
        return True
    if re.search(r'\|[^|]+\|', stripped):
        return True
    return False


def _is_escaped(text: str, idx: int) -> bool:
    backslashes = 0
    j = idx - 1
    while j >= 0 and text[j] == '\\':
        backslashes += 1
        j -= 1
    return backslashes % 2 == 1


def _find_parentheses_pairs(text: str):
    stack = []
    pairs = []
    for i, ch in enumerate(text):
        if ch == '(' and not _is_escaped(text, i):
            stack.append(i)
        elif ch == ')' and not _is_escaped(text, i):
            if stack:
                start = stack.pop()
                pairs.append((start, i))
    return pairs


def _repair_inline_parentheses_plain(text: str) -> str:
    pairs = _find_parentheses_pairs(text)
    if not pairs:
        return text

    candidates = []
    for start, end in pairs:
        inner = text[start + 1:end]
        if '\n' in inner:
            continue
        if start > 0 and re.match(r'[A-Za-z0-9_\\]', text[start - 1]):
            continue
        if end + 1 < len(text) and re.match(r'[A-Za-z0-9_\\]', text[end + 1]):
            continue
        if not _is_mathish(inner):
            continue
        candidates.append((start, end))

    if not candidates:
        return text

    # 选择外层优先，避免嵌套 \( \)
    candidates.sort(key=lambda p: (p[0], -(p[1] - p[0])))
    selected = []
    for start, end in candidates:
        overlaps = False
        for s_start, s_end in selected:
            if not (end < s_start or start > s_end):
                overlaps = True
                break
        if not overlaps:
            selected.append((start, end))

    if not selected:
        return text

    out = text
    for start, end in sorted(selected, key=lambda p: p[0], reverse=True):
        inner = out[start + 1:end]
        out = out[:start] + f'\\({inner}\\)' + out[end + 1:]
    return out


def repair_inline_parentheses(content: str) -> str:
    """
    将非数学环境中的 ( ... )，若内容看起来像数学表达式，则替换为 \\( ... \\)。
    这是保守策略：只在明显“数学化”时转换，以避免误伤普通括号。
    """
    parts = _MATH_SPAN_RE.split(content)
    for i in range(0, len(parts), 2):
        parts[i] = _repair_inline_parentheses_plain(parts[i])
    return ''.join(parts)


@pytest.mark.parametrize(
    "input_text, expected_output",
    [
        (
            "设 (f:\\mathbb{R}^n\\to\\mathbb{R}) 在点 (x^\\star) 可微。",
            "设 \\(f:\\mathbb{R}^n\\to\\mathbb{R}\\) 在点 \\(x^\\star\\) 可微。",
        ),
        (
            "当 (t=0) 时，(r>0) 成立。",
            "当 \\(t=0\\) 时，\\(r>0\\) 成立。",
        ),
        (
            "普通括号 (see Appendix) 不应被替换。",
            "普通括号 (see Appendix) 不应被替换。",
        ),
        (
            "函数调用 f(x) 不应被替换。",
            "函数调用 f(x) 不应被替换。",
        ),
        (
            "函数调用 f(x^2) 不应被替换。",
            "函数调用 f(x^2) 不应被替换。",
        ),
        (
            "已有数学 $ (x+y) $ 不应被替换。",
            "已有数学 $ (x+y) $ 不应被替换。",
        ),
        (
            "行间 \\[ (x+y) \\] 不应被替换。",
            "行间 \\[ (x+y) \\] 不应被替换。",
        ),
        (
            "这只有在 (\\nabla f (x^\\star)=0) 时才可能成立。",
            "这只有在 \\(\\nabla f (x^\\star)=0\\) 时才可能成立。",
        ),
        (
            "（中文）(否则取 (d=\\nabla f (x^\\star)) 会得到 (|\\nabla f (x^\\star)|^2>0) 矛盾)。",
            "（中文）(否则取 \\(d=\\nabla f (x^\\star)\\) 会得到 \\(|\\nabla f (x^\\star)|^2>0\\) 矛盾)。",
        ),
    ],
)
def test_repair_inline_parentheses(input_text, expected_output):
    assert repair_inline_parentheses(input_text) == expected_output


if __name__ == "__main__":
    pytest.main(["-v", __file__])
