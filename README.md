
# 项目简介

**LatexFormatting** 是一个用于格式化 LaTeX 和 Markdown 文件的实用工具。该工具提供了多种选项来规范化数学公式和文本格式，特别是对由 ChatGPT 生成的 LaTeX 公式进行处理。

![窗口界面](https://github.com/GALVINLAI/formatting/blob/main/screenshot.jpg)

## 主要功能

1. 将多行空行变成单行空行
2. 规范化各级标题
3. 规范 `\item` 格式
4. 规范 `$` 包围的行内公式格式
5. 将 `\(` 和 `\)` 替换为 `$` 包围，并自动规范内部格式
6. 规范 `equation` 环境内部格式
7. 规范 `$$` 环境内部格式
8. 将 `\[ 和 \]` 替换为 `$$` 环境，并自动规范内部格式
9. 将 `equation` 替换为 `$$` 环境，并自动规范内部格式
10. 将 `\[ 和 \]` 替换为 `equation` 环境，并自动规范内部格式
11. 将 `$$` 替换为 `equation` 环境，并自动规范内部格式
12. 去掉 `align` 和 `equation` 环境中用于不显示 tag 的 `*` 号
13. 将 Markdown 的加粗/斜体/标题等变成 LaTeX 对应物
14. 将内嵌在 `equation` 中的 `aligned` 环境变成单独的 `align` 环境

## 使用方法

有两种途径：

### 方法 1：从终端中打开（MAC，或者 WINDOWS 系统皆可）

请确认安装了 `pyperclip` 库 (本项目唯一的python非标准库)。
```sh
pip install pyperclip
```
在根目录下运行 `main.py` 会自动打开使用界面。
```sh
python main.py
```

### 方法 2：打包成可执行文件 `formatting.exe` 即可使用。支持多开。（仅限 WINDOWS 系统）

具体打包方法请看下面开发说明。

【警告⚠️】 该软件可能会被杀毒软件识别并清除，请加入白名单。详情原因参考 [PyInstaller打包的exe被防毒软件报毒怎么办](https://blog.csdn.net/cclbanana/article/details/136010033)

### 注意事项

如果左侧输入框变化时，右侧输出框没有反应。说明出了bug，请关闭重启。

后续工作。 参考 [Latex中正则表达式替换_latex替换-CSDN博客](https://blog.csdn.net/qq_46577007/article/details/128247975) ，逐渐增加新功能。


# 开发说明

## 环境要求

- Python 3.x
- 必要的 Python 库：
  - `tkinter` （`tk` 是 python 标准库）
  - `pyperclip`
  - `pyinstaller` （如需另外生成exe文件的话）

## 项目结构

```plaintext
project/
│
├── main.py                      # 主程序文件
├── icon.ico                     # 程序图标
├── text_processing.py           # 文本处理模块
├── file_operations.py           # 文件操作模块
└── README.md                    # 开发说明（本文件）
```

## 构建可执行文件

在 `main.py` 所在的目录下运行如下，使用 `PyInstaller` 创建一个可执行exe文件：
```sh
pyinstaller --onefile --noconsole --name formatting --icon=icon.ico --distpath ./ main.py
```

## 代码结构说明

**`main.py`**：主程序文件，包含 GUI 界面及主要逻辑。

**`text_processing.py`** 和 **`file_operations.py`** 文件包含具体的文本处理和文件操作函数，请根据项目需要进行定义。


## 贡献指南

1. Fork 此项目。
2. 创建你的功能分支 (`git checkout -b feature/AmazingFeature`)。
3. 提交你的更改 (`git commit -m 'Add some AmazingFeature'`)。
4. 推送到分支 (`git push origin feature/AmazingFeature`)。
5. 创建一个新的 Pull Request。

## 联系方式

如有任何问题或建议，请联系作者：

- 邮箱：galvin.lai@outlook.com
- GitHub: [GALVINLAI](https://github.com/GALVINLAI/formatting)





