import sys
from pathlib import Path
from PySide6.QtCore import QFile
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QApplication, QFileDialog, QMainWindow, QMessageBox

class MainWindow:
    def __init__(self):
        self.current_file: Path | None = None

        loader = QUiLoader()
        ui_file = QFile("mainWindow.ui")

        if not ui_file.open(QFile.ReadOnly):
            raise RuntimeError("mainWindow.ui を開けません")

        self.window = loader.load(ui_file)
        ui_file.close()

        if self.window is None:
            raise RuntimeError("mainWindow.uiの読み込みに失敗しました")

        self.connect_signals()
        self.update_title()

    def connect_signals(self):
        self.window.actionNew.triggered.connect(self.new_file)
        self.window.actionOpen.triggered.connect(self.open_file)
        self.window.actionSave.triggered.connect(self.save_file)
        self.window.actionSaveAs.triggered.connect(self.save_file_as)
        self.window.actionExit.triggered.connect(self.window.close)

    def new_file(self):
        self.window.textEdit.clear()
        self.current_file = None
        self.update_title()

    def open_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self.window,
            "ファイルを開く",
            "",
            "テキストファイル (*.txt);;すべてのファイル (*)",
        )

        if not file_path:
            return

        try:
            text = Path(file_path).read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError) as error:
            QMessageBox.critical(
                self.window,
                "読み込みエラー",
                f"ファイルを読み込めませんでした。\n\n{error}",
            )
            return

        self.window.textEdit.setPlainText(text)
        self.current_file = Path(file_path)
        self.update_title()

    def save_file(self):
        if self.current_file is None:
            self.save_file_as()
            return

        self.write_file(self.current_file)

    def save_file_as(self):
        file_path, _ = QFileDialog.getSaveFileName(
            self.window,
            "名前を付けて保存",
            "",
            "テキストファイル (*.txt);;すべてのファイル (*)",
        )

        if not file_path:
            return

        self.current_file = Path(file_path)
        self.write_file(self.current_file)

    def write_file(self, file_path: Path):
        text = self.window.textEdit.toPlainText()

        try:
            file_path.write_text(text, encoding="utf-8")
        except OSError as error:
            QMessageBox.critical(
                self.window,
                "保存エラー",
                f"ファイルを保存できませんでした。\n\n{error}",
            )
            return

        self.update_title()

    def update_title(self):
        if self.current_file is None:
            filename = "無題"
        else:
            filename = self.current_file.name

        self.window.setWindowTitle(f"{filename} - PySide6 メモ帳")

    def show(self):
        self.window.show()

def main():
    app = QApplication(sys.argv)

    main_window = MainWindow()
    main_window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
