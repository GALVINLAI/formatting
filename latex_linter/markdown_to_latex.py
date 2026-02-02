"""
将 Markdown 标记（标题/加粗/斜体）转换为 LaTeX 对应物
"""

import re


def markdown_to_latex(content: str) -> str:
    """
    支持的转换：
    - # / ## / ### 标题 -> \\section / \\subsection / \\subsubsection
    - **bold** -> \\textbf{bold}
    - *italic* -> \\textit{italic}
    说明：仅处理最常见的 Markdown 语法，不覆盖所有复杂嵌套情况。
    """
    # 标题
    content = re.sub(r'^# (.+)$', r'\\section{\1}', content, flags=re.MULTILINE)
    content = re.sub(r'^## (.+)$', r'\\subsection{\1}', content, flags=re.MULTILINE)
    content = re.sub(r'^### (.+)$', r'\\subsubsection{\1}', content, flags=re.MULTILINE)

    # 列表：无序与有序（简单一层）
    def convert_list(lines, is_ordered):
        env = 'enumerate' if is_ordered else 'itemize'
        out = [f'\\\\begin{{{env}}}']
        for line in lines:
            if is_ordered:
                m = re.match(r'^\\s*\\d+\\.\\s+(.*)$', line)
            else:
                m = re.match(r'^\\s*[-*]\\s+(.*)$', line)
            if m:
                out.append(f'    \\\\item {m.group(1)}')
        out.append(f'\\\\end{{{env}}}')
        return out

    lines = content.splitlines()
    new_lines = []
    i = 0
    while i < len(lines):
        line = lines[i]
        if re.match(r'^\\s*[-*]\\s+', line):
            block = []
            while i < len(lines) and re.match(r'^\\s*[-*]\\s+', lines[i]):
                block.append(lines[i])
                i += 1
            new_lines.extend(convert_list(block, is_ordered=False))
            continue
        if re.match(r'^\\s*\\d+\\.\\s+', line):
            block = []
            while i < len(lines) and re.match(r'^\\s*\\d+\\.\\s+', lines[i]):
                block.append(lines[i])
                i += 1
            new_lines.extend(convert_list(block, is_ordered=True))
            continue
        new_lines.append(line)
        i += 1
    content = '\n'.join(new_lines)

    # 加粗
    content = re.sub(r'\*\*(.+?)\*\*', r'\\textbf{\1}', content)
    # 斜体（避免处理 ** 已经替换掉）
    content = re.sub(r'(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)', r'\\textit{\1}', content)

    return content
