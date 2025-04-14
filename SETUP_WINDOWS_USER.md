# 🎬 YouTubeショート自動翻訳ツールの導入手順（Windows）

## 🎯 このツールでできること
YouTubeショートの音声を自動で文字起こしし、日本語に翻訳して、テキストファイルとして保存します。

---

## ✅ ステップ0：準備

| 必要なもの | 用途 | ダウンロード先 |
|------------|------|----------------|
| Python（3.10〜3.13） | ツールを動かすため | https://www.python.org/downloads/ |
| FFmpeg | 音声変換・ノイズ除去 | https://ffmpeg.org/download.html |
| Git | Whisperライブラリのインストールに必要 | https://git-scm.com/ |

---

## 🧩 ステップ1：コードの取得

### ZIPで取得する場合（初心者向け）

1. リポジトリページを開く  
   👉 https://github.com/torachanmeow/translate-youtube-short

2. 緑の「Code」ボタン → 「Download ZIP」

3. ダウンロードしたZIPファイルを右クリック → 「すべて展開」

### Gitで取得する場合（Git導入済の方）

```bash
git clone https://github.com/torachanmeow/translate-youtube-short.git
cd translate-youtube-short
```

---

## 🧪 ステップ2：Python のインストール

1. Python公式サイト：https://www.python.org/downloads/

2. インストール時に「Add Python to PATH」に必ずチェックを入れる

---

## 🎧 ステップ3：FFmpeg のインストールとパス設定

1. https://www.gyan.dev/ffmpeg/builds/ より `ffmpeg-release-essentials.zip` をダウンロード

2. 解凍し、`bin` フォルダのパスをコピー（例：`C:\tools\ffmpeg\bin`）

3. Windowsの環境変数「Path」に追加

---

## 🔧 ステップ4：仮想環境の作成と有効化

1. コマンドプロンプトを開く

2. 展開またはクローンしたフォルダに移動

```bash
cd パス\translate-youtube-short-main
```

3. 仮想環境を作成して有効化

```bash
python -m venv venv
venv\Scripts\activate
```

---

## 📦 ステップ5：依存ライブラリのインストール（※初回のみ）

初回のみ、必要なライブラリをインストールします

```bash
python -m pip install --upgrade pip
pip install --no-cache-dir -r requirements.txt
```
> 💡 venv に含まれる pip は古い場合があります。最新版にアップデートしておくことで、依存関係の問題やエラーを防げます。

> ⚠️ `openai-whisper` は GitHub から直接インストールされるため、Git が必須です。

---

## 🚀 ステップ6：ツールの実行

```bash
python translate_youtube_short.py
```

もしくは、以下の `run.bat` をダブルクリックして実行することもできます。

---

## 🟢 Windows向け：run.bat での簡単起動

仮想環境を構築済であれば、`run.bat` をダブルクリックするだけで翻訳ツールを実行できます。

```bat
@echo off
setlocal

if not exist "venv\Scripts\activate.bat" (
    echo [ERROR] Python virtual environment not found.
    echo Please follow these setup steps first:
    echo   1. python -m venv venv
    echo   2. venv\Scripts\activate.bat
    echo   3. pip install -r requirements.txt
    pause
    exit /b
)

call venv\Scripts\activate.bat
python translate_youtube_short.py
pause
```

> 仮想環境を作成していない場合は、先にステップ4～5を実行してください。

---

## 💬 補足・トラブル時の対応

- `ffmpeg` や `python` のインストール・パス設定が正しくない場合、音声抽出に失敗します
- `venv`（仮想環境） を有効にせずに `python` を実行すると、モジュールが見つからない場合があります
- `git` がインストールされていないと `openai-whisper` のインストールに失敗します