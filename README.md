# PySide6 Notepad

PySide6 と Qt Designer を使用して作成した、学習用のシンプルなメモ帳アプリケーションです。

PythonによるGUIアプリケーション開発の学習を目的として作成しており、ファイル操作やQtのイベント処理などを段階的に実装しています。

---

## Version 2.0

Version 2.0では、一般的なテキストエディタと同様の「未保存データ管理」を実装しました。

### 主な機能

* 新規作成
* ファイルを開く
* 上書き保存
* 名前を付けて保存
* 終了
* 編集状態をタイトルバーに「*」で表示
* 新規作成時の保存確認
* ファイルを開く前の保存確認
* 終了時の保存確認
* UTF-8テキストファイル対応
* エラーダイアログ表示

---

## スクリーンショット

Version 1.0 の実行画面です
![Main Window](images/mainwindow.png)

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

## Version 2.0で学習した内容

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

## 今後の予定（Version 3.0）

* Undo
* Redo
* Cut
* Copy
* Paste

さらに機能を追加しながら、実用的なGUIアプリケーションへ発展させていく予定です。

---

## ライセンス

MIT License
