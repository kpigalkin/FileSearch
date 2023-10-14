from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTreeView, QFileSystemModel, QLineEdit
from PyQt5.QtCore import QDir, QSortFilterProxyModel, QRegExp, Qt
import sys
import os


class FileManager(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(200, 200, 900, 500)
        self.setWindowTitle('File Manager')

        self.home_path = QDir.homePath()
        # model
        self.model = QFileSystemModel()
        self.model.setFilter(QDir.AllEntries | QDir.Hidden | QDir.NoDotAndDotDot)
        self.model.setRootPath(self.home_path)

        self.proxy_model = QSortFilterProxyModel()
        self.proxy_model.setSourceModel(self.model)
        self.proxy_model.setRecursiveFilteringEnabled(True)

        self.tree_view = QTreeView()
        self.tree_view.setModel(self.proxy_model)
        self.tree_view.setColumnWidth(0, 400)
        self.tree_view.setRootIndex(self.proxy_model.mapFromSource(
            self.model.index(self.home_path)
        ))

        # text input
        self.input_line = QLineEdit()
        self.input_line.setPlaceholderText("Browse files...")
        self.input_line.textChanged.connect(self.search_files)

        # layout
        layout = QVBoxLayout()
        layout.addWidget(self.input_line)
        layout.addWidget(self.tree_view)
        self.setLayout(layout)

    def search_files(self, text):
        if text:
            self.tree_view.expandAll()
            self.proxy_model.setFilterRegExp(
                QRegExp(text, Qt.CaseInsensitive, QRegExp.FixedString)
            )
        else:
            self.tree_view.setRootIndex(self.proxy_model.mapFromSource(
                self.model.index(self.home_path)
            ))
            self.tree_view.collapseAll()


if __name__ == '__main__':
    os.chmod("main.py", 0o666)
    app = QApplication(sys.argv)
    file_manager = FileManager()
    file_manager.show()
    sys.exit(app.exec_())
