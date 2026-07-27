import sys
from pathlib import Path

from PySide6.QtCore import QEvent, QFile, QObject
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QApplication, QFileDialog, QMessageBox

class MainWindow(QObject):
    def __init__(self):
        super().__init__()

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

        # ウインドウの終了イベントを監視する
        self.window.installEventFilter(self)

        # 起動直後は未変更状態とする。
        self.window.textEdit.document().setModified(False)

        self.update_title()

    def connect_signals(self):
        self.window.actionNew.triggered.connect(self.new_file)
        self.window.actionOpen.triggered.connect(self.open_file)
        self.window.actionSave.triggered.connect(self.save_file)
        self.window.actionSaveAs.triggered.connect(self.save_file_as)
        self.window.actionExit.triggered.connect(self.window.close)

        # 編集メニュー
        self.window.actionUndo.triggered.connect(self.window.textEdit.undo)
        self.window.actionRedo.triggered.connect(self.window.textEdit.redo)
        self.window.actionCut.triggered.connect(self.window.textEdit.cut)
        self.window.actionCopy.triggered.connect(self.window.textEdit.copy)
        self.window.actionPaste.triggered.connect(self.window.textEdit.paste)
        self.window.actionSelectAll.triggered.connect(self.window.textEdit.selectAll)

        # テキストの変更状態が変わったときにタイトルを更新する
        self.window.textEdit.document().modificationChanged.connect(
            self.update_title
        )

    def new_file(self):
        '''新しい文章を作成する'''
        if not self.confirm_save():
            return
        
        self.window.textEdit.clear()
        self.current_file = None

        # clear()のあとに文章を未変更状態にする
        self.window.textEdit.document().setModified(False)

        self.update_title()

    def open_file(self):
        '''テキストファイルを開く'''
        if not self.confirm_save():
            return
        
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

        # 読み込んだ直後は文章を未変更状態
        self.window.textEdit.document().setModified(False)

        self.update_title()

    def save_file(self) -> bool:
        if self.current_file is None:
            return self.save_file_as()

        return self.write_file(self.current_file)

    def save_file_as(self) -> bool:
        """ファイル名を指定して保存する"""
        file_path, _ = QFileDialog.getSaveFileName(
            self.window,
            "名前を付けて保存",
            "",
            "テキストファイル (*.txt);;すべてのファイル (*)",
        )

        if not file_path:
            return False

        new_file = Path(file_path)
        if not self.write_file(new_file):
            return False
        
        self.current_file = new_file
        self.update_title()

        return True
        
    def write_file(self, file_path: Path) -> bool:
        """指定されたファイルへテキストを書き込む"""
        text = self.window.textEdit.toPlainText()

        try:
            file_path.write_text(text, encoding="utf-8")
        except OSError as error:
            QMessageBox.critical(
                self.window,
                "保存エラー",
                f"ファイルを保存できませんでした。\n\n{error}",
            )
            return False
        
        # 保存が成功したので未変更状態に戻す
        self.window.textEdit.document().setModified(False)
        self.update_title()

        return True

    def confirm_save(self) -> bool:
        """
        未保存の変更がある場合に保存確認を行う。
        戻り値:
            True:
                新規作成または終了処理を続行する。
            False:
                処理を中止する。
        """
        document = self.window.textEdit.document()
        if not document.isModified():
            return True

        result = QMessageBox.question(
            self.window,
            "保存の確認",
            "内容が変更されています。\n保存しますか？",
                QMessageBox.StandardButton.Save
                | QMessageBox.StandardButton.Discard
                | QMessageBox.StandardButton.Cancel,
                QMessageBox.StandardButton.Save
        )

        if result == QMessageBox.StandardButton.Save:
            return self.save_file()
        if result == QMessageBox.StandardButton.Discard:
            return True

        return False        

    def update_title(self):
        """タイトルバーの文字列を更新する"""
        if self.current_file is None:
            filename = "無題"
        else:
            filename = self.current_file.name

        if self.window.textEdit.document().isModified():
            modified_mark = "*"
        else:
            modified_mark = ""

        self.window.setWindowTitle(f"{modified_mark}{filename} - PySide6 メモ帳")

    def eventFilter(self, watched, event):
        """ウィンドウ終了時のCloseイベントを処理する。"""
        if watched is self.window and event.type() == QEvent.Type.Close:
            if self.confirm_save():
                event.accept()
            else:
                event.ignore()

            return True

        return super().eventFilter(watched, event)

    def show(self):
        self.window.show()

def main():
    app = QApplication(sys.argv)

    main_window = MainWindow()
    main_window.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()
