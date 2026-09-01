import pandas as pd
import matplotlib.pyplot as plt

LDO_VAR = "5t"
METRIC = "Loop Phase" # PSRR / Loop Gain / Loop Phase / Noise

H_LINES = False
# Define your custom horizontal line values here
H_LINE_1 = 65
H_LINE_2 = 2

# Use Matplotlib's native MathText engine instead of external LaTeX
# This provides the exact same Computer Modern font without system dependencies
plt.rcParams.update({
    "text.usetex": False, 
    "font.family": "serif",
    "font.serif": ["cmr10"], # Computer Modern Roman natively
    "mathtext.fontset": "cm", # Computer Modern for math
    "axes.labelsize": 14,
    "font.size": 14,
    "legend.fontsize": 12,
    "xtick.labelsize": 12,
    "ytick.labelsize": 12,
    "axes.formatter.use_mathtext": True
})

# Load the dataset (update 'your_data.csv' to your actual filename)
df = pd.read_csv(f'../csv/{LDO_VAR}_ldo/{LDO_VAR}_{METRIC.lower().replace(' ', '_')}.csv')

# Initialize the figure
plt.figure(figsize=(8, 5))

# Plot each trim_select configuration
# Note: Underscores in labels are escaped for LaTeX compatibility
plt.plot(df["Loop Phase deg (iload=0.0005,trim_select=0) X"], 
         df["Loop Phase deg (iload=0.0005,trim_select=0) Y"], 
         label=r"$V_{OUT} = 2.3V$")

plt.plot(df["Loop Phase deg (iload=0.0005,trim_select=1) X"], 
         df["Loop Phase deg (iload=0.0005,trim_select=1) Y"], 
         label=r"$V_{OUT} = 2.1V$")

plt.plot(df["Loop Phase deg (iload=0.0005,trim_select=2) X"], 
         df["Loop Phase deg (iload=0.0005,trim_select=2) Y"], 
         label=r"$V_{OUT} = 1.6V$")

# Add custom horizontal lines
if H_LINES:
    plt.axhline(y=H_LINE_1, color='red', linestyle='--', alpha=0.8)
    plt.axhline(y=H_LINE_2, color='red', linestyle='--', alpha=0.8)

# Configure axes 
# PSRR graphs standardly use a logarithmic scale for the frequency axis
plt.xscale('log')
plt.xlabel(r"Frequency (Hz)")
plt.ylabel(r"deg")
plt.title(METRIC + r" ($I_{LOAD} = 500μA$)")

# Add grid and legend
plt.grid(True, which="both", linestyle="--", alpha=0.5)
plt.legend(loc="best")

# Render and save
plt.tight_layout()
plt.savefig(f"../images/{LDO_VAR}_{METRIC.lower().replace(' ', '_')}.svg")
plt.show()