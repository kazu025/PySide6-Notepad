# PySide6 Notepad

PySide6 と Qt Designer を使用して作成した、学習用のシンプルなメモ帳アプリケーションです。

PythonによるGUIアプリケーション開発を学ぶことを目的として、機能を段階的に追加しながら開発しています。

---

## Version 14.0

テキストの置換機能を追加しました。

編集メニューまたは `Ctrl+H` から置換処理を開始し、
検索する文字列と置換後の文字列を順番に入力すると、
文書内の一致する文字列をすべて置換できます。

対象文字列が見つからない場合はメッセージを表示し、
置換後は文書を変更済み状態にしてタイトルバーへ `*` を表示します。

### 追加した機能

* テキストの一括置換
* `Ctrl+H` ショートカット
* `QInputDialog.getText()` による検索文字列入力
* `QInputDialog.getText()` による置換文字列入力
* `str.count()` による置換対象件数の取得
* `str.replace()` による全文置換
* 対象文字列が存在しない場合のメッセージ表示
* 空文字への置換による文字列削除
* 置換件数の表示
* `QTextDocument.setModified(True)` による変更状態の反映

---

## 現在の機能

* ✅ ファイルの新規作成
* ✅ 開く
* ✅ 保存
* ✅ 名前を付けて保存
* ✅ 未保存変更の管理
* ✅ Undo / Redo
* ✅ Cut / Copy / Paste
* ✅ Select All
* ✅ 検索（Ctrl+F）
* ✅ 次を検索（F3）
* ✅ ラップアラウンド検索
* ✅ 行番号表示
* ✅ 列番号表示
* ✅ 文字数表示
* ✅ フォント変更
* ✅ フォントサイズ変更
* ✅ 最近使ったファイル（MRU）
* ✅ 履歴の保存
* ✅ 履歴からファイルを開く
* ✅ 履歴をクリア
* ✅ UTF-8 / Shift_JIS の文字コード選択
* ✅ 文字コード指定による読み込み・保存
* ✅ ウィンドウサイズ変更
* ✅ テキスト編集領域の自動リサイズ
* ✅ ウィンドウ位置・サイズの保存と復元
* ✅ 折り返し表示のON / OFF
* ✅ 折り返し表示設定の保存と復元
* ✅ テキスト表示の拡大・縮小
* ✅ ズーム状態の保存と復元
* ✅ 初期表示サイズへのリセット
* ✅ テキストファイルのドラッグ＆ドロップ読み込み
* ✅ 非テキストファイルのドロップ防止
* ✅ ドロップ時の未保存データ確認
* ✅ 指定行へ移動（Ctrl+G）
* ✅ 現在行を初期値とした行番号入力
* ✅ 文書範囲内へのカーソル移動
* ✅ テキストの一括置換（Ctrl+H）
* ✅ 置換対象件数の表示
* ✅ 置換後の未保存状態（*）管理

---

## スクリーンショット

現在の実行画面です。

![Main Window](images/mainwindow_ver14.0.png)

---

## 開発環境

* Python 3.10+
* PySide6 6.11.1
* Qt Designer
* Linux Mint
* Visual Studio Code

---

## 使用ライブラリ

```bash
pip install PySide6
```

---

## 実行方法

```bash
python3 main.py
```

---

## プロジェクト構成

```text
PySide6-Notepad/
├── main.py
├── mainWindow.ui
├── README.md
└── images/
```

---

## 学んだこと

### Version 14.0

* `QInputDialog.getText()` を利用した置換文字列の入力
* Python文字列の `str.count()`
* Python文字列の `str.replace()`
* `QTextEdit.toPlainText()` による全文取得
* `QTextEdit.setPlainText()` による全文更新
* `QTextDocument.setModified(True)` による変更状態の明示
* `modificationChanged` シグナルとタイトルバー更新の関係
* 画面上のテキスト変更とQTextDocumentの変更状態は別に管理されること
* 既存の未保存変更管理との連携

### Version 13.0

* QInputDialog.getInt()
* QTextDocument.blockCount()
* QTextCursor.blockNumber()
* QTextDocument.findBlockByNumber()
* QTextBlock.position()
* QTextBlock.isValid()
* QTextCursor.setPosition()
* QTextEdit.setTextCursor()
* QTextEdit.ensureCursorVisible()
* ユーザー向け行番号とQt内部の0始まりblock番号の変換

### Version 12.0

* QWidget.setAcceptDrops()
* DragEnterイベント
* Dropイベント
* QEvent.Type.DragEnter
* QEvent.Type.Drop
* QMimeData
* mimeData().hasUrls()
* mimeData().urls()
* QUrl.toLocalFile()
* pathlib.Pathによる拡張子判定
* ドラッグ＆ドロップ時のファイル形式チェック
* eventFilter()で複数種類のイベントを処理する方法
* 既存処理を再利用する設計

### Version 11.0

* QTextEdit.zoomIn()
* QTextEdit.zoomOut()
* ズーム段階の管理
* QSettingsによる数値設定の保存
* アプリ起動時のズーム状態復元
* QActionのショートカット設定

### Version 10.0

