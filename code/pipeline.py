from __future__ import annotations
import json
from typing import Dict, Any
from langdetect import detect
from code.classifiers.intent_classifier import (
    IntentClassifier,
)
from code.classifiers.product_area_classifier import (
    classify_product_area,
)
from code.classifiers.risk_classifier import (
    RiskClassifier,
)
from code.generation.response_generator import (
    ResponseGenerator,
)
from code.logs.logger import (
    PipelineLogger,
)
from code.retrieval.hybrid import (
    HybridSearch,
)
from code.safety.injection_detector import (
    InjectionDetector,
)
from code.safety.pii_detector import (
    PIIDetector,
)
from code.tools.tool_planner import (
    ToolPlanner,
)
from code.utils.parsing import (
    parse_issue,
    flatten_conversation,
    latest_user_message,
    normalize_whitespace,
)
from code.utils.query_expansion import (
    expand_query,
)
class SupportPipeline:
    def __init__(self):
        print(
            "\nINITIALIZING PIPELINE...\n"
        )
        self.logger = (
            PipelineLogger()
        )
        self.search_engine = (
            HybridSearch()
        )
        self.injection_detector = (
            InjectionDetector()
        )
        self.pii_detector = (
            PIIDetector()
        )
        self.intent_classifier = (
            IntentClassifier()
        )
        self.risk_classifier = (
            RiskClassifier()
        )
        self.tool_planner = (
            ToolPlanner()
        )
        self.generator = (
            ResponseGenerator()
        )
    def process_row(
        self,
        row: Dict[str, Any]
    ) -> Dict[str, Any]:
        print("===================")
        print("NEW TICKET")
        print("===================")
        subject = str(
            row.get("subject")
            or row.get("Subject")
            or ""
        ).strip()
        company = str(
            row.get("company")
            or row.get("Company")
            or ""
        ).strip()
        issue = str(
            row.get("issue")
            or row.get("Issue")
            or row.get("conversation")
            or row.get("Conversation")
            or ""
        ).strip()
        print("SUBJECT:")
        print(subject)
        print("COMPANY:")
        print(company)
        messages = parse_issue(
            issue
        )
        convo = flatten_conversation(
            messages
        )
        latest = latest_user_message(
            messages
        )
        if not latest:
            latest = issue
        ticket_text = (
            normalize_whitespace(
                f"{subject}\n"
                f"{company}\n"
                f"{convo}"
            )
        )
        query = (
            normalize_whitespace(
                expand_query(
                    f"{subject} "
                    f"{company} "
                    f"{latest}"
                )
            )
        )
        print("QUERY:")
        print(query)
        self.logger.log(
            f"QUERY: {query}"
        )
        try:
            language = detect(
                ticket_text
            )
        except Exception:
            language = "en"
        pii_result = (
            self.pii_detector.detect(
                ticket_text
            )
        )
        injection_result = (
            self.injection_detector.detect(
                ticket_text
            )
        )
        request_type = (
            self.intent_classifier.classify(
                ticket_text
            )
        )
        risk_level = (
            self.risk_classifier.classify(
                ticket_text,
                injection_detected = injection_result.is_adversarial,
                pii_detected=(
                    pii_result.pii_detected
                ),
            )
        )
        product_area = (
            classify_product_area(
                text=query,
                company=company,
            )
        )
        evidence = (
            self.search_engine.search(
                query=query,
                company_hint=company,
                top_k=5,
            )
        )
        print(
            f"EVIDENCE FOUND: "
            f"{len(evidence)}"
        )
        self.logger.log(
            f"EVIDENCE_COUNT: "
            f"{len(evidence)}"
        )
        if evidence:
            print("TOP RESULT:")
            print(
                evidence[0]["path"]
            )
            print("TOP SCORE:")
            print(
                evidence[0][
                    "rerank_score"
                ]
            )
            self.logger.log(
                f"TOP_RESULT: "
                f"{evidence[0]['path']}"
            )
        top_score = (
            evidence[0][
                "rerank_score"
            ]
            if evidence
            else 0.0
        )
        source_documents = list({
            d["path"]
            for d in evidence
        })
        escalated = False
        if (
            injection_result
            .is_adversarial
        ):
            escalated = True
        if risk_level in {
            "high",
            "critical",
        }:
            escalated = True
        if not evidence:
            escalated = True
        response = (
            self.generator.generate(
                ticket_text=ticket_text,
                evidence=evidence,
                product_area=product_area,
                request_type=request_type,
                risk_level=risk_level,
                escalated=escalated,
            )
        )
        actions = (
            self.tool_planner.plan(
                ticket_text,
                pii_result.pii_detected,
                risk_level,
                escalated,
            )
        )
        status = (
            "escalated"
            if escalated
            else "replied"
        )
        confidence_score = round(
            min(
                max(
                    0.50 + (top_score / 100),
                    0.45,
                ),
                0.92,
            ),

            2,
        )
        if escalated:
            confidence_score = min(
                confidence_score,
                0.75,
            )
        self.logger.log(
            f"STATUS: {status}"
        )
        self.logger.log(
            f"RISK_LEVEL: "
            f"{risk_level}"
        )
        self.logger.log(
            f"CONFIDENCE: "
            f"{confidence_score}"
        )
        self.logger.log(
            f"ACTIONS: "
            f"{actions}"
        )
        self.logger.log(
            "-" * 60
        )
        return {
            "status":
                status,
            "product_area":
                product_area,
            "response":
                response,
            "justification":
                (
                    f"risk={risk_level}; "
                    f"retrieval_score="
                    f"{round(top_score, 4)}"
                ),
            "request_type":
                request_type,
            "confidence_score":
                confidence_score,
            "source_documents":
                "|".join(
                    source_documents
                ),
            "risk_level":
                risk_level,
            "pii_detected":
                bool(
                    pii_result
                    .pii_detected
                ),
            "language":
                language,
            "actions_taken":
                json.dumps(
                    actions
                ),
        }