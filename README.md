詳しいセットアップ手順については [SETUP_WINDOWS_USER.md](./SETUP_WINDOWS_USER.md) をご覧ください。

# 🎧 YouTube Shorts 字幕翻訳ツール（Whisper + DeepTranslator）

YouTubeショート動画の音声を自動で文字起こしし、日本語に翻訳するツールです。  
Whisper による高精度の音声認識と、Deep Translator（Google翻訳）による翻訳を組み合わせ、簡単にテキストログを生成します。  
Google翻訳は翻訳精度が不十分な場合もあるため、**生成AI（ChatGPTなど）に直接貼り付けて翻訳を依頼できるプロンプトもログ内に付属**しています。

---

## ✅ 主な特徴

- 🎙 OpenAI Whisper（`openai/whisper`）公式実装で高精度な音声文字起こし
- 🔊 Demucs によるボーカル抽出機能（背景音を除去しセリフ抽出）
- ✨ FFmpeg によるノイズ除去 + 再エンコードで Whisper に最適化
- 🌐 Deep Translator（Google翻訳）で日本語に即時翻訳
- 📄 出力結果は `translation_<動画ID>.txt` に自動保存
- 🧹 一時ファイル（MP3/WAV）は自動削除、キャッシュ不要
- 🖥 CLIベースでシンプル、翻訳元言語を選択可能（英語・中国語・台湾語 etc...）

---

## 🧩 動作環境

- Python：3.10 ～ 3.13（3.13動作確認済み）
- `ffmpeg`：インストール済でパスが通っていること（[公式サイト](https://ffmpeg.org/download.html) 参照）
- `demucs`：仮想環境内にインストールされていること（`venv/Scripts/demucs.exe`）

> ✅ **仮想環境（venv）前提での運用を推奨します。**  
> `demucs` 実行は `venv/Scripts/demucs.exe` を明示的に使用します。

---

## 🚀 使い方

```bash
python translate_youtube_short.py
```

実行後、以下の対話が表示されます：

1. 🎞 **YouTube Shorts のURL** を入力  
2. 🌍 **翻訳元の言語** を番号で選択  
3. 文字起こし・翻訳処理が自動で進行し、`translation_<動画ID>.txt` に保存されます。

---

## 📁 出力ファイル例

```
translation_<動画ID>.txt
├─ 🎬 タイトル: ショート動画のタイトル
├─ 🔗 URL: ショート動画のURL
├─ 🔈 音声認識結果:
├─ 🌐 日本語訳:
├─ 📄 生成AI用プロンプト:
│   ├─ ChatGPTなどに貼り付けるための翻訳指示テンプレート
│   ├─ 原文テキストを再掲
│   └─ 貼り付け対象範囲を明示（点線より下）
```

---

## 🔧 言語設定のカスタマイズ

`translate_youtube_short.py` 内の `LANGUAGE_MAP` を編集することで、翻訳対象言語を自由に追加できます。

```python
LANGUAGE_MAP = {
    "1": {"label": "英語", "whisper": "en", "translator": "en"},
    "2": {"label": "中国語・簡体字", "whisper": "zh", "translator": "zh-CN"},
    "3": {"label": "中国語・繁体字（台湾）", "whisper": "zh", "translator": "zh-TW"},
    "4": {"label": "韓国語", "whisper": "ko", "translator": "ko"},
    "5": {"label": "インドネシア語", "whisper": "id", "translator": "id"},
}
```

---

## ⚖ ライセンス・利用について

このツールは MIT ライセンスです（個人・非商用利用向け）。  
以下のOSSに依存しています：

- [`openai/whisper`](https://github.com/openai/whisper)
- [`yt-dlp`](https://github.com/yt-dlp/yt-dlp)
- [`deep-translator`](https://github.com/nidhaloff/deep-translator)
- [`demucs`](https://github.com/facebookresearch/demucs)
- [`ffmpeg`](https://ffmpeg.org/)

> ⚠️ Deep Translator は Google翻訳のWebラッパーを使用しています。商用利用には注意してください。

---

## 🙋‍♂️ 備考

- Whisperはローカル実行でAPIキー不要
- 翻訳処理にはインターネット接続が必要
- 長尺や通常のYouTube動画は対象外（ショート推奨）