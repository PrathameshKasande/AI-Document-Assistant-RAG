from langchain_core.documents import Document

from src.retriever import (
    retrieve_documents
)


class MockVectorStore:


    def similarity_search_with_score(

        self,

        question,

        k

    ):

        return [

            (

                Document(

                    page_content=(
                        "Machine Learning uses data."
                    ),

                    metadata={

                        "chunk_id": 1,

                        "source": "ml.pdf",

                        "page": 1

                    }

                ),

                0.10

            )

        ]


def test_retrieve_documents():

    chunks = [

        Document(

            page_content=(
                "Introduction to AI"
            ),

            metadata={

                "chunk_id": 0,

                "source": "ml.pdf",

                "page": 1

            }

        ),


        Document(

            page_content=(
                "Machine Learning uses data."
            ),

            metadata={

                "chunk_id": 1,

                "source": "ml.pdf",

                "page": 1

            }

        ),


        Document(

            page_content=(
                "Deep Learning uses neural networks."
            ),

            metadata={

                "chunk_id": 2,

                "source": "ml.pdf",

                "page": 2

            }

        )

    ]


    vector_store = MockVectorStore()


    documents = retrieve_documents(

        question=(
            "What is Machine Learning?"
        ),

        vector_store=vector_store,

        all_chunks=chunks

    )


    assert len(documents) > 0


def test_retrieved_document_contains_answer():

    chunks = [

        Document(

            page_content=(
                "Python is a programming language."
            ),

            metadata={

                "chunk_id": 0,

                "source": "python.pdf",

                "page": 1

            }

        )

    ]


    class MockStore:


        def similarity_search_with_score(

            self,

            question,

            k

        ):

            return [

                (

                    chunks[0],

                    0.1

                )

            ]


    documents = retrieve_documents(

        question=(
            "What is Python?"
        ),

        vector_store=MockStore(),

        all_chunks=chunks

    )


    assert (
        "Python"
        in documents[0].page_content
    )