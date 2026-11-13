"""Figures 15.1 (architecture) and 15.8 (deployment pipeline). Run from the repository root."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

plt.style.use("shared/kb.mplstyle")
NAVY, TEAL, GOLD, GREY, CORAL = "#1B2A41", "#0E9AA7", "#A8841A", "#4A5561", "#C8553D"


def box(ax, x, y, w, h, title, lines, colour, fill="white", mono=False, size=7.8, tsize=9):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.35,rounding_size=1.0",
                                facecolor=fill, edgecolor=colour, linewidth=1.3))
    ax.text(x + w / 2, y + h - 1.8, title, ha="center", va="top", fontsize=tsize, fontweight="bold",
            color=NAVY, family="monospace" if mono else None)
    ax.text(x + w / 2, y + h - 5.2, "\n".join(lines), ha="center", va="top", fontsize=size, color=GREY,
            linespacing=1.35)


def arrow(ax, a, b, colour=GREY, style="-|>"):
    ax.add_patch(FancyArrowPatch(a, b, arrowstyle=style, mutation_scale=10, color=colour, lw=1.0))


# ---- 15.1 architecture
fig, ax = plt.subplots(figsize=(11, 6.2))
ax.set_xlim(0, 110)
ax.set_ylim(0, 62)
ax.axis("off")
pages = [("1 Data", "CSV, SQLite\nread-only SELECT"), ("2 Prepare", "cleaning options\nchange log"),
         ("3 Explore", "summaries\ncharts"), ("4 Model", "target, features\nlive metrics"),
         ("5 Insights", "grounded AI text\nvalidated, labelled"), ("6 Report", "HTML / Markdown\nexport")]
for i, (t, d) in enumerate(pages):
    x = 1 + i * 18.2
    box(ax, x, 44, 16, 14, t, d.split("\n"), GOLD if i in (0, 5) else TEAL, "#FBF5E6" if i in (0, 5) else "white")
    if i < 5:
        arrow(ax, (x + 16.3, 51), (x + 18, 51))
ax.text(55, 60.8, "views/  (one file per page; app.py holds only navigation)", ha="center", fontsize=8.5, color=NAVY)
ax.add_patch(FancyBboxPatch((1, 26), 107, 12, boxstyle="round,pad=0.3,rounding_size=1", facecolor="#EEF1F5",
                            edgecolor=NAVY, linewidth=1))
ax.text(54.5, 35.5, "st.session_state:  dataset  →  prepared  →  model  →  insights", ha="center",
        fontsize=9, color=NAVY, family="monospace")
ax.text(54.5, 30, "changing an earlier step clears the later ones, so no page shows results for old data",
        ha="center", fontsize=7.8, color=GREY, style="italic")
mods = [("data.py", "new"), ("loader.py", "P1"), ("cleaning.py", "P1"), ("profiling.py", "P1"), ("charts.py", "Ch 8, P1"),
        ("modelling.py", "new: Ch 11-12"), ("insights.py", "new"), ("llm_client.py", "Ch 14"), ("report.py", "new")]
for i, (m, src) in enumerate(mods):
    x = 1 + i * 12.05
    box(ax, x, 6, 10.6, 11, m, [src], CORAL if m in ("insights.py", "llm_client.py") else TEAL, mono=True, size=7.3, tsize=6.8)
ax.text(54.5, 0.5, "workspace/  package: plain functions, tested without Streamlit", ha="center", fontsize=8.5, color=NAVY)
for x in (9, 27, 45, 64, 82, 100):
    arrow(ax, (x, 43.3), (x, 38.6), style="<|-|>")
arrow(ax, (54.5, 25.4), (54.5, 17.6), style="<|-|>")
fig.savefig("chapters/ch15/figures/fig_15_1_architecture.png", dpi=200)
plt.close(fig)

# ---- 15.8 deployment pipeline
fig, ax = plt.subplots(figsize=(11, 4.2))
ax.set_xlim(0, 110)
ax.set_ylim(0, 40)
ax.axis("off")
steps = [("Your computer", ["app folder", "pytest passes", "requirements.txt", "no secrets in files"], GOLD, "#FBF5E6"),
         ("GitHub", ["public repository", "git push", ".gitignore keeps out", ".env, secrets.toml"], NAVY, "#EEF1F5"),
         ("Community Cloud", ["Create app: repo,", "branch, app.py path", "Advanced settings:", "Python 3.12, Secrets"], TEAL, "white"),
         ("Build", ["installs requirements", "starts streamlit run", "logs visible in", "Manage app"], TEAL, "white"),
         ("Public URL", ["…streamlit.app", "share in README", "and on LinkedIn", "redeploys on push"], GOLD, "#FBF5E6")]
for i, (t, lines, c, f) in enumerate(steps):
    x = 1 + i * 22
    box(ax, x, 10, 19, 22, t, lines, c, f, size=8)
    if i < 4:
        arrow(ax, (x + 19.4, 21), (x + 21.6, 21))
ax.text(55, 2, "Secrets typed into Community Cloud reach the app as st.secrets (and as environment variables); "
        "they never enter the repository", ha="center", fontsize=8, color=CORAL, style="italic")
fig.savefig("chapters/ch15/figures/fig_15_8_deployment.png", dpi=200)
print("wrote fig_15_1_architecture.png and fig_15_8_deployment.png")
