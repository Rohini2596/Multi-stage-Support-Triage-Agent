import pandas as pd

from collections import Counter

from code.agent import (
    SupportAgent,
)


def main():

    agent = SupportAgent()

    df = pd.read_csv(
        "support_tickets/support_tickets.csv"
    )

    total = len(df)

    escalated = 0

    replied = 0

    unsupported = 0

    contamination = 0

    confidence_scores = []

    retrieval_scores = []

    domain_correct = 0

    domain_total = 0

    status_counter = Counter()

    retrieval_quality_counter = Counter()

    print("=" * 60)
    print("RUNNING FULL DATASET EVALUATION")
    print("=" * 60)

    for idx, row in df.iterrows():

        try:

            result = (
                agent.pipeline.process_row(
                    row.to_dict()
                )
            )

            status = result.get(
                "status",
                "unknown",
            )

            status_counter[status] += 1

            if status == "escalated":
                escalated += 1
            else:
                replied += 1

            confidence = result.get(
                "confidence_score",
                0.0,
            )

            confidence_scores.append(
                confidence
            )

            justification = result.get(
                "justification",
                "",
            )

            # RETRIEVAL QUALITY
            if (
                "retrieval_quality="
                in justification
            ):

                quality = (
                    justification
                    .split(
                        "retrieval_quality="
                    )[1]
                    .split(";")[0]
                    .strip()
                )

                retrieval_quality_counter[
                    quality
                ] += 1

            # UNSUPPORTED
            if (
                "unsupported=True"
                in justification
            ):
                unsupported += 1

            # RETRIEVAL SCORE
            if (
                "retrieval_score="
                in justification
            ):

                try:

                    score = float(
                        justification
                        .split(
                            "retrieval_score="
                        )[1]
                        .split(";")[0]
                    )

                    retrieval_scores.append(
                        score
                    )

                except:
                    pass

            # DOMAIN CHECK
            company = str(
                row.get(
                    "company",
                    "",
                )
            ).lower()

            sources = result.get(
                "source_documents",
                "",
            )

            if sources:

                paths = sources.split("|")

                domain_total += len(paths)

                for p in paths:

                    p_lower = p.lower()

                    if (
                        company in p_lower
                    ):
                        domain_correct += 1
                    else:
                        contamination += 1

        except Exception as e:

            print(
                f"FAILED ROW {idx}: {e}"
            )

    print("\n")
    print("=" * 60)
    print("FINAL METRICS")
    print("=" * 60)

    avg_confidence = round(
        sum(confidence_scores)
        / max(
            1,
            len(confidence_scores),
        ),
        4,
    )

    avg_retrieval = round(
        sum(retrieval_scores)
        / max(
            1,
            len(retrieval_scores),
        ),
        4,
    )

    contamination_rate = round(
        (
            contamination
            / max(1, domain_total)
        ) * 100,
        2,
    )

    retrieval_accuracy = round(
        (
            domain_correct
            / max(1, domain_total)
        ) * 100,
        2,
    )

    print(
        f"TOTAL TICKETS: {total}"
    )

    print(
        f"ESCALATED: {escalated}"
    )

    print(
        f"REPLIED: {replied}"
    )

    print(
        f"UNSUPPORTED: {unsupported}"
    )

    print(
        f"AVG CONFIDENCE: "
        f"{avg_confidence}"
    )

    print(
        f"AVG RETRIEVAL SCORE: "
        f"{avg_retrieval}"
    )

    print(
        f"RETRIEVAL ACCURACY: "
        f"{retrieval_accuracy}%"
    )

    print(
        f"CONTAMINATION RATE: "
        f"{contamination_rate}%"
    )

    print("\nSTATUS DISTRIBUTION")

    for k, v in status_counter.items():

        print(f"{k}: {v}")

    print("\nRETRIEVAL QUALITY")

    for k, v in retrieval_quality_counter.items():

        print(f"{k}: {v}")


if __name__ == "__main__":
    main()