import re

from langdetect import detect


def process_text(text: str):
    cleaned_text = re.sub(r"[^:(),.!?“”\'\w\s]", "", text)
    word_count = len(cleaned_text.split())
    language = detect(text)

    return {
        "processed_text": cleaned_text,
        "word_count": word_count,
        "language": language,
    }
