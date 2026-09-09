import re


def normalize_text(text):

    if not text:

        return ""


    text = text.lower()


    text = re.sub(
        r"[^a-z0-9\s]",
        " ",
        text
    )


    text = re.sub(
        r"\s+",
        " ",
        text
    )


    return text.strip()


def get_words(text):

    normalized = normalize_text(
        text
    )


    return set(
        normalized.split()
    )


# ==========================================
# ANSWER RELEVANCY
# ==========================================

def calculate_answer_relevancy(

    answer,

    ground_truth

):

    answer_words = get_words(
        answer
    )


    truth_words = get_words(
        ground_truth
    )


    if not answer_words:

        return 0.0


    if not truth_words:

        return 0.0


    common_words = (
        answer_words.intersection(
            truth_words
        )
    )


    score = (

        len(common_words)

        /

        len(truth_words)

    )


    return round(
        score,
        4
    )


# ==========================================
# ANSWER CORRECTNESS
# ==========================================

def calculate_answer_correctness(

    answer,

    ground_truth

):

    answer_words = get_words(
        answer
    )


    truth_words = get_words(
        ground_truth
    )


    if not answer_words:

        return 0.0


    if not truth_words:

        return 0.0


    common_words = (

        answer_words

        .intersection(

            truth_words

        )

    )


    precision = (

        len(common_words)

        /

        len(answer_words)

    )


    recall = (

        len(common_words)

        /

        len(truth_words)

    )


    if precision + recall == 0:

        return 0.0


    f1_score = (

        2

        *

        (

            precision

            *

            recall

        )

        /

        (

            precision

            +

            recall

        )

    )


    return round(
        f1_score,
        4
    )


# ==========================================
# CONTEXT PRECISION
# ==========================================

def calculate_context_precision(

    retrieved_documents,

    expected_chunk_id

):

    if not retrieved_documents:

        return 0.0


    relevant_count = 0


    for document in retrieved_documents:

        chunk_id = document.metadata.get(
            "chunk_id"
        )


        if chunk_id == expected_chunk_id:

            relevant_count += 1


    score = (

        relevant_count

        /

        len(retrieved_documents)

    )


    return round(
        score,
        4
    )


# ==========================================
# CONTEXT RECALL
# ==========================================

def calculate_context_recall(

    retrieved_documents,

    expected_chunk_id

):

    for document in retrieved_documents:

        chunk_id = document.metadata.get(
            "chunk_id"
        )


        if chunk_id == expected_chunk_id:

            return 1.0


    return 0.0


# ==========================================
# HIT RATE
# ==========================================

def calculate_hit_rate(

    retrieved_documents,

    expected_chunk_id

):

    return calculate_context_recall(

        retrieved_documents,

        expected_chunk_id

    )


# ==========================================
# OVERALL SCORE
# ==========================================

def calculate_overall_score(metrics):

    metric_values = [

        metrics.get(
            "answer_relevancy",
            0
        ),

        metrics.get(
            "answer_correctness",
            0
        ),

        metrics.get(
            "context_precision",
            0
        ),

        metrics.get(
            "context_recall",
            0
        ),

        metrics.get(
            "hit_rate",
            0
        )

    ]


    if not metric_values:

        return 0.0


    score = (

        sum(metric_values)

        /

        len(metric_values)

    )


    return round(
        score,
        4
    )