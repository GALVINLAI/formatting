import tkinter as tk
from tkinter import messagebox, ttk
import pyperclip
import json
from text_processing import replace_text
from file_operations import select_files, replace_text_in_files, select_folder, get_files_in_folder
from datetime import datetime

# 定义元数据
metadata = {
    "title": "LatexFormatting (Latex数学公式源码格式化工具) 【持续开发中】",
    "author": "赖小戴",
    "version": "1.3",
    "update_date": datetime.now().strftime("%Y-%m-%d"),
    "description": "用于格式化LaTeX和Markdown文件的实用工具。",
    "resource_url": "https://github.com/GALVINLAI/formatting",
    "email": "galvin.lai@outlook.com"
}

# 保存复选框状态的文件名
CHECKBOX_STATE_FILE = "checkbox_states.json"

class ToolTip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip = None
        self.id = None
        widget.bind("<Enter>", self.schedule_tooltip)
        widget.bind("<Leave>", self.hide_tooltip)

    def schedule_tooltip(self, event):
        self.id = self.widget.after(700, self.show_tooltip)

    def show_tooltip(self):
        if self.tooltip or not self.text:
            return
        x, y, _, _ = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 25
        self.tooltip = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")
        label = tk.Label(tw, text=self.text, justify='left',
                         background="#ffffff", relief='solid', borderwidth=1,
                         wraplength=200)
        label.pack(ipadx=1)

    def hide_tooltip(self, event):
        if self.id:
            self.widget.after_cancel(self.id)
            self.id = None
        if self.tooltip:
            self.tooltip.destroy()
            self.tooltip = None

def get_options():
    """
    获取所有复选框的值，返回一个包含所有选项的字典。
    """
    return {local_key: var.get() for local_key, var in checkbox_vars.items()}

def save_checkbox_states():
    """
    保存复选框的状态到文件。
    """
    options = get_options()
    options["auto_copy"] = auto_copy_checkbox_var.get()  # 将 auto_copy_checkbox_var 的状态加入保存的选项中
    with open(CHECKBOX_STATE_FILE, 'w', encoding='utf-8') as f:
        json.dump(options, f, ensure_ascii=False, indent=4)
    messagebox.showinfo("保存状态", "复选框状态已保存。")

def load_checkbox_states():
    """
    从文件加载复选框状态。
    """
    try:
        with open(CHECKBOX_STATE_FILE, 'r', encoding='utf-8') as f:
            options = json.load(f)
            for key, value in options.items():
                if key in checkbox_vars:
                    checkbox_vars[key].set(value)
            # 加载 auto_copy 复选框状态
            if "auto_copy" in options:
                auto_copy_checkbox_var.set(options["auto_copy"])
    except FileNotFoundError:
        pass

def update_output_text(event=None):
    """
    获取输入文本框中的文本，根据选项进行处理，并将修改后的文本显示在输出文本框中，同时复制到剪贴板（如果复选框勾选）。
    """
    input_text = input_text_widget.get("1.0", tk.END)  # 获取输入文本框的内容
    options = get_options()  # 获取选项
    modified_text = replace_text(input_text, options)  # 处理文本
    output_text_widget.delete("1.0", tk.END)  # 清空输出文本框
    output_text_widget.insert(tk.END, modified_text)  # 插入修改后的文本
    if auto_copy_checkbox_var.get():  # 如果自动复制复选框被选中
        pyperclip.copy(modified_text)  # 复制修改后的文本到剪贴板

def copy_to_clipboard():
    """
    将输出文本框中的内容复制到剪贴板。
    """
    modified_text = output_text_widget.get("1.0", tk.END)
    pyperclip.copy(modified_text)

def process_files(file_paths):
    """
    根据选项处理选择的文件，并显示完成信息。
    """
    if file_paths:
        options = get_options()  # 获取选项
        replace_text_in_files(file_paths, options)  # 处理文件
        messagebox.showinfo("完成", "所有选中的文件已完成修改。")
    else:
        print("未选择文件")

def open_and_replace_files():
    """
    打开文件选择对话框并处理选择的文件。
    """
    file_paths = select_files()
    process_files(file_paths)

def open_and_replace_files_in_folder():
    """
    打开文件夹选择对话框并处理文件夹中的所有文件。
    """
    folder_path = select_folder()
    if folder_path:
        file_paths = get_files_in_folder(folder_path)
        process_files(file_paths)
    else:
        print("未选择文件夹")

def show_about():
    """
    显示关于信息的对话框。
    """
    about_message = (
        f"{metadata['title']}\n\n"
        f"作者: {metadata['author']}\n"
        f"版本: {metadata['version']}\n"
        f"更新日期：{metadata['update_date']}\n\n"
        f"{metadata['description']}\n\n"
        f"资源地址：{metadata['resource_url']}\n"
        f"联系邮箱：{metadata['email']}"
    )
    messagebox.showinfo("关于", about_message)

def create_button(frame, text, command, tooltip_text):
    """
    创建一个按钮并添加到指定的框架中。
    """
    button = ttk.Button(frame, text=text, command=command)
    button.pack(side=tk.LEFT, padx=5, pady=5)
    ToolTip(button, tooltip_text)  # 添加 tooltip

