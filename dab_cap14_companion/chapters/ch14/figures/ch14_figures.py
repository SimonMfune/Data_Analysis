"""Figures 14.1 (request/response flow) and 14.2 (llm_client design). Run from the repository root."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

plt.style.use("shared/kb.mplstyle")
NAVY, TEAL, GOLD, GREY, CORAL = "#1B2A41", "#0E9AA7", "#A8841A", "#4A5561", "#C8553D"


def box(ax, x, y, w, h, title, lines, colour, fill="white", mono=False, size=8):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.4,rounding_size=1.2",
                                facecolor=fill, edgecolor=colour, linewidth=1.4))
    ax.text(x + w / 2, y + h - 2.2, title, ha="center", va="top", fontsize=9.5, fontweight="bold",
            color=NAVY, family="monospace" if mono else None)
    ax.text(x + w / 2, y + h - 6, "\n".join(lines), ha="center", va="top", fontsize=size, color=GREY,
            linespacing=1.4)


def arrow(ax, a, b, label=None, dy=1.3, colour=GREY):
    ax.add_patch(FancyArrowPatch(a, b, arrowstyle="-|>", mutation_scale=11, color=colour, lw=1.1))
    if label:
        ax.text((a[0] + b[0]) / 2, (a[1] + b[1]) / 2 + dy, label, ha="center", fontsize=7.8, color=GREY,
                style="italic")


# ---- 14.1 request/response flow
fig, ax = plt.subplots(figsize=(10.5, 4.6))
ax.set_xlim(0, 105)
ax.set_ylim(0, 48)
ax.axis("off")
box(ax, 1, 22, 20, 22, "Your data", ["computed statistics", "or minimised text", "(never raw tables", "or personal data)"], GOLD, "#FBF5E6")
box(ax, 27, 22, 22, 22, "Prompt", ["system: role", "user: context, rules,", "data block, output", "format"], TEAL)
box(ax, 57, 22, 20, 22, "Provider API", ["counts input tokens", "model generates", "output tokens", "bills both"], NAVY, "#EEF1F5")
box(ax, 84, 22, 20, 22, "Reply", ["text (or JSON)", "token usage", "never trusted as is"], TEAL)
box(ax, 57, 1, 47, 15, "Validation (Section 14.8)", ["schema check  ·  numbers cross-checked against the data", "IDs exist  ·  agreement with known labels  ·  human sample"], CORAL, "#FBEDEA")
arrow(ax, (21.8, 33), (26.2, 33))
arrow(ax, (49.8, 33), (56.2, 33))
ax.text(53, 18.5, "sent over HTTPS\nwith your API key", ha="center", fontsize=7.8, color=GREY, style="italic")
arrow(ax, (77.8, 33), (83.2, 33))
arrow(ax, (94, 21.2), (94, 16.8))
arrow(ax, (56.2, 8.5), (11, 8.5), "accept, or retry / reject", dy=1.3)
arrow(ax, (11, 8.5), (11, 21.2))
fig.savefig("chapters/ch14/figures/fig_14_1_flow.png", dpi=200)
plt.close(fig)

# ---- 14.2 llm_client design
fig, ax = plt.subplots(figsize=(10.5, 5.2))
ax.set_xlim(0, 105)
ax.set_ylim(0, 56)
ax.axis("off")
box(ax, 1, 34, 24, 19, "Analysis code", ["client = get_client()", "client.complete(prompt,", "  system=...)"], GOLD, "#FBF5E6", mono=False)
box(ax, 33, 30, 38, 23, "LLMClient", ["one method: complete()", "retries 429 / 5xx with back-off", "optional disk cache (.llm_cache/)",
                                       "counts calls and tokens", "returns LLMResponse"], NAVY, "#EEF1F5", mono=True)
box(ax, 79, 34, 25, 19, ".env (never in Git)", ["LLM_PROVIDER", "LLM_MODEL", "OPENAI_API_KEY", "ANTHROPIC_API_KEY", "GOOGLE_API_KEY"], GOLD, "#FBF5E6", size=7.5)
arrow(ax, (25.8, 43), (32.2, 43))
arrow(ax, (78.2, 43), (71.8, 43))
ax.text(75, 31, "read by\nget_client()", ha="center", fontsize=7.8, color=GREY, style="italic")
names = [("MockProvider", ["offline, free", "deterministic", "mistakes=True"]),
         ("OpenAIProvider", ["responses.create", "output_text"]),
         ("AnthropicProvider", ["messages.create", "content blocks"]),
         ("GoogleProvider", ["models.generate_", "content, text"])]
for i, (title, lines) in enumerate(names):
    x = 2 + i * 26
    box(ax, x, 2, 23, 17, title, lines, TEAL if i else CORAL, mono=True, size=7.6)
    arrow(ax, (52, 29.2), (x + 11.5, 19.8))
ax.text(52, 23.5, "same interface: generate(prompt, system, model, max_tokens) -> text, tokens in, tokens out",
        ha="center", fontsize=7.8, color=GREY, style="italic",
        bbox={"facecolor": "white", "edgecolor": "none", "pad": 1})
fig.savefig("chapters/ch14/figures/fig_14_2_client_design.png", dpi=200)
print("wrote fig_14_1_flow.png and fig_14_2_client_design.png")
