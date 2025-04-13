import os
import shutil
import subprocess
from deep_translator import GoogleTranslator
import yt_dlp
import whisper

# Whisperモデル初期化（openai/whisper使用）
whisper_model = whisper.load_model("medium")

# 言語オプション：Whisper用とDeepTranslator用を分けて管理
LANGUAGE_MAP = {
    "1": {"label": "英語", "whisper": "en", "translator": "en"},
    "2": {"label": "中国語・簡体字", "whisper": "zh", "translator": "zh-CN"},
    "3": {"label": "中国語・繁体字（台湾）", "whisper": "zh", "translator": "zh-TW"},
    "4": {"label": "韓国語", "whisper": "ko", "translator": "ko"},
    "5": {"label": "インドネシア語", "whisper": "id", "translator": "id"},
}

# YouTubeから音声ダウンロード（mp3を生成）
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

# mp3 → wav 変換（ffmpeg使用）
def convert_mp3_to_wav(mp3_path, wav_path):
    if os.path.exists(wav_path):
        os.remove(wav_path)
    subprocess.run(["ffmpeg", "-y", "-i", mp3_path, "-filter:a", "loudnorm", wav_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

# ffmpegでWAVを再エンコード（形式修正）
def reencode_wav(input_path, output_path):
    if os.path.exists(output_path):
        os.remove(output_path)
    subprocess.run(["ffmpeg", "-y", "-i", input_path, "-acodec", "pcm_s16le", "-ar", "44100", output_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

# Demucs CLIでボーカル抽出（CLIで安定動作）
def run_demucs_cli(input_path):
    # venv配下のdemucs.exeを明示的に指定
    demucs_path = os.path.join("venv", "Scripts", "demucs.exe")
    if not os.path.exists(demucs_path):
        raise RuntimeError(f"❌ demucs 実行ファイルが見つかりません: {demucs_path}")

    subprocess.run([
        demucs_path,
        "-n", "htdemucs",
        "--two-stems", "vocals",
        input_path
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    return os.path.join("separated", "htdemucs", os.path.splitext(os.path.basename(input_path))[0], "vocals.wav")

# ffmpegでノイズ除去（afftdnフィルター使用）
def reduce_noise(input_wav_path, output_wav_path):
    if os.path.exists(output_wav_path):
        os.remove(output_wav_path)
    subprocess.run(["ffmpeg", "-y", "-i", input_wav_path, "-af", "afftdn", output_wav_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

# Whisper用に再エンコード
def reencode_for_whisper(input_path, output_path="whisper_ready.wav"):
    if os.path.exists(output_path):
        os.remove(output_path)
    subprocess.run([
        "ffmpeg", "-y", "-i", input_path,
        "-acodec", "pcm_s16le",
        "-ar", "16000",
        "-ac", "1",
        output_path
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return output_path

# Whisperで音声認識
def transcribe_audio(wav_path, whisper_lang):
    result = whisper_model.transcribe(wav_path, language=whisper_lang)
    return result["text"]

# DeepTranslatorで翻訳
def translate_text(text, translator_lang):
    return GoogleTranslator(source=translator_lang, target='ja').translate(text)

# 整形処理（句点や記号で分割）
def format_text(text):
    for p in ["。", "？", "！", "!", "?", "\n"]:
        text = text.replace(p, p + "\n")
    return text.strip()

# ログ保存
def save_translation_log(video_title, video_url, video_id, zh_text, ja_text, lang_config):
    filename = f"translation_{video_id}.txt"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"🎬 タイトル: {video_title}\n")
        f.write(f"🔗 URL: {video_url}\n\n")
        f.write("🔈 音声認識結果:\n")
        f.write(format_text(zh_text) + "\n\n")
        f.write(f"🌐 {lang_config['label']} ⇒ 日本語訳:\n")
        f.write(format_text(ja_text) + "\n")
    print(f"\n✅ 結果を {filename} に保存しました。")

# --- メイン実行 ---
if __name__ == "__main__":
    # 使用するデバイス（CPU/GPU）を表示
    print("Device set to use:", whisper_model.device)

    # ユーザーに YouTube Shorts の URL を入力してもらう
    video_url = input("🎞 YouTubeショートのURLを入力してください: ").strip()

    # 言語選択（英語 / 中国語 / 台湾語）
    print("\n🌍 翻訳元の言語を選択してください：")
    for key, val in LANGUAGE_MAP.items():
        print(f"{key}. {val['label']}（{val['translator']}）")
    lang_num = input("番号を入力（1〜3）: ").strip()

    lang_config = LANGUAGE_MAP.get(lang_num)
    if not lang_config:
        print("❌ 無効な選択です。終了します。")
        exit(1)

    # 一時ファイル名を定義
    mp3_file = "shorts_audio.mp3"
    wav_file = "shorts_audio.wav"
    clean_wav_file = "shorts_audio_clean.wav"
    vocals_file = "vocals.wav"
    denoised_file = "vocals_denoised.wav"

    # 動画の音声をダウンロードし、mp3 を取得
    title, url, video_id = download_audio(video_url)

    # mp3 → wav に変換
    convert_mp3_to_wav(mp3_file, wav_file)

    # ffmpegで形式を再エンコード（Whisper等が扱いやすいように）
    reencode_wav(wav_file, clean_wav_file)

    # Demucs でボーカル成分のみを抽出
    vocals_path = run_demucs_cli(clean_wav_file)

    # 抽出したボーカル音声にノイズ除去をかける
    reduce_noise(vocals_path, denoised_file)

    # Whisper 用にモノラル・16kHz に再エンコード
    whisper_ready = reencode_for_whisper(denoised_file)

    # Whisper で音声認識を実行
    transcribed = transcribe_audio(whisper_ready, lang_config["whisper"])

    # Google翻訳で日本語に翻訳（DeepTranslator使用）
    translated = translate_text(transcribed, lang_config["translator"])

    # 認識結果と翻訳結果をコンソール出力
    print("\n🔈 音声認識結果（" + lang_config['label'] + "）:\n" + format_text(transcribed))
    print(f"\n🌐 {lang_config['label']} ⇒ 日本語訳:\n" + format_text(translated))

    # ログファイルとして txt に保存
    save_translation_log(title, url, video_id, transcribed, translated, lang_config)

    # 一時ファイル（mp3, wav, vocalsなど）を削除
    for path in [mp3_file, wav_file, clean_wav_file, vocals_file, denoised_file, whisper_ready]:
        if os.path.exists(path):
            os.remove(path)

    # Demucs が生成した 'separated' フォルダも削除
    demucs_output_dir = os.path.join("separated")
    if os.path.exists(demucs_output_dir):
        shutil.rmtree(demucs_output_dir)