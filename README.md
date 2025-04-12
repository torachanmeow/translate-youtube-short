# 🎧 YouTube Shorts 字幕翻訳ツール（Whisper + DeepTranslator）

YouTubeショート動画の音声を自動で文字起こしし、日本語に翻訳するツールです。  
Whisper による高精度の音声認識と、Deep Translator（Google翻訳）による翻訳を組み合わせ、簡単にテキストログを生成します。

---

## ✅ 主な特徴

- 🎙 OpenAI Whisper（`openai/whisper-medium`）で高精度な音声文字起こし
- 🌐 Deep Translator（Google翻訳）で日本語に即時翻訳
- 📄 出力結果は `translation_<動画ID>.txt` に自動保存
- 🧹 MP3/WAV は一時ファイルとして削除され、キャッシュが残りません
- 🖥 CLIベースでシンプル、翻訳元言語を選択可能（英語・中国語・台湾語）

---

## 🧩 動作環境

- Python：3.10〜3.13（3.13対応確認済み）
- `ffmpeg` コマンドが利用可能であること（音声変換に使用）
💡 ffmpeg の導入については [公式サイト](https://ffmpeg.org/download.html) を参照してください。

---

## 📦 インストール手順

仮想環境の使用は任意です。以下のコマンドで必要なライブラリを一括インストールできます：

```bash
pip install --no-cache-dir \
  yt-dlp \
  transformers \
  deep-translator \
  git+https://github.com/openai/whisper.git
```

または、`requirements.txt` を使う場合は以下のように実行します：

```bash
pip install --no-cache-dir -r requirements.txt
```

---

## 🚀 使い方

```bash
python translate_youtube_short.py
```

実行すると、以下のように対話形式で進行します：

1. 🎞 **YouTube Shorts のURL** を入力  
2. 🌍 **翻訳元の言語** を以下から番号で選択  
   ```
   1. 英語（en）
   2. 中国語・簡体字（zh）
   3. 中国語・繁体字（zh-TW）
   ```

3. 自動で以下の処理を実施：
   - 音声ダウンロード（MP3）
   - WAV変換（FFmpeg）
   - Whisperによる音声認識
   - Deep Translatorによる日本語翻訳
   - 翻訳ログ（`translation_<動画ID>.txt`）の保存
   - 一時ファイル（mp3/wav）の削除

---

## 📁 出力ファイル例

```
translation_xaA_hQ4EDE0.txt
├─ 🎬 タイトル: ショート動画のタイトル
├─ 🔗 URL: ショート動画のURL
├─ 🔈 音声認識結果:
├─ 🌐 日本語訳:
```

---

## ⚖ ライセンス・利用について

このツールは**個人利用またはクローズドな用途**を想定しています。  
コードは MIT ライセンスに準拠しており、自由に利用・改変可能ですが、**翻訳結果の再配布や商用利用における責任は一切負いません**。

> Whisperモデルや翻訳エンジンの仕様変更により、将来的に動作しなくなる可能性もあります。

---

## 🙋‍♂️ 備考

- Whisperモデルはローカル実行されますが、翻訳はインターネット接続が必要です（Google翻訳APIを内部で使用）
- 長尺の動画には非対応です（ショート動画専用）

---