import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# -----------------------------
# 1. Load Data
# -----------------------------
df = pd.read_csv("master.csv")

df["log2Error"] = pd.to_numeric(df["log2Error"], errors="coerce")
df = df.dropna(subset=["log2Error", "condition"])

# -----------------------------
# 2. Compute Means
# -----------------------------
summary = (
    df.groupby("condition")["log2Error"]
    .mean()
    .reset_index()
    .rename(columns={"log2Error": "mean_log2Error"})
)

# -----------------------------
# 3. Bootstrap 95% CI
# -----------------------------
def bootstrap_ci(data, n_boot=10000):
    means = []
    n = len(data)
    for _ in range(n_boot):
        sample = np.random.choice(data, size=n, replace=True)
        means.append(np.mean(sample))
    lower = np.percentile(means, 2.5)
    upper = np.percentile(means, 97.5)
    return lower, upper

ci_lower = []
ci_upper = []

for cond in summary["condition"]:
    values = df[df["condition"] == cond]["log2Error"].values
    lower, upper = bootstrap_ci(values)
    ci_lower.append(lower)
    ci_upper.append(upper)

summary["ci_lower"] = ci_lower
summary["ci_upper"] = ci_upper

# -----------------------------
# 4. Rank Best → Worst
# -----------------------------
summary = summary.sort_values("mean_log2Error").reset_index(drop=True)

# -----------------------------
# 5. Plot (Cleveland Style)
# -----------------------------
plt.figure()

y_positions = np.arange(len(summary))

plt.errorbar(
    summary["mean_log2Error"],
    y_positions,
    xerr=[
        summary["mean_log2Error"] - summary["ci_lower"],
        summary["ci_upper"] - summary["mean_log2Error"]
    ],
    fmt='o'
)

plt.yticks(y_positions, summary["condition"])
plt.xlabel("Mean log2Error")
plt.title("Visualization Performance (Lower is Better)")
plt.gca().invert_yaxis()

plt.tight_layout()

plt.savefig(
    "C:\\Users\\liliy\\OneDrive\\Desktop\\Data_Vis_HW\\a3-experiment\\img\\visualization_performance.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()