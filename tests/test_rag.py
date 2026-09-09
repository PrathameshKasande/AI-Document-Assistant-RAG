from unittest.mock import patch

from langchain_core.documents import Document

from src.rag_pipeline import (
    create_prompt,
    answer_question
)


def test_create_prompt():

    question = (
        "What is Machine Learning?"
    )


    context = (
        "Machine Learning is a "
        "subset of Artificial Intelligence."
    )


    prompt = create_prompt(

        question,

        context

    )


    assert question in prompt


    assert context in prompt


def test_prompt_contains_rules():

    prompt = create_prompt(

        "What is AI?",

        "AI is Artificial Intelligence."

    )


    assert (
        "Use ONLY information"
        in prompt
    )


def test_prompt_contains_context():

    context = (
        "Python is used for Data Science."
    )


    prompt = create_prompt(

        "What is Python used for?",

        context

    )


    assert context in prompt


@patch(
    "src.rag_pipeline.generate_answer"
)
@patch(
    "src.rag_pipeline.retrieve_documents"
)
def test_answer_question(

    mock_retrieve,

    mock_generate

):

    document = Document(

        page_content=(
            "Machine Learning learns patterns "
            "from data."
        ),

        metadata={

            "source": "ml.pdf",

            "page": 1,

            "chunk_id": 0

        }

    )


    mock_retrieve.return_value = [

        document

    ]


    mock_generate.return_value = (

        "Machine Learning learns "
        "patterns from data."

    )


    answer, sources = answer_question(

        question=(
            "What is Machine Learning?"
        ),

        vector_store=None,

        all_chunks=[document]

    )


    assert (
        "Machine Learning"
        in answer
    )


    assert len(sources) == 1


def test_answer_question_no_documents():

    from unittest.mock import patch


    with patch(

        "src.rag_pipeline.retrieve_documents",

        return_value=[]

    ):


        answer, sources = answer_question(

            question=(
                "Unknown question"
            ),

            vector_store=None,

            all_chunks=[]

        )


        assert len(sources) == 0


        assert (
            "uploaded documents"
            in answer
        )