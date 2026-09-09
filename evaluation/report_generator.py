def generate_summary(results):

    if not results:

        return {

            "total_questions": 0,

            "answer_relevancy": 0,

            "answer_correctness": 0,

            "context_precision": 0,

            "context_recall": 0,

            "hit_rate": 0,

            "overall_score": 0

        }


    total_questions = len(
        results
    )


    metric_totals = {

        "answer_relevancy": 0,

        "answer_correctness": 0,

        "context_precision": 0,

        "context_recall": 0,

        "hit_rate": 0,

        "overall_score": 0

    }


    for result in results:

        metrics = result.get(
            "metrics",
            {}
        )


        metric_totals[
            "answer_relevancy"
        ] += metrics.get(
            "answer_relevancy",
            0
        )


        metric_totals[
            "answer_correctness"
        ] += metrics.get(
            "answer_correctness",
            0
        )


        metric_totals[
            "context_precision"
        ] += metrics.get(
            "context_precision",
            0
        )


        metric_totals[
            "context_recall"
        ] += metrics.get(
            "context_recall",
            0
        )


        metric_totals[
            "hit_rate"
        ] += metrics.get(
            "hit_rate",
            0
        )


        metric_totals[
            "overall_score"
        ] += result.get(
            "overall_score",
            0
        )


    summary = {

        "total_questions":
            total_questions,


        "answer_relevancy":

            round(

                metric_totals[
                    "answer_relevancy"
                ]

                /

                total_questions,

                4

            ),


        "answer_correctness":

            round(

                metric_totals[
                    "answer_correctness"
                ]

                /

                total_questions,

                4

            ),


        "context_precision":

            round(

                metric_totals[
                    "context_precision"
                ]

                /

                total_questions,

                4

            ),


        "context_recall":

            round(

                metric_totals[
                    "context_recall"
                ]

                /

                total_questions,

                4

            ),


        "hit_rate":

            round(

                metric_totals[
                    "hit_rate"
                ]

                /

                total_questions,

                4

            ),


        "overall_score":

            round(

                metric_totals[
                    "overall_score"
                ]

                /

                total_questions,

                4

            )

    }


    return summary