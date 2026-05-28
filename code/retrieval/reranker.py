import re
class SimpleReranker:
    def __init__(self):
        pass
    def _tokenize(self, text: str):
        return set(
            re.findall(
                r"\w+",
                text.lower(),
            )
        )
    BAD_MIXES = {
        "visa": ["claude", "hackerrank","anthropic",],
        "claude": ["visa-emergency", "hackerrank","travel-support",],
        "devplatform": ["visa","claude","anthropic",],
    }
    ALIAS_MAP = {
        "hackerrank": "devplatform",
        "anthropic": "claude",
    }
    def rerank(self, query: str, results, company_hint=None, top_k: int = 5,):
        query_tokens = (self._tokenize(query))
        reranked = []
        normalized_hint = None
        if company_hint:
            normalized_hint = (company_hint.lower().strip())
            normalized_hint = self.ALIAS_MAP.get(normalized_hint, normalized_hint)
        for r in results:
            text_tokens = (
                self._tokenize(
                    r["text"]
                )
            )
            overlap = len(
                query_tokens.intersection(
                    text_tokens
                )
            )
            exact_phrase_boost = 0
            if len(query.split()) > 3 and query.lower() in r["text"].lower():
                exact_phrase_boost = 5
            path_boost = 0
            path = r["path"].lower()
            # BOOST REFUND DOCS
            if "refund" in path and (not company_hint  or company_hint.lower() in r.get("company",  "" ).lower()):
                path_boost += 1
            # BOOST SUBSCRIPTION DOCS
            if "subscription" in path:
                path_boost += 2
            # BOOST BILLING DOCS
            if "billing" in path:
                path_boost += 2
            # PENALIZE LEGAL/PROMO DOCS
            if (
                "privacy" in path
                or "legal" in path
                or "sweepstakes" in path
            ):
                path_boost -= 4
            # PENALIZE GENERIC INDEX FILES
            if "index.md" in path:
                path_boost -= 5
            generic_terms = [ "faq", "overview", "general", "introduction",]
            if any(term in path for term in generic_terms):
                path_boost -= 2
            # COMPANY BOOST
            company_boost = 0
            if normalized_hint:
                result_company = (r.get("company", "").strip().lower())
                if normalized_hint in result_company:
                    company_boost += 8
            if normalized_hint:
                bad_terms = self.BAD_MIXES.get(
                    normalized_hint,
                    [],
                )
                if any(
                    term in path
                    for term in bad_terms
                ):
                    path_boost -= 8
                if (
                    normalized_hint == "visa"
                    and "claude" in path
                ):
                    path_boost -= 15
            final_score = (
                r["score"]
                + overlap
                + exact_phrase_boost
                + path_boost
                + company_boost
            )
            normalized_score = round(max(0.0, min(final_score, 100.0)), 4)
            reranked.append({
                **r,
                "rerank_score":
                    normalized_score,
            })
        reranked.sort(
            key=lambda x: (
                -x["rerank_score"],
                x.get("company", ""),
                x["path"],
                x["text"][:50],
            )
        )
        return reranked[:top_k]