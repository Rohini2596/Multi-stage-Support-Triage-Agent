from __future__ import annotations
import json
from typing import Dict, Any
from langdetect import detect
from langdetect import DetectorFactory
DetectorFactory.seed = 7
from code.classifiers.intent_classifier import (
    IntentClassifier,
)
from code.safety.unsupported_detector import (
    UnsupportedDetector,
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
from code.retrieval.confidence import (
    ConfidenceCalibrator,
)
from code.retrieval.router import (
    ProductRouter,
)
from code.safety.adversarial_detector import (
    AdversarialDetector,
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
            "INITIALIZING PIPELINE..."
        )
        self.logger = (
            PipelineLogger()
        )
        self.search_engine = (
            HybridSearch()
        )
        self.confidence_calibrator = (
            ConfidenceCalibrator()
        )
        self.unsupported_detector = (
            UnsupportedDetector()
        )
        self.product_router = (
            ProductRouter()
        )
        self.adversarial_detector = (
            AdversarialDetector()
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
        adversarial_result = (
            self.adversarial_detector.detect(
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
                injection_detected = adversarial_result.is_adversarial,
                pii_detected=(
                    pii_result.pii_detected
                ),
            )
        )
        SECURITY_KEYWORDS = [
            "hacked",
            "hack",
            "fraud",
            "stolen card",
            "security breach",
            "unauthorized transaction",
            "account takeover",
            "phishing",
            "scam",
        ]
        if any(
            keyword in ticket_text.lower()
            for keyword in SECURITY_KEYWORDS
        ):
            risk_level = "critical"
            self.logger.log("SECURITY_ESCALATION_TRIGGERED")
        product_area = (
            self.product_router.route(query)
        )
        if adversarial_result.is_adversarial:
            self.logger.log(
                f"ADVERSARIAL_ATTACK: "
                f"{adversarial_result.attack_type}"
            )
            self.logger.log(
                f"ATTACK_PATTERNS: "
                f"{adversarial_result.matched_patterns}"
            )

            self.logger.log(
                f"ATTACK_RISK_SCORE: "
                f"{adversarial_result.risk_score}"
            )
            safe_response = (
                "Your request contains unsafe or "
                "unauthorized instructions. "
                "This ticket has been escalated "
                "to a human support specialist."
            )
            return {
                "status": "escalated",
                "product_area": "security",
                "response": safe_response,
                "justification": (
                    f"Adversarial content detected: "
                    f"{adversarial_result.attack_type}"
                ),
                "request_type": "invalid",
                "confidence_score": 0.20,
                "source_documents": "",
                "risk_level": "critical",
                "pii_detected": bool(pii_result.pii_detected),
                "language": language,
                "actions_taken": json.dumps(["escalated_due_to_attack"]),
            }   
        evidence = (
            self.search_engine.search(
                query=query,
                company_hint=(None if product_area == "general" else product_area),
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
        retrieval_assessment = (
            self.confidence_calibrator.assess(evidence=evidence, risk_level=risk_level,))
        unsupported_result = (self.unsupported_detector.detect(text=ticket_text,retrieval_quality=(retrieval_assessment.retrieval_quality),top_score=top_score,))
        self.logger.log(
            f"UNSUPPORTED_DETECTED: "
            f"{unsupported_result.is_unsupported}"
        )
        self.logger.log(
            f"UNSUPPORTED_REASON: "
            f"{unsupported_result.reason}"
        )
        self.logger.log(
            f"TOP_SCORE: "
            f"{top_score}"
        )
        self.logger.log(
            f"RETRIEVAL_QUALITY: "
            f"{retrieval_assessment.retrieval_quality}"
        )
        self.logger.log(
            f"RETRIEVAL_REASON: "
            f"{retrieval_assessment.reason}"
        )
        source_documents = []
        seen_paths = set()
        for d in evidence:
            path = d["path"]
            if path not in seen_paths:
                seen_paths.add(path)
                source_documents.append(path)
        escalated = False
        self.logger.log(
            f"SOURCE_DOCS: "
            f"{source_documents[:3]}"
        )
        if risk_level == "critical":
            escalated = True
        elif (risk_level == "high") and retrieval_assessment.retrieval_quality in {"moderate", "weak"}:
            escalated = True
        elif retrieval_assessment.should_escalate:
            escalated = True
        elif (
            pii_result.pii_detected
            and request_type == "bug"
        ):
            escalated = True
        if unsupported_result.is_unsupported:
            escalated = True
            self.logger.log("UNSUPPORTED_TICKET_ESCALATION")
        self.logger.log(
            f"ESCALATED: {escalated}"
        )
        self.logger.log(
            f"FINAL_RETRIEVAL_QUALITY: "
            f"{retrieval_assessment.retrieval_quality}"
            )
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
                adversarial_result.is_adversarial,
            )
        )
        status = (
            "escalated"
            if escalated
            else "replied"
        )
        confidence_score = (
            retrieval_assessment.confidence_score
        )
        if escalated:
            confidence_score -= 0.10
        if risk_level in {"high", "critical"}:
             confidence_score -= 0.08
        confidence_score = max(0.20, min(confidence_score, 0.98))
        confidence_score = round(confidence_score, 2)
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
                    f"retrieval_quality="
                    f"{retrieval_assessment.retrieval_quality}; "
                    f"retrieval_reason="
                    f"{retrieval_assessment.reason}; "
                    f"retrieval_score="
                    f"{round(top_score, 4)}; "
                    f"evidence_count="
                    f"{len(evidence)}; "
                    f"pii="
                    f"{pii_result.pii_detected}; "
                    f"unsupported="
                    f"{unsupported_result.is_unsupported}; "
                    f"adversarial="
                    f"{adversarial_result.is_adversarial}"
                ),
            "request_type":
                request_type,
            "confidence_score":
                confidence_score,
            "source_documents":
                "|".join(
                    source_documents[:3]
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
                    actions, 
                    sort_keys=True
                ),
        }
        
        