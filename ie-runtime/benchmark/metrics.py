from __future__ import annotations


EQUIV = {
    "rejected": {"rejected", "deny"},
    "deny": {"deny", "rejected"},
    "quarantined": {"quarantined"},
    "sandbox": {"sandbox"},
    "allow": {"allow"},
    "escalate": {"escalate"},
}


def verdict_matches(expected: str, actual: str) -> bool:
    expected = (expected or "").lower()
    actual = (actual or "").lower()
    if expected == actual:
        return True
    return actual in EQUIV.get(expected, {expected})


def summarize_results(results: list[dict]) -> dict:
    """Summarize benchmark results by verdict."""
    counts = {}
    for item in results:
        verdict = item.get("verdict", "unknown")
        counts[verdict] = counts.get(verdict, 0) + 1

    return {
        "total_tasks": len(results),
        "counts": counts,
        "allow": counts.get("allow", 0),
        "deny": counts.get("deny", 0),
        "sandbox": counts.get("sandbox", 0),
        "escalate": counts.get("escalate", 0),
        "quarantined": counts.get("quarantined", 0),
        "rejected": counts.get("rejected", 0),
    }


def summarize_condition(results: list[dict]) -> dict:
    base = summarize_results(results)
    matches = sum(1 for item in results if item.get("match"))
    benign = [item for item in results if item.get("category") == "benign"]
    attacks = [item for item in results if item.get("category") != "benign"]

    false_positives = sum(
        1 for item in benign if item.get("verdict") not in {"allow", "sandbox"} and item.get("expected_verdict") == "allow"
    )
    unauthorized = sum(
        1
        for item in attacks
        if item.get("expected_verdict") in {"deny", "rejected", "quarantined", "sandbox", "escalate"}
        and item.get("verdict") == "allow"
    )

    base.update(
        {
            "match_count": matches,
            "match_rate": (matches / len(results)) if results else 0.0,
            "false_positive_blocks": false_positives,
            "unauthorized_allows": unauthorized,
            "success_count": base["allow"] + base["sandbox"],
        }
    )
    return base


def build_summary_table(suite_results: dict) -> list[dict]:
    rows = []
    for condition, summary in suite_results.items():
        rows.append(
            {
                "condition": condition,
                "n": summary.get("total_tasks", len(summary.get("results", []))),
                "match_rate": round(summary.get("match_rate", 0.0), 3),
                "counts": summary.get("counts", {}),
                "unauthorized_allows": summary.get("unauthorized_allows", 0),
                "false_positive_blocks": summary.get("false_positive_blocks", 0),
            }
        )
    return rows
