import os
import nbformat
import re
from openai import OpenAI

'''
自动将本仓库中的所有py，md文件翻译成指定语言。翻译好的文件会直接覆盖原文件。
注意：需要你自行注册并获得自己的deepseek API key。然后将其存放在环境变量中DEEPSEEK_API_KEY。
或者使用其他LLM的API key。
'''

# 从环境变量中读取 API 密钥
api_key = os.getenv("DEEPSEEK_API_KEY")
if not api_key:
    raise ValueError("Please set the DEEPSEEK_API_KEY environment variable.")

client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")

def translate_text(text, prompt):
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": text},
        ],
        stream=False
    )
    translation = response.choices[0].message.content.strip()
    return translation


def contains_chinese(text):
    return re.search(r'[\u4e00-\u9fff]', text) is not None

def deal_python_block(content, prompt):
    if content.startswith('```python'):
        content = content[len('```python'):].strip()
    if content.endswith('```'):
        content = content[:-len('```')].strip()
    return content
    
def translate_notebook(input_path, output_path, target_language):
    with open(input_path, 'r', encoding='utf-8') as f:
        notebook = nbformat.read(f, as_version=4)
    
    total_cells = len(notebook.cells)
    contains_chinese_flag = any(contains_chinese(cell.source) for cell in notebook.cells)
    
    if not contains_chinese_flag:
        print(f"No Chinese characters found in the notebook {input_path}. Skipping translation.")
        return
    
    for idx, cell in enumerate(notebook.cells):
        print(f"Processing cell {idx + 1} of {total_cells} in file {input_path} ({(idx + 1) / total_cells:.2%} complete)")
        if contains_chinese(cell.source):
            if cell.cell_type == 'markdown':
                prompt = f"将以下中文Markdown内容翻译为{target_language}。只返回翻译后的Markdown代码。对于latex数学格式，内联数学内容需要使用$符号，行间数学内容需要用$$符号。"
                cell.source = translate_text(cell.source, prompt)
            elif cell.cell_type == 'code':
                prompt = f"将下面代码脚本中的注释翻译为{target_language}。不要修改代码本身。只返回完全翻译的代码脚本。"
                translated_content = translate_text(cell.source, prompt)
                cell.source = deal_python_block(translated_content)
        else:
            print(f"No Chinese characters found in cell {idx + 1} of file {input_path}. Skipping translation.")
    
    with open(output_path, 'w', encoding='utf-8') as f:
        nbformat.write(notebook, f)

    print(f"Translation completed for {input_path}. Output saved to {output_path}")

def translate_file(input_path, output_path, target_language, file_type):
    with open(input_path, 'r', encoding='utf-8') as f:
        content = f.read()

    if contains_chinese(content, prompt):
        if file_type == 'markdown':
            prompt = f"将以下中文Markdown内容翻译为{target_language}。只返回翻译后的Markdown代码。"
        elif file_type == 'python':
            prompt = f"将下面代码脚本中的注释翻译为{target_language}。不要修改代码本身。只返回完全翻译的代码脚本。"
        
        print(f"Processing {file_type} file {input_path}")

        split_index = 212
        lines = content.splitlines()
        if len(lines) > 300:
            # When the .py file has more than 300 lines, an error will be thrown and the user will be notified to manually specify the split line number:
            first_half = "\n".join(lines[:split_index])
            second_half = "\n".join(lines[split_index:])
            translated_first_half = deal_python_block(translate_text(first_half))
            translated_second_half = deal_python_block(translate_text(second_half))
            translated_content = translated_first_half + "\n" + translated_second_half
        else:
            translated_content = deal_python_block(translate_text(content, prompt))

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(translated_content)

        print(f"Translation completed for {input_path}. Output saved to {output_path}")
    else:
        print(f"No Chinese characters found in {input_path}. Skipping translation.")

def process_files(base_path, target_language='英文'):
    for root, _, files in os.walk(base_path):
        for file in files:
            file_path = os.path.join(root, file)
            if file in excluded_files:
                print(f"Skipping excluded file {file_path}")
                continue
            if file.endswith('.ipynb'):
                output_path = file_path.replace('.ipynb', '.ipynb') # '_translated.ipynb'
                translate_notebook(file_path, output_path, target_language)
            elif file.endswith('.py'):
                output_path = file_path.replace('.py', '.py')
                translate_file(file_path, output_path, target_language, 'python')
            elif file.endswith('.md'):
                output_path = file_path.replace('.md', '.md')
                translate_file(file_path, output_path, target_language, 'markdown')

# 示例调用
base_path = 'latex_linter' # 指定文件夹
base_path = './'

# 指定要排除的文件名列表
excluded_files = [
    'example.ipynb',
    'checkbox_states.json',
    'tanslate_ai.py'
]

process_files(base_path, target_language='英文')

