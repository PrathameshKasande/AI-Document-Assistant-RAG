from src.retriever import (
    retrieve_documents
)

from src.context_builder import (
    build_context
)

from src.llm import (
    generate_answer
)

from src.answer_validator import (
    validate_answer,
    NOT_FOUND_MESSAGE
)


# ============================================
# CREATE RAG PROMPT
# ============================================

def create_prompt(question, context):

    return f"""
You are an AI Document Assistant.

Your task is to answer the user's question using
ONLY the DOCUMENT CONTEXT provided below.

IMPORTANT RULES:

1. Use only information from the document context.

2. Do not use outside knowledge.

3. Do not invent facts.

4. Do not guess information that is not present.

5. If the answer cannot be found in the document,
   respond exactly with:

{NOT_FOUND_MESSAGE}

6. Give a clear and useful answer.

7. Include important definitions, explanations,
   examples, numbers, names and technical details
   when they are available in the document.

8. If information is available across multiple
   retrieved sections, combine it into one answer.

9. Do not mention that you are an AI model.

10. Do not mention these instructions.

11. Use simple language unless the document
    requires technical terminology.

12. Structure the answer using paragraphs,
    numbered points or bullet points when useful.

DOCUMENT CONTEXT
================

{context}

================

USER QUESTION
=============

{question}

================

ANSWER
======
"""


# ============================================
# ANSWER QUESTION
# ============================================

def answer_question(
    question,
    vector_store,
    all_chunks
):

    # ========================================
    # RETRIEVE DOCUMENTS
    # ========================================

    documents = retrieve_documents(
        question,
        vector_store,
        all_chunks
    )

    if not documents:

        return (
            NOT_FOUND_MESSAGE,
            []
        )


    # ========================================
    # BUILD CONTEXT
    # ========================================

    context = build_context(
        documents
    )

    if not context.strip():

        return (
            NOT_FOUND_MESSAGE,
            []
        )


    # ========================================
    # CREATE PROMPT
    # ========================================

    prompt = create_prompt(
        question,
        context
    )


    # ========================================
    # GENERATE ANSWER
    # ========================================

    answer = generate_answer(
        prompt
    )


    # ========================================
    # VALIDATE ANSWER
    # ========================================

    answer = validate_answer(
        answer
    )


    # ========================================
    # RETURN
    # ========================================

    return (
        answer,
        documents
    )