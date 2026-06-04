# LIFT: Link-level Interrupted Flow Traffic dynamics simulation
Ying-Chuan Ni <br />
Traffic Engineering Group, Institute for Transport Planning and Systems, ETH Zurich

## Introduction
LIFT is the Python implementation of the mesoscopic link transmission model. It is specifically designed for road traffic environments in an urban network considering its interrupted flow dynamics. It overcomes the challenges in the aspect of multi-commodity flow (multiple OD paths) in macroscopic modeling and has lower computation requirement compared to microscopic simulation. In addition, it is able to consider some detailed driving behavior, such as turning and start-up delay, to enhance the simulation accuracy.

## Instructions

### Required package
- Python 3.1
- numpy
- matplotlib

### Configuration
In config.py, you can enter information regarding traffic dynamics, driving behavioral parameters, network layout, inflow demand, and post-processing setups. The parameters of the traffic model, including effective vehicle length, free-flow speed, backward wave speed, start-up reaction time, saturation flow, also need to be defined there.

### Model
model.py contains the model implemention. The model description can be found in the research paper at the bottom of the this README.md. 

### Post-processing and visualization
The post-processing and visualization include the evolutions of average link density and mean path speed. Note that the recording of travel time starts from the entry request of each vehicle instead of the actual entry time into the network so that the vertical queueing time caused by spillback can be considered.

### Run
main.py executes the simulation, post-processing, output storage, and visualization.

### Sample case study
The sample codes are based on a virtual 2X4 single-lane signalized road network, as shown in the picture below. Other detailed information, including the OD path composition and inflow demand, can also be found in the research paper.
![2X4_network_grid](https://github.com/user-attachments/assets/94f15cb4-b696-4765-affd-9b88afa2b2be)

## Note
In the current implementation, traffic dynamics and driving behavioral parameters, e.g., speed, reaction time, and saturation flow rate, etc., are fixed values which apply to all road links and vehicles.

## To cite
Ni, Y.-C., Kouvelas, A., & Makridis, M. A. (2026). Simulating link-level interrupted flow traffic dynamics and the comparison between different models for urban road networks. *Simulation Modelling Practice and Theory*, *147*, 103252.
https://doi.org/10.1016/j.simpat.2026.103252

## Contact information
For questions, please feel free to contact the author via email (ying-chuan.ni@ivt.baug.ethz.ch).

## Acknowledgement
The author would like to thank Szu-Tung Chen for supporting the code development.
