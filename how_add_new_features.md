# Adding New Features

## Step 1: Add the Core Code for the New Feature

Create a Python file named `new_feature_name.py` in the `latex_linter` folder. The format of the file is as follows. The test cases section is optional, but it must include a function named `new_feature_name` that matches the .py file. The input to this function is the entire text content of the input box, and the return value is the content of the output box, which will be further processed by other features.

```python
"""
Description of the new feature
"""

import re
import pytest

def new_feature_name(content):
    # Implementation code
    return content

# Test cases
@pytest.mark.parametrize(
    "input_text, expected_output",
    [
        ("This is an equation: $$a + b = c$$.", "This is an equation: \\begin{equation}a + b = c\\end{equation}."),
        ("Multiple equations: $$x + y = z$$ and $$a^2 + b^2 = c^2$$.", "Multiple equations: \\begin{equation}x + y = z\\end{equation} and \\begin{equation}a^2 + b^2 = c^2\\end{equation}."),
    ]
)
def test_new_feature_name(input_text, expected_output):
    assert new_feature_name(input_text) == expected_output

# Run tests
if __name__ == "__main__":
    pytest.main(["-v", __file__])
```

## Step 2: Automatically Add to the GUI Using `add_features_auto.py`

Run the following command in the terminal at the root directory:

```sh
python add_features_auto.py --name new_feature_name --description 'Custom new feature (for demonstration purposes only)'  
```

Running `main.py` will show that the new feature has been added to the GUI. At this point, the process of adding a new feature is complete. By default, the new feature is turned off. If you want it to be enabled by default, you need to manually modify `main.py` as detailed below.

## Additional Information

The following content explains the tasks automatically performed in Step 2.

### Integration in `text_processing.py`

Open `text_processing.py` and import the new feature at the beginning:

```python
from latex_linter.new_feature_name import new_feature_name
```

Then add the statement for processing the new feature in the `replace_text` function:

```python
# ---------- Description of the new feature ----------
if options['new_feature_name']:
    content = new_feature_name(content)
```

### Update `main.py`

Open `main.py` and add the following content to `options`. The final `False` indicates that it is not selected initially. If you want it to be selected by default, you can set it to `True`.

```python
("new_feature_name", "Description of the new feature", False)
```

After completing the above steps, running `main.py` will show the effect of the new feature. Note that the new feature will only appear in the exe program after regenerating the exe program.