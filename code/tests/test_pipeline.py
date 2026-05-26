from code.pipeline import (
    SupportPipeline,
)


def main():

    pipeline = (
        SupportPipeline()
    )

    sample_ticket = {

        "Subject":
            "Refund not received",

        "Company":
            "claude",

        "Issue":
            """
Customer:
I cancelled my Claude Pro
subscription last week
but I still got charged.

Can I get a refund?
"""
    }

    result = (
        pipeline.process_row(
            sample_ticket
        )
    )

    print(
        "\nFINAL PIPELINE RESULT\n"
    )

    print("=" * 60)

    for k, v in result.items():

        print(f"\n{k}:")
        print(v)


if __name__ == "__main__":

    main()