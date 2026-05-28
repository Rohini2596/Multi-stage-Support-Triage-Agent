class ProductRouter:

    PRODUCT_KEYWORDS = {
        "visa": [
            "visa",
            "card",
            "payment",
            "refund",
            "chargeback",
            "billing",
            "transaction",
        ],

        "claude": [
            "claude",
            "anthropic",
            "prompt",
            "conversation",
            "chat",
            "token",
            "api",
        ],

        "devplatform": [
            "hackerrank",
            "assessment",
            "candidate",
            "interview",
            "jobvite",
            "sso",
            "developer",
        ],
    }

    def route(
        self,
        text: str,
    ) -> str:

        text = text.lower()

        scores = {
            "visa": 0,
            "claude": 0,
            "devplatform": 0,
        }

        for product, keywords in (
            self.PRODUCT_KEYWORDS.items()
        ):

            for keyword in keywords:

                if keyword in text:
                    scores[product] += 1

        best_product = max(
            scores,
            key=scores.get,
        )

        if scores[best_product] == 0:
            return "general"

        return best_product