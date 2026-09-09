import os
import hashlib

import streamlit as st


from src.config import (
    UPLOAD_DIR,
    EMBEDDING_MODEL,
    LLM_MODEL
)


from src.document_processor import (
    extract_pdf_text
)


from src.table_extractor import (
    extract_tables
)


from src.chunker import (
    create_chunks
)


from src.vector_store import (
    create_vector_store,
    save_vector_store
)


from src.rag_pipeline import (
    answer_question
)


# ============================================
# EVALUATION IMPORTS
# ============================================

from evaluation.dataset_generator import (
    generate_evaluation_dataset
)


from evaluation.evaluation_data import (
    save_dataset,
    save_results
)


from evaluation.evaluator import (
    evaluate_dataset
)


from evaluation.report_generator import (
    generate_summary
)


# ============================================
# PAGE CONFIG
# ============================================

st.set_page_config(

    page_title="AI Document Assistant",

    page_icon="🤖",

    layout="wide",

    initial_sidebar_state="expanded"

)


# ============================================
# SESSION STATE
# ============================================

if "vector_store" not in st.session_state:

    st.session_state.vector_store = None


if "all_chunks" not in st.session_state:

    st.session_state.all_chunks = []


if "messages" not in st.session_state:

    st.session_state.messages = []


if "question_cache" not in st.session_state:

    st.session_state.question_cache = {}


if "processed_files" not in st.session_state:

    st.session_state.processed_files = []


# ============================================
# EVALUATION SESSION STATE
# ============================================

if "evaluation_dataset" not in st.session_state:

    st.session_state.evaluation_dataset = []


if "evaluation_results" not in st.session_state:

    st.session_state.evaluation_results = []


if "evaluation_summary" not in st.session_state:

    st.session_state.evaluation_summary = None


# ============================================
# QUESTION NORMALIZATION
# ============================================

def normalize_question(question):

    return (
        question
        .lower()
        .strip()
        .replace("?", "")
        .replace(".", "")
    )


# ============================================
# QUESTION HASH
# ============================================

def get_question_hash(question):

    normalized = normalize_question(
        question
    )


    return hashlib.md5(

        normalized.encode()

    ).hexdigest()


# ============================================
# RESET EVALUATION
# ============================================

def reset_evaluation():

    st.session_state.evaluation_dataset = []

    st.session_state.evaluation_results = []

    st.session_state.evaluation_summary = None


# ============================================
# HEADER
# ============================================

st.title(
    "🤖 AI Document Assistant"
)


st.caption(
    "Advanced RAG-Powered PDF Assistant | "
    "Ask detailed questions from your documents"
)


# ============================================
# SIDEBAR
# ============================================

with st.sidebar:

    st.header(
        "⚙️ System Information"
    )


    st.subheader(
        "Embedding Model"
    )


    st.caption(
        EMBEDDING_MODEL
    )


    st.subheader(
        "Vector Database"
    )


    st.caption(
        "FAISS"
    )


    st.subheader(
        "LLM Model"
    )


    st.caption(
        LLM_MODEL
    )


    st.divider()


    # ========================================
    # DOCUMENT STATUS
    # ========================================

    st.subheader(
        "📊 Document Status"
    )


    st.write(
        f"Documents: "
        f"{len(st.session_state.processed_files)}"
    )


    st.write(
        f"Chunks: "
        f"{len(st.session_state.all_chunks)}"
    )


    # ========================================
    # EVALUATION STATUS
    # ========================================

    st.divider()


    st.subheader(
        "📈 Evaluation Status"
    )


    st.write(
        f"Evaluation Questions: "
        f"{len(st.session_state.evaluation_dataset)}"
    )


    if st.session_state.evaluation_summary:

        score = (

            st.session_state.evaluation_summary.get(
                "overall_score",
                0
            )

            * 100

        )


        st.write(
            f"Overall Score: {score:.2f}%"
        )


    else:

        st.write(
            "Overall Score: Not evaluated"
        )


    st.divider()


    # ========================================
    # CLEAR CHAT
    # ========================================

    if st.button(

        "🗑️ Clear Chat",

        use_container_width=True

    ):

        st.session_state.messages = []

        st.session_state.question_cache = {}

        st.rerun()


    # ========================================
    # RESET DOCUMENTS
    # ========================================

    if st.button(

        "🔄 Reset Documents",

        use_container_width=True

    ):

        st.session_state.vector_store = None

        st.session_state.all_chunks = []

        st.session_state.messages = []

        st.session_state.question_cache = {}

        st.session_state.processed_files = []


        # RESET EVALUATION

        reset_evaluation()


        st.rerun()


