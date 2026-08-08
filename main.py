import sys
from pathlib import Path

from PySide6.QtCore import QEvent, QFile, QObject, QSettings
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QApplication, QFileDialog, QMessageBox, QInputDialog, QFontDialog, QMenu, QTextEdit
from PySide6.QtGui import QAction, QActionGroup

class MainWindow(QObject):
    def __init__(self):
        super().__init__()

        self.current_file: Path | None = None
        self.search_text = ""

        self.current_encoding = "utf-8"

        self.zoom_level = 0 # 0:基準 +1:一段拡大  -1:縮小
        # --- UIのロード ---
        loader = QUiLoader()
        ui_file = QFile("mainWindow.ui")

        if not ui_file.open(QFile.ReadOnly):
            raise RuntimeError("mainWindow.ui を開けません")

        self.window = loader.load(ui_file)
        ui_file.close()
        
        if self.window is None:
            raise RuntimeError("mainWindow.uiの読み込みに失敗しました")
        # --- UIのロード ---
        # --- アクションのグループ化 ---
        self.encode_action_group = QActionGroup(self.window)
        self.encode_action_group.addAction(self.window.actionEncodingUtf8)
        self.encode_action_group.addAction(self.window.actionEncodingShiftJis)
        self.window.actionEncodingUtf8.setChecked(True)
        self.encode_action_group.setExclusive(True) # グループ内のActionは同時に１つしか選択できないようにする

        # ファイルドラッグ&ドロップを有効にする
        self.window.setAcceptDrops(True)
        self.window.textEdit.setAcceptDrops(False) # QTextEditのドロップイベントは無効にする

        # --- 最近使ったファイルメニューの作成 ---
        self.recent_files_menu = QMenu("最近使ったファイル", self.window)
        self.window.menu.addMenu(self.recent_files_menu)

        self.settings = QSettings("kazu025", "PySide6-Notepad",)

        save_zoom_level = self.settings.value("ZoomLevel", 0, type=int)
        self.apply_zoom_level(save_zoom_level)
        self.zoom_level = save_zoom_level

        word_wrap = self.settings.value("WordWrap", True, type=bool)
        self.window.actionWordWrap.setChecked(word_wrap)
        self.apply_word_wrap(word_wrap)


        # --- ウィンドウ設定の保存 ---
        geometry = self.settings.value("WindowGeometry")
        if geometry is not None:
            self.window.restoreGeometry(geometry)

        self.max_recent_files = 5
        self.recent_files = self.load_recent_files()
        # --- 最近使ったファイルメニューの作成 ---

        self.connect_signals()
        self.update_recent_files_menu()

        self.window.statusBar().showMessage("準備完了")

        # ウインドウの終了イベントを監視する
        self.window.installEventFilter(self)

        # 起動直後は未変更状態とする。
        self.window.textEdit.document().setModified(False)

        self.update_title()
        self.update_status_bar()

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
        self.window.actionFind.triggered.connect(self.search_text_dialog)
        self.window.actionFindNext.triggered.connect(self.find_next)

        self.window.textEdit.cursorPositionChanged.connect(self.update_status_bar)
        self.window.textEdit.textChanged.connect(self.update_status_bar)

        # 書式メニュー
        self.window.actionFont.triggered.connect(self.change_font)

        # エンコードメニュー
        self.window.actionEncodingUtf8.triggered.connect(self.set_encoding_utf8)
        self.window.actionEncodingShiftJis.triggered.connect(self.set_encoding_shift_jis)

        # 表示メニュー
        self.window.actionWordWrap.triggered.connect(self.toggle_word_wrap)

        self.window.actionZoomIn.triggered.connect(self.zoom_in)
        self.window.actionZoomOut.triggered.connect(self.zoom_out)
        self.window.actionZoomReset.triggered.connect(self.zoom_reset)

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
        self.add_recent_file(new_file)

        return True
        
    def write_file(self, file_path: Path) -> bool:
        """指定されたファイルへテキストを書き込む"""
        text = self.window.textEdit.toPlainText()

        try:
            file_path.write_text(text, encoding=self.current_encoding)
        except UnicodeEncodeError as error:
            QMessageBox.critical(
                self.window,
                "文字コードエラー",
                f"{self.current_encoding} では保存できない文字が含まれています。\n\n{error}",
            )
            return False
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
        """ウィンドウのイベントを処理する"""
        if watched is self.window:
            if event.type() == QEvent.Type.DragEnter:
                if event.mimeData().hasUrls():
                    event.acceptProposedAction()
                else:
                    event.ignore()

                return True

            if event.type() == QEvent.Type.Drop:
                self.drop_file(event)
                return True

            if event.type() == QEvent.Type.Close:
                if self.confirm_save():
                    # --- ウィンドウの位置とサイズを保存する ---
                    self.settings.setValue("WindowGeometry", self.window.saveGeometry())
                    event.accept()
                else:
                    event.ignore()

                return True

        return False

    def show(self):
        self.window.show()

    def search_text_dialog(self) -> None:
        text, ok = QInputDialog.getText(
            self.window,
            "検索",
            "検索する文字を入力してください"
        )

        if not ok or not text:
            return

        self.search_text = text

        cursor = self.window.textEdit.textCursor()
        cursor.movePosition(cursor.MoveOperation.Start)
        self.window.textEdit.setTextCursor(cursor)

        self.find_next()

    def find_next(self) -> None:
        if not self.search_text:
            self.search_text_dialog()
            return

        found = self.window.textEdit.find(self.search_text)

        if found:
            return

        # 文書の先頭へ戻る
        cursor = self.window.textEdit.textCursor()
        cursor.movePosition(cursor.MoveOperation.Start)
        self.window.textEdit.setTextCursor(cursor)

        # もう一度検索
        found = self.window.textEdit.find(self.search_text)

        if found:
            QMessageBox.information(
                self.window,
                "検索",
                "文書の最後まで検索しました。\n先頭から検索します。"
            )
        else:
            QMessageBox.information(
                self.window,
                "検索",
                f"「{self.search_text}」は見つかりませんでした"
            )

    def update_status_bar(self):
        cursor = self.window.textEdit.textCursor()
        line = cursor.blockNumber() + 1
        column = cursor.positionInBlock() + 1
        character_count = len(self.window.textEdit.toPlainText())

        font = self.window.textEdit.font()
        font_family = font.family()
        font_size = font.pointSize()

        encoding_display_name = self.get_encoding_display_name()

        self.window.statusBar().showMessage(f"Ln {line}, Col {column} | 文字数: {character_count} | {font_family} {font_size}pt | {encoding_display_name}")

    def change_font(self) -> None:
        """テキストエディタのフォントを変更する"""
        current_font = self.window.textEdit.font()

        ok, selected_font = QFontDialog.getFont(current_font, self.window, "フォントの選択")
        if not ok:
            return

        self.window.textEdit.setFont(selected_font)
        self.update_status_bar()

    def load_recent_files(self) -> list[str]:
        """保存されている最近使ったファイル一覧を読み込む"""
        recent_files = self.settings.value("recentFiles", [])

        if isinstance(recent_files, str):
            return [recent_files]

        return list(recent_files)

    def add_recent_file(self, file_path: Path) -> None:
        """指定されたファイルを最近使ったファイル一覧へ追加する"""
        path_string = str(file_path.resolve())
        if path_string in self.recent_files:
            self.recent_files.remove(path_string)

        self.recent_files.insert(0, path_string)
        self.recent_files = self.recent_files[:self.max_recent_files]

        self.settings.setValue("recentFiles", self.recent_files)
        self.update_recent_files_menu()

    def update_recent_files_menu(self) -> None:
        """最近使ったファイルメニューを再構築する"""
        menu = self.recent_files_menu
        menu.clear()

        if not self.recent_files:
            action = QAction("履歴はありません", self.window)
            action.setEnabled(False)
            menu.addAction(action)
            return

        for index, file_path in enumerate(self.recent_files, start=1):
            action = QAction(
                f"{index}. {file_path}",
                self.window,
            )
            # file_pathを保持してクリック時に開く
            action.triggered.connect(
                lambda checked=False, path=file_path:
                  self.open_recent_file(path)
            )

            menu.addAction(action)

        menu.addSeparator()
        clear_action = QAction("履歴をクリア", self.window)
        clear_action.triggered.connect(self.clear_recent_files)
        menu.addAction(clear_action)

    def clear_recent_files(self) -> None:
        """最近使ったファイル一覧をクリアする"""
        result = QMessageBox.question(
            self.window,
            "履歴のクリア",
            "最近使ったファイル一覧をクリアしますか？",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        if result == QMessageBox.StandardButton.Yes:
            self.recent_files.clear()
            self.settings.remove("recentFiles")
            self.update_recent_files_menu()

    def open_recent_file(self, file_path: str) -> None:
        """最近使ったファイル一覧からファイルを開く"""
        if not self.confirm_save():
            return 

        path = Path(file_path)

        if not path.exists():
            QMessageBox.warning(self.window, "ファイルは見つかりません", f"次のファイルは存在しません。\n\n{path}",)

            self.recent_files.remove(file_path)
            self.settings.setValue("recentFiles", self.recent_files,)
            self.update_recent_files_menu()
            return

        self.load_file(path)

    def open_file(self) -> None:
        """ファイル選択ダイアログからテキストファイルを開く"""
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

        self.load_file(Path(file_path))

    def load_file(self, file_path: Path) -> bool:
        """指定されたテキストファイルを読み込む"""
        try:
            text = file_path.read_text(encoding=self.current_encoding)
        except UnicodeDecodeError as error:
            QMessageBox.critical(self.window, "文字コードエラー", f"{self.current_encoding} では読み込めない文字が含まれています。\n\n 文字コードを変更して、もう一度開いてください。{error}")
            return False
        except OSError as error:
            QMessageBox.critical(self.window, "読み込みエラー", f"ファイルを読み込めませんでした。\n\n{error}")
            return False

        self.window.textEdit.setPlainText(text)
        self.current_file = file_path
        self.window.textEdit.document().setModified(False)
        self.update_title()
        self.add_recent_file(file_path)
        return True

    def set_encoding_utf8(self) -> None:
        """エンコードをUTF-8に設定する"""
        self.current_encoding = "utf-8"
        self.update_status_bar()

    def set_encoding_shift_jis(self) -> None:
        """エンコードをShift_JISに設定する"""
        self.current_encoding = "shift_jis"
        self.update_status_bar()

    def get_encoding_display_name(self) -> str:
        """表示用の文字コード名を取得する"""
        if self.current_encoding == "utf-8":
            return "UTF-8"

        return "Shift_JIS"

    def toggle_word_wrap(self, checked: bool) -> None:
        """テキストの折返し表示を切り替える"""
        self.apply_word_wrap(checked)
        self.settings.setValue("WordWrap", checked)
        
    def apply_word_wrap(self, checked: bool) -> None:
        if checked:
            self.window.textEdit.setLineWrapMode(QTextEdit.LineWrapMode.WidgetWidth)
        else:
            self.window.textEdit.setLineWrapMode(QTextEdit.LineWrapMode.NoWrap)

    def zoom_in(self) -> None:
        """テキストを拡大する"""
        self.window.textEdit.zoomIn(1)
        self.zoom_level += 1
        self.settings.setValue("ZoomLevel", self.zoom_level)
        self.update_status_bar()

    def zoom_out(self) -> None:
        """テキストを縮小する"""
        self.window.textEdit.zoomOut(1)
        self.zoom_level -= 1
        self.settings.setValue("ZoomLevel", self.zoom_level)
        self.update_status_bar()

    def zoom_reset(self) -> None:
        """テキストの拡大率をリセットする"""
        if self.zoom_level > 0:
            self.window.textEdit.zoomOut(self.zoom_level)
        elif self.zoom_level < 0:
            self.window.textEdit.zoomIn(-self.zoom_level)
        self.zoom_level = 0
        self.settings.setValue("ZoomLevel", self.zoom_level)
        self.update_status_bar()

    def apply_zoom_level(self, level: int) -> None:
        """指定された拡大率を適用する"""
        if level > 0:
            self.window.textEdit.zoomIn(level)
        elif level < 0:
            self.window.textEdit.zoomOut(-level)
        self.update_status_bar()

    def drop_file(self, event) -> None:
        """ファイルがドロップされたときの処理"""
        urls = event.mimeData().urls()
        if not urls:
            return

        file_path = urls[0].toLocalFile()
        if not file_path:
            return

        path = Path(file_path)

        if not path.is_file():
            QMessageBox.warning(self.window, "ファイルではありません", f"次のパスはファイルではありません。\n\n{path}")
            return

        # テキストファイル以外は開かない
        if path.suffix.lower() != ".txt":
            QMessageBox.warning(self.window, "ファイル形式エラー", f"次のファイルはテキストファイルではありません。\n\n{path}")
            return

        if not self.confirm_save():
            return

        self.load_file(path)

        event.acceptProposedAction()

def main():
    app = QApplication(sys.argv)

    main_window = MainWindow()
    main_window.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()
