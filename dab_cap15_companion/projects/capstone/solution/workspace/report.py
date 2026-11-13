"""Page 6: an exportable summary of the whole analysis, as Markdown or a self-contained HTML page."""
import base64
import html
import io
from datetime import datetime

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

from . import charts

DISCLOSURE = ("AI-generated draft. Produced by a language model from the model output shown above; every "
              "figure was checked automatically against that output. Review before acting.")


def effects_chart_png(result, top: int = 10) -> bytes:
    """A horizontal bar chart of the largest coefficients, as PNG bytes."""
    charts.use_house_style()
    t = result.coefficients.head(top).iloc[::-1]
    fig, ax = plt.subplots(figsize=(7, 0.35 * len(t) + 1.2))
    colours = [charts.TEAL if c > 0 else charts.CORAL for c in t["coefficient"]]
    ax.barh(t["feature"], t["coefficient"], color=colours)
    ax.axvline(0, color=charts.INK, linewidth=0.8)
    ax.set_xlabel("Coefficient (per SD for numbers; vs reference for categories)")
    ax.set_title(f"Largest effects on {result.target}")
    ax.grid(axis="y", visible=False)
    ax.grid(axis="x", visible=True)
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=150, bbox_inches="tight")
    plt.close(fig)
    return buf.getvalue()


def md_table(df: pd.DataFrame) -> str:
    """A Markdown table without extra dependencies."""
    cols = [str(c) for c in df.columns]
    rows = [[f"{v:.3f}" if isinstance(v, float) else str(v) for v in r] for r in df.itertuples(index=False)]
    return "\n".join(["| " + " | ".join(cols) + " |", "|" + "---|" * len(cols)]
                     + ["| " + " | ".join(r) + " |" for r in rows])


def build_markdown(name, df, log, result, insight) -> str:
    """The report as Markdown. `insight` is (reply, problems) or None."""
    lines = [f"# Analysis report: {name}", "",
             f"Generated {datetime.now():%d %B %Y %H:%M} with the AI-Enhanced Predictive Analytics Workspace.", "",
             "## Data", f"- {len(df):,} rows and {df.shape[1]} columns after preparation.", ""]
    if log is not None and not log.empty:
        lines += ["## Preparation", md_table(log), ""]
    if result is not None:
        lines += ["## Model", f"- {result.kind.title()} regression predicting **{result.target}** from "
                  f"{len(result.features)} features: {', '.join(result.features)}.",
                  f"- Trained on {result.n_train:,} rows, tested on {result.n_test:,}."]
        lines += [f"- {k.replace('_', ' ')}: {v:.3f}" for k, v in result.metrics.items()] + [""]
        lines += ["### Largest effects", md_table(result.coefficients.head(10)), ""]
    if insight is not None:
        reply, problems = insight
        lines += ["## Recommendations", f"*{DISCLOSURE}*", ""]
        for i, rec in enumerate(reply.recommendations, 1):
            lines += [f"{i}. **{rec.title}.** {rec.detail} (evidence: {', '.join(f'{e:g}' for e in rec.evidence)})"]
        lines += ["", "**Caveats.** " + " ".join(reply.caveats), f"**Confidence:** {reply.confidence}.",
                  "**Validation:** " + ("all figures matched the model output." if not problems
                                        else f"{len(problems)} problem(s): " + "; ".join(problems)), ""]
    lines += ["## Limitations", "- Coefficients describe associations in past data, not causes.",
              "- Results apply to data like the training data; check before using on new populations."]
    return "\n".join(lines)


def build_html(markdown_text: str, chart_png: bytes | None) -> str:
    """A self-contained HTML page: the Markdown as preformatted sections, plus the chart inline."""
    body = []
    for block in markdown_text.split("\n\n"):
        if block.startswith("# "):
            body.append(f"<h1>{html.escape(block[2:])}</h1>")
        elif block.startswith("## ") or block.startswith("### "):
            head, _, rest = block.partition("\n")
            level = 2 if block.startswith("## ") else 3
            body.append(f"<h{level}>{html.escape(head.lstrip('# '))}</h{level}>")
            if rest:
                body.append(f"<pre>{html.escape(rest)}</pre>")
        else:
            body.append(f"<pre>{html.escape(block)}</pre>")
    if chart_png:
        img = base64.b64encode(chart_png).decode()
        body.insert(3, f'<img alt="Largest effects" style="max-width:100%" src="data:image/png;base64,{img}">')
    style = ("body{font-family:Inter,Arial,sans-serif;color:#1B2A41;max-width:900px;margin:2em auto;}"
             "h1,h2,h3{color:#1B2A41}pre{white-space:pre-wrap;font-family:inherit}")
    return f"<!DOCTYPE html><html><head><meta charset='utf-8'><title>Analysis report</title>" \
           f"<style>{style}</style></head><body>{''.join(body)}</body></html>"
