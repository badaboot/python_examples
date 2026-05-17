import whisper
import sys

# python3 test_whisper.py 'audio/your_audio_file.mp3'
print(f"Received: {sys.argv[0]} file_path {sys.argv[1]}")
if len(sys.argv) < 2:
    print("Usage: python script.py <mp3_file_path>")
    sys.exit(1)

model = whisper.load_model("small")  # tiny, base, small, medium, large
# Set the initial_prompt here
prompt_text = "以下是普通话的句子."

actual_result = model.transcribe(sys.argv[1], initial_prompt=prompt_text, language='zh', fp16=False) # FP16 is not supported on CPU
print(actual_result["text"])
