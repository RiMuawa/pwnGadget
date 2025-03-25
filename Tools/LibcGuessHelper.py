from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QLabel
from PyQt6.QtCore import Qt

class LibcGuessHelper(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Libc Guess Helper")
        self.setGeometry(100, 100, 600, 200)

        # 初始化UI
        self.init_ui()

    def init_ui(self):
        self.layout = QVBoxLayout()

        # 输入框：真实地址
        self.real_addr_input = QLineEdit(self)
        self.real_addr_input.setPlaceholderText("输入函数的真实地址 (real_addr)")
        self.real_addr_input.textChanged.connect(self.calculate_result)
        self.layout.addWidget(self.real_addr_input)

        # 输入框：libc 偏移地址
        self.libc_addr_input = QLineEdit(self)
        self.libc_addr_input.setPlaceholderText("输入函数在 libc 中的偏移地址 (libc_addr)")
        self.libc_addr_input.textChanged.connect(self.calculate_result)
        self.layout.addWidget(self.libc_addr_input)

        # 输入框：要猜测的函数地址
        self.guess_addr_libc_input = QLineEdit(self)
        self.guess_addr_libc_input.setPlaceholderText("输入要猜测的函数在 libc 中的地址 (guess_addr_libc)")
        self.guess_addr_libc_input.textChanged.connect(self.calculate_result)
        self.layout.addWidget(self.guess_addr_libc_input)

        # 显示结果：libc base
        self.libc_base_label = QLabel("libc 基地址：", self)
        self.libc_base_label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        self.layout.addWidget(self.libc_base_label)

        # 显示结果：guess_addr_mem
        self.guess_addr_mem_label = QLabel("猜测的内存地址：", self)
        self.guess_addr_mem_label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        self.layout.addWidget(self.guess_addr_mem_label)

        self.setLayout(self.layout)

    def calculate_result(self):
        try:
            # 获取输入框的值并转换为整数
            real_addr = int(self.real_addr_input.text(), 16) if self.real_addr_input.text() else None
            libc_addr = int(self.libc_addr_input.text(), 16) if self.libc_addr_input.text() else None
            guess_addr_libc = int(self.guess_addr_libc_input.text(), 16) if self.guess_addr_libc_input.text() else None

            if real_addr is not None and libc_addr is not None:
                libc_base = real_addr - libc_addr
                self.libc_base_label.setText(f"libc 基地址：{hex(libc_base)}")
            else:
                self.libc_base_label.setText("libc 基地址：")

            if real_addr is not None and libc_addr is not None and guess_addr_libc is not None:
                libc_base = real_addr - libc_addr
                guess_addr_mem = libc_base + guess_addr_libc
                self.guess_addr_mem_label.setText(f"猜测的内存地址：{hex(guess_addr_mem)}")
            else:
                self.guess_addr_mem_label.setText("猜测的内存地址：")
        except ValueError:
            # 输入不是有效的十六进制
            self.libc_base_label.setText("输入的地址格式不正确！")
            self.guess_addr_mem_label.setText("")
