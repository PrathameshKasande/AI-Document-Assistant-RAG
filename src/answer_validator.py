NOT_FOUND_MESSAGE = (
    "I could not find this information "
    "in the uploaded documents."
)


def validate_answer(answer):

    if not answer:

        return NOT_FOUND_MESSAGE


    answer = answer.strip()


    if len(answer) < 5:

        return NOT_FOUND_MESSAGE


    return answer