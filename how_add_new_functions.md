# 添加新功能

## 第一步：添加新功能的核心代码

在 `latex_linter` 文件夹中创建一个 Python 文件，命名为 `new_feature_name.py`。文件格式如下。测试用例部分不是必须的，但是必须包含一个与 py 文件同名的函数 `new_feature_name`。该函数的输入是整个输入框的文本内容，返回值是输出框的内容，这个输出内容会被其他功能进一步处理。

```python
"""
新功能的说明
"""

import re
import pytest

def new_feature_name(content):
    # 实现代码
    return content

# 测试用例
@pytest.mark.parametrize(
    "input_text, expected_output",
    [
        ("This is an equation: $$a + b = c$$.", "This is an equation: \\begin{equation}a + b = c\\end{equation}."),
        ("Multiple equations: $$x + y = z$$ and $$a^2 + b^2 = c^2$$.", "Multiple equations: \\begin{equation}x + y = z\\end{equation} and \\begin{equation}a^2 + b^2 = c^2\\end{equation}."),
    ]
)
def test_new_feature_name(input_text, expected_output):
    assert new_feature_name(input_text) == expected_output

# 运行测试
if __name__ == "__main__":
    pytest.main(["-v", __file__])
```

## 第二步：使用 `add_features_auto.py` 自动添加到 GUI

在根目录下的终端运行以下命令：

```sh
python add_features_auto.py --name new_feature_name --description '自定义的新功能（仅用做演示）'  
```

运行 `main.py`，可以看到新功能已经添加到 GUI 中。至此，完成添加新功能的步骤。默认新功能是关闭的，如果要默认开启，需要在 `main.py` 手动修改，详细如下。

## 额外其他

下面内容是第二步自动执行任务的说明。

### 在 `text_processing.py` 中集成

打开 `text_processing.py`，在开头导入新功能：

```python
from latex_linter.new_feature_name import new_feature_name
```

然后在 `replace_text` 函数中加入新功能处理的语句：

```python
# ---------- 新功能的说明 ----------
if options['new_feature_name']:
    content = new_feature_name(content)
```

### 更新 `main.py`

打开 `main.py`，在 `options` 中添加如下内容。最后的 `False` 表示初始状态不勾选，若需要默认勾选，可以设置为 `True`。

```python
("new_feature_name", "新功能的说明", False)
```

完成以上步骤后，运行 `main.py` 即可看到新功能的效果。需要注意的是，只有在重新生成 exe 程序后，exe 程序中才会显示新功能。