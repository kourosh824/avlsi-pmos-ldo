import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import make_interp_spline

LDO_VAR = "cm"

INTERPOL = True

H_LINES_EN = False
H_LINES = [65, 2]

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

df = pd.read_csv(f'../csv/{LDO_VAR}_ldo/{LDO_VAR}_loop_phase.csv')

# Extract original X data
trim_x_orig = df["Loop Phase deg (iload=0.0005,trim_select=0) X"].values

# FIX 3: Use geomspace to generate 300 logarithmically spaced points instead of linspace
if INTERPOL:
    x_plot = np.geomspace(trim_x_orig.min(), trim_x_orig.max(), 300)
else:
    x_plot = trim_x_orig

y_plot = []
trim_title = [r"$V_{OUT} = 2.3V$", r"$V_{OUT} = 2.1V$", r"$V_{OUT} = 1.6V$"]

for i in range(3):
    y = df[f"Loop Phase deg (iload=0.0005,trim_select={i}) Y"].values
    if INTERPOL:
        # Create the spline function
        spl = make_interp_spline(trim_x_orig, y, k=3)
        # FIX 2: Evaluate the spline at the new log-spaced points!
        y_plot.append(spl(x_plot))
    else:
        y_plot.append(y)

# Initialize the figure
plt.figure(figsize=(8, 5))

# Plot each trim_select configuration
for i in range(3):
    # Use semilogx natively for better log-scale grid handling
    plt.semilogx(x_plot, y_plot[i], label=trim_title[i])

# Configure axes 
x_min = x_plot.min()
x_max = x_plot.max()
plt.gca().set_xlim(left=x_min, right=x_max)

plt.xlabel(r"Frequency (Hz)")
plt.ylabel(r"Loop Phase (deg)")

if H_LINES_EN:
    for ln in H_LINES:
        plt.hlines(y=ln, xmin=x_min, xmax=x_max, color='red', linestyle='--', alpha=0.8)

# Add grid and legend
plt.grid(True, which="both", linestyle="--", alpha=0.5)
plt.legend(loc="best")

# Render and save
plt.tight_layout()
# Ensure double quotes are used in f-string methods here as well
plt.savefig(f"../images/{LDO_VAR}_loop_phase.svg")
plt.show()