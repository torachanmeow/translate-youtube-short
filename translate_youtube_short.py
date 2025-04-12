import os
import subprocess
from transformers import pipeline
from deep_translator import GoogleTranslator
import yt_dlp

# 言語オプション：Whisper用とDeepTranslator用を分けて管理
LANGUAGE_MAP = {
    "1": {"label": "英語", "whisper": "english", "translator": "en"},
    "2": {"label": "中国語・簡体字", "whisper": "chinese", "translator": "zh"},
    "3": {"label": "中国語・繁体字（台湾）", "whisper": "chinese", "translator": "zh-TW"},
}

# Whisperモデル初期化
whisper_pipe = pipeline(
    task="automatic-speech-recognition",
    model="openai/whisper-medium",
    device="cpu"
)

# Step 1: YouTubeから音声ダウンロード（mp3を生成）
def download_audio(video_url, output_basename="shorts_audio"):
    mp3_path = output_basename + ".mp3"
    if os.path.exists(mp3_path):
        os.remove(mp3_path)

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': output_basename,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(video_url, download=True)
        return info_dict.get("title", "No Title"), video_url, info_dict.get("id", "noid")

# Step 2: mp3 → wav 変換（ffmpeg使用）
def convert_mp3_to_wav(mp3_path, wav_path):
    if os.path.exists(wav_path):
        os.remove(wav_path)

    subprocess.run([
        "ffmpeg", "-y", "-i", mp3_path, wav_path
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

# Step 3: Whisperで音声認識
def transcribe_audio(wav_path, whisper_lang):
    result = whisper_pipe(
        wav_path,
        generate_kwargs={"language": whisper_lang},
        return_timestamps=True
    )
    return result["text"]

# Step 4: DeepTranslatorで翻訳
def translate_text(text, translator_lang):
    return GoogleTranslator(source=translator_lang, target='ja').translate(text)

# Step 5: 整形処理（句点や記号で分割）
def format_text(text):
    for p in ["。", "？", "！", "!", "?", "\n"]:
        text = text.replace(p, p + "\n")
    return text.strip()

# Step 6: ログ保存
def save_translation_log(video_title, video_url, video_id, zh_text, ja_text):
    filename = f"translation_{video_id}.txt"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"🎬 タイトル: {video_title}\n")
        f.write(f"🔗 URL: {video_url}\n\n")
        f.write("🔈 音声認識結果:\n")
        f.write(format_text(zh_text) + "\n\n")
        f.write("🌐 日本語訳:\n")
        f.write(format_text(ja_text) + "\n")
    print(f"\n✅ 結果を {filename} に保存しました。")

# --- メイン実行 ---
if __name__ == "__main__":
    print("Device set to use:", whisper_pipe.device)

    video_url = input("🎞 YouTubeショートのURLを入力してください: ").strip()

    print("\n🌍 翻訳元の言語を選択してください：")
    for key, val in LANGUAGE_MAP.items():
        print(f"{key}. {val['label']}（{val['translator']}）")
    lang_num = input("番号を入力（1〜3）: ").strip()

    lang_config = LANGUAGE_MAP.get(lang_num)
    if not lang_config:
        print("❌ 無効な選択です。終了します。")
        exit(1)

    mp3_file = "shorts_audio.mp3"
    wav_file = "shorts_audio.wav"

    # 音声・動画情報の取得と変換
    title, url, video_id = download_audio(video_url)
    convert_mp3_to_wav(mp3_file, wav_file)

    # Whisperで音声認識（言語指定）
    transcribed = transcribe_audio(wav_file, lang_config["whisper"])

    # 翻訳
    translated = translate_text(transcribed, lang_config["translator"])

    # 結果出力
    print("\n🔈 音声認識結果（元言語）:\n" + format_text(transcribed))
    print("\n🌐 日本語訳:\n" + format_text(translated))

    # ログ保存
    save_translation_log(title, url, video_id, transcribed, translated)

    # 一時ファイル削除
    if os.path.exists(mp3_file):
        os.remove(mp3_file)
    if os.path.exists(wav_file):
        os.remove(wav_file)