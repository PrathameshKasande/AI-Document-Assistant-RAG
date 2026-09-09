import json
import re

from src.llm import generate_answer


def extract_json(text):

    text = text.strip()


    text = re.sub(
        r"```json",
        "",
        text
    )


    text = re.sub(
        r"```",
        "",
        text
    )


    match = re.search(

        r"\[.*\]",

        text,

        re.DOTALL

    )


    if match:

        return match.group()


    return text


def generate_evaluation_dataset(

    chunks,

    number_of_samples=10

):

    if not chunks:

        return []


    selected_chunks = chunks[
        :number_of_samples
    ]


    dataset = []


    for index, chunk in enumerate(
        selected_chunks
    ):

        prompt = f"""
You are generating an evaluation dataset
for a RAG system.

Create ONE question and answer pair
using ONLY the document content below.

DOCUMENT CONTENT:

{chunk.page_content}

Return ONLY valid JSON.

Format:

{{
    "question": "question here",
    "ground_truth": "complete answer here"
}}
"""


        try:

            response = generate_answer(
                prompt
            )


            clean_response = (
                response
                .replace(
                    "```json",
                    ""
                )
                .replace(
                    "```",
                    ""
                )
                .strip()
            )


            item = json.loads(
                clean_response
            )


            item["source"] = (
                chunk.metadata.get(
                    "source",
                    "Unknown"
                )
            )


            item["page"] = (
                chunk.metadata.get(
                    "page",
                    "Unknown"
                )
            )


            item["chunk_id"] = (
                chunk.metadata.get(
                    "chunk_id",
                    -1
                )
            )


            dataset.append(
                item
            )


        except Exception:

            continue


    return dataset