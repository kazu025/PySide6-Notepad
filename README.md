# PySide6 Notepad

PySide6 と Qt Designer を使用して作成した、学習用のシンプルなメモ帳アプリケーションです。

PythonによるGUIアプリケーション開発を学ぶことを目的として、機能を段階的に追加しながら開発しています。

---

## Version 7.0

最近使ったファイル（MRU）機能を追加しました。

QSettingsを利用してファイル履歴を保存し、
アプリを再起動しても履歴を保持します。

### 追加した機能

- 最近使ったファイル（MRU）
- 最近使ったファイルの履歴保存
- アプリ再起動後も履歴を保持
- 履歴からファイルを開く
- 履歴をクリア
- 存在しないファイルを自動的に履歴から削除

---

## 現在の機能

- ✅ ファイルの新規作成
- ✅ 開く
- ✅ 保存
- ✅ 名前を付けて保存
- ✅ 未保存変更の管理
- ✅ Undo / Redo
- ✅ Cut / Copy / Paste
- ✅ Select All
- ✅ 検索（Ctrl+F）
- ✅ 次を検索（F3）
- ✅ ラップアラウンド検索
- ✅ 行番号表示
- ✅ 列番号表示
- ✅ 文字数表示
- ✅ フォント変更
- ✅ フォントサイズ変更
- ✅ 最近使ったファイル（MRU）
- ✅ 履歴の保存
- ✅ 履歴からファイルを開く
- ✅ 履歴をクリア
  
---

## 開発環境

* Python 3.x
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

### Version 7.0

- QSettings
- QMenu
- QAction（動的生成）
- addMenu()
- addSeparator()
- lambda式によるシグナル接続
- 設定情報の永続化

### Version 6.0

- QFontDialog
- QFontDialog.getFont()
- QFont
- QWidget.setFont()
- 現在のフォント取得
- ダイアログのOK／キャンセル判定

### Version 5.0

- QStatusBar
- QStatusBar.showMessage()
- cursorPositionChangedシグナル
- textChangedシグナル
- QTextCursor
- blockNumber()
- positionInBlock()
- ステータスバーの更新

### Version 4.0

- QTextEdit.find()
- QInputDialog
- 検索機能の実装
- ラップアラウンド検索
- QTextCursor

### Version 3.0
- QAction
- triggeredシグナル
- QTextEdit標準編集機能
- ショートカットキーの設定
- Qt Designerとの連携

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

## Version 8.0（予定）

- 文字コード（UTF-8 / Shift_JIS）の選択

---

## バージョン履歴

### Version 1.0
- 新規作成
- 開く
- 保存
- 名前を付けて保存

### Version 2.0
- 未保存変更の管理
- タイトルバーに変更マーク（*）
- 終了時・新規作成時・ファイルを開く前の保存確認

### Version 3.0
- Undo / Redo
- Cut / Copy / Paste
- Select All
- ショートカットキー対応

### Version 4.0
- 検索（Ctrl+F）
- 次を検索（F3）
- ラップアラウンド検索

### Version 5.0

- ステータスバー
- 行番号表示（Line）
- 列番号表示（Column）
- 文字数表示
  
### Version 6.0

- フォント選択ダイアログ
- フォントファミリ変更
- フォントサイズ変更
  
### Version 7.0

- 最近使ったファイル（MRU）
- 履歴の保存
- 履歴からファイルを開く
- 履歴をクリア
- 存在しないファイルの自動削除

## Linux環境での注意

pip版PySide6は独自のQtライブラリを使用するため、
システム側のFcitx5 Qt6入力プラグインと互換性がない場合があります。

その場合、PySide6アプリ内で日本語IME入力が利用できないことがあります。

---

## ライセンス

MIT License
