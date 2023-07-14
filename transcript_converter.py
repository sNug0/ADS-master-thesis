import pandas as pd
import os
from string import punctuation

# Specify the path to the folder containing the ort files
path = ""
root = os.path.join(os.getcwd(), path)


def parse_ort(file_path):
    # Read the ort file
    with open(file_path, "r", encoding="latin-1") as file:
        lines = file.readlines()
    speakers_text = []
    for i in range(len(lines)):
        line = lines[i]

        if line.startswith('"IntervalTier"'):
            i += 1
            speaker_name = lines[i].strip()
            i += 1
            start_time = float(lines[i])
            i += 1
            end_time = float(lines[i])
            i += 1
            talk_count = int(lines[i])
            i += 1
            for _ in range(talk_count):
                start_time = float(lines[i])
                i += 1
                end_time = float(lines[i])
                i += 1
                text = str(lines[i].strip().replace('"', ""))
                i += 1
                speakers_text.append((speaker_name, start_time, end_time, text))
    return speakers_text


for path, subdirs, files in os.walk(root):
    for name in files:
        file_path = os.path.join(path, name)

        speaker_texts = parse_ort(file_path)
        # Remove empty rows

        filtered_speaker_texts = []

        for item in speaker_texts:
            if item[3].strip():  # Check if the text is not empty or whitespace
                filtered_speaker_texts.append(item)

        # Create the transcript dictionary

        transcript = []

        for item in filtered_speaker_texts:
            transcript.append(
                {"speaker": item[0], "start": item[1], "end": item[2], "text": item[3]}
            )

        # Sort the transcript according to the starting time stamp

        transcript.sort(key=lambda x: x["start"])

        df = pd.DataFrame(
            transcript, columns=["speaker", "start_time", "end_time", "text"]
        )
        file_name = os.path.splitext(os.path.basename(file_path))[0]

        # Remove annotations from transcript
        # TODO convert to function
        def annotation_cleaner(df):
            replace_list = [
                "xxx",
                "ggg",
                "Xxx",
                "*d",
                "*u",
                "*a",
                "*v",
                "*x",
                "*z",
                "*c",
            ]
            for item in replace_list:
                df.replace(item, "", regex=True, inplace=True)
            return df

        df = annotation_cleaner(df)

        # Remove newlines, double quotes, etc. and convert to a single string
        out = (
            " ".join(df["text"])
            .replace("\n", " ")
            .replace("\r", " ")
            .replace('""', "")
            .replace("  ", " ")
            .replace(" .", ".")
        )

        for s in punctuation:
            out = out.replace(s, "")

        # Save string to txt file with same name as ort file
        with open(f"{file_name}.txt", "w", encoding="utf-8") as f:
            f.write(out)
