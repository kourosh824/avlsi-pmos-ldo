import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

LDO_VAR = "5t"

H_LINES_EN = False
H_LINES = [2.3, 1.6]

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

df = pd.read_csv(f'../csv/{LDO_VAR}_ldo/{LDO_VAR}_tran_load.csv')

# Clean data (convert to numeric, turn strings into NaN)
df = df.apply(pd.to_numeric, errors='coerce')

trim_title = [r"$V_{OUT} = 2.3V$", r"$V_{OUT} = 2.1V$", r"$V_{OUT} = 1.6V$"]

# Initialize the figure
plt.figure(figsize=(8, 5))

# Variables to track the absolute min and max time across all curves (now in us)
global_x_min = float('inf')
global_x_max = float('-inf')

# Plot each trim_select configuration
for i in range(3):
    x_col = f"Vout (iload=0.0005,trim_select={i}) X"
    y_col = f"Vout (iload=0.0005,trim_select={i}) Y"
    
    # Isolate the curve and drop its specific NaNs
    curve_df = df[[x_col, y_col]].dropna()
    
    # Extract vectors and CONVERT time to microseconds (multiply by 1e6)
    x_vals = curve_df[x_col].values * 1e6
    y_vals = curve_df[y_col].values
    
    # Track limits for the axes
    global_x_min = min(global_x_min, x_vals.min())
    global_x_max = max(global_x_max, x_vals.max())
    
    # Plot using standard linear interpolation
    plt.plot(x_vals, y_vals, label=trim_title[i])

# Configure axes using the scaled microsecond limits
plt.gca().set_xlim(left=global_x_min, right=global_x_max)

# Update the label to show microseconds using LaTeX math mode
plt.xlabel(r"Time ($\mu s$)")
plt.ylabel(r"Output Voltage (V)")

if H_LINES_EN:
    for ln in H_LINES:
        plt.hlines(y=ln, xmin=global_x_min, xmax=global_x_max, color='red', linestyle='--', alpha=0.8)

# Explicitly turn on minor ticks for a linear scale
plt.minorticks_on()
plt.grid(True, which="major", linestyle="-", alpha=0.6)
plt.grid(True, which="minor", linestyle="--", alpha=0.3)

plt.legend(loc="best")

# Render and save
plt.tight_layout()
plt.savefig(f"../images/{LDO_VAR}_tran_load.svg")
plt.show()