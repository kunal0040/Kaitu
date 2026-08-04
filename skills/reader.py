import re
import os
from audio import preprocess_text, speak

def chunk_text(text: str, max_chars: int = 350):

    sentences = re.split(r"(?<=[.!?]) +", text)
    chunks = []
    current_chunk = ""

    for sentence in sentences:
        if len(current_chunk) + len(sentence) <= max_chars:
            current_chunk += sentence + " "
        else:
            if current_chunk:
                chunks.append(current_chunk.strip())
            current_chunk = sentence + " "

    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks

def execute_reading(source: str) -> str:

    raw_text = ""

    if os.path.isfile(source):
        try:
            with open(source, "r", encoding="utf-8") as f:
                raw_text = f.read()
        except Exception as e:
            return f"Failed to read file at {source}. Error: {e}"

    else:
        raw_text = source

    if not raw_text.strip():
        return "The provided text source seems empty!"

    cleaned_text = preprocess_text(raw_text)

    chunks = chunk_text(cleaned_text)

    print(f"[READING]: Starting narration of {len(chunks)} chunks...")
    for index, chunk in enumerate(chunks, 1):
        print(f"[Reader Chunk {index}/{len(chunks)}]: {chunk}")
        speak(chunk)

    return "Finished reading the text..."
