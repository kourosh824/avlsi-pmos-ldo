import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import make_interp_spline
import matplotlib.ticker as ticker

LDO_VAR = "cm"
INTERPOL = True

# Matplotlib configuration for IEEE LaTeX style (Computer Modern fonts)
plt.rcParams.update({
    "text.usetex": False, 
    "font.family": "serif",
    "font.serif": ["cmr10"], 
    "mathtext.fontset": "cm", 
    "mathtext.default": "rm",
    "axes.labelsize": 12,   # Adjusted slightly for IEEE column width constraints
    "font.size": 12,
    "legend.fontsize": 10,
    "xtick.labelsize": 10,
    "ytick.labelsize": 10,
    "axes.formatter.use_mathtext": True
})

# Load datasets
df_gain = pd.read_csv(f'../csv/{LDO_VAR}_ldo/{LDO_VAR}_loop_gain.csv')
df_phase = pd.read_csv(f'../csv/{LDO_VAR}_ldo/{LDO_VAR}_loop_phase.csv')

# Extract original X data (Frequency)
trim_x_orig = df_gain["Loop Gain dB20 (iload=0.0005,trim_select=0) X"].values

if INTERPOL:
    x_plot = np.geomspace(trim_x_orig.min(), trim_x_orig.max(), 300)
else:
    x_plot = trim_x_orig

y_gain = []
y_phase = []
trim_title = [r"$V_{OUT} = 2.3V$", r"$V_{OUT} = 2.1V$", r"$V_{OUT} = 1.6V$"]

# Process Y data for both Gain and Phase
for i in range(3):
    yg = df_gain[f"Loop Gain dB20 (iload=0.0005,trim_select={i}) Y"].values
    yp = df_phase[f"Loop Phase deg (iload=0.0005,trim_select={i}) Y"].values
    
    if INTERPOL:
        spl_g = make_interp_spline(trim_x_orig, yg, k=3)
        spl_p = make_interp_spline(trim_x_orig, yp, k=3)
        y_gain.append(spl_g(x_plot))
        y_phase.append(spl_p(x_plot))
    else:
        y_gain.append(yg)
        y_phase.append(yp)

# Initialize the figure with 2 rows, 1 column, and a shared X-axis
# figsize=(3.5, 5) is commonly used for a single-column IEEE figure. 
# You can increase it to (6, 6) if the figure will span two columns.
fig, (ax_gain, ax_phase) = plt.subplots(2, 1, figsize=(6, 6), sharex=True)

# Plot Gain
for i in range(3):
    ax_gain.semilogx(x_plot, y_gain[i], label=trim_title[i])
ax_gain.set_ylabel(r"Loop Gain (dB)")

# Add a 0 dB reference line for the Gain plot (Phase Margin crossover point)
ax_gain.axhline(y=0, color='black', linestyle='-.', alpha=0.5, linewidth=1)

# Plot Phase
for i in range(3):
    ax_phase.semilogx(x_plot, y_phase[i], label=trim_title[i])
ax_phase.set_xlabel(r"Frequency (Hz)")
ax_phase.set_ylabel(r"Loop Phase ($^\circ$)")

# Add a 0 degree (or -180 depending on your simulator) reference line for phase
ax_phase.axhline(y=0, color='black', linestyle='-.', alpha=0.5, linewidth=1)

# Configure axes bounds and grids for BOTH subplots
x_min = x_plot.min()
x_max = x_plot.max()

for ax in [ax_gain, ax_phase]:
    ax.set_xlim(left=x_min, right=x_max)
    
    # Enforce logarithmic grids correctly
    ax.xaxis.set_major_locator(ticker.LogLocator(base=10.0, numticks=15))
    ax.xaxis.set_minor_locator(ticker.LogLocator(base=10.0, subs=np.arange(2, 10), numticks=15))
    ax.xaxis.set_minor_formatter(ticker.NullFormatter())
    
    # Apply grids
    ax.grid(True, which="major", linestyle="-", alpha=0.6)
    ax.grid(True, which="minor", linestyle="--", alpha=0.3)

# Add legend only to the top plot to avoid redundancy
ax_gain.legend(loc="best")

# Render and save
# h_pad minimizes the whitespace between the two vertically stacked plots
plt.tight_layout(h_pad=0.5)
plt.savefig(f"../images/{LDO_VAR}_bode_plot.svg")
plt.show()