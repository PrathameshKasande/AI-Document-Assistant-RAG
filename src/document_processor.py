import os
import pymupdf

from langchain_core.documents import Document

from src.text_cleaner import clean_text
from src.logger import get_logger


logger = get_logger(__name__)


def extract_pdf_text(file_path):
    """
    Extract text from a PDF file page-by-page.

    Each PDF page is converted into a LangChain Document
    with useful metadata for downstream chunking and retrieval.
    """

    documents = []

    file_name = os.path.basename(file_path)

    try:
        # Open PDF using the new PyMuPDF API
        pdf = pymupdf.open(file_path)

        logger.info(
            "Processing PDF: %s | Total pages: %s",
            file_name,
            len(pdf)
        )

        for page_number in range(len(pdf)):

            page = pdf.load_page(page_number)

            # Extract text from the page
            text = page.get_text("text")

            # Clean extracted text
            text = clean_text(text)

            # Skip empty pages
            if not text:
                logger.warning(
                    "Empty page skipped: %s | Page: %s",
                    file_name,
                    page_number + 1
                )
                continue

            # Create LangChain document
            document = Document(
                page_content=text,
                metadata={
                    "source": file_name,
                    "page": page_number + 1,
                    "document_type": "pdf",
                    "file_name": file_name
                }
            )

            documents.append(document)

        # Close PDF
        pdf.close()

        logger.info(
            "Text extraction completed: %s | Pages extracted: %s",
            file_name,
            len(documents)
        )

        return documents

    except Exception as error:

        logger.error(
            "PDF extraction failed for %s: %s",
            file_name,
            error
        )

        raise