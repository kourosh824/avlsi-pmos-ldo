# Capacitor-Less PMOS LDO Regulators in 130nm CMOS

This repository contains the complete design documentation, simulation data, and presentation materials for an academic VLSI project: **"A Comparative Analysis of Two Capacitor-Less LDO Topologies in 130nm CMOS Technology."**

The project focuses on the spec-driven co-design of two low dropout (LDO) regulators utilizing different Error Amplifier topologies (a 5T OTA and a Telescopic OTA) to meet strict constraints on quiescent current, low-frequency PSRR, and phase margin. A third topology (Current Mirror OTA) was also studied but was not added to the final report because it couldn't achieve all target specifications. You can see this third topology in the project's presentation.

## Project Target Specifications
* **Technology:** 130nm CMOS
* **Supply Voltage:** 3.0 V
* **Bias Current:** 5 μΑ
* **Load Specifications:** 500 µA max load, 50 pF load capacitance
* **Quiescent Current:** < 100 µA
* **Saturation Margin:** > 50 mV
* **Reference Voltage:** 1.2 V ± 1 %
* **Output Voltages:** 2.3 V, 2.1 V, 1.6 V
* **Compensation Capacitor:** < 7 pF
* **Phase Margin @ No-Load:** > 60°
* **Phase Margin @ Full-Load:** > 70°
* **Loop Gain @ 1 Hz:** > 50 dB
* **PSRR:** See project's report
* **Output-Referred Noise:** See project's report

## Repository Structure

* **`images/`** 
  Contains Python scripts utilizing `schemdraw` to programmatically generate circuit diagrams, alongside the exported scalable vector graphics (`.svg`) files used throughout the documentation.

* **`logbook/`** 
  Contains the `.tex` source and `.pdf` files for the project logbook. This documents the initial mathematical derivations, sizing strategies, and early design phases (Note: actively maintained during the primary design phase but superseded by the final report).

* **`presentation/`** 
  Contains the LaTeX (Beamer) source and final `.pdf` slides used for the project defense. This presentation was designed for an audience of professors, PhD candidates, and peer students.

* **`report/`** 
  Contains the comprehensive project report in LaTeX format and its compiled `.pdf`. It is formatted as an IEEE academic paper, detailing the theoretical framework, device sizing methodologies, AC/DC simulation results, and topological comparisons.

* **`simulations/`** 
  The core data directory containing:
  * Raw `.csv` data extracted directly from Cadence Virtuoso simulations.
  * Python plotting scripts (`matplotlib`) used to parse and visualize the simulation data.
  * The final IEEE-compliant `.svg` waveform plots incorporated into the report and presentation.

## Tools Used
* **Circuit Design & Simulation:** Cadence Virtuoso
* **Data Visualization & Schematics:** Python (`matplotlib`, `schemdraw`)
* **Typesetting:** LaTeX (`IEEEtran`, `Beamer`, `booktabs`)

## Author
**Kourosh N. Baygi**

National Technical University of Athens (NTUA)  
School of Electrical & Computer Engineering