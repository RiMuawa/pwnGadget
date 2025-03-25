import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QMenuBar, QStackedWidget, QLabel, QMenu
from PyQt6.QtGui import QAction, QActionGroup
from PyQt6.QtGui import QKeySequence
from Tools.Hex2strTransfomer import HexToStrWindow  # 导入第一个组件
from Tools.LibcGuessHelper import LibcGuessHelper  # 导入第二个组件

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("芝士窗口")
        self.setGeometry(100, 100, 600, 400)

        # 默认字节序设置
        self.current_endian = "little"
        self.ignoreSpace = False

        # 初始化UI
        self.init_ui()

    def init_ui(self):
        # 创建主窗口的中央widget
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # 使用 QStackedWidget 实现组件切换
        self.stack = QStackedWidget(self)
        layout = QVBoxLayout(central_widget)
        layout.addWidget(self.stack)

        # 添加欢迎界面
        self.welcome_widget = self.create_welcome_widget()
        self.stack.addWidget(self.welcome_widget)

        # 添加第一个工具组件
        self.hex_to_str_window = HexToStrWindow()
        self.hex_to_str_window.set_endian(self.current_endian)  # 初始化传递字节序
        self.stack.addWidget(self.hex_to_str_window)

        # 添加第二个工具组件
        self.libc_guess_helper = LibcGuessHelper()
        self.stack.addWidget(self.libc_guess_helper)

        # 创建菜单栏
        self.menu_bar = QMenuBar(self)
        self.setMenuBar(self.menu_bar)

        # 菜单栏选项
        tool_menu = self.menu_bar.addMenu("Tools")
        setting_menu = self.menu_bar.addMenu("Settings")

        # 添加Tools菜单项：切换到 Hex to ASCII 工具
        hex_tool_action = QAction("Hex to ASCII", self)
        hex_tool_action.triggered.connect(lambda: self.stack.setCurrentWidget(self.hex_to_str_window))
        tool_menu.addAction(hex_tool_action)

        # 添加Tools菜单项：切换到 Libc Guess Helper
        libc_tool_action = QAction("Libc Guess Helper", self)
        libc_tool_action.triggered.connect(lambda: self.stack.setCurrentWidget(self.libc_guess_helper))
        tool_menu.addAction(libc_tool_action)

        # 创建Settings菜单项: 设置大端序/小端序
        endian_menu = QMenu("端序", self)
        endian_menu.setParent(self)
        setting_menu.addMenu(endian_menu)

        # 添加端序设置的具体选项    
        endian_group = QActionGroup(self)  # 互斥的字节序设置
        little_endian_action = QAction("小端序 (little)", self, checkable=True)
        little_endian_action.setChecked(True)  # 默认选中小端序
        little_endian_action.triggered.connect(lambda: self.set_endian("little"))
        endian_menu.addAction(little_endian_action)
        endian_group.addAction(little_endian_action)

        big_endian_action = QAction("大端序 (big)", self, checkable=True)
        big_endian_action.triggered.connect(lambda: self.set_endian("big"))
        endian_menu.addAction(big_endian_action)
        endian_group.addAction(big_endian_action)

        # 创建Settings菜单项: 忽略输入中的空格
        ignoreSpace_menu = QAction("忽略空格", self)
        ignoreSpace_menu.setCheckable(True)
        ignoreSpace_menu.triggered.connect(lambda: self.set_ignoreSpace())
        setting_menu.addAction(ignoreSpace_menu)        

        # 添加退出选项到 Settings 菜单
        exit_action = QAction("退出", self)
        exit_action.triggered.connect(self.close)
        exit_action.setShortcut(QKeySequence("Ctrl+Q"))
        setting_menu.addAction(exit_action)

    def set_endian(self, endian):
        """设置字节序"""
        self.current_endian = endian
        self.hex_to_str_window.set_endian(endian)  # 向 HexToStrWindow 传递字节序设置

    def set_ignoreSpace(self):
        self.ignoreSpace = not self.ignoreSpace
        self.hex_to_str_window.set_ignoreSpace(self.ignoreSpace)
        print(f"忽略空格: {self.ignoreSpace}")

    def create_welcome_widget(self):
        welcome_widget = QWidget(self)
        layout = QVBoxLayout(welcome_widget)

        welcome_label = QLabel("超级无敌pwn大王的小工具", self)
        welcome_label.setStyleSheet("font-size: 18px; text-align: center;")
        layout.addWidget(welcome_label)

        # 返回欢迎界面
        return welcome_widget

def main():
    app = QApplication(sys.argv)

    main_window = MainWindow()
    main_window.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()
