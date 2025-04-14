# 🎬 YouTubeショート自動翻訳ツールの導入手順（Windows）

## 🎯 このツールでできること
YouTubeショートの音声を自動で文字起こしし、日本語に翻訳して、テキストファイルとして保存します。

---

## ✅ ステップ0：準備

| 必要なもの | 用途 | ダウンロード先 |
|------------|------|----------------|
| Python（3.10〜3.13） | ツールを動かすため | https://www.python.org/downloads/ |
| FFmpeg | 音声変換・ノイズ除去 | https://ffmpeg.org/download.html |
| Git（任意） | Gitクローンで取得する場合 | https://git-scm.com/ |

---

## 🧩 ステップ1：コードの取得

### ZIPで取得する場合（初心者向け）

1. リポジトリページを開く  
   👉 [https://github.com/torachanmeow/translate-youtube-short](https://github.com/torachanmeow/translate-youtube-short)

2. 緑の「Code」ボタン → 「Download ZIP」

3. ダウンロードしたZIPファイルを右クリック → 「すべて展開」

### Gitで取得する場合（Git導入済の方）

コマンドプロンプトまたはPowerShellで次を実行：

```bash
git clone https://github.com/torachanmeow/translate-youtube-short.git
cd translate-youtube-short
```

---

## 🧪 ステップ2：Python のインストール

1. Python公式サイト：[https://www.python.org/downloads/](https://www.python.org/downloads/)

2. インストール時に「Add Python to PATH」に必ずチェックを入れる

---

## 🎧 ステップ3：FFmpeg のインストールとパス設定

1. [https://www.gyan.dev/ffmpeg/builds/](https://www.gyan.dev/ffmpeg/builds/) より `ffmpeg-release-essentials.zip` をダウンロード

2. 解凍し、`bin` フォルダのパスをコピー（例：`C:\tools\ffmpeg\bin`）

3. Windowsの環境変数「Path」に追加

---

## 🔧 ステップ4：仮想環境の作成と有効化

1. コマンドプロンプトを開く

2. 展開またはクローンしたフォルダに移動：

```bash
cd パス\translate-youtube-short-main  # ZIP展開時の例
```

3. 仮想環境を作成して有効化：

```bash
python -m venv venv
venv\Scripts\activate
```

---

## 📦 ステップ5：依存ライブラリのインストール（※初回のみ）

初回のみ、必要なライブラリをインストールします：

```bash
pip install --no-cache-dir -r requirements.txt
```

---

## 🚀 ステップ6：ツールの実行

```bash
python translate_youtube_short.py
```

実行すると、対話形式で次の入力が求められます：

1. YouTube Shorts のURL  
2. 翻訳元の言語（番号で選択）

翻訳結果は `translation_<動画ID>.txt` に保存されます。

---

## 💬 補足・トラブル時の対応

- **FFmpeg や Python が正しくインストール・設定されていない場合**、ツールは正しく動作しません
- 特に、`ffmpeg.exe` のパスが環境変数 `Path` に通っていないとエラーになります
- `venv`（仮想環境）を有効にしてから実行しないと、必要なライブラリが見つからず失敗します