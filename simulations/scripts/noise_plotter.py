import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import make_interp_spline
import matplotlib.ticker as ticker # <--- REQUIRED FOR LOG GRIDS

LDO_VAR = "cm"

INTERPOL = True

H_LINES_EN = False
H_LINES = []

# Use Matplotlib's native MathText engine
plt.rcParams.update({
    "text.usetex": False, 
    "font.family": "serif",
    "font.serif": ["cmr10"], 
    "mathtext.fontset": "cm", 
    "mathtext.default": "rm",
    "axes.labelsize": 14,
    "font.size": 14,
    "legend.fontsize": 12,
    "xtick.labelsize": 12,
    "ytick.labelsize": 12,
    "axes.formatter.use_mathtext": True
})

df = pd.read_csv(f'../csv/{LDO_VAR}_ldo/{LDO_VAR}_noise.csv')

# Extract original X data
trim_x_orig = df["Noise (iload=0.0005,trim_select=0) X"].values

if INTERPOL:
    x_plot = np.geomspace(trim_x_orig.min(), trim_x_orig.max(), 300)
else:
    x_plot = trim_x_orig

y_plot = []
trim_title = [r"$V_{OUT} = 2.3V$", r"$V_{OUT} = 2.1V$", r"$V_{OUT} = 1.6V$"]

for i in range(3):
    y = df[f"Noise (iload=0.0005,trim_select={i}) Y"].values
    if INTERPOL:
        spl = make_interp_spline(trim_x_orig, y, k=3)
        y_plot.append(spl(x_plot))
    else:
        y_plot.append(y)

# Initialize the figure
plt.figure(figsize=(8, 5))

# Plot each trim_select configuration
for i in range(3):
    plt.semilogx(x_plot, y_plot[i], label=trim_title[i])

# Configure axes 
x_min = x_plot.min()
x_max = x_plot.max()
plt.gca().set_xlim(left=x_min, right=x_max)

plt.xlabel(r"Frequency (Hz)")
plt.ylabel(r"Output Noise $(dBV/\sqrt{Hz})$")

if H_LINES_EN:
    for ln in H_LINES:
        plt.hlines(y=ln, xmin=x_min, xmax=x_max, color='red', linestyle='--', alpha=0.8)

# Force Matplotlib to calculate 10 ticks per decade (major and minor)
plt.gca().xaxis.set_major_locator(ticker.LogLocator(base=10.0, numticks=15))
plt.gca().xaxis.set_minor_locator(ticker.LogLocator(base=10.0, subs=np.arange(2, 10), numticks=15))
plt.gca().xaxis.set_minor_formatter(ticker.NullFormatter()) # Hide minor tick labels

# Split the grid into major (solid) and minor (dashed) for clarity
plt.grid(True, which="major", linestyle="-", alpha=0.6)
plt.grid(True, which="minor", linestyle="--", alpha=0.3)
# ------------------------

plt.legend(loc="best")

plt.tight_layout()
# Fixed the single quotes in the f-string here as well
plt.savefig(f"../images/{LDO_VAR}_noise.svg")
plt.show()