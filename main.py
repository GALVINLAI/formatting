import tkinter as tk
from tkinter import messagebox, ttk
import pyperclip
import json
from text_processing import replace_text  # 你的自定义文本处理模块
from file_operations import select_files, replace_text_in_files, select_folder, get_files_in_folder  # 你的自定义文件操作模块
from datetime import datetime
from functools import partial

# 定义元数据
metadata = {
    "title": "LatexFormatting (Latex数学公式源码格式化工具)",
    "author": "赖小戴",
    "version": "2.0",
    "update_date": "2026-01-31",
    "description": "用于格式化LaTeX和Markdown文件的实用工具。",
    "resource_url": "https://github.com/GALVINLAI/formatting",
    "email": "laizhijian100@outlook.com",
}

# 保存复选框状态的文件名
CHECKBOX_STATE_FILE = "checkbox_states.json"
LAST_STATE_NAME = "上一次关闭时状态"

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

def save_checkbox_states(state_name=LAST_STATE_NAME):
    """
    保存复选框的状态到文件。
    """
    options = get_options()
    options["auto_copy"] = auto_copy_checkbox_var.get()

    all_states = load_all_states()
    all_states[state_name] = options

    with open(CHECKBOX_STATE_FILE, 'w', encoding='utf-8') as f:
        json.dump(all_states, f, ensure_ascii=False, indent=4)

    update_state_menu()

def load_checkbox_states(state_name=None, show_warning=False):
    """
    从文件加载复选框状态。
    """
    try:
        with open(CHECKBOX_STATE_FILE, 'r', encoding='utf-8') as f:
            all_states = json.load(f)
            if state_name and state_name in all_states:
                options = all_states[state_name]
                for key, value in options.items():
                    if key in checkbox_vars:
                        checkbox_vars[key].set(value)
                if "auto_copy" in options:
                    auto_copy_checkbox_var.set(options["auto_copy"])
                CURRENT_STATE_VAR.set(state_name)  # 更新当前状态变量
                update_state_menu()  # 更新菜单显示
            elif show_warning:
                messagebox.showwarning("警告", "状态名称无效或不存在。")
    except FileNotFoundError:
        pass

