import re
import pytest
# from latex_linter.format_item import format_item

def replace_fullwidth_punctuation(content):
    """
    将常见的全角标点符号替换为英文的标点符号，同时处理小数点、邮箱和网址
    """
    # 定义全角标点符号与其对应的英文标点符号的映射
    punctuation_map = {
        '，': ',',
        '、': ',',
        '。': '.',
        '！': '!',
        '？': '?',
        '：': ':',
        '；': ';',
        '（': '(',
        '）': ')',
        '【': '[',
        '】': ']',
        '“': '"',
        '”': '"',
        '‘': "'",
        '’': "'",
    }

    # 替换全角标点符号为对应的英文标点符号
    for fullwidth, halfwidth in punctuation_map.items():
        content = content.replace(fullwidth, halfwidth)

    # 使用正则表达式去除中文字符之间的空格
    content = re.sub(r'(?<=[\u4e00-\u9fff]) +(?=[\u4e00-\u9fff])', '', content)
    
    # 确保半角标点符号前面没有空格，排除数字中的小数点和邮箱、网址的处理
    # 排除紧接着数字和字母的 . 号
    content = re.sub(r' +(?=[,!?;:()"\[\]])(?!\w)', '', content)

    # 确保半角标点符号后面有且仅有一个空格，排除小数点、邮箱和网址的处理
    # 使用负向前瞻排除紧接着数字或字母的点号 . 
    # content = re.sub(r'([,.!?;:])', r'\1 ', content)
    

    # 1. 处理 ,!?;: 后面的空格，点号在此不处理
    # 负向前瞻 (?=\S) 确保标点后面有非空白字符
    content = re.sub(r'([,!?;:])(?=\S)', r'\1 ', content)

    # 2. 处理点号 .，但排除前后同时是字母或数字的情况（小数点、邮箱和网址的不处理点号）
    # 使用负向前瞻和负向后瞻，确保点号前后不能同时是字母或数字
    content = re.sub(r'(?<![a-zA-Z0-9])\.(?![a-zA-Z0-9])(?=\S)', r'. ', content)

    # 如果有多余的空格，替换为一个空格
    content = re.sub(r'([,.!?;:]) {2,}', r'\1 ', content)  

    # 将行间公式末尾的常见标点符号移到 $ 符号外面
    content = re.sub(r'\$(.*?)\s*([.,!?;:])\$', r'$\1$\2', content)
    content = re.sub(r'\\right\$(\.)', r'\\right.$', content) # debug：将 “\right$.”  变成  “\right.$”


    # 确保括号包围的内容首尾没有多余的空格
    content = re.sub(r'\(\s*(.*?)\s*\)', r'(\1)', content)

    # 确保左括号前面有且仅有一个空格
    content = re.sub(r'(?<!\s)\(', r' (', content)

    # content = format_item(content)

    # 处理 \href{xx} 中内容的空格，移除花括号内的空格
    content = re.sub(r'\\href{(.*?)}', lambda m: r'\href{' + m.group(1).replace(' ', '') + '}', content)

    # 将 "$ ." 替换为 "$."
    content = re.sub(r'\$\s*\.', r'$.', content)

    return content

# 测试用例
@pytest.mark.parametrize(
    "input_text, expected_output",
    [
        ("你好，世界！", "你好, 世界!"),
        ("这是一个测试。", "这是一个测试."),
        ("（测试）", "(测试)"),
        ("使用【全角】符号。", "使用[全角]符号."),
        ("‘单引号’和“双引号”。", "'单引号'和\"双引号\"."),
        ("数值 3.14 是小数。", "数值 3.14 是小数."),
        ("网址是 example.com。", "网址是 example.com."),
        ("邮箱是 test@example.com。", "邮箱是 test@example.com."),
    ]
)
def test_replace_fullwidth_punctuation(input_text, expected_output):
    assert replace_fullwidth_punctuation(input_text) == expected_output

# 运行测试
if __name__ == "__main__":
    pytest.main(["-v", __file__])