# ============================================
# PDF UPLOAD
# ============================================

st.subheader(
    "📄 Upload PDF Documents"
)


uploaded_files = st.file_uploader(

    "Upload one or multiple PDF files",

    type=["pdf"],

    accept_multiple_files=True

)


# ============================================
# PROCESS DOCUMENTS
# ============================================

if uploaded_files:

    if st.button(

        "🚀 Process Documents",

        use_container_width=True

    ):


        all_documents = []

        processed_files = []


        progress_bar = st.progress(
            0
        )


        status_text = st.empty()


        try:

            total_files = len(
                uploaded_files
            )


            for index, uploaded_file in enumerate(
                uploaded_files
            ):


                status_text.write(
                    f"Processing: "
                    f"{uploaded_file.name}"
                )


                # =================================
                # SAVE PDF
                # =================================

                file_path = os.path.join(

                    UPLOAD_DIR,

                    uploaded_file.name

                )


                with open(
                    file_path,
                    "wb"
                ) as file:

                    file.write(
                        uploaded_file.getbuffer()
                    )


                # =================================
                # EXTRACT TEXT
                # =================================

                text_documents = (
                    extract_pdf_text(
                        file_path
                    )
                )


                # =================================
                # EXTRACT TABLES
                # =================================

                table_documents = (
                    extract_tables(
                        file_path
                    )
                )


                # =================================
                # COMBINE DOCUMENTS
                # =================================

                all_documents.extend(
                    text_documents
                )


                all_documents.extend(
                    table_documents
                )


                processed_files.append(
                    uploaded_file.name
                )


                # =================================
                # PROGRESS
                # =================================

                progress = int(

                    (
                        (index + 1)

                        /

                        total_files
                    )

                    * 100

                )


                progress_bar.progress(
                    progress
                )


            # =====================================
            # CREATE CHUNKS
            # =====================================

            status_text.write(
                "Creating document chunks..."
            )


            chunks = create_chunks(
                all_documents
            )


            if not chunks:

                raise ValueError(
                    "No document chunks were created."
                )


            # =====================================
            # CREATE VECTOR STORE
            # =====================================

            status_text.write(
                "Creating FAISS vector database..."
            )


            vector_store = (
                create_vector_store(
                    chunks
                )
            )


            # =====================================
            # SAVE VECTOR STORE
            # =====================================

            save_vector_store(
                vector_store
            )


            # =====================================
            # SAVE SESSION
            # =====================================

            st.session_state.vector_store = (
                vector_store
            )


            st.session_state.all_chunks = (
                chunks
            )


            st.session_state.processed_files = (
                processed_files
            )


            # =====================================
            # RESET CHAT
            # =====================================

            st.session_state.messages = []


            st.session_state.question_cache = {}


            # =====================================
            # RESET EVALUATION
            # =====================================

            reset_evaluation()


            progress_bar.progress(
                100
            )


            status_text.empty()


            st.success(
                "Documents processed successfully!"
            )


            st.info(
                f"""
📄 Documents Processed: {len(processed_files)}

🧩 Total Chunks: {len(chunks)}

📊 Tables are included when available.

🤖 Your documents are now ready for AI-powered questions
and RAG evaluation.
"""
            )


        except Exception as error:

            st.error(
                f"Processing Error: {error}"
            )


# ============================================
# CHAT SECTION
# ============================================

st.divider()


st.subheader(
    "💬 Chat with Your Documents"
)


# ============================================
# DISPLAY CHAT HISTORY
# ============================================

for message in st.session_state.messages:


    with st.chat_message(
        message["role"]
    ):


        st.markdown(
            message["content"]
        )


# ============================================
# CHAT INPUT
# ============================================