def create_checkbox(frame, text, var, row, col):
    """
    创建一个复选框并添加到指定的框架中，指定行和列。
    """
    checkbox = ttk.Checkbutton(frame, text=text, variable=var)
    checkbox.grid(row=row, column=col, sticky='w', padx=5, pady=2)

# 创建主窗口
root = tk.Tk()
root.title(f"{metadata['title']} 版本: {metadata['version']} 更新日期：{metadata['update_date']}")
# 设置窗口图标
root.iconbitmap("icon.ico")

# 设置样式
style = ttk.Style()
style.configure("TButton", padding=3, relief="flat", background="#ccc")
style.configure("TCheckbutton", padding=3)
style.configure("TRadiobutton", padding=3)

# 创建按钮框架并添加按钮
button_frame = ttk.Frame(root)
button_frame.pack(pady=10)

create_button(button_frame, "选择md或tex文件并修改", open_and_replace_files, "支持批量选择")
create_button(button_frame, "选择文件夹并修改所有md和tex文件", open_and_replace_files_in_folder, "含子文件夹")
create_button(button_frame, "保存当前复选框状态", save_checkbox_states, "下次启动时自动恢复")
create_button(button_frame, "关于", show_about, "")

# 创建选项框架并添加复选框
options_frame = ttk.Frame(root)
options_frame.pack(pady=10)

options = [
    ("add_space_between_cjk_and_english", "在中日韩字符和英文或数字之间添加空格", True),
    ("remove_extra_newlines", "将多行空行变成单行空行", True),
    ("format_single_dollar", "行内公式：规范 $ ... $ 环境", False),
    ("format_parentheses", "行内公式：规范 \\( ... \\) 环境", False),
    ("parentheses_to_single_dollar", "行内公式：替换 \\( ... \\) 为 $ ... $ 环境 【特别针对ChatGPT的回答】", False),
    ("format_equations", "行间公式：规范 equation 环境", False),
    ("format_dollars", "行间公式：规范 $$ ... $$ 环境", False),
    ("format_square_brackets", "行间公式：规范 \\[ ... \\] 环境", False),
    ("square_brackets_to_dollars", "行间公式：替换 \\[ ... \\] 为 $$ ... $$ 环境【特别针对ChatGPT的回答】", False),
    ("equations_to_dollars", "行间公式：替换 equation 为 $$ ... $$ 环境", False),
    ("square_brackets_to_equations", "行间公式：替换 \\[ ... \\] 为 equation 环境", False),
    ("dollars_to_equations", "行间公式：替换 $$ ... $$ 为 equation 环境", False),
    ("replace_equation_aligned", "将内嵌在 equation 中的 aligned 环境变成单独的 align 环境", False),
    ("remove_asterisks_tags", "去掉 align 和 equation 环境中用于不显示tag的 * 号", False),
    ("format_item", "规范 \\item 格式", False),
    ("capitalize_titles", "规范化各级标题", True),
    ("convert_markdown_titles_to_latex", "将 Markdown 的标题等变成 latex 对应物", False),
    ("replace_stars_with_textbf", "将 Markdown 的 ** 包围变成 \\textbf 环境", False),
    ("replace_stars_with_textit", "将 Markdown 的 * 包围变成 \\textit 环境", False),
    ("repalce_all_markdown", "去掉所有Markdown特征", False),
    ("format_aligns", "规范 align 环境", False),
    ("some_small_utilities", "some_small_utilities", False),
]

checkbox_vars = {option[0]: tk.BooleanVar(value=option[2]) for option in options}

for idx, (key, text, _) in enumerate(options):
    row = idx // 2  # 计算行数
    col = idx % 2  # 计算列数
    create_checkbox(options_frame, text, checkbox_vars[key], row, col)

# 创建左侧文本框和标签的容器
left_frame = ttk.LabelFrame(root, text="原始内容（比如GPT的回答）", padding=10)
left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
input_text_widget = tk.Text(left_frame, wrap="word", width=50, height=10, font=("Consolas", 10))
input_text_widget.pack(fill=tk.BOTH, expand=True)

# 创建右侧文本框和标签的容器
right_frame = ttk.LabelFrame(root, text="修改后的内容", padding=10)
right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)
output_text_widget = tk.Text(right_frame, wrap="word", width=50, height=10, font=("Consolas", 10))
output_text_widget.pack(fill=tk.BOTH, expand=True)

# 添加复选框和按钮到右侧文本框容器
auto_copy_checkbox_var = tk.BooleanVar()
auto_copy_checkbox = ttk.Checkbutton(right_frame, text="修改后内容自动复制到剪贴板", variable=auto_copy_checkbox_var)
auto_copy_checkbox.pack(side=tk.LEFT, padx=5, pady=5)

copy_button = ttk.Button(right_frame, text="复制到剪贴板", command=copy_to_clipboard)
copy_button.pack(side=tk.LEFT, padx=5, pady=5)

def on_input_text_change(event):
    """
    检测输入文本框的修改，并触发更新输出文本框的内容。
    """
    input_text_widget.edit_modified(False)
    update_output_text()

input_text_widget.bind("<<Modified>>", on_input_text_change)

# 启动主循环前加载复选框状态
load_checkbox_states()

# 启动主循环
root.mainloop()
