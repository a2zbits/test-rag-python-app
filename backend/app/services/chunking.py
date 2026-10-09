import re

_CONTROL_CHARS = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f￾￿]")
_HYPHEN_BREAK = re.compile(r"(\w)-\n(\w)")
_PARAGRAPH_BREAK = re.compile(r"\n\s*\n")
_WHITESPACE = re.compile(r"\s+")


def clean_text(text: str) -> str:
    """Remove obvious PDF extraction artifacts; keep paragraph breaks."""
    text = _CONTROL_CHARS.sub("", text.replace("\r\n", "\n").replace("\r", "\n"))
    text = text.replace("­", "").replace(" ", " ")
    text = _HYPHEN_BREAK.sub(r"\1\2", text)
    paragraphs = (_WHITESPACE.sub(" ", p).strip() for p in _PARAGRAPH_BREAK.split(text))
    return "\n\n".join(p for p in paragraphs if p)


def chunk_text(text: str, chunk_size: int, chunk_overlap: int) -> list[str]:
    """Deterministic character-based chunking that prefers breaking at spaces."""
    if chunk_size <= 0:
        raise ValueError("chunk_size must be positive")
    if not 0 <= chunk_overlap < chunk_size:
        raise ValueError("chunk_overlap must be >= 0 and < chunk_size")

    text = text.strip()
    if len(text) <= chunk_size:
        return [text] if text else []

    chunks: list[str] = []
    start = 0
    while start < len(text):
        end = min(start + chunk_size, len(text))
        if end < len(text):
            min_end = start + max(chunk_overlap + 1, chunk_size // 2)
            space = text.rfind(" ", min_end, end)
            if space != -1:
                end = space
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        if end >= len(text):
            break
        start = end - chunk_overlap
        space = text.find(" ", start, end)
        if space != -1:
            start = space + 1
    return chunks
