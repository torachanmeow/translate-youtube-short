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
- `ffmpeg`：インストール済でパスが通っていること -- 💡 ffmpeg の導入については [公式サイト](https://ffmpeg.org/download.html) を参照してください。
- `demucs`：仮想環境内にインストール済であること（venv/Scripts/demucs.exe）

> ✅ **仮想環境（venv）前提での運用を推奨します。**  
> `demucs` 実行は `venv/Scripts/demucs.exe` を明示的に使用します。

---

## 📦 セットアップ手順

### 1. 仮想環境の作成と有効化

```bash
python -m venv venv
venv\Scripts\activate    # Windows の場合
```

### 2. 依存パッケージのインストール

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
   4. 韓国語（ko）
   5. インドネシア語（id）
   ```

3. 自動で以下の処理を実施：

   - YouTube音声を `.mp3` でダウンロード
   - `.wav` に変換（音量正規化）
   - Demucs によりセリフ音声だけを分離
   - FFmpeg によるノイズ除去
   - Whisper が文字起こし（`openai/whisper-medium` モデル使用）
   - DeepTranslator による日本語翻訳
   - 結果ログを `translation_<動画ID>.txt` に保存
   - 中間ファイルを削除（MP3 / WAV）

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

## 🔧 言語設定のカスタマイズについて

本ツールでは、`translate_youtube_short.py` 内の `LANGUAGE_MAP` を編集することで、翻訳元の言語を自由に追加・変更できます。

```python
LANGUAGE_MAP = {
    "1": {"label": "英語", "whisper": "en", "translator": "en"},
    "2": {"label": "中国語・簡体字", "whisper": "zh", "translator": "zh-CN"},
    "3": {"label": "中国語・繁体字（台湾）", "whisper": "zh", "translator": "zh-TW"},
    "4": {"label": "韓国語", "whisper": "ko", "translator": "ko"},
    "5": {"label": "インドネシア語", "whisper": "id", "translator": "id"},
}
```

- `label`: ユーザーに表示する言語名
- `whisper`: Whisper に渡す言語コード（ISO 639-1 準拠）
- `translator`: Deep Translator に渡す翻訳用の言語コード

> ✅ これにより、**スペイン語・ヒンディー語・ロシア語・ベトナム語**なども容易に追加できます。

---

## ⚖ ライセンス・利用について

このツールは MIT ライセンスのもとで公開されています。  
**個人利用または非商用のクローズド用途**を想定しており、自由に改変・再配布が可能です。

ただし、本ツールは以下の外部OSSライブラリに依存しており、それぞれに独自のライセンスが適用されます：

- [`openai/whisper`](https://github.com/openai/whisper)（MIT）
- [`yt-dlp`](https://github.com/yt-dlp/yt-dlp)（Unlicense）
- [`deep-translator`](https://github.com/nidhaloff/deep-translator)（MIT）※ Google翻訳の非公式ラッパーを使用
- [`demucs`](https://github.com/facebookresearch/demucs)（MIT）
- [`ffmpeg`](https://ffmpeg.org/)（LGPL/GPL）

> ⚠️ **注意**：翻訳処理には Deep Translator による Google 翻訳の Web ラッパーが使われています。  
> Google が提供する正式な API を利用しているわけではなく、商用・大量翻訳などに利用する場合は、  
> Google の[利用規約](https://policies.google.com/terms?hl=ja)に反しないよう十分ご注意ください。

## 🙋‍♂️ 備考

- Whisperモデルはローカルで実行され、APIキー等は不要です
- 翻訳にはインターネット接続が必要です（DeepTranslator が Google翻訳へアクセス）
- 長尺動画や非ショート動画は処理対象外です（1分程度推奨）