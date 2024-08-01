import os
import argparse
import sys

'''
该代码旨在自动化将新功能集成到现有的 Python 项目中。它通过在 text_processing.py 和 main.py 文件中插入必要的代码，实现对新功能的支持。用户需要提供新功能的名称和描述，该描述必须用单引号括起来。代码会进行以下操作：

导入新功能：在 text_processing.py 中添加导入语句。
功能调用：在 text_processing.py 中添加或更新功能调用以及注释。
更新选项：在 main.py 中添加或更新功能描述，以便在 GUI 中显示。
'''

def update_text_processing_file(feature_name, feature_description, text_processing_file='text_processing.py'):
    # 更新 text_processing.py 文件
    with open(text_processing_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()  # 读取文件中的所有行
    
    # 检查新功能是否已经集成
    import_statement = f'from latex_linter.{feature_name} import {feature_name}\n'
    function_call = f"    # ---------- {feature_description} ----------\n    if options['{feature_name}']:\n        content = {feature_name}(content)\n\n"
    
    # 如果导入语句尚未添加，则添加到导入语句的开头
    if import_statement not in lines:
        # 找到第一个非导入语句的位置，插入导入语句
        for i, line in enumerate(lines):
            if line.startswith('import') or line.startswith('from'):
                continue
            else:
                lines.insert(i, import_statement)
                break
    
    # 检查是否已经存在新功能的调用并更新注释
    feature_updated = False
    for i, line in enumerate(lines):
        if line.strip().startswith(f"# ----------") and f"if options['{feature_name}']:" in lines[i+1]:
            # 更新注释为新的功能描述
            lines[i] = f"    # ---------- {feature_description} ----------\n"
            feature_updated = True
            print(f"Updated comment for {feature_name} in {text_processing_file}.")
            break

    # 如果功能调用不存在，则在最后一个 return 之前插入新功能调用
    if not feature_updated:
        for i in reversed(range(len(lines))):
            if lines[i].strip().startswith('return'):
                lines.insert(i, function_call)
                print(f"Added new feature call for {feature_name} in {text_processing_file}.")
                break
    
    # 将更新后的内容写回到文件
    with open(text_processing_file, 'w', encoding='utf-8') as file:
        file.writelines(lines)
    
    print(f"Integrated {feature_name} into {text_processing_file}.")

def update_main_file(feature_name, feature_description, main_file='main.py'):
    # 更新 main.py 文件
    with open(main_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()  # 读取文件中的所有行

    # 定义选项行
    option_line = f'    ("{feature_name}", "{feature_description}", False),\n'
    option_updated = False
    
    # 检查并更新功能选项
    for i, line in enumerate(lines):
        # 找到功能名称对应的行，更新描述
        if line.strip().startswith(f'("{feature_name}",'):
            parts = line.split(',')
            if len(parts) >= 3:
                # 更新描述
                parts[1] = f' "{feature_description}"'
                lines[i] = ','.join(parts)
                option_updated = True
                print(f"Updated description for {feature_name} in {main_file}.")
            break
    
    # 如果选项行不存在，则在 options 列表中添加
    if not option_updated:
        for i, line in enumerate(lines):
            if line.strip().startswith('options = ['):
                lines.insert(i+1, option_line)
                print(f"Added new option for {feature_name} in {main_file}.")
                break

    # 将更新后的内容写回到文件
    with open(main_file, 'w', encoding='utf-8') as file:
        file.writelines(lines)

    print(f"Updated options in {main_file}.")

if __name__ == "__main__":
    # 创建解析器
    parser = argparse.ArgumentParser(description="将新功能集成到现有的 Python 文件中。")
    
    # 添加命令行参数
    parser.add_argument('--name', required=True, help='要集成的新功能名称，必须是latex_linter文件夹中的py文件名，其中包含同名函数。')
    parser.add_argument('--description', required=True, help='新功能的文字描述，必须用单引号括起来，显示在GUI中。')

    # 示例用法
    # python add_features_auto.py --name new_feature_name --description '自定义的新功能（仅用做演示）'  

    # 解析参数
    args = parser.parse_args()
    
    # 获取命令行参数
    feature_name = args.name
    feature_description = args.description

    # 检查feature_description是否用单引号括起来
    if not (feature_description.startswith("'") and feature_description.endswith("'")):
        print("Error: The feature description must be enclosed in single quotes.")
        sys.exit(1)

    # 去掉单引号
    feature_description = feature_description[1:-1]
    
    # 调用功能集成函数
    update_text_processing_file(feature_name, feature_description)
    update_main_file(feature_name, feature_description)
