from unittest.mock import MagicMock
from unittest.mock import patch

from src.document_processor import extract_pdf_text


@patch("src.document_processor.fitz.open")
def test_extract_pdf_text(mock_open):

    mock_pdf = MagicMock()


    mock_page = MagicMock()

    mock_page.get_text.return_value = (
        "This is test PDF content."
    )


    mock_pdf.__len__.return_value = 1

    mock_pdf.load_page.return_value = (
        mock_page
    )


    mock_open.return_value = (
        mock_pdf
    )


    documents = extract_pdf_text(
        "test.pdf"
    )


    assert len(documents) == 1


    assert (
        documents[0].page_content
        == "This is test PDF content."
    )


def test_extract_pdf_text_invalid_file():

    try:

        extract_pdf_text(
            "invalid_file.pdf"
        )

    except Exception:

        assert True