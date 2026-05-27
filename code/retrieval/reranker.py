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
    def rerank(self, query: str, results, company_hint=None, top_k: int = 5,):
        query_tokens = (self._tokenize(query))
        reranked = []
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
            if query.lower() in (r["text"].lower()):
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
            company_penalty = 0
            if company_hint:
                result_company = ( r.get("company", "").strip().lower())
                if (
                    result_company == company_hint.strip().lower()
                ):
                    
                    company_boost += 15
                else:
                    company_penalty -= 25
            final_score = (
                r["score"]
                + overlap
                + exact_phrase_boost
                + path_boost
                + company_boost
                + company_penalty
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