"""
LatexFormatting — PySide6 GUI 版本 (紧凑左栏布局)
=====================================================
用于格式化 LaTeX 和 Markdown 文件的实用工具。
原 Tkinter 版本: main.py / formatting.pyw
PySide6 版本: main_pyside6.py

布局说明:
  左栏: 标签切换 + 单栏复选框
  右栏: 上=输出框 → 中=操作按钮 → 下=输入框
  使「粘贴→查看结果→复制」操作路径最短
"""

import sys
import json

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QPushButton, QCheckBox, QComboBox, QPlainTextEdit,
    QGroupBox, QDialog, QLineEdit, QLabel, QMessageBox,
    QScrollArea, QFrame,
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QIcon

from text_processing import replace_text
from file_operations import (
    select_files, replace_text_in_files, select_folder, get_files_in_folder,
)

# ============================================================
# 元数据
# ============================================================
METADATA = {
    "title": "LatexFormatting (Latex数学公式源码格式化工具)",
    "author": "赖小戴",
    "version": "2.0-pyside6",
    "update_date": "2026-04-25",
    "description": "用于格式化LaTeX和Markdown文件的实用工具。",
    "resource_url": "https://github.com/GALVINLAI/formatting",
    "email": "laizhijian100@outlook.com",
}

CHECKBOX_STATE_FILE = "checkbox_states.json"
LAST_STATE_KEY = "_last_state"
PRESETS_KEY = "presets"
AUTO_COPY_KEY = "_auto_copy"


def load_all_data():
    """加载完整的状态文件。返回 { PRESETS_KEY: {...}, LAST_STATE_KEY: {...}, AUTO_COPY_KEY: bool }"""
    try:
        with open(CHECKBOX_STATE_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {PRESETS_KEY: {}, LAST_STATE_KEY: {}, AUTO_COPY_KEY: True}


def save_all_data(data):
    """将完整数据写入状态文件。"""
    with open(CHECKBOX_STATE_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def list_presets(data):
    """返回所有用户预设的名称列表。"""
    return list(data.get(PRESETS_KEY, {}).keys())


def get_preset(data, name):
    """获取指定预设的选项字典。"""
    return data.get(PRESETS_KEY, {}).get(name, {})


def set_preset(data, name, options):
    """设置（保存/覆盖）一个预设。"""
    if PRESETS_KEY not in data:
        data[PRESETS_KEY] = {}
    data[PRESETS_KEY][name] = dict(options)


def delete_preset(data, name):
    """删除一个预设。"""
    data.get(PRESETS_KEY, {}).pop(name, None)


def rename_preset(data, old_name, new_name):
    """重命名一个预设。"""
    presets = data.get(PRESETS_KEY, {})
    if old_name in presets:
        presets[new_name] = presets.pop(old_name)


def get_last_state(data):
    """获取上次关闭时的状态。"""
    return data.get(LAST_STATE_KEY, {})


def set_last_state(data, options):
    """保存上次关闭时的状态。"""
    data[LAST_STATE_KEY] = dict(options)


def get_auto_copy(data):
    """获取自动复制设置。"""
    return data.get(AUTO_COPY_KEY, True)


def set_auto_copy(data, value):
    """设置自动复制。"""
    data[AUTO_COPY_KEY] = bool(value)

# ============================================================
# 选项定义: (key, 显示文本, 默认值, 分组)
# 分组: "common"=常用, "formula"=公式, "general"=通用
# ============================================================
OPTIONS = [
    # --- 常用（默认开启项 + GPT修复）---
    ("add_space_between_cjk_and_english", "中日韩字符与英文间加空格", False, "common"),
    ("remove_extra_newlines", "多行空行合并为单行", True, "common"),
    ("repair_display_brackets", "修复 [ … ] → \\[ … \\] 【GPT缺失斜杠】", False, "common"),
    ("repair_inline_parentheses", "修复 ( … ) → \\( … \\) 【GPT缺失斜杠】", False, "common"),
    ("repair_inline_parentheses_aggressive", "修复 ( ) 【激进·可能误伤】", False, "common"),
    ("parentheses_to_single_dollar", "\\( … \\) → $ … $ 【适合ChatGPT】", True, "common"),
    ("square_brackets_to_dollars", "\\[ … \\] → $$ … $$ 【适合ChatGPT】", True, "common"),

    # --- 公式（定界符转换 + 格式规范）---
    ("equations_to_dollars", "equation → $$ … $$", False, "formula"),
    ("square_brackets_to_equations", "\\[ … \\] → equation", False, "formula"),
    ("dollars_to_equations", "$$ … $$ → equation", False, "formula"),
    ("format_single_dollar", "规范 $ … $ 环境", False, "formula"),
    ("format_parentheses", "规范 \\( … \\) 环境", False, "formula"),
    ("format_equations", "规范 equation 环境", False, "formula"),
    ("format_dollars", "规范 $$ … $$ 环境", False, "formula"),
    ("format_square_brackets", "规范 \\[ … \\] 环境", False, "formula"),
    ("format_aligns", "规范 align 环境", False, "formula"),
    ("equations_to_equations_star", "equation → equation* (无label时)", False, "formula"),

    # --- 通用（Markdown + 其他）---
    ("remove_markdown", "一键去除 Markdown 标记", False, "general"),
    ("markdown_to_latex", "Markdown → LaTeX", False, "general"),
    ("replace_fullwidth_punctuation", "全角标点替换（高数B讲义用）", False, "general"),
]

# 标签分组定义
TAB_GROUPS = [
    ("常用", "common"),
    ("公式", "formula"),
    ("通用", "general"),
]


# ============================================================
# 状态管理函数
# ============================================================
def load_all_states():
    try:
        with open(CHECKBOX_STATE_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


def save_states_to_file(all_states):
    with open(CHECKBOX_STATE_FILE, 'w', encoding='utf-8') as f:
        json.dump(all_states, f, ensure_ascii=False, indent=4)


# ============================================================
# 保存状态对话框（另存为）
# ============================================================
class SaveAsDialog(QDialog):
    def __init__(self, parent=None, existing_names=None):
        super().__init__(parent)
        self.setWindowTitle("另存为")
        self.setFixedSize(400, 100)
        self.setModal(True)
        self._existing = existing_names or []

        layout = QHBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.addWidget(QLabel("配置名称:"))
        self.name_edit = QLineEdit()
        self.name_edit.setPlaceholderText("输入配置名称...")
        layout.addWidget(self.name_edit)

        save_btn = QPushButton("保存")
        save_btn.clicked.connect(self.on_save)
        layout.addWidget(save_btn)

    def on_save(self):
        name = self.name_edit.text().strip()
        if not name:
            QMessageBox.warning(self, "警告", "请提供一个配置名称。")
            return

        if name in self._existing:
            reply = QMessageBox.question(
                self, "确认",
                f"配置 '{name}' 已存在。是否覆盖？",
                QMessageBox.Yes | QMessageBox.No,
            )
            if reply == QMessageBox.No:
                return

        self._result = name
        self.accept()

    def result_name(self):
        return getattr(self, '_result', None)


# ============================================================
# 重命名对话框
# ============================================================
class RenameDialog(QDialog):
    def __init__(self, parent=None, old_name="", existing_names=None):
        super().__init__(parent)
        self.setWindowTitle("重命名配置")
        self.setFixedSize(400, 100)
        self.setModal(True)
        self._old_name = old_name
        self._existing = existing_names or []

        layout = QHBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.addWidget(QLabel("新名称:"))
        self.name_edit = QLineEdit(old_name)
        self.name_edit.selectAll()
        layout.addWidget(self.name_edit)

        rename_btn = QPushButton("重命名")
        rename_btn.clicked.connect(self.on_rename)
        layout.addWidget(rename_btn)

    def on_rename(self):
        name = self.name_edit.text().strip()
        if not name:
            QMessageBox.warning(self, "警告", "名称不能为空。")
            return

        if name != self._old_name and name in self._existing:
            QMessageBox.warning(self, "警告", f"配置 '{name}' 已存在。")
            return

        self._result = name
        self.accept()

    def result_name(self):
        return getattr(self, '_result', None)


# ============================================================
# 主窗口
# ============================================================
class LatexFormattingWindow(QMainWindow):
    """LatexFormatting 主窗口 — 左栏标签页 + 右栏上下布局"""

    def __init__(self):
        super().__init__()
        self.setWindowTitle(
            f"{METADATA['title']} 版本: {METADATA['version']} 更新日期：{METADATA['update_date']}"
        )
        self.setMinimumSize(720, 500)

        try:
            self.setWindowIcon(QIcon("icon.ico"))
        except Exception:
            pass

        self.checkboxes: dict[str, QCheckBox] = {}
        self.current_preset_name = ""
        self._current_tab = "common"  # 当前加载的用户预设名（空=未保存的自定义状态）

        # 保存各组复选框的 widget 引用，用于切换显示/隐藏
        self._tab_pages: dict[str, QWidget] = {}

        self._setup_ui()

        # 自动缩放到刚好容纳所有控件的最小尺寸
        self.adjustSize()

        # 启动时加载上次关闭时的状态
        data = load_all_data()
        last_opts = get_last_state(data)
        if last_opts:
            for k, v in last_opts.items():
                if k in self.checkboxes:
                    self.checkboxes[k].setChecked(v)
        self.auto_copy_cb.setChecked(get_auto_copy(data))
        self.update_preset_combo()

    # --------------------------------------------------
    # UI 构建
    # --------------------------------------------------
    def _setup_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QVBoxLayout(central)
        main_layout.setContentsMargins(4, 4, 4, 4)
        main_layout.setSpacing(3)

        # 主体: 水平分割（顶部无工具栏，全部控件集中在右侧两文本框之间）
        body = QHBoxLayout()
        body.setSpacing(4)

        self._create_left_panel(body)
        self._create_right_panel(body)

        main_layout.addLayout(body, stretch=1)

    def _create_left_panel(self, parent_layout):
        """左栏: 标签切换按钮 + 单栏复选框"""
        left_widget = QWidget()
        left_widget.setFixedWidth(280)
        left_layout = QVBoxLayout(left_widget)
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.setSpacing(1)

        # 用 QGroupBox 包裹选项区
        option_group = QGroupBox("格式化选项")
        option_layout = QVBoxLayout(option_group)
        option_layout.setContentsMargins(4, 12, 4, 4)
        option_layout.setSpacing(1)

        # 标签切换按钮行（QPushButton 原生风格，无自定义样式）
        tab_bar = QHBoxLayout()
        tab_bar.setSpacing(1)
        self._tab_buttons = []
        for label, group_key in TAB_GROUPS:
            btn = QPushButton(label)
            btn.setCheckable(True)
            btn.setFixedHeight(26)
            btn.clicked.connect(lambda checked, g=group_key: self._switch_tab(g))
            self._tab_buttons.append(btn)
            tab_bar.addWidget(btn)
        option_layout.addLayout(tab_bar)

        # 复选框滚动区（单栏）
        self._scroll_area = QScrollArea()
        self._scroll_area.setWidgetResizable(True)
        self._scroll_area.setFrameShape(QFrame.NoFrame)
        self._scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self._scroll_content = QWidget()
        self._scroll_layout = QVBoxLayout(self._scroll_content)
        self._scroll_layout.setContentsMargins(2, 2, 2, 2)
        self._scroll_layout.setSpacing(2)

        # 为每组创建复选框容器
        for label, group_key in TAB_GROUPS:
            page = QWidget()
            page_layout = QVBoxLayout(page)
            page_layout.setContentsMargins(0, 0, 0, 0)
            page_layout.setSpacing(2)

            group_options = [(k, t, d) for k, t, d, g in OPTIONS if g == group_key]
            for key, text, default in group_options:
                cb = QCheckBox(text)
                cb.setChecked(default)
                cb.stateChanged.connect(self.on_checkbox_changed)
                self.checkboxes[key] = cb
                page_layout.addWidget(cb)

            page_layout.addStretch()
            self._tab_pages[group_key] = page
            self._scroll_layout.addWidget(page)
            page.setVisible(False)

        self._scroll_layout.addStretch()
        self._scroll_area.setWidget(self._scroll_content)
        option_layout.addWidget(self._scroll_area, stretch=1)

        # 默认选中第一个标签
        self._switch_tab(TAB_GROUPS[0][1])

        left_layout.addWidget(option_group, stretch=1)
        parent_layout.addWidget(left_widget)

    def _switch_tab(self, group_key: str):
        """切换标签页"""
        self._current_tab = group_key
        for btn, (label, g_key) in zip(self._tab_buttons, TAB_GROUPS):
            btn.setChecked(g_key == group_key)

        for g_key, page in self._tab_pages.items():
            page.setVisible(g_key == group_key)

    def _create_right_panel(self, parent_layout):
        """右栏: 上=合并工具栏 → 输出框 → 剪贴板 → 输入框"""
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(2)

        # ---- 顶部: 合并工具栏（文件操作 + 预设管理 + 关于）----
        tool_group = QGroupBox("操作")
        tool_layout = QVBoxLayout(tool_group)
        tool_layout.setContentsMargins(4, 12, 4, 4)
        tool_layout.setSpacing(4)

        tool_grid = QGridLayout()
        tool_grid.setSpacing(4)

        # 第0行: 文件操作
        self.bulk_file_btn = QPushButton("批量修改文件")
        self.bulk_file_btn.clicked.connect(self.open_and_replace_files)
        tool_grid.addWidget(self.bulk_file_btn, 0, 0, 1, 2)

        self.bulk_folder_btn = QPushButton("批量修改文件夹")
        self.bulk_folder_btn.clicked.connect(self.open_and_replace_files_in_folder)
        tool_grid.addWidget(self.bulk_folder_btn, 0, 2, 1, 2)

        # 第1行: 预设选择（占两格）+ 另存为 + 重命名
        self.preset_combo = QComboBox()
        self.preset_combo.setMinimumWidth(120)
        self.preset_combo.currentIndexChanged.connect(self.on_preset_selected)
        tool_grid.addWidget(self.preset_combo, 1, 0, 1, 2)

        save_as_btn = QPushButton("另存为")
        save_as_btn.clicked.connect(self.save_as_preset)
        tool_grid.addWidget(save_as_btn, 1, 2)

        rename_btn = QPushButton("重命名")
        rename_btn.clicked.connect(self.rename_preset)
        tool_grid.addWidget(rename_btn, 1, 3)

        # 第2行: 删除 + 恢复默认 + 关于
        delete_btn = QPushButton("删除")
        delete_btn.clicked.connect(self.delete_preset)
        tool_grid.addWidget(delete_btn, 2, 0)

        reset_btn = QPushButton("恢复默认")
        reset_btn.clicked.connect(self.reset_to_defaults)
        tool_grid.addWidget(reset_btn, 2, 1)

        about_btn = QPushButton("关于")
        about_btn.setFixedWidth(80)
        about_btn.clicked.connect(self.show_about)
        tool_grid.addWidget(about_btn, 2, 2)

        tool_grid.setColumnStretch(4, 1)

        tool_layout.addLayout(tool_grid)

        right_layout.addWidget(tool_group)

        # ---- 输出框 ----
        out_group = QGroupBox("修改后的内容")
        out_inner = QVBoxLayout(out_group)
        out_inner.setContentsMargins(4, 12, 4, 4)
        self.output_text = QPlainTextEdit()
        self.output_text.setFont(QFont("Consolas", 10))
        self.output_text.setReadOnly(True)
        self.output_text.setPlaceholderText("格式化结果将自动显示在这里...")
        out_inner.addWidget(self.output_text)
        right_layout.addWidget(out_group, stretch=3)

        # ---- 剪贴板 ----
        clip_group = QGroupBox("剪贴板")
        clip_layout = QHBoxLayout(clip_group)
        clip_layout.setContentsMargins(4, 12, 4, 4)
        clip_layout.setSpacing(4)

        self.auto_copy_cb = QCheckBox("修改后内容自动复制")
        self.auto_copy_cb.setChecked(True)
        clip_layout.addWidget(self.auto_copy_cb)

        copy_btn = QPushButton("复制到剪贴板")
        copy_btn.clicked.connect(self.copy_to_clipboard)
        clip_layout.addWidget(copy_btn)

        clear_btn = QPushButton("清空文本框")
        clear_btn.clicked.connect(self.clear_text_boxes)
        clip_layout.addWidget(clear_btn)

        clip_layout.addStretch()
        right_layout.addWidget(clip_group)

        # ---- 输入框 ----
        in_group = QGroupBox("原始内容（比如GPT的回答）")
        in_inner = QVBoxLayout(in_group)
        in_inner.setContentsMargins(4, 12, 4, 4)
        self.input_text = QPlainTextEdit()
        self.input_text.setFont(QFont("Consolas", 10))
        self.input_text.setPlaceholderText("在此粘贴GPT的回答...")
        self.input_text.textChanged.connect(self.update_output_text)
        in_inner.addWidget(self.input_text)
        right_layout.addWidget(in_group, stretch=2)

        parent_layout.addWidget(right_widget, stretch=1)

    # --------------------------------------------------
    # 业务逻辑
    # --------------------------------------------------
    def update_output_text(self):
        input_text = self.input_text.toPlainText()
        if not input_text:
            return
        options = self.get_options()
        modified_text = replace_text(input_text, options)
        self.output_text.setPlainText(modified_text)
        if self.auto_copy_cb.isChecked():
            QApplication.clipboard().setText(modified_text)
        self.check_state_match()

    def copy_to_clipboard(self):
        QApplication.clipboard().setText(self.output_text.toPlainText())

    def clear_text_boxes(self):
        self.input_text.clear()
        self.output_text.clear()

    def process_files(self, file_paths):
        if file_paths:
            replace_text_in_files(file_paths, self.get_options())
            QMessageBox.information(self, "完成", "所有选中的文件已完成修改。")

    def open_and_replace_files(self):
        self.process_files(select_files())

    def open_and_replace_files_in_folder(self):
        folder = select_folder()
        if folder:
            self.process_files(get_files_in_folder(folder))

    def show_about(self):
        msg = (
            f"{METADATA['title']}\n\n作者: {METADATA['author']}\n"
            f"版本: {METADATA['version']}\n更新日期：{METADATA['update_date']}\n\n"
            f"{METADATA['description']}\n\n"
            f"资源地址：{METADATA['resource_url']}\n联系邮箱：{METADATA['email']}"
        )
        QMessageBox.about(self, "关于", msg)

    # --------------------------------------------------
    # 预设管理
    # --------------------------------------------------
    def get_options(self):
        """获取当前复选框的值。"""
        return {k: cb.isChecked() for k, cb in self.checkboxes.items()}

    def update_preset_combo(self):
        """更新预设下拉列表。"""
        data = load_all_data()
        names = list_presets(data)

        self.preset_combo.blockSignals(True)
        self.preset_combo.clear()
        # 首项: "上次使用的配置"（占位，选中不做任何操作）
        self.preset_combo.addItem("◆ 上次任务状态", None)
        for name in names:
            self.preset_combo.addItem(name, name)

        # 如果当前有选中的预设，设为选中
        if self.current_preset_name and self.current_preset_name in names:
            idx = self.preset_combo.findData(self.current_preset_name)
            if idx >= 0:
                self.preset_combo.setCurrentIndex(idx)
        else:
            self.preset_combo.setCurrentIndex(0)  # 默认显示"上次任务状态"

        self.preset_combo.blockSignals(False)

    def on_preset_selected(self, index):
        """从下拉列表选择了一个预设。"""
        if index < 0:
            return
        name = self.preset_combo.itemData(index)
        # "上次任务状态" 或重复选择，不做操作
        if name is None or name == self.current_preset_name:
            return

        data = load_all_data()
        opts = get_preset(data, name)
        if opts:
            for k, v in opts.items():
                if k in self.checkboxes:
                    self.checkboxes[k].setChecked(v)
            self.current_preset_name = name
            # 触发重新处理
            if self.input_text.toPlainText():
                self.update_output_text()

    def save_as_preset(self):
        """将当前配置另存为一个预设。"""
        data = load_all_data()
        existing = list_presets(data)
        dialog = SaveAsDialog(self, existing)
        if dialog.exec() == QDialog.Accepted:
            name = dialog.result_name()
            if name:
                opts = self.get_options()
                set_preset(data, name, opts)
                set_auto_copy(data, self.auto_copy_cb.isChecked())
                save_all_data(data)
                self.current_preset_name = name
                self.update_preset_combo()

    def rename_preset(self):
        """重命名当前选中的预设。"""
        if not self.current_preset_name:
            QMessageBox.information(self, "提示", "请先选择一个预设配置。")
            return

        data = load_all_data()
        existing = list_presets(data)
        dialog = RenameDialog(self, self.current_preset_name, existing)
        if dialog.exec() == QDialog.Accepted:
            new_name = dialog.result_name()
            if new_name and new_name != self.current_preset_name:
                rename_preset(data, self.current_preset_name, new_name)
                save_all_data(data)
                self.current_preset_name = new_name
                self.update_preset_combo()

    def delete_preset(self):
        """删除当前选中的预设。"""
        if not self.current_preset_name:
            QMessageBox.information(self, "提示", "请先选择一个预设配置。")
            return

        reply = QMessageBox.question(
            self, "确认删除",
            f"确定要删除预设配置 '{self.current_preset_name}' 吗？",
            QMessageBox.Yes | QMessageBox.No,
        )
        if reply == QMessageBox.Yes:
            data = load_all_data()
            delete_preset(data, self.current_preset_name)
            save_all_data(data)
            self.current_preset_name = ""
            self.update_preset_combo()

    def reset_to_defaults(self):
        """将所有复选框恢复为默认值。"""
        for key, _, default, _ in OPTIONS:
            if key in self.checkboxes:
                self.checkboxes[key].setChecked(default)
        self.current_preset_name = ""
        self.update_preset_combo()
        if self.input_text.toPlainText():
            self.update_output_text()

    def check_state_match(self):
        """检查当前复选框状态是否匹配某个已保存的预设。"""
        opts = self.get_options()
        data = load_all_data()
        for name in list_presets(data):
            if opts == get_preset(data, name):
                if name != self.current_preset_name:
                    self.current_preset_name = name
                    self.update_preset_combo()
                return
        # 不匹配任何预设
        self.current_preset_name = ""
        self.update_preset_combo()

    def on_checkbox_changed(self):
        self.check_state_match()
        if self.input_text.toPlainText():
            self.update_output_text()

    def closeEvent(self, event):
        # 关闭时保存当前状态
        data = load_all_data()
        set_last_state(data, self.get_options())
        set_auto_copy(data, self.auto_copy_cb.isChecked())
        save_all_data(data)
        event.accept()


# ============================================================
def main():
    app = QApplication(sys.argv)
    app.setApplicationName(METADATA["title"])
    app.setStyle("Fusion")
    window = LatexFormattingWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