question = st.chat_input(

    "Ask a detailed question about your PDF documents..."

)


if question:


    # ========================================
    # CHECK DOCUMENTS
    # ========================================

    if st.session_state.vector_store is None:


        st.warning(
            "Please upload and process "
            "PDF documents first."
        )


    else:


        # ====================================
        # SAVE USER MESSAGE
        # ====================================

        st.session_state.messages.append(

            {

                "role": "user",

                "content": question

            }

        )


        # ====================================
        # DISPLAY USER MESSAGE
        # ====================================

        with st.chat_message(
            "user"
        ):


            st.markdown(
                question
            )


        # ====================================
        # QUESTION HASH
        # ====================================

        question_hash = get_question_hash(
            question
        )


        # ====================================
        # DUPLICATE QUESTION CACHE
        # ====================================

        if question_hash in (

            st.session_state.question_cache

        ):


            answer = (

                st.session_state.question_cache[
                    question_hash
                ]

            )


            with st.chat_message(
                "assistant"
            ):


                st.markdown(
                    answer
                )


            st.session_state.messages.append(

                {

                    "role": "assistant",

                    "content": answer

                }

            )


        else:


            # =================================
            # GENERATE NEW ANSWER
            # =================================

            with st.chat_message(
                "assistant"
            ):


                with st.spinner(

                    "Searching document context and "
                    "generating complete answer..."

                ):


                    try:


                        answer, sources = (

                            answer_question(

                                question,

                                st.session_state.vector_store,

                                st.session_state.all_chunks

                            )

                        )


                        # =========================
                        # DISPLAY ANSWER
                        # =========================

                        st.markdown(
                            answer
                        )


                        # =========================
                        # SHOW SOURCES
                        # =========================

                        if sources:


                            with st.expander(
                                "📚 View Sources"
                            ):


                                unique_sources = set()


                                for source in sources:


                                    file_name = (

                                        source.metadata.get(
                                            "source",
                                            "Unknown"
                                        )

                                    )


                                    page = (

                                        source.metadata.get(
                                            "page",
                                            "Unknown"
                                        )

                                    )


                                    source_type = (

                                        source.metadata.get(
                                            "document_type",
                                            "text"
                                        )

                                    )


                                    unique_sources.add(

                                        (

                                            str(file_name),

                                            str(page),

                                            str(source_type)

                                        )

                                    )


                                for (

                                    file_name,

                                    page,

                                    source_type

                                ) in sorted(
                                    unique_sources
                                ):


                                    st.write(

                                        f"📄 {file_name} | "
                                        f"Page: {page} | "
                                        f"Type: {source_type}"

                                    )


                        # =========================
                        # SAVE ANSWER
                        # =========================

                        st.session_state.messages.append(

                            {

                                "role": "assistant",

                                "content": answer

                            }

                        )


                        # =========================
                        # CACHE QUESTION
                        # =========================

                        st.session_state.question_cache[

                            question_hash

                        ] = answer


                    except Exception as error:


                        st.error(

                            f"Answer Generation Error: "
                            f"{error}"

                        )


# ============================================
# RAG EVALUATION SECTION
# ============================================

st.divider()


st.subheader(
    "📊 RAG Evaluation Dashboard"
)


st.caption(
    "Evaluate retrieval quality and answer quality "
    "using questions generated from uploaded PDF content."
)


# ============================================
# CHECK DOCUMENTS
# ============================================

if st.session_state.vector_store is None:


    st.info(
        "📄 Upload and process PDF documents "
        "before running RAG evaluation."
    )


