import fitz
import re


def clean_page_text(text):

    # Remove excessive dots
    text = re.sub(r"\.{2,}", " ", text)

    # Remove multiple newlines
    text = re.sub(r"\n+", "\n", text)

    # Remove excessive spaces
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def is_noisy_page(text):

    lower = text.lower()

    bad_keywords = [
        "contents",
        "bibliographical",
        "historical remarks"
    ]

    if any(k in lower for k in bad_keywords):
        return True

    # Too many dots usually means TOC
    if text.count(".") > 30:
        return True

    return False


def extract_text_from_pdf(pdf_path):

    doc = fitz.open(pdf_path)

    clean_pages = []

    for page_num, page in enumerate(doc):

        text = page.get_text("text")

        text = clean_page_text(text)

        # Skip empty pages
        if len(text) < 200:
            continue

        # Skip noisy pages
        if is_noisy_page(text):
            continue

        clean_pages.append(text)

    return clean_pages