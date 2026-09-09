from src.config import (
    TOP_K,
    NEIGHBOR_WINDOW
)


def retrieve_documents(

    question,

    vector_store,

    all_chunks

):

    results = (
        vector_store.similarity_search_with_score(

            question,

            k=TOP_K

        )
    )


    retrieved_ids = set()

    selected_chunks = []


    for document, score in results:

        chunk_id = document.metadata.get(
            "chunk_id"
        )


        if chunk_id not in retrieved_ids:

            retrieved_ids.add(
                chunk_id
            )


            selected_chunks.append(
                document
            )


    # =====================================
    # CREATE LOOKUP
    # =====================================

    chunk_lookup = {

        chunk.metadata.get(
            "chunk_id"
        ): chunk

        for chunk in all_chunks

    }


    final_chunks = {}


    # =====================================
    # ADD NEIGHBORS
    # =====================================

    for document in selected_chunks:

        chunk_id = document.metadata.get(
            "chunk_id"
        )


        source = document.metadata.get(
            "source"
        )


        for offset in range(

            -NEIGHBOR_WINDOW,

            NEIGHBOR_WINDOW + 1

        ):

            neighbor_id = (
                chunk_id + offset
            )


            if neighbor_id in chunk_lookup:

                neighbor = chunk_lookup[
                    neighbor_id
                ]


                neighbor_source = (
                    neighbor.metadata.get(
                        "source"
                    )
                )


                if neighbor_source == source:

                    final_chunks[
                        neighbor_id
                    ] = neighbor


    # =====================================
    # SORT
    # =====================================

    documents = sorted(

        final_chunks.values(),

        key=lambda document:
        document.metadata.get(
            "chunk_id",
            0
        )

    )


    return documents