* QTextEditの折り返し表示
* `QTextEdit.setLineWrapMode()`
* `QTextEdit.LineWrapMode.WidgetWidth`
* `QTextEdit.LineWrapMode.NoWrap`
* checkableなQAction
* QActionのchecked状態
* シグナルからbool値を受け取る方法
* 表示設定と処理の分離
* QSettingsによる表示設定の永続化
* アプリ起動時の設定復元

### Version 9.0

* Qt DesignerのLayout
* QVBoxLayout
* QWidget.saveGeometry()
* QWidget.restoreGeometry()
* QSettingsによるウィンドウ状態の保存
* eventFilter()での終了イベント処理
* GUI部品の自動リサイズ

### Version 8.0

* Pythonの文字コード（encoding）
* UTF-8 / Shift_JIS
* QActionGroup
* QActionのcheckable
* 排他的なAction選択
* UnicodeEncodeError
* UnicodeDecodeError
* Pythonのstrとファイルエンコーディングの関係

### Version 7.0

* QSettings
* QMenu
* QAction（動的生成）
* addMenu()
* addSeparator()
* lambda式によるシグナル接続
* 設定情報の永続化

### Version 6.0

* QFontDialog
* QFontDialog.getFont()
* QFont
* QWidget.setFont()
* 現在のフォント取得
* ダイアログのOK／キャンセル判定

### Version 5.0

* QStatusBar
* QStatusBar.showMessage()
* cursorPositionChangedシグナル
* textChangedシグナル
* QTextCursor
* blockNumber()
* positionInBlock()
* ステータスバーの更新

### Version 4.0

* QTextEdit.find()
* QInputDialog
* 検索機能の実装
* ラップアラウンド検索
* QTextCursor

### Version 3.0

* QAction
* triggeredシグナル
* QTextEdit標準編集機能
* ショートカットキーの設定
* Qt Designerとの連携

### Version 2.0

* Qt Designerで作成したUIの読み込み
* QUiLoaderの利用
* QFileDialogによるファイル操作
* pathlibによるファイル入出力
* QMessageBoxによるダイアログ表示
* QTextDocumentによる変更状態の管理
* modificationChangedシグナル
* eventFilter()による終了イベントの処理
* Pythonの型ヒント（Type Hint）

---

## バージョン履歴

### Version 1.0

* 新規作成
* 開く
* 保存
* 名前を付けて保存

### Version 2.0

* 未保存変更の管理
* タイトルバーに変更マーク（*）
* 終了時・新規作成時・ファイルを開く前の保存確認

### Version 3.0

* Undo / Redo
* Cut / Copy / Paste
* Select All
* ショートカットキー対応

### Version 4.0

* 検索（Ctrl+F）
* 次を検索（F3）
* ラップアラウンド検索

### Version 5.0

* ステータスバー
* 行番号表示（Line）
* 列番号表示（Column）
* 文字数表示

### Version 6.0

* フォント選択ダイアログ
* フォントファミリ変更
* フォントサイズ変更

### Version 7.0

* 最近使ったファイル（MRU）
* 履歴の保存
* 履歴からファイルを開く
* 履歴をクリア
* 存在しないファイルの自動削除

### Version 8.0

* UTF-8 / Shift_JIS の文字コード選択
* QActionGroupによる排他的選択
* 選択した文字コードで読み込み・保存
* ステータスバーに文字コードを表示
* UnicodeDecodeError / UnicodeEncodeError のエラー処理

### Version 9.0

* ウィンドウサイズ変更
* QTextEditの自動リサイズ
* ウィンドウ位置・サイズの保存
* アプリ起動時のウィンドウ状態復元

### Version 10.0

* 折り返し表示のON / OFF
* WidgetWidth / NoWrapの切り替え
* checkable QActionによる表示状態管理
* QSettingsによる折り返し設定の保存
* アプリ再起動時の折り返し設定復元

### Version 11.0

* テキスト表示の拡大・縮小
* 初期表示サイズへのリセット
* ズーム操作のショートカットキー
* QSettingsによるズーム状態の保存
* アプリ再起動時のズーム状態復元

### Version 12.0

* テキストファイルのドラッグ＆ドロップ読み込み
* DragEnter / Dropイベントへの対応
* `.txt` ファイルのみ読み込み可能
* 非テキストファイルの読み込み防止
* ドロップ時の未保存データ確認
* ドロップしたファイルのMRUへの追加

### Version 13.0

* 指定行へ移動
* `Ctrl+G` ショートカット
* 現在行を初期値として表示
* 1行目から最終行までの入力範囲制限
* 指定行の先頭へカーソル移動

### Version 14.0

* テキストの一括置換
* `Ctrl+H` ショートカット
* 検索文字列と置換文字列の入力
* `str.count()` による置換件数の取得
* `str.replace()` による全文置換
* 対象文字列が存在しない場合のメッセージ表示
* 空文字への置換による文字列削除
* 置換後の変更状態をタイトルバーの `*` に反映

---

## Linux環境での注意

pip版PySide6は独自のQtライブラリを使用するため、
システム側のFcitx5 Qt6入力プラグインと互換性がない場合があります。

その場合、PySide6アプリ内で日本語IME入力が利用できないことがあります。

---

## ライセンス

このプロジェクトは MIT License のもとで公開しています。
詳細は [LICENSE](./LICENSE) を参照してください。
