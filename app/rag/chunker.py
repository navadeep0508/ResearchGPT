from langchain_text_splitters import RecursiveCharacterTextSplitter

import re


def is_toc_chunk(chunk):

    # Too many dots = TOC
    if chunk.count(".") > 15:
        return True

    # Many isolated numbers
    numbers = re.findall(r"\b\d+\b", chunk)

    if len(numbers) > 20:
        return True

    # Many short lines
    lines = chunk.split("\n")

    short_lines = [l for l in lines if len(l.strip()) < 30]

    if len(short_lines) > len(lines) * 0.7:
        return True

    return False


def clean_chunks(chunks):

    cleaned = []

    for chunk in chunks:

        chunk = chunk.strip()

        if len(chunk) < 200:
            continue

        if is_toc_chunk(chunk):
            continue

        cleaned.append(chunk)

    return cleaned
def chunk_text(text: str):

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=150
    )

    chunks = text_splitter.split_text(text)

    return clean_chunks(chunks)

def normalize_text(text):

    # Remove excessive newlines
    text = re.sub(r"\n+", "\n", text)

    # Fix spaced letters
    text = re.sub(r"(\b\w)\s+(?=\w\b)", r"\1", text)

    # Remove repeated dots
    text = re.sub(r"\.{2,}", " ", text)

    return text