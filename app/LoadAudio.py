import whisper
import os
import warnings


warnings.filterwarnings("ignore")
model = whisper.load_model("base")
UPLOAD_FOLDER = 'app/audio_files'
call_file = os.path.join(UPLOAD_FOLDER, "call.txt")

transcriptions = []

def transcrypt_files():
    files = os.listdir(UPLOAD_FOLDER)

    if os.path.exists(call_file):
        os.remove(call_file)

    for file in files:
        if not file.endswith((".wav", ".mp3", ".m4a", ".ogg", ".flac")):
                continue
        audio_path = os.path.join(UPLOAD_FOLDER, file)
        print("Transcribing:", file)
        result = model.transcribe(audio_path, fp16=False)
        print("Done:", file)
        text = result["text"]
        
        with open(call_file, "a", encoding="utf-8") as call_txt:
            text = result["text"]
            call_txt.write(f"\n===== {file} =====\n")
            call_txt.write(text + "\n")


