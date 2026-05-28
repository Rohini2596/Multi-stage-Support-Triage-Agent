from code.agent import (
    SupportAgent,
)

from code.evaluation.evaluation import (
    EvaluationTracker,
)

from code.tests.eval_cases import (
    EVAL_CASES,
)


def main():

    agent = SupportAgent()

    tracker = EvaluationTracker()

    print("=" * 60)
    print("RUNNING EVALUATION SUITE")
    print("=" * 60)

    for idx, case in enumerate(EVAL_CASES):

        print("\n")
        print("=" * 60)

        print(
            f"CASE {idx + 1}"
        )

        print("=" * 60)

        query = case["query"]

        expected_domain = (
            case["domain"]
        )

        expected_escalation = (
            case["should_escalate"]
        )

        expected_unsupported = (
            case["unsupported"]
        )

        print(
            f"QUERY: {query}"
        )

        fake_ticket = {
            "subject":
                "Evaluation Test",

            "company":
                expected_domain,

            "issue":
                query,
        }

        result = (
            agent.pipeline.process_row(
                fake_ticket
            )
        )

        retrieved_paths = (
            result.get(
                "source_documents",
                "",
            ).split("|")
        )

        predicted_escalation = (
            result.get("status")
            == "escalated"
        )

        predicted_unsupported = (
            "unsupported=True"
            in result.get(
                "justification",
                "",
            )
        )

        tracker.log_retrieval(
            retrieved_paths,
            expected_domain,
        )

        tracker.log_escalation(
            predicted_escalation,
            expected_escalation,
        )

        tracker.log_unsupported(
            predicted_unsupported,
            expected_unsupported,
        )

        print("\nRESULT")

        print(result)

    print("\n")
    print("=" * 60)
    print("FINAL METRICS")
    print("=" * 60)

    summary = tracker.summary()

    for k, v in summary.items():

        print(f"{k}: {v}")


if __name__ == "__main__":
    main()