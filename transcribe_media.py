import os
import whisper
import json
from tqdm import tqdm
model = whisper.load_model("tiny.en")  
def transcribe_file(file_path):
    """Transcribes an audio/video file using Whisper AI."""
    try:
        result = model.transcribe(file_path)
        return result["text"]
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return None
    
def process_folder(input_folder, output_file):
    """Scans a folder, transcribes media files, and saves the results."""
    transcriptions = {}
    if not os.path.exists(input_folder):
        print(f"Error: The directory '{input_folder}' does not exist.")
        return
    
    media_files = []
    for root, _, files in os.walk(input_folder):
        for file in files:
            if file.lower().endswith((".mp3", ".mp4", ".wav", ".m4a", ".aac")):
                media_files.append(os.path.join(root, file))

    if not media_files:
        print(" No audio or video files found in the directory.")
        return

    print(f"Found {len(media_files)} media file(s). Starting transcription...")
    for file_path in tqdm(media_files, desc="Transcribing files"):
        print(f"Processing: {file_path}")
        transcription = transcribe_file(file_path)
        if transcription:
            transcriptions[file_path] = transcription
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(transcriptions, f, indent=4, ensure_ascii=False)

    print(f"\n Transcriptions saved to: {output_file}")

if __name__ == "__main__":
    input_folder = r"D:\media_files"  
    output_file = os.path.join(input_folder, "transcriptions.json")  

    process_folder(input_folder, output_file)
