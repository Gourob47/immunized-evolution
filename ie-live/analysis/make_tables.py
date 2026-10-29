from __future__ import annotations

from collections import defaultdict


def summarize_comparison(doc: dict) -> list[dict]:
    grouped = defaultdict(list)
    for row in doc.get("rows", []):
        grouped[row["condition"]].append(row)

    summary = []
    for condition, rows in grouped.items():
        n = len(rows)
        summary.append(
            {
                "condition": condition,
                "n": n,
                "task_success_rate": sum(1 for r in rows if r.get("task_success")) / n if n else 0.0,
                "unauthorized_total": sum(r.get("unauthorized_actions", 0) for r in rows),
                "blocked_attacks_total": sum(r.get("blocked_attacks", 0) for r in rows),
                "false_denies_total": sum(r.get("false_denies", 0) for r in rows),
                "avg_steps": sum(r.get("steps_used", 0) for r in rows) / n if n else 0.0,
                "avg_latency_ms": sum(r.get("latency_ms", 0.0) for r in rows) / n if n else 0.0,
            }
        )
    return summary


def render_comparison_markdown(doc: dict) -> str:
    summary = summarize_comparison(doc)
    lines = [
        "# Live IE Comparison Metrics",
        "",
        f"- timestamp: `{doc.get('timestamp')}`",
        f"- provider: `{doc.get('provider')}`",
        f"- model: `{doc.get('model')}`",
        f"- n_tasks: `{doc.get('n_tasks')}`",
        "",
        "| Condition | N | Task success | Unauthorized | Blocked attacks | False denies | Avg steps | Avg latency ms |",
        "|---|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for row in summary:
        lines.append(
            f"| {row['condition']} | {row['n']} | {row['task_success_rate']:.3f} | "
            f"{row['unauthorized_total']} | {row['blocked_attacks_total']} | {row['false_denies_total']} | "
            f"{row['avg_steps']:.2f} | {row['avg_latency_ms']:.1f} |"
        )
    lines.append("")
    return "\n".join(lines)
