import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

LDO_VAR = "cm"

H_LINES_EN = False
H_LINES = [2.3, 1.6]

# Matplotlib configuration for IEEE LaTeX style (Computer Modern fonts)
plt.rcParams.update({
    "text.usetex": False, 
    "font.family": "serif",
    "font.serif": ["cmr10"], 
    "mathtext.fontset": "cm", 
    "mathtext.default": "rm",
    "axes.labelsize": 12,
    "font.size": 12,
    "legend.fontsize": 10,
    "xtick.labelsize": 10,
    "ytick.labelsize": 10,
    "axes.formatter.use_mathtext": True
})

# Load both datasets
df_load = pd.read_csv(f'../csv/{LDO_VAR}_ldo/{LDO_VAR}_tran_load.csv')
df_noload = pd.read_csv(f'../csv/{LDO_VAR}_ldo/{LDO_VAR}_tran_noload.csv')

# Clean data (convert to numeric, turn strings into NaN)
df_load = df_load.apply(pd.to_numeric, errors='coerce')
df_noload = df_noload.apply(pd.to_numeric, errors='coerce')

trim_title = [r"$V_{OUT} = 2.3V$", r"$V_{OUT} = 2.1V$", r"$V_{OUT} = 1.6V$"]

# Initialize a stacked figure sharing the X-axis
fig, (ax_load, ax_noload) = plt.subplots(2, 1, figsize=(6, 6), sharex=True)

# Variables to track the absolute min and max time across all curves (in us)
global_x_min = float('inf')
global_x_max = float('-inf')

# Plot each trim_select configuration
for i in range(3):
    # --- LOAD PLOT (500uA) ---
    xl_col = f"Vout (iload=0.0005,trim_select={i}) X"
    yl_col = f"Vout (iload=0.0005,trim_select={i}) Y"
    
    curve_load = df_load[[xl_col, yl_col]].dropna()
    xl_vals = curve_load[xl_col].values * 1e6
    yl_vals = curve_load[yl_col].values
    
    ax_load.plot(xl_vals, yl_vals, label=trim_title[i])
    
    # --- NO-LOAD PLOT (0A) ---
    # Based on your previous prompt, iload is exactly 0 in the column headers for noload
    xn_col = f"Vout (iload=0,trim_select={i}) X"
    yn_col = f"Vout (iload=0,trim_select={i}) Y"
    
    curve_noload = df_noload[[xn_col, yn_col]].dropna()
    xn_vals = curve_noload[xn_col].values * 1e6
    yn_vals = curve_noload[yn_col].values
    
    ax_noload.plot(xn_vals, yn_vals, label=trim_title[i])
    
    # Track limits for the shared X-axis
    global_x_min = min(global_x_min, xl_vals.min(), xn_vals.min())
    global_x_max = max(global_x_max, xl_vals.max(), xn_vals.max())

# --- CONFIGURE AXES & STYLING ---

# Configure Load Subplot
ax_load.set_ylabel(r"Output Voltage (V)")
ax_load.set_title(r"$I_{LOAD} = 500\mu A$")

# Configure No-Load Subplot
ax_noload.set_ylabel(r"Output Voltage (V)")
ax_noload.set_xlabel(r"Time ($\mu s$)")
ax_noload.set_title(r"$I_{LOAD} = 0A$")

# Apply global boundaries and grids to BOTH subplots
for ax in [ax_load, ax_noload]:
    ax.set_xlim(left=global_x_min, right=global_x_max)
    
    if H_LINES_EN:
        for ln in H_LINES:
            ax.hlines(y=ln, xmin=global_x_min, xmax=global_x_max, color='red', linestyle='--', alpha=0.8)
            
    # Explicitly turn on minor ticks for linear scale
    ax.minorticks_on()
    ax.grid(True, which="major", linestyle="-", alpha=0.6)
    ax.grid(True, which="minor", linestyle="--", alpha=0.3)

# Add legend only to the top plot to save space
ax_load.legend(loc="best")

# Render and save
plt.tight_layout(h_pad=0.5)
plt.savefig(f"../images/{LDO_VAR}_tran.svg")
plt.show()