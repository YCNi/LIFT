# LIFT: Link-level Interrupted Flow Traffic dynamics modeling
Ying-Chuan Ni <br />
Traffic Engineering Group, Institute for Transport Planning and Systems, ETH Zurich

## Introduction
LIFT is a mesoscopic model for urban traffic considering its interrupted flow dynamics. It overcomes the challenges in macroscopic modeling and has lower computation requirement compared to microscopic simulation.

## Instructions
### Building the network and adding inflow demand
The sample codes are using a virtual case study network, as shown in the picture below. The detailed information, including the OD path composition and inflow demand, can be found in the research paper at the bottom of the page.
![2X4_network_grid](https://github.com/user-attachments/assets/94f15cb4-b696-4765-affd-9b88afa2b2be)
In the LIFT_setup.py, you can find the way to enter the network and demand information. The parameters of the traffic model, including effective vehicle length, free-flow speed, backward wave speed, start-up reaction time, saturation flow, also need to be defined there.

### Running the simulation
After editing the LIFT_setup.py, use the LIFT_run.py to run the simulation.

### Visualizing the outcome
LIFT_plot.py includes the visualization of link density evolutions and mean path speed evolutions during the simulation period.

## Citing our work
To appear. Please stay tuned.

