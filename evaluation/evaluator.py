from src.rag_pipeline import (
    answer_question
)

from src.retriever import (
    retrieve_documents
)

from evaluation.metrics import (

    calculate_answer_relevancy,

    calculate_answer_correctness,

    calculate_context_precision,

    calculate_context_recall,

    calculate_hit_rate,

    calculate_overall_score

)


def evaluate_single_question(

    item,

    vector_store,

    all_chunks

):

    question = item.get(
        "question",
        ""
    )


    ground_truth = item.get(
        "ground_truth",
        ""
    )


    expected_chunk_id = item.get(
        "chunk_id",
        -1
    )


    # =====================================
    # GET RAG ANSWER
    # =====================================

    answer, sources = answer_question(

        question,

        vector_store,

        all_chunks

    )


    # =====================================
    # GET RETRIEVED DOCUMENTS
    # =====================================

    retrieved_documents = retrieve_documents(

        question,

        vector_store,

        all_chunks

    )


    # =====================================
    # CALCULATE METRICS
    # =====================================

    metrics = {

        "answer_relevancy":

            calculate_answer_relevancy(

                answer,

                ground_truth

            ),


        "answer_correctness":

            calculate_answer_correctness(

                answer,

                ground_truth

            ),


        "context_precision":

            calculate_context_precision(

                retrieved_documents,

                expected_chunk_id

            ),


        "context_recall":

            calculate_context_recall(

                retrieved_documents,

                expected_chunk_id

            ),


        "hit_rate":

            calculate_hit_rate(

                retrieved_documents,

                expected_chunk_id

            )

    }


    overall_score = (

        calculate_overall_score(
            metrics
        )

    )


    result = {

        "question": question,

        "ground_truth": ground_truth,

        "generated_answer": answer,

        "expected_chunk_id": expected_chunk_id,

        "metrics": metrics,

        "overall_score": overall_score

    }


    return result


def evaluate_dataset(

    dataset,

    vector_store,

    all_chunks

):

    results = []


    for item in dataset:

        result = evaluate_single_question(

            item,

            vector_store,

            all_chunks

        )


        results.append(
            result
        )


    return results