import pymupdf as fitz


def extract_section_title(text: str) -> str:
    """
    Attempts to identify a section/chapter title from the beginning
    of a page's text.
    """

    lines = [line.strip() for line in text.splitlines() if line.strip()]

    if not lines:
        return ""

    first_line = lines[0]

    # Common heading patterns
    heading_keywords = [
        "chapter",
        "section",
        "topic",
        "unit",
    ]

    first_line_lower = first_line.lower()

    # Example:
    # Chapter 1: Compound Interest
    # Section 2: Geometry
    # Unit 3: Algebra
    for keyword in heading_keywords:
        if first_line_lower.startswith(keyword):
            return first_line

    # Numbered headings such as:
    # 1. Compound Interest
    # 2. Geometry and Trigonometry
    if len(first_line) > 2:
        if first_line[0].isdigit() and "." in first_line[:4]:
            return first_line

    return ""


def extract_text_by_page(file_path: str) -> list[dict]:
    """
    Extracts text from a PDF, page by page.

    Returns:
    [
        {
            "page_number": 1,
            "text": "...",
            "section_title": "Chapter 1: Compound Interest"
        },
        ...
    ]

    Pages with no extractable text are skipped.
    """

    pages_data = []

    with fitz.open(file_path) as doc:
        current_section_title = ""

        for page in doc:
            text = page.get_text().strip()

            if not text:
                continue

            detected_section = extract_section_title(text)

            if detected_section:
                current_section_title = detected_section

            pages_data.append({
                "page_number": page.number + 1,
                "text": text,
                "section_title": current_section_title,
            })

    return pages_data