import re
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QLabel, QScrollArea, QFrame
from PyQt6.QtCore import Qt

class HexToStrWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("16进制转ASCII工具")
        self.setGeometry(100, 100, 600, 400)

        # 初始化字节序，默认为小端序
        self.endian = "little"
        self.ignoreSpace = False

        # 初始化UI
        self.init_ui()

    def init_ui(self):
        # 主布局
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(10, 10, 10, 10)

        # 创建顶部输入区域
        self.input_area = QVBoxLayout()  # 管理所有输入框的布局
        self.input_area.setContentsMargins(0, 0, 0, 0)
        self.input_area.setAlignment(Qt.AlignmentFlag.AlignTop)  # 设置对齐方式为顶部对齐

        # 创建第一个输入框
        self.add_new_input()  # 添加第一个输入框

        # 创建一个用于容纳多个输入框的滚动区域
        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)
        scroll_content = QWidget()
        scroll_content.setLayout(self.input_area)
        scroll_area.setWidget(scroll_content)

        # 创建底部的结果显示区域
        self.result_label = QLabel("输出:", self)
        self.result_label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        self.result_label.setFrameShape(QFrame.Shape.Panel)
        self.result_label.setFrameShadow(QFrame.Shadow.Sunken)
        self.result_label.setStyleSheet("padding: 10px; font-size: 14px;")
        self.result_label.setMinimumHeight(50)

        # 添加组件到主布局
        self.layout.addWidget(scroll_area)  # 滚动输入区域
        self.layout.addWidget(self.result_label)  # 固定输出区域

        # 设置输入区域和结果区域的比例,确保输入框占满空间
        self.layout.setStretch(0, 10)
        self.layout.setStretch(1, 1)  

        # 设置主布局
        self.setLayout(self.layout)

    def set_endian(self, endian):
        """设置字节序"""
        self.endian = endian
        self.handle_input_change()  # 切换字节序后，重新计算结果

    def set_ignoreSpace(self, ifIgnore):
        """设置是否忽略空格"""
        self.ignoreSpace = ifIgnore
        self.handle_input_change()

    def add_new_input(self):
        input_box = QLineEdit(self)
        input_box.setPlaceholderText("请输入'0x'开头的16进制数")
        input_box.textChanged.connect(self.handle_input_change)
        self.input_area.addWidget(input_box)  # 将输入框添加到输入区域布局的顶部



    def handle_input_change(self):
        """实时监听输入框内容变化"""
        #1. 获取当前所有输入框的内容
        inputs = [box.text() for box in self.findChildren(QLineEdit)]

        #2. 检查是否需要添加新的输入框
        if inputs and inputs[-1].strip():
            if len(self.findChildren(QLineEdit)) == len(inputs):
                self.add_new_input()

        #3. 转换并更新结果
        self.update_result(inputs)

    def hex2str(self, hex_strings):
        """将十六进制字符串转换为ASCII字符串"""
        combined_hex = ''.join(hex_strings).replace('0x', '')  # 合并输入，去掉 "0x"
        byte_data = bytes.fromhex(combined_hex)

        # 根据字节序调整字节数据
        if self.endian == "little":
            byte_data = byte_data[::-1]

        result = []
        for byte in byte_data:
            char = chr(byte)
            if char.isprintable():
                result.append(char)  # 可见字符直接输出
            else:
                result.append(f"\\x{byte:02x}")  # 不可见字符转换为 \xNN 形式

        return ''.join(result)

    def update_result(self, inputs):
        """更新输出结果"""
        # 使用正则表达式匹配有效十六进制字符串
        
        pattern = re.compile(r'0x[0-9a-fA-F]+')
        valid_hex = [match.group() for input_str in inputs for match in pattern.finditer(input_str)]
        #has_invalid_char = any(not bool(re.fullmatch(pattern, input_str)) for input_str in inputs)
        has_invalid_char = False

        print(valid_hex)
        #print(has_invalid_char)

        if not valid_hex or has_invalid_char:
            self.result_label.setText("请输入'0x'开头的有效16进制字符串！")
        else:
            # 转换为ASCII并显示
            try:
                result = self.hex2str(valid_hex)
                self.result_label.setText(f"转换结果：{result}")
            except ValueError:
                self.result_label.setText("输入完整的一个字节!")