def load_all_states():
    """
    加载所有保存的状态。
    """
    try:
        with open(CHECKBOX_STATE_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

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
    check_state_match()  # 检查当前状态是否匹配任何已保存的状态

def copy_to_clipboard():
    """
    将输出文本框中的内容复制到剪贴板。
    """
    modified_text = output_text_widget.get("1.0", tk.END)
    pyperclip.copy(modified_text)

def clear_text_boxes():
    """
    清空输入和输出文本框的内容。
    """
    input_text_widget.delete("1.0", tk.END)
    output_text_widget.delete("1.0", tk.END)

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
    checkbox = ttk.Checkbutton(frame, text=text, variable=var, takefocus=False)
    padx = (10, 30) if col == 0 else (30, 10)
    checkbox.grid(row=row, column=col, sticky='w', padx=padx, pady=3)
    var.trace_add('write', on_checkbox_change)  # 添加 trace 方法

def update_state_menu():
    """
    更新下拉菜单，显示所有保存的状态。
    """
    state_menu['menu'].delete(0, 'end')
    all_states = load_all_states()
    current_state = CURRENT_STATE_VAR.get()
    for state_name in all_states.keys():
        label = state_name
        if state_name == current_state:
            label = f"✓ {state_name}"  # 在当前状态前添加打勾标记
        state_menu['menu'].add_command(label=label, command=partial(load_checkbox_states, state_name, True))




def open_save_state_popup():
    """
    打开一个弹出窗口，输入状态名称以保存当前状态。
    """
    popup = tk.Toplevel(root)
    popup.title("保存状态")

    tk.Label(popup, text="输入新状态名称:").pack(side=tk.LEFT, padx=5, pady=5)
    state_name_entry = ttk.Entry(popup, width=20)
    state_name_entry.pack(side=tk.LEFT, padx=5, pady=5)

    def on_save():
        state_name = state_name_entry.get()
        if state_name:
            all_states = load_all_states()
            if state_name in all_states:
                # 提示是否覆盖现有状态
                if messagebox.askyesno("确认", f"状态 '{state_name}' 已存在。是否覆盖？"):
                    save_checkbox_states(state_name)
                    CURRENT_STATE_VAR.set(state_name)  # 更新当前状态变量
                    popup.destroy()
                else:
                    popup.destroy()
            else:
                save_checkbox_states(state_name)
                CURRENT_STATE_VAR.set(state_name)  # 更新当前状态变量
                popup.destroy()
        else:
            messagebox.showwarning("警告", "请提供一个状态名称。")

    save_button = ttk.Button(popup, text="保存", command=on_save)
    save_button.pack(side=tk.LEFT, padx=5, pady=5)

def check_state_match():
    """
    检查当前复选框状态是否匹配任何已保存的状态。
    如果不匹配，则清除当前状态。
    """
    options = get_options()
    options["auto_copy"] = auto_copy_checkbox_var.get()
    all_states = load_all_states()

    for state_name, saved_options in all_states.items():
        if options == saved_options:
            CURRENT_STATE_VAR.set(state_name)
            update_state_menu()
            return

    CURRENT_STATE_VAR.set("")  # 没有匹配的状态
    update_state_menu()

def on_checkbox_change(*args):
    """
    当复选框状态发生变化时调用的函数。
    """
    check_state_match()

# 创建主窗口
root = tk.Tk()
root.title(f"{metadata['title']} 版本: {metadata['version']} 更新日期：{metadata['update_date']}")
# 设置窗口图标
root.iconbitmap("icon.ico")

# 在创建主窗口后初始化 CURRENT_STATE_VAR
CURRENT_STATE_VAR = tk.StringVar(root)

# 设置样式
style = ttk.Style()
style.configure("TButton", padding=1, relief="flat", background="#ccc")
style.configure("TCheckbutton", padding=3)
style.configure("TRadiobutton", padding=3)

# 创建按钮框架并添加按钮
button_frame = ttk.Frame(root)
button_frame.pack(pady=10)

# 创建批量修改文件或文件夹的下拉菜单
bulk_menu_button = ttk.Menubutton(button_frame, text="批量修改文件或文件夹", direction="below")
bulk_menu = tk.Menu(bulk_menu_button, tearoff=0)
bulk_menu.add_command(label="选择md或tex文件并修改", command=open_and_replace_files)
bulk_menu.add_command(label="选择文件夹并修改所有md和tex文件", command=open_and_replace_files_in_folder)
bulk_menu_button["menu"] = bulk_menu
bulk_menu_button.pack(side=tk.LEFT, padx=5, pady=5)

# 创建状态选择下拉菜单
state_var = tk.StringVar(root)
state_menu = ttk.OptionMenu(button_frame, state_var, "选择任务状态", *[])
state_menu.pack(side=tk.LEFT, padx=5)
update_state_menu()

# 添加保存状态按钮
save_button = ttk.Button(button_frame, text="保存并命名当前任务状态", command=open_save_state_popup)
save_button.pack(side=tk.LEFT, padx=5)

create_button(button_frame, "关于", show_about, "")

# 创建一个带滚动条的框架
container = ttk.Frame(root)
container.pack(pady=12, fill='both', expand=True)

canvas = tk.Canvas(container, height=300)
scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview, width=20)
options_frame = ttk.Frame(canvas)
options_frame.grid_columnconfigure(0, weight=1, uniform="options")
options_frame.grid_columnconfigure(1, weight=1, uniform="options")

options_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(
        scrollregion=canvas.bbox("all")
    )
)

canvas.create_window((0, 0), window=options_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

# 添加鼠标滚轮支持
def on_mouse_wheel(event):
    canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

canvas.bind("<Enter>", lambda event: canvas.bind_all("<MouseWheel>", on_mouse_wheel))
canvas.bind("<Leave>", lambda event: canvas.unbind_all("<MouseWheel>"))

options = [
    ("replace_fullwidth_punctuation", "高数B讲义制作用", False),
    ("add_space_between_cjk_and_english", "在中日韩字符和英文或数字之间添加空格", True),
    ("remove_extra_newlines", "将多行空行变成单行空行", True),
    ("repair_display_brackets", "将独立行的 [ ... ] 识别为 \\[ ... \\] 【GPT缺失斜杠】", True),
    ("repair_inline_parentheses", "将疑似数学 ( ... ) 识别为 \\( ... \\)【GPT缺失斜杠】（可能不奏效）", True),
    ("parentheses_to_single_dollar", "行内公式：替换 \\( ... \\) 为 $ ... $ 环境【适合ChatGPT】", True),
    ("square_brackets_to_dollars", "行间公式：替换 \\[ ... \\] 为 $$ ... $$ 环境【适合ChatGPT】", True),
    ("equations_to_dollars", "行间公式：替换 equation 为 $$ ... $$ 环境", False),
    ("square_brackets_to_equations", "行间公式：替换 \\[ ... \\] 为 equation 环境", False),
    ("dollars_to_equations", "行间公式：替换 $$ ... $$ 为 equation 环境", False),
    ("format_single_dollar", "行内公式：规范 $ ... $ 环境", False),
    ("format_parentheses", "行内公式：规范 \\( ... \\) 环境", False),
    ("format_equations", "行间公式：规范 equation 环境", False),
    ("format_dollars", "行间公式：规范 $$ ... $$ 环境", False),
    ("format_square_brackets", "行间公式：规范 \\[ ... \\] 环境", False),
    ("format_aligns", "行间公式：规范 align 环境", False),
    ("equations_to_equations_star", "行间公式：若无 label, 替换 equation 为 equation*", False),
]

checkbox_vars = {option[0]: tk.BooleanVar(value=option[2]) for option in options}

# 根据 options 的长度是奇数还是偶数来决定是否需要加 1。
half = len(options) // 2 if len(options) % 2 == 0 else len(options) // 2 + 1

for idx, (key, text, _) in enumerate(options):
    col = 0 if idx < half else 1
    row = idx % half
    create_checkbox(options_frame, text, checkbox_vars[key], row, col)

options_frame.update_idletasks()
canvas.configure(height=options_frame.winfo_reqheight() + 8)

# 创建文本框和标签的容器
text_frame = ttk.Frame(root)
text_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=10)

# 创建左侧文本框和标签
left_frame = ttk.LabelFrame(text_frame, text="原始内容（比如GPT的回答）", padding=10)
left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
input_text_widget = tk.Text(left_frame, wrap="word", width=50, height=10, font=("Consolas", 10))
input_text_widget.pack(fill=tk.BOTH, expand=True)

# 创建右侧文本框和标签
right_frame = ttk.LabelFrame(text_frame, text="修改后的内容", padding=10)
right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)
output_text_widget = tk.Text(right_frame, wrap="word", width=50, height=10, font=("Consolas", 10))
output_text_widget.pack(fill=tk.BOTH, expand=True)

# 添加复选框和按钮到右侧文本框容器
auto_copy_checkbox_var = tk.BooleanVar()
auto_copy_checkbox = ttk.Checkbutton(right_frame, text="修改后内容自动复制", variable=auto_copy_checkbox_var)
auto_copy_checkbox.pack(side=tk.LEFT, padx=5, pady=5)

copy_button = ttk.Button(right_frame, text="复制到剪贴板", command=copy_to_clipboard)
copy_button.pack(side=tk.LEFT, padx=5, pady=5)

clear_button = ttk.Button(right_frame, text="清空文本框", command=clear_text_boxes)
clear_button.pack(side=tk.LEFT, padx=5, pady=5)

def on_input_text_change(event):
    """
    检测输入文本框的修改，并触发更新输出文本框的内容。
    """
    update_output_text()
    input_text_widget.edit_modified(False)
    

input_text_widget.bind("<<Modified>>", on_input_text_change)

# 启动主循环前加载复选框状态
load_checkbox_states(LAST_STATE_NAME)

# 窗口关闭时保存状态
def on_closing():
    save_checkbox_states(LAST_STATE_NAME)
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)

# 启动主循环
root.mainloop()
