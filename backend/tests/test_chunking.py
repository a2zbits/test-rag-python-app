import pytest

from app.services.chunking import chunk_text, clean_text


def test_clean_text_fixes_artifacts():
    raw = "Annual  leave is 25\x00 days.\nIt re-\nsets yearly.  \n\n\n  Next   paragraph.\r\n"
    assert clean_text(raw) == "Annual leave is 25 days. It resets yearly.\n\nNext paragraph."


def test_clean_text_blank_input():
    assert clean_text(" \n\x00 \n") == ""


def test_short_text_single_chunk():
    assert chunk_text("hello world", 100, 10) == ["hello world"]
    assert chunk_text("", 100, 10) == []


def test_chunk_size_and_overlap_are_respected():
    text = " ".join(f"w{i}" for i in range(200))
    chunks = chunk_text(text, 100, 20)
    assert len(chunks) > 1
    assert all(len(c) <= 100 for c in chunks)
    # consecutive chunks share overlapping text
    assert all(set(a.split()[-2:]) & set(b.split()) for a, b in zip(chunks, chunks[1:]))
    assert chunk_text(text, 100, 20) == chunks  # deterministic


def test_smaller_size_gives_more_chunks():
    text = " ".join(f"w{i}" for i in range(200))
    assert len(chunk_text(text, 50, 5)) > len(chunk_text(text, 200, 5))


def test_no_overlap_chunks_cover_all_words():
    text = " ".join(f"w{i}" for i in range(100))
    assert " ".join(chunk_text(text, 60, 0)).split() == text.split()


@pytest.mark.parametrize("size,overlap", [(0, 0), (10, 10), (10, -1)])
def test_invalid_config(size, overlap):
    with pytest.raises(ValueError):
        chunk_text("some text here", size, overlap)
