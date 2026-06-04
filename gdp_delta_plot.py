"""
Plot delta(epsilon) for Gaussian-DP -> (epsilon, delta)-DP conversion.

From the conversion theorem:
    delta(eps) = Phi(A) - exp(eps) * Phi(B)
    A = -eps/eta + eta/2
    B = -eps/eta - eta/2
where Phi is the standard Gaussian CDF.
"""
import numpy as np
import pandas as pd
import plotly.express as px
import scipy.stats as stats

Phi = stats.norm.cdf

# Work directly in the normalized variable t = eps / eta^2.
# Substituting eps = t * eta^2 into the conversion:
#     A = -eps/eta + eta/2 =  eta * (1/2 - t)
#     B = -eps/eta - eta/2 = -eta * (1/2 + t)
#     delta = Phi(A) - exp(t * eta^2) * Phi(B)
t = np.linspace(0, 1.333, 1000)
etas = (5, 6, 7)

frames = []
for eta in etas:
    A = eta * (0.5 - t)
    B = -eta * (0.5 + t)
    delta = Phi(A) - np.exp(t * eta ** 2) * Phi(B)
    frames.append(pd.DataFrame({"x": t, "delta": delta, "eta": str(eta)}))

df = pd.concat(frames, ignore_index=True)

# Normalize x = eps/eta^2 -> regime boundaries collapse to 1/4 and 1 for all eta
fig = px.line(
    df, x="x", y="delta", color="eta",
    title="δ vs ε/η²  —  regimes line up for all η",
    labels={"x": "ε / η²", "delta": "δ", "eta": "η"},
)
# Linear y-axis; drop the rotated axis title and place δ upright above the axis
fig.update_yaxes(title_text="")
fig.update_xaxes(range=[0, 1.333])
fig.update_layout(
    title_x=0.5,  # center the title
    width=1200, height=603,
    legend=dict(x=0.97, y=0.97, xanchor="right", yanchor="top",
                bgcolor="rgba(255,255,255,0.6)", bordercolor="gray",
                borderwidth=1),  # legend inside the plot
)
fig.add_annotation(text="δ", xref="paper", yref="paper", x=-0.02, y=1.04,
                   showarrow=False, font=dict(size=16))

# Shade the three regimes once, in normalized coordinates
fig.add_vrect(x0=df["x"].min(), x1=0.25, fillcolor="rgba(214,39,40,0.10)",
              line_width=0, annotation_text="vacuous (δ≈1)",
              annotation_position="top left")
fig.add_vrect(x0=0.25, x1=1.0, fillcolor="rgba(255,193,7,0.15)",
              line_width=0, annotation_text="transition",
              annotation_position="top")
fig.add_vrect(x0=1.0, x1=df["x"].max(), fillcolor="rgba(44,160,44,0.10)",
              line_width=0, annotation_text="negligible (δ≈0)",
              annotation_position="top right")
fig.add_vline(x=0.25, line_dash="dot", line_color="gray")
fig.add_vline(x=1.0, line_dash="dot", line_color="gray")

fig.show()
fig.write_html("gdp_delta_regimes.html")

# Static 4:3 PNG via matplotlib (no headless-browser dependency)
import matplotlib.pyplot as plt

fig2, ax = plt.subplots(figsize=(12, 6.03))  # 1200x603 px at dpi=100
ax.axvspan(0, 0.25, color="tab:red", alpha=0.10)
ax.axvspan(0.25, 1.0, color="gold", alpha=0.15)
ax.axvspan(1.0, 1.333, color="tab:green", alpha=0.10)
ax.axvline(0.25, ls=":", color="gray")
ax.axvline(1.0, ls=":", color="gray")
for eta in etas:
    sub = df[df["eta"] == str(eta)]
    ax.plot(sub["x"], sub["delta"], label=f"η = {eta}")
ax.text(0.125, 0.5, "vacuous\n(δ≈1)", ha="center", va="center")
ax.text(0.625, 0.5, "transition", ha="center", va="center")
ax.text(1.17, 0.5, "negligible\n(δ≈0)", ha="center", va="center")
ax.set_xlim(0, 1.333)
ax.set_xlabel(r"$\epsilon\,/\,\eta^2$")
ax.set_ylabel(r"$\delta$", rotation=0, labelpad=12)
ax.set_title(r"$\delta$ vs $\epsilon/\eta^2$ — regimes line up for all $\eta$")
ax.legend(loc="upper right", framealpha=0.6)
# Top/bottom kept as before; left & right margins set to 50px (of 1200px width)
fig2.subplots_adjust(left=100/1200, right=1 - 50/1200, bottom=0.1202, top=0.9319)
fig2.savefig("assets/img/gdp_delta_regimes.png", dpi=100)
