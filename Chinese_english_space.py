import re
'''
在中日韩字符和英文或数字之间添加空格
'''
def add_space_between_cjk_and_english(text: str) -> str:
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

# 测试示例
text = """
这是一段包含中文和English的句子。2024年是一个特别的年份。
これは日本語とEnglishを含む文です。2024 年は特別な年です。
이것은 한국어와English가 포함된 문장입니다. 2024년은 특별한 해로.
"""

text2 = """
在LeanCloud上，數據儲存是圍繞AVObject進行的。
今天出去買菜花了5000元。
我家的光纖入屋寬頻有 10Gbps，SSD 一共有 20TB。
新MacBook Pro有15%的CPU性能提升。
"""

result = add_space_between_cjk_and_english(text2)
print(result)
