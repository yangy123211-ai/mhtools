from PySide6.QtWidgets import QWidget


class PluginInterface(QWidget):
    """
    所有新功能插件都必须继承这个类。
    """

    def __init__(self, parent=None):
        super().__init__(parent)

    def get_name(self):
        """返回显示在标签页上的名字"""
        raise NotImplementedError("插件必须定义名称")

    def get_icon(self):
        """(可选) 返回图标"""
        return None