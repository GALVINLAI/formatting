"""
去除 Markdown 标记（标题/加粗/斜体）
"""

import re


def remove_markdown(content: str) -> str:
    """
    删除最常见的 Markdown 标记：
    - # / ## / ### 标题前缀
    - **bold** -> bold
    - *italic* -> italic
    说明：只做轻量级清理，避免破坏普通文本。
    """
    content = re.sub(r'^#{1,6} ', '', content, flags=re.MULTILINE)
    # 列表：去掉无序/有序前缀
    content = re.sub(r'^\\s*[-*]\\s+', '', content, flags=re.MULTILINE)
    content = re.sub(r'^\\s*\\d+\\.\\s+', '', content, flags=re.MULTILINE)
    content = re.sub(r'\*\*(.+?)\*\*', r'\1', content)
    content = re.sub(r'(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)', r'\1', content)
    return content