else:


    # ========================================
    # EVALUATION SETTINGS
    # ========================================

    st.markdown(
        "### ⚙️ Evaluation Settings"
    )


    evaluation_samples = st.slider(

        "Number of Evaluation Questions",

        min_value=3,

        max_value=20,

        value=5,

        step=1

    )


    st.caption(
        "The system will generate questions and "
        "reference answers from your uploaded documents."
    )


    # ========================================
    # GENERATE EVALUATION DATASET
    # ========================================

    if st.button(

        "📝 Generate Evaluation Dataset",

        use_container_width=True

    ):


        with st.spinner(

            "Generating evaluation questions "
            "and reference answers..."

        ):


            try:


                dataset = (

                    generate_evaluation_dataset(

                        st.session_state.all_chunks,

                        number_of_samples=
                        evaluation_samples

                    )

                )


                if dataset:


                    st.session_state.evaluation_dataset = (
                        dataset
                    )


                    st.session_state.evaluation_results = []


                    st.session_state.evaluation_summary = None


                    save_dataset(
                        dataset
                    )


                    st.success(

                        f"Successfully generated "
                        f"{len(dataset)} evaluation questions!"

                    )


                else:


                    st.error(

                        "Could not generate evaluation "
                        "questions. Please try again."

                    )


            except Exception as error:


                st.error(

                    f"Evaluation Dataset Error: "
                    f"{error}"

                )


    # ========================================
    # DISPLAY EVALUATION DATASET
    # ========================================

    if st.session_state.evaluation_dataset:


        st.divider()


        st.subheader(
            "📋 Generated Evaluation Dataset"
        )


        st.caption(
            "Review the generated questions and "
            "reference answers before evaluation."
        )


        for index, item in enumerate(

            st.session_state.evaluation_dataset,

            start=1

        ):


            with st.expander(

                f"Question {index}: "
                f"{item.get('question', 'Unknown Question')}"

            ):


                st.markdown(
                    "#### ❓ Question"
                )


                st.write(
                    item.get(
                        "question",
                        ""
                    )
                )


                st.markdown(
                    "#### 🎯 Ground Truth"
                )


                st.write(
                    item.get(
                        "ground_truth",
                        ""
                    )
                )


                st.markdown(
                    "#### 📄 Source Information"
                )


                col1, col2, col3 = st.columns(
                    3
                )


                with col1:


                    st.write(
                        f"Source: "
                        f"{item.get('source', 'Unknown')}"
                    )


                with col2:


                    st.write(
                        f"Page: "
                        f"{item.get('page', 'Unknown')}"
                    )


                with col3:


                    st.write(
                        f"Chunk ID: "
                        f"{item.get('chunk_id', 'Unknown')}"
                    )


    # ========================================
    # RUN RAG EVALUATION
    # ========================================

    if st.session_state.evaluation_dataset:


        st.divider()


        st.subheader(
            "🚀 Run Evaluation"
        )


        if st.button(

            "🚀 Run RAG Evaluation",

            use_container_width=True

        ):


            progress_bar = st.progress(
                0
            )


            status_text = st.empty()


            try:


                status_text.write(
                    "Running RAG evaluation..."
                )


                results = (

                    evaluate_dataset(

                        st.session_state.evaluation_dataset,

                        st.session_state.vector_store,

                        st.session_state.all_chunks

                    )

                )


                progress_bar.progress(
                    70
                )


                status_text.write(
                    "Generating evaluation report..."
                )


                summary = generate_summary(
                    results
                )


                progress_bar.progress(
                    90
                )


                st.session_state.evaluation_results = (
                    results
                )


                st.session_state.evaluation_summary = (
                    summary
                )


                save_results(
                    results
                )


                progress_bar.progress(
                    100
                )


                status_text.empty()


                st.success(
                    "🎉 RAG Evaluation Completed Successfully!"
                )


            except Exception as error:


                status_text.empty()


                st.error(

                    f"RAG Evaluation Error: "
                    f"{error}"

                )


    # ========================================
    # DISPLAY EVALUATION RESULTS
    # ========================================

    if st.session_state.evaluation_summary:


        st.divider()


        st.subheader(
            "📈 Evaluation Results"
        )


        summary = (
            st.session_state.evaluation_summary
        )


        # ====================================
        # TOTAL QUESTIONS
        # ====================================

        st.info(

            f"📋 Total Evaluation Questions: "
            f"{summary.get('total_questions', 0)}"

        )


        # ====================================
        # METRICS ROW 1
        # ====================================

        col1, col2, col3 = st.columns(
            3
        )


        with col1:


            st.metric(

                "🎯 Answer Relevancy",

                f"{summary.get('answer_relevancy', 0) * 100:.2f}%"

            )


        with col2:


            st.metric(

                "✅ Answer Correctness",

                f"{summary.get('answer_correctness', 0) * 100:.2f}%"

            )


        with col3:


            st.metric(

                "🔍 Context Precision",

                f"{summary.get('context_precision', 0) * 100:.2f}%"

            )


        # ====================================
        # METRICS ROW 2
        # ====================================

        col1, col2, col3 = st.columns(
            3
        )


        with col1:


            st.metric(

                "📚 Context Recall",

                f"{summary.get('context_recall', 0) * 100:.2f}%"

            )


        with col2:


            st.metric(

                "🎯 Retrieval Hit Rate",

                f"{summary.get('hit_rate', 0) * 100:.2f}%"

            )


        with col3:


            st.metric(

                "🏆 Overall RAG Score",

                f"{summary.get('overall_score', 0) * 100:.2f}%"

            )


        # ====================================
        # SCORE INTERPRETATION
        # ====================================

        overall_score = (

            summary.get(
                "overall_score",
                0
            )

            * 100

        )


        st.divider()


        st.subheader(
            "📊 Score Interpretation"
        )


        if overall_score >= 85:


            st.success(

                "Excellent RAG performance. "
                "The system is retrieving relevant "
                "context and generating useful answers."

            )


        elif overall_score >= 70:


            st.info(

                "Good RAG performance. "
                "There is room for improvement in "
                "retrieval or answer generation."

            )


        elif overall_score >= 50:


            st.warning(

                "Moderate RAG performance. "
                "Consider improving chunking, "
                "retrieval, or prompts."

            )


        else:


            st.error(

                "Low RAG performance. "
                "Review your embedding model, "
                "chunking strategy, retrieval logic, "
                "and LLM prompt."

            )


        # ====================================
        # DETAILED RESULTS
        # ====================================

        st.divider()


        st.subheader(
            "🔍 Detailed Evaluation Results"
        )


        for index, result in enumerate(

            st.session_state.evaluation_results,

            start=1

        ):


            with st.expander(

                f"Evaluation {index}: "
                f"{result.get('question', 'Unknown Question')}"

            ):


                st.markdown(
                    "### ❓ Question"
                )


                st.write(
                    result.get(
                        "question",
                        ""
                    )
                )


                st.markdown(
                    "### 🎯 Ground Truth"
                )


                st.write(
                    result.get(
                        "ground_truth",
                        ""
                    )
                )


                st.markdown(
                    "### 🤖 Generated Answer"
                )


                st.write(
                    result.get(
                        "generated_answer",
                        ""
                    )
                )


                # ================================
                # INDIVIDUAL SCORE
                # ================================

                score = (

                    result.get(
                        "overall_score",
                        0
                    )

                    * 100

                )


                st.metric(

                    "Overall Score",

                    f"{score:.2f}%"

                )


                # ================================
                # INDIVIDUAL METRICS
                # ================================

                metrics = result.get(
                    "metrics",
                    {}
                )


                metric_col1, metric_col2, metric_col3 = (
                    st.columns(
                        3
                    )
                )


                with metric_col1:


                    st.write(

                        f"Answer Relevancy: "
                        f"{metrics.get('answer_relevancy', 0) * 100:.2f}%"

                    )


                    st.write(

                        f"Context Recall: "
                        f"{metrics.get('context_recall', 0) * 100:.2f}%"

                    )


                with metric_col2:


                    st.write(

                        f"Answer Correctness: "
                        f"{metrics.get('answer_correctness', 0) * 100:.2f}%"

                    )


                    st.write(

                        f"Hit Rate: "
                        f"{metrics.get('hit_rate', 0) * 100:.2f}%"

                    )


                with metric_col3:


                    st.write(

                        f"Context Precision: "
                        f"{metrics.get('context_precision', 0) * 100:.2f}%"

                    )


                    st.write(

                        f"Expected Chunk ID: "
                        f"{result.get('expected_chunk_id', 'Unknown')}"

                    )


        # ====================================
        # RAW RESULTS
        # ====================================

        st.divider()


        with st.expander(
            "🧾 View Raw Evaluation Results"
        ):


            st.json(
                st.session_state.evaluation_results
            )