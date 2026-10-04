    digest = sha256(path)


    document = pymupdf.open(path)


    try:
        for page_number, page in enumerate(document, start=1):
            yield {
                "document": path.name,
                "path": str(path),
                "sha256": digest,
                "page": page_number,
                "text": page.get_text("text"),
            }
    finally:
        document.close()




def features(text: str):
    """
    Lightweight deterministic classification of page contents.
