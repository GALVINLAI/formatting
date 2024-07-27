import os
from openai import OpenAI

# 从环境变量中读取 API 密钥
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("Please set the OPENAI_API_KEY environment variable.")

client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")

def translate_via_ai(text, language="English"):
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": f"Translate all Chinese text to {language} in the following text."},
            {"role": "user", "content": text},
        ],
        stream=False
    )
    return response.choices[0].message.content

def process_file(file_path, split_index=None):
    print(f"Processing file: {file_path}")

    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    if file_path.endswith('.py'):
        lines = content.splitlines()
        if len(lines) > 300:
            # When the .py file has more than 300 lines, an error will be thrown and the user will be notified to manually specify the split line number:
            if split_index is None:
                raise ValueError(f"The file {file_path} has more than 300 lines. Please manually specify the split index.")
            else:
                first_half = "\n".join(lines[:split_index])
                second_half = "\n".join(lines[split_index:])
                
                translated_first_half = translate_via_ai(first_half)
                translated_second_half = translate_via_ai(second_half)
                
                if translated_first_half.startswith('```python'):
                    translated_first_half = translated_first_half[len('```python'):].strip()
                if translated_first_half.endswith('```'):
                    translated_first_half = translated_first_half[:-len('```')].strip()
                    
                if translated_second_half.startswith('```python'):
                    translated_second_half = translated_second_half[len('```python'):].strip()
                if translated_second_half.endswith('```'):
                    translated_second_half = translated_second_half[:-len('```')].strip()
                    
                translated_content = translated_first_half + "\n" + translated_second_half
        else:
            translated_content = translate_via_ai(content)
            
            if translated_content.startswith('```python'):
                translated_content = translated_content[len('```python'):].strip()
            if translated_content.endswith('```'):
                translated_content = translated_content[:-len('```')].strip()
    else:
        translated_content = translate_via_ai(content)

    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(translated_content)

def process_directory(directory, split_index=None):
    for root, _, files in os.walk(directory):
        for file_name in files:
            if file_name.endswith('.py') or file_name.endswith('.md') or file_name.endswith('.json'):
                file_path = os.path.join(root, file_name)
                process_file(file_path, split_index)

# Call the processing function, passing in the root directory path of the code repository
if __name__ == "__main__":
    repo_directory = os.path.dirname(os.path.abspath(__file__))
    split_index = 187  # You can manually specify the split line number here, for example, split_index = 150
    process_directory(repo_directory, split_index)