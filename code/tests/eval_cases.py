EVAL_CASES = [

    {
        "query":
            "My Visa card was hacked",
        "domain":
            "visa",
        "should_escalate":
            True,
        "unsupported":
            False,
    },

    {
        "query":
            "Claude API rate limit exceeded",
        "domain":
            "claude",
        "should_escalate":
            False,
        "unsupported":
            False,
    },

    {
        "query":
            "Hackerrank SSO integration failing",
        "domain":
            "devplatform",
        "should_escalate":
            False,
        "unsupported":
            False,
    },

    {
        "query":
            "Quantum banana teleportation failed",
        "domain":
            "general",
        "should_escalate":
            True,
        "unsupported":
            True,
    },
]