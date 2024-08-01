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