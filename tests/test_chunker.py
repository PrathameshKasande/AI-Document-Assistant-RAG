from langchain_core.documents import Document

from src.chunker import create_chunks


def test_create_chunks():

    document = Document(

        page_content=(
            "Machine Learning is useful for "
            "data analysis and prediction. "
            * 100
        ),

        metadata={
            "source": "test.pdf",
            "page": 1
        }

    )

    chunks = create_chunks(
        [document]
    )

    assert len(chunks) > 0


def test_chunk_has_metadata():

    document = Document(

        page_content=(
            "Artificial Intelligence is a "
            "branch of computer science."
        ),

        metadata={
            "source": "ai.pdf",
            "page": 1
        }

    )

    chunks = create_chunks(
        [document]
    )

    assert "chunk_id" in chunks[0].metadata

    assert chunks[0].metadata["source"] == "ai.pdf"

    assert chunks[0].metadata["page"] == 1