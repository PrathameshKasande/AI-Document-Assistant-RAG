import json
import os


BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)


EVALUATION_DIR = os.path.join(
    BASE_DIR,
    "data",
    "evaluation"
)


DATASET_PATH = os.path.join(
    EVALUATION_DIR,
    "evaluation_dataset.json"
)


RESULTS_PATH = os.path.join(
    EVALUATION_DIR,
    "evaluation_results.json"
)


def ensure_evaluation_directory():

    os.makedirs(
        EVALUATION_DIR,
        exist_ok=True
    )


def save_dataset(dataset):

    ensure_evaluation_directory()


    with open(
        DATASET_PATH,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            dataset,
            file,
            indent=4,
            ensure_ascii=False
        )


def load_dataset():

    ensure_evaluation_directory()


    if not os.path.exists(
        DATASET_PATH
    ):

        return []


    try:

        with open(
            DATASET_PATH,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(
                file
            )


    except (
        json.JSONDecodeError,
        OSError
    ):

        return []


def save_results(results):

    ensure_evaluation_directory()


    with open(
        RESULTS_PATH,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            results,
            file,
            indent=4,
            ensure_ascii=False
        )


def load_results():

    ensure_evaluation_directory()


    if not os.path.exists(
        RESULTS_PATH
    ):

        return []


    try:

        with open(
            RESULTS_PATH,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(
                file
            )


    except (
        json.JSONDecodeError,
        OSError
    ):

        return []