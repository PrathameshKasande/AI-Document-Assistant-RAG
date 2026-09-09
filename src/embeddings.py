from langchain_huggingface import (
    HuggingFaceEmbeddings
)

from src.config import (
    EMBEDDING_MODEL
)


def get_embeddings():

    embeddings = HuggingFaceEmbeddings(

        model_name=EMBEDDING_MODEL,

        model_kwargs={

            "device": "cpu"

        },

        encode_kwargs={

            "normalize_embeddings": True

        }

    )


    return embeddings