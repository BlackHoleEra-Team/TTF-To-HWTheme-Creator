import sys
import os
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                               QLabel, QFileDialog, QGroupBox, QProgressBar, QTextEdit, QScrollArea)
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon, QFont
from qfluentwidgets import (FluentIcon, PrimaryPushButton, setTheme, Theme,
                            LineEdit, PushButton, ComboBox, InfoBar, InfoBarPosition)

from tools import create_hwt_file


class HWTGeneratorApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("华为主题字体包生成器")
        self.setGeometry(100, 100, 800, 650)
        self.setMinimumSize(700, 600)

        self.setWindowIcon(QIcon("app_icon.png"))

        setTheme(Theme.AUTO)

        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)
        self.main_layout = QVBoxLayout(self.main_widget)
        self.main_layout.setContentsMargins(30, 30, 30, 30)
        self.main_layout.setSpacing(20)

        title_label = QLabel("华为主题字体包生成器")
        title_label.setFont(QFont("Microsoft YaHei", 18, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("color: #00A1D6; margin-bottom: 20px;")
        self.main_layout.addWidget(title_label)

        self.create_form_group()

        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setVisible(False)
        self.main_layout.addWidget(self.progress_bar)

        self.log_area = QTextEdit()
        self.log_area.setReadOnly(True)
        self.log_area.setPlaceholderText("操作日志将显示在这里...")
        self.log_area.setMinimumHeight(150)
        self.main_layout.addWidget(self.log_area)

        self.create_button_group()

        self.font_file = ""
        self.preview_file = ""
        self.output_file = ""

        self.statusBar().showMessage("就绪")

    def create_form_group(self):
        file_group = QGroupBox("文件设置")
        file_layout = QVBoxLayout()
        file_group.setLayout(file_layout)

        font_layout = QHBoxLayout()
        font_label = QLabel("字体文件 (.ttf):")
        self.font_edit = LineEdit()
        self.font_edit.setReadOnly(True)
        self.font_edit.setPlaceholderText("请选择字体文件")
        font_btn = PushButton("浏览...")
        font_btn.setIcon(FluentIcon.FOLDER)
        font_btn.clicked.connect(self.select_font_file)
        font_layout.addWidget(font_label)
        font_layout.addWidget(self.font_edit, 1)
        font_layout.addWidget(font_btn)
        file_layout.addLayout(font_layout)

        preview_layout = QHBoxLayout()
        preview_label = QLabel("预览图 (.jpg):")
        self.preview_edit = LineEdit()
        self.preview_edit.setReadOnly(True)
        self.preview_edit.setPlaceholderText("可选 - 选择预览图片")
        preview_btn = PushButton("浏览...")
        preview_btn.setIcon(FluentIcon.PHOTO)
        preview_btn.clicked.connect(self.select_preview_file)
        preview_layout.addWidget(preview_label)
        preview_layout.addWidget(self.preview_edit, 1)
        preview_layout.addWidget(preview_btn)
        file_layout.addLayout(preview_layout)

        output_layout = QHBoxLayout()
        output_label = QLabel("输出文件 (.hwt):")
        self.output_edit = LineEdit()
        self.output_edit.setReadOnly(True)
        self.output_edit.setPlaceholderText("请选择输出位置和文件名")
        output_btn = PushButton("浏览...")
        output_btn.setIcon(FluentIcon.SAVE)
        output_btn.clicked.connect(self.select_output_file)
        output_layout.addWidget(output_label)
        output_layout.addWidget(self.output_edit, 1)
        output_layout.addWidget(output_btn)
        file_layout.addLayout(output_layout)

        self.main_layout.addWidget(file_group)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        self.main_layout.addWidget(scroll_area)

        info_group = QGroupBox("主题信息")
        info_layout = QVBoxLayout()
        info_group.setLayout(info_layout)

        title_layout = QHBoxLayout()
        title_label = QLabel("主题英文名称:")
        self.title_edit = LineEdit()
        self.title_edit.setText("HarmonyOS Sans")
        title_layout.addWidget(title_label)
        title_layout.addWidget(self.title_edit)
        info_layout.addLayout(title_layout)

        title_cn_layout = QHBoxLayout()
        title_cn_label = QLabel("主题中文名称:")
        self.title_cn_edit = LineEdit()
        self.title_cn_edit.setText("华为鸿蒙字体")
        title_cn_layout.addWidget(title_cn_label)
        title_cn_layout.addWidget(self.title_cn_edit)
        info_layout.addLayout(title_cn_layout)

        author_layout = QHBoxLayout()
        author_label = QLabel("作者:")
        self.author_edit = LineEdit()
        self.author_edit.setText("Your Name")
        author_layout.addWidget(author_label)
        author_layout.addWidget(self.author_edit)
        info_layout.addLayout(author_layout)

        designer_layout = QHBoxLayout()
        designer_label = QLabel("设计师:")
        self.designer_edit = LineEdit()
        self.designer_edit.setText("Designer Name")
        designer_layout.addWidget(designer_label)
        designer_layout.addWidget(self.designer_edit)
        info_layout.addLayout(designer_layout)

        screen_layout = QHBoxLayout()
        screen_label = QLabel("屏幕适配:")
        self.screen_combo = ComboBox()
        self.screen_combo.addItems(["FHD+", "HD", "Full HD", "2K", "4K"])
        screen_layout.addWidget(screen_label)
        screen_layout.addWidget(self.screen_combo)
        info_layout.addLayout(screen_layout)

        font_layout = QHBoxLayout()
        font_name_label = QLabel("字体英文名称:")
        self.font_edit_name = LineEdit()
        self.font_edit_name.setText("HarmonyOS Sans")
        font_layout.addWidget(font_name_label)
        font_layout.addWidget(self.font_edit_name)
        info_layout.addLayout(font_layout)

        font_cn_layout = QHBoxLayout()
        font_cn_label = QLabel("字体中文名称:")
        self.font_cn_edit = LineEdit()
        self.font_cn_edit.setText("华为鸿蒙字体")
        font_cn_layout.addWidget(font_cn_label)
        font_cn_layout.addWidget(self.font_cn_edit)
        info_layout.addLayout(font_cn_layout)

        version_layout = QHBoxLayout()
        version_label = QLabel("版本号:")
        self.version_edit = LineEdit()
        self.version_edit.setText("1.0.0")
        version_layout.addWidget(version_label)
        version_layout.addWidget(self.version_edit)
        info_layout.addLayout(version_layout)

        scroll_area.setWidget(info_group)

    def create_button_group(self):
        button_layout = QHBoxLayout()
        button_layout.setContentsMargins(0, 10, 0, 10)

        self.reset_btn = PushButton("重置")
        self.reset_btn.setIcon(FluentIcon.DELETE)
        self.reset_btn.clicked.connect(self.reset_form)
        self.reset_btn.setMinimumHeight(40)

        self.generate_btn = PrimaryPushButton("生成主题包")
        self.generate_btn.setIcon(FluentIcon.SEND)
        self.generate_btn.clicked.connect(self.generate_theme)
        self.generate_btn.setMinimumHeight(40)

        self.exit_btn = PushButton("退出")
        self.exit_btn.setIcon(FluentIcon.CLOSE)
        self.exit_btn.clicked.connect(self.close)
        self.exit_btn.setMinimumHeight(40)

        button_layout.addWidget(self.reset_btn)
        button_layout.addWidget(self.generate_btn)
        button_layout.addWidget(self.exit_btn)

        self.main_layout.addLayout(button_layout)

    def select_font_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "选择字体文件", "", "字体文件 (*.ttf *.otf)"
        )
        if file_path:
            self.font_file = file_path
            self.font_edit.setText(file_path)

    def select_preview_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "选择预览图片", "", "图片文件 (*.jpg *.jpeg *.png)"
        )
        if file_path:
            self.preview_file = file_path
            self.preview_edit.setText(file_path)

    def select_output_file(self):
        file_path, _ = QFileDialog.getSaveFileName(
            self, "保存主题包", "", "华为主题包 (*.hwt)"
        )
        if file_path:
            if not file_path.endswith('.hwt'):
                file_path += '.hwt'
            self.output_file = file_path
            self.output_edit.setText(file_path)

    def reset_form(self):
        self.font_edit.clear()
        self.preview_edit.clear()
        self.output_edit.clear()
        self.title_edit.setText("HarmonyOS Sans")
        self.title_cn_edit.setText("华为鸿蒙字体")
        self.author_edit.setText("Your Name")
        self.designer_edit.setText("Designer Name")
        self.screen_combo.setCurrentIndex(0)
        self.font_edit_name.setText("HarmonyOS Sans")
        self.font_cn_edit.setText("华为鸿蒙字体")
        self.version_edit.setText("1.0.0")
        self.log_area.clear()

    def log_message(self, message):
        self.log_area.append(f"[INFO] {message}")
        self.statusBar().showMessage(message)

    def show_error(self, title, message):
        InfoBar.error(
            title=title,
            content=message,
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP,
            duration=5000,
            parent=self
        )
        self.log_message(f"[ERROR] {title}: {message}")

    def show_success(self, title, message):
        InfoBar.success(
            title=title,
            content=message,
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP,
            duration=3000,
            parent=self
        )
        self.log_message(f"[SUCCESS] {title}: {message}")

    def generate_theme(self):
        if not self.font_file:
            self.show_error("错误", "请选择字体文件")
            return

        if not self.output_file:
            self.show_error("错误", "请设置输出文件路径")
            return

        if not os.path.exists(self.font_file):
            self.show_error("错误", "字体文件不存在，请重新选择")
            return

        if self.preview_file and not os.path.exists(self.preview_file):
            self.show_error("错误", "预览图文件不存在，请重新选择")
            return

        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(10)

        try:
            title = self.title_edit.text() or "My Font"
            title_cn = self.title_cn_edit.text() or "我的字体"
            author = self.author_edit.text() or "unknown"
            designer = self.designer_edit.text() or "unknown"
            screen = self.screen_combo.currentText()
            version = self.version_edit.text() or "1.0.0"
            font = self.font_edit_name.text() or "My Font"
            font_cn = self.font_cn_edit.text() or "我的字体"

            preview_img = self.preview_file if self.preview_file else None

            self.progress_bar.setValue(30)

            create_hwt_file(
                self.output_file,
                self.font_file,
                preview_img,
                title=title,
                title_cn=title_cn,
                author=author,
                designer=designer,
                screen=screen,
                version=version,
                font=font,
                font_cn=font_cn
            )

            self.progress_bar.setValue(100)
            self.show_success("成功", f"主题包已成功生成: {os.path.basename(self.output_file)}")

        except Exception as e:
            self.progress_bar.setValue(0)
            self.show_error("错误", f"生成主题包时出错: {str(e)}")
        finally:
            self.progress_bar.setVisible(False)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    font = QFont("Microsoft YaHei", 10)
    app.setFont(font)

    window = HWTGeneratorApp()
    window.show()
    sys.exit(app.exec())