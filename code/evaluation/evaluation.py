from collections import defaultdict


class EvaluationTracker:

    def __init__(self):

        self.metrics = defaultdict(int)

    def log_retrieval(
        self,
        retrieved_paths,
        expected_domain,
    ):

        total = len(retrieved_paths)

        correct = 0

        for p in retrieved_paths:

            if (
                f"data\\{expected_domain}\\"
                in p.lower()
            ):
                correct += 1

        contamination = total - correct

        self.metrics[
            "retrieval_total"
        ] += total

        self.metrics[
            "retrieval_correct"
        ] += correct

        self.metrics[
            "retrieval_contamination"
        ] += contamination

    def log_escalation(
        self,
        predicted,
        expected,
    ):

        if predicted == expected:

            self.metrics[
                "escalation_correct"
            ] += 1

        self.metrics[
            "escalation_total"
        ] += 1

    def log_unsupported(
        self,
        predicted,
        expected,
    ):

        if predicted == expected:

            self.metrics[
                "unsupported_correct"
            ] += 1

        self.metrics[
            "unsupported_total"
        ] += 1

    def summary(self):

        retrieval_total = max(
            1,
            self.metrics[
                "retrieval_total"
            ]
        )

        escalation_total = max(
            1,
            self.metrics[
                "escalation_total"
            ]
        )

        unsupported_total = max(
            1,
            self.metrics[
                "unsupported_total"
            ]
        )

        retrieval_accuracy = round(
            (
                self.metrics[
                    "retrieval_correct"
                ]
                / retrieval_total
            ) * 100,
            2,
        )

        contamination_rate = round(
            (
                self.metrics[
                    "retrieval_contamination"
                ]
                / retrieval_total
            ) * 100,
            2,
        )

        escalation_accuracy = round(
            (
                self.metrics[
                    "escalation_correct"
                ]
                / escalation_total
            ) * 100,
            2,
        )

        unsupported_accuracy = round(
            (
                self.metrics[
                    "unsupported_correct"
                ]
                / unsupported_total
            ) * 100,
            2,
        )

        return {
            "retrieval_accuracy":
                retrieval_accuracy,

            "contamination_rate":
                contamination_rate,

            "escalation_accuracy":
                escalation_accuracy,

            "unsupported_accuracy":
                unsupported_accuracy,
        }