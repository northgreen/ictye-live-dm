from PyQt5.QtCore import QSize, QRect, Qt
from PyQt5.QtWidgets import QLayout, QWidget, QLabel


class SettingLayout(QLayout):
    def __init__(self, parent=None):
        super(SettingLayout, self).__init__(parent)
        self.items = {}
        self.item = {}

    def addItem(self, widget, label=None):
        self.item[widget] = label

    def addWidget(self, widget, label: str = None):
        label = QLabel(label)
        self.items[widget] = label
        super(SettingLayout, self).addWidget(label)
        super(SettingLayout, self).addWidget(widget)

    def count(self):
        return len(self.items)

    def itemAt(self, index):
        if 0 <= index < len(self.items):
            return list(self.items.keys())[index]
        return None

    def takeAt(self, index):
        if 0 <= index < len(self.items):
            item = list(self.items.keys())[index]
            label = self.items.pop(item)
            return item, label
        return None, None

    def sizeHint(self):
        return self.minimumSize()

    def minimumSize(self):
        min_size = QSize()
        for widget in self.items:
            min_size = min_size.expandedTo(widget.minimumSize())
        return min_size

    def setGeometry(self, rect):
        super(SettingLayout, self).setGeometry(rect)
        self.layout(rect)

    def layout(self, rect=QRect()):
        if not self.items:
            return

        x = rect.x()
        y = rect.y()

        width = rect.width()
        item_height = 50

        items_copy = self.items.copy()

        for widget, label in items_copy.items():
            if label:
                label.setGeometry(QRect(x, y + item_height // 2, width // 4, item_height))
                label.setAlignment(Qt.AlignHCenter)
            else:
                continue

            content_area = QRect(x + width // 4 if label else x, y, 2 * width // 4 if label else width, item_height)
            widget.setGeometry(content_area)
            y += item_height
