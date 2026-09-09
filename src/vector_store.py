import os

from langchain_community.vectorstores import (
    FAISS
)

from src.embeddings import (
    get_embeddings
)

from src.config import (
    VECTOR_STORE_DIR
)

from src.logger import (
    get_logger
)


logger = get_logger(__name__)


INDEX_NAME = "faiss_index"


def create_vector_store(chunks):

    embeddings = get_embeddings()


    vector_store = FAISS.from_documents(
        chunks,
        embeddings
    )


    logger.info(
        "FAISS created with %s chunks",
        len(chunks)
    )


    return vector_store


def save_vector_store(vector_store):

    vector_store.save_local(
        VECTOR_STORE_DIR,
        index_name=INDEX_NAME
    )


    logger.info(
        "FAISS vector store saved"
    )


def load_vector_store():

    embeddings = get_embeddings()


    index_path = os.path.join(
        VECTOR_STORE_DIR,
        f"{INDEX_NAME}.faiss"
    )


    if not os.path.exists(
        index_path
    ):

        return None


    return FAISS.load_local(

        VECTOR_STORE_DIR,

        embeddings,

        index_name=INDEX_NAME,

        allow_dangerous_deserialization=True

    )