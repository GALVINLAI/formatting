# 添加新功能

在 `latex_linter` 文件夹中创建 py 文件，命名为 `new_feature_name.py`。文件格式如下。测试用例部分不是必须的。但是必须包含一个和 py 文件同名的函数。函数 `new_feature_name(content)` 的输入是整个输入框的文本内容。返回的是输出框的内容。当然，输出的内容还会作为输入，被别的功能再进行处理。

```python
"""
新功能的说明
"""

import re
import pytest

def new_feature_name(content):
    ... # 实现代码
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

打开 `text_processing.py`, 将新功能在开头导入: `from latex_linter.new_feature_name import new_feature_name`. 在 `replace_text` 函数中加入新功能处理的语句。如下。
```python
# ---------- 新功能的说明 ----------
if options['new_feature_name']:
	content = new_feature_name(content)
```

打开 `main.py`，在 `options` 中添加如下。最后的 `False` 表示，初始默认是不勾选状态。`True` 同理。
```python
("new_feature_name", "新功能的说明", False)
```

以上就完成了 " 添加新功能 " 的全部流程。运行 `main.py` 即可看到效果。当然，只有重新生成 exe 程序，exe 程序才会显示新功能。
