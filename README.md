# 重要说明
> 2026-01-26 v2.0 声明：
>
> 2025 年下半年开始，GPT 复制的内容出现“公式定界符缺失反斜杠”的问题（如 `\[ ... \]` 变成 `[ ... ]`，`\(...\)` 变成 `( ... )`）。本版本新增对应修复功能以适配这一变化。
>

# **程序下载链接** 

- v2.0 (MAC 应用程序, WINDOWS 应用程序)  xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
- v1.4 (WINDOWS 应用程序 )   https://pan.quark.cn/s/1ebd3ea4ca20 


# 项目简介


**LatexFormatting** 是一个用于格式化 LaTeX 和 Markdown 文件的实用工具。该工具提供了多种选项来规范化数学公式和文本格式，特别是对由 ChatGPT 生成的 LaTeX 公式进行处理。

简单的演示（新的视频还没做）
[【数学科研向】将 ChatGPT 的回答复制到 Markdown 文件并正常编译数学公式](https://www.bilibili.com/video/BV1HCV7eyEjm/?share_source=copy_web&vd_source=4b19b22e0433c87d80739f9648c6e390)

![窗口界面](https://github.com/GALVINLAI/formatting/blob/main/formatting_88MZxhi81t.png)

## 主要功能

1. **高数B讲义制作用（全角标点替换等）**  
   默认启用: ❌

2. **在中日韩字符和英文或数字之间添加空格**  
   默认启用: ✅

3. **将多行空行变成单行空行**  
   默认启用: ✅

4. **GPT缺失斜杠：将独立行的 `[ ... ]` 识别为 `\[ ... \]`**  
   默认启用: ✅

5. **GPT缺失斜杠：将疑似数学 `( ... )` 识别为 `\( ... \)`（保守）**  
   默认启用: ✅

6. **【激进】将 `(n)/(a)/(x)/(F')/(f(x))` 等识别为 `\( ... \)`（可能误伤普通括号）**  
   默认启用: ❌

7. **行内公式：替换 `\( ... \)` 为 `$ ... $` 环境【适合ChatGPT】**  
   默认启用: ✅

8. **行间公式：替换 `\[ ... \]` 为 `$$ ... $$` 环境【适合ChatGPT】**  
   默认启用: ✅

9. **行间公式：替换 `equation` 为 `$$ ... $$` 环境**  
   默认启用: ❌

10. **行间公式：替换 `\[ ... \]` 为 `equation` 环境**  
    默认启用: ❌

11. **行间公式：替换 `$$ ... $$` 为 `equation` 环境**  
    默认启用: ❌

12. **行内公式：规范 `$ ... $` 环境**  
    默认启用: ❌

13. **行内公式：规范 `\( ... \)` 环境**  
    默认启用: ❌

14. **行间公式：规范 `equation` 环境**  
    默认启用: ❌

15. **行间公式：规范 `$$ ... $$` 环境**  
    默认启用: ❌

16. **行间公式：规范 `\[ ... \]` 环境**  
    默认启用: ❌

17. **行间公式：规范 `align` 环境**  
    默认启用: ❌

18. **行间公式：若无 `label`，替换 `equation` 为 `equation*`**  
    默认启用: ❌


## 额外说明

1. 可以保存当前复选框情况，下次开启自动复现。
2. 可以批量处理文件夹内所有 `.md` 或 `.tex` 文件。
3. 可以选择自动复制或者手动复制修改后内容。

# 使用方法

## 方法 1：从终端中打开（MAC 或者 WINDOWS 系统皆可）

请确认安装了 `pyperclip` 库
```sh
pip install pyperclip
```
在根目录下运行 `main.py` 会自动打开使用界面。
```sh
python main.py
```

## 方法 2：打包成可执行文件 `formatting.exe` 或者 MAC 应用程序 即可使用。支持多开。

具体打包方法请看下面开发说明。

WINDOWS exe: 该软件可能会被杀毒软件识别并清除，请加入白名单。详情原因参考 [PyInstaller打包的exe被防毒软件报毒怎么办](https://blog.csdn.net/cclbanana/article/details/136010033)

MAC 应用程序: 左上角的关闭按钮没用，只能用 MAC+Q 退出

## ⚠️ 注意事项

如果左侧输入框变化时，右侧输出框没有反应。说明出了bug，请关闭重启。


## 如果typora不能正常编译公式

请在 `typora` 偏好设置中，请在 `Markdown` 的设置看是否与下图相同

![typora_markdown_setting](https://github.com/GALVINLAI/formatting/blob/main/typora_markdown_setting.png)


# 开发说明

## 环境要求

- Python 3.x
- 必要的 Python 库：
  - `tkinter` （`tk` 是 python 标准库）
  - `pyperclip`
  - `pyinstaller` （如需自己生成 exe文件 或者 mac 的应用程序的话）

## 项目结构

```plaintext
project/
│
├── main.py                      # 主程序文件
├── icon.ico                     # Windows 程序图标
├── icon.icns                    # mac 程序图标
├── text_processing.py           # 文本处理模块
├── file_operations.py           # 文件操作模块
└── README.md                    # 开发说明（本文件）
```

## 代码结构说明

**`main.py`**：主程序文件，包含 GUI 界面及主要逻辑。

**`text_processing.py`** 和 **`file_operations.py`** 文件包含具体的文本处理和文件操作函数，请根据项目需要进行定义。

## 如何添加自定义的新功能

详见根目录下另一个 `how_add_new_features.md` 文件。

## 构建可执行文件 `formatting` （WINDOWS 系统）

在 `main.py` 所在的目录下运行如下，使用 `PyInstaller` 创建一个可执行exe文件：
```sh
pyinstaller --onefile --noconsole --name formatting --icon=icon.ico --distpath ./ main.py
```
或者直接在双击 `get_exe.bat`。

## 构建应用程序 `formatting` （MAC 系统）

```sh
pyinstaller --onedir --windowed --name formatting --icon=icon.icns --distpath ./ main.py
```

--onefile 版本，启动会慢一些。


## 联系方式

如有任何问题或建议，请联系作者：

- 邮箱：galvin.lai@outlook.com
- GitHub: [GALVINLAI](https://github.com/GALVINLAI/formatting)

