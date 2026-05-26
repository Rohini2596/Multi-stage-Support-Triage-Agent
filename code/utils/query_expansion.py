TRANSLATIONS = {
    "reembolso": "refund",
    "suscripción": "subscription",
    "cobrado": "charged",
    "cobraron": "charged",
    "facturación": "billing",
    "cancelé": "cancelled",
    "cancelar": "cancel",
    # FRENCH
    "remboursement": "refund",
    "abonnement": "subscription",
    "facturation": "billing",
    "annuler": "cancel",
    # HINDI
    "रिफंड": "refund",
    "सदस्यता": "subscription",
    "भुगतान": "payment",
}
def expand_query(text: str) -> str:
    if not text:
        return ""
    out = text
    lower = text.lower()
    for foreign, english in (
        TRANSLATIONS.items()
    ):
        if foreign in lower:
            out += f" {english}"
    return out