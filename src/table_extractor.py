import os
import pdfplumber

from langchain_core.documents import Document

from src.logger import get_logger


logger = get_logger(__name__)


def table_to_text(table):

    rows = []


    for row in table:

        if not row:

            continue


        cleaned_row = []


        for cell in row:

            if cell is None:

                cleaned_row.append(
                    ""
                )

            else:

                cleaned_row.append(
                    str(cell).strip()
                )


        rows.append(
            " | ".join(cleaned_row)
        )


    return "\n".join(rows)


def extract_tables(file_path):

    documents = []

    file_name = os.path.basename(
        file_path
    )


    try:

        with pdfplumber.open(
            file_path
        ) as pdf:


            for page_number, page in enumerate(
                pdf.pages
            ):


                tables = page.extract_tables()


                for table_number, table in enumerate(
                    tables
                ):


                    table_text = table_to_text(
                        table
                    )


                    if table_text.strip():

                        document = Document(

                            page_content=(
                                "TABLE:\n\n"
                                + table_text
                            ),

                            metadata={

                                "source": file_name,

                                "page": page_number + 1,

                                "table_number": table_number + 1,

                                "document_type": "table"

                            }

                        )


                        documents.append(
                            document
                        )


        logger.info(
            "Tables extracted from %s",
            file_name
        )


        return documents


    except Exception as error:

        logger.warning(
            "Table extraction failed: %s",
            error
        )

        return []