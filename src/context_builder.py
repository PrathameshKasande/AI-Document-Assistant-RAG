def build_context(documents):

    context_parts = []

    seen_chunks = set()


    for document in documents:

        chunk_id = document.metadata.get(
            "chunk_id"
        )


        if chunk_id in seen_chunks:

            continue


        seen_chunks.add(
            chunk_id
        )


        source = document.metadata.get(
            "source",
            "Unknown"
        )


        page = document.metadata.get(
            "page",
            "Unknown"
        )


        document_type = document.metadata.get(
            "document_type",
            "text"
        )


        content = document.page_content.strip()


        if not content:

            continue


        context_parts.append(

            f"""
SOURCE: {source}

PAGE: {page}

CONTENT TYPE: {document_type}

CONTENT:

{content}

------------------------------------
"""

        )


    return "\n".join(
        context_parts
    )