from langchain_text_splitters import (
    RecursiveCharacterTextSplitter
)

from src.config import (
    CHUNK_SIZE,
    CHUNK_OVERLAP
)


def create_chunks(documents):

    splitter = RecursiveCharacterTextSplitter(

        chunk_size=CHUNK_SIZE,

        chunk_overlap=CHUNK_OVERLAP,

        separators=[
            "\n\n",
            "\n",
            ". ",
            " ",
            ""
        ]

    )


    chunks = []

    global_chunk_id = 0


    for document in documents:

        split_documents = splitter.split_documents(
            [document]
        )


        for chunk in split_documents:

            chunk.metadata[
                "chunk_id"
            ] = global_chunk_id


            chunks.append(
                chunk
            )


            global_chunk_id += 1


    return chunks 