from code.pipeline import (
    SupportPipeline,
)
def main():
    pipeline = (
        SupportPipeline()
    )
    sample_ticket = {
        "Subject":
            "Problema de reembolso",
        "Company":
            "claude",
        "Issue":
            """
Cliente:
Cancelé mi suscripción
pero todavía me cobraron.
¿Puedo obtener un reembolso?
"""
    }
    result = (
        pipeline.process_row(
            sample_ticket
        )
    )
    print("MULTILINGUAL TEST")
    print("=" * 60)
    for k, v in result.items():
        print(f"\n{k}:")
        print(v)
if __name__ == "__main__":
    main()