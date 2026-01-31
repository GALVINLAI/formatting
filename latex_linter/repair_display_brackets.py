r"""
将 GPT 输出中独立成行的 [ ... ] 识别为行间公式并改为 \[ ... \]
"""

import re
import pytest

_OPEN_LINE_RE = re.compile(r'^\s*\[\s*$')
_CLOSE_LINE_RE = re.compile(r'^\s*\]\s*$')


def repair_display_brackets(content: str) -> str:
    """
    将独立成行的 [ 与 ] 转换为 \\[ 与 \\]，用作行间公式定界符。
    仅在 [ 和 ] 各自单独成行时才转换，以避免误伤普通方括号用法。
    """
    lines = content.splitlines(keepends=True)
    out = []
    i = 0
    while i < len(lines):
        line = lines[i]
        if _OPEN_LINE_RE.match(line):
            j = i + 1
            while j < len(lines) and not _CLOSE_LINE_RE.match(lines[j]):
                j += 1
            if j < len(lines):
                out.append(line.replace('[', r'\[', 1))
                out.extend(lines[i + 1:j])
                out.append(lines[j].replace(']', r'\]', 1))
                i = j + 1
                continue
        out.append(line)
        i += 1
    return ''.join(out)


@pytest.mark.parametrize(
    "input_text, expected_output",
    [
        (
            "Text before\n[\n\\nabla f(x^*)=0\n]\nText after\n",
            "Text before\n\\[\n\\nabla f(x^*)=0\n\\]\nText after\n",
        ),
        (
            "  [  \n  x+y=1  \n  ]  \n",
            "  \\[  \n  x+y=1  \n  \\]  \n",
        ),
        (
            "Inline [x+y] should stay.\n",
            "Inline [x+y] should stay.\n",
        ),
        (
            "Lone opening bracket\n[\nNo closing\n",
            "Lone opening bracket\n[\nNo closing\n",
        ),
    ],
)
def test_repair_display_brackets(input_text, expected_output):
    assert repair_display_brackets(input_text) == expected_output


if __name__ == "__main__":
    pytest.main(["-v", __file__])
