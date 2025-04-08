from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QLabel, QScrollArea, QFrame
from PyQt6.QtWidgets import QPushButton, QApplication
from PyQt6.QtCore import Qt

class FakeChunk(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Fake Chunk构造小工具")
        self.setGeometry(100, 100, 600, 400)

        self.init_ui()

    def init_ui(self):
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(10, 10, 10, 10)

        self.input_area = QVBoxLayout()
        self.input_area.setContentsMargins(0, 0, 0, 0)
        self.input_area.setAlignment(Qt.AlignmentFlag.AlignTop)

        # 创建各个字段的输入框
        self.prev_size_input = self.create_input("prev_size(前一个chunk的大小)")
        self.size_input = self.create_input("size (当前chunk的大小)")
        self.fd_input = self.create_input("fd (前一个chunk的地址)")
        self.bk_input = self.create_input("bk (后一个chunk的地址)")
        self.data_input = self.create_input("data (填充内容)")

        # 滚动区域封装
        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)
        scroll_content = QWidget()
        scroll_content.setLayout(self.input_area)
        scroll_area.setWidget(scroll_content)

        # 输出区域
        self.result_label = QLabel("payload:", self)
        self.result_label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        self.result_label.setFrameShape(QFrame.Shape.Panel)
        self.result_label.setFrameShadow(QFrame.Shadow.Sunken)
        self.result_label.setStyleSheet("padding: 10px; font-size: 14px;")
        self.result_label.setMinimumHeight(50)

        # 添加复制按钮
        self.copy_button = QPushButton("copy")
        self.copy_button.clicked.connect(self.copy_to_clipboard)
        self.layout.addWidget(self.copy_button)


        # 添加到主布局
        self.layout.addWidget(scroll_area)
        self.layout.addWidget(self.result_label)

        self.layout.setStretch(0, 10)
        self.layout.setStretch(1, 1)

        self.setLayout(self.layout)

    def create_input(self, placeholder):
        input_box = QLineEdit(self)
        input_box.setPlaceholderText(placeholder)
        input_box.textChanged.connect(self.update_result)
        self.input_area.addWidget(input_box)
        return input_box

    def update_result(self):
        prev_size = self.prev_size_input.text().strip()
        size = self.size_input.text().strip()
        fd = self.fd_input.text().strip()
        bk = self.bk_input.text().strip()
        data = self.data_input.text().strip()

        # 拼接表达式字符串
        payload_str = f"payload = p64({prev_size}) + p64({size}) + p64({fd}) + p64({bk}) + {data}"
        self.result_label.setText(payload_str)
    
    def copy_to_clipboard(self):
        clipboard = QApplication.clipboard()
        clipboard.setText(self.result_label.text())

