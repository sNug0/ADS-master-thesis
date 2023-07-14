import os
from string import punctuation

# Specify path containing whisper transcripts in .txt format
path = ""
root = os.path.join(os.getcwd(), path)
# Walk through specified path and files
for path, subdirs, files in os.walk(root):
    for name in files:
        file_path = os.path.join(path, name)
        # Read transcript
        with open(file_path, encoding="utf-8") as f_in:
            transcript = f_in.readline()

        # Remove punctuation
        for p in punctuation:
            transcript = transcript.replace(p, "")

        file_name = os.path.splitext(os.path.basename(file_path))[0]
        # Write cleaned transcript to new file
        with open(f"{file_name}_clean", "w", encoding="utf-8") as f_out:
            f_out.write(transcript)
