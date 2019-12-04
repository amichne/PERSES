# Perses
## Water Infrastructure Component Failure Analysis Platform
Perses was written as a tool to understand, and perform analysis over, the differing rates of failure for city water infrascructure components. This mainly comes in the form of longitudal simulations (150 years was standard for the thesis paper), with rate-of-failure depending largely upon both the temperature profile of a simulation, and the failure curve used for the given component population.

The main functions are to allow a user to simulate a real-world hydraulic network, and recieve output regarding both the status of the network at a given temporal resolution, and component failures that occur in the system.
This allows analysis of failure rates of components, as well as the ability to realistically understand how these failures might affect "network outages", or the failure of the network to deliver water to demand nodes.

To read more about the research powered by this project, please refer to the [Manuscript](https://drive.google.com/open?id=1Wr1HyVtZFwwCHVUoKX5YsYZeiHx_1ISL)

Any questions can be addressed to austinmichne@gmail.com

## Simulation Inputs
* Valid EPAnet Network
* Component Populations (integer values defining the number of Iron Pipes, PVC Pipes, and Pump Motor/Electrical boxes)
* Component Failure Cumulative Failure Distributions (CDF) for each component populations (4 per simulation)
* Temperature-at-Surface Max Profile (in newline delimited format, a single float on a row indicating TasMax, where the index is the day the temperature occurs)
* Diurnal Temperature Profile (CSV format, with the columns ```day_n,T_min,T_max```. Diurnal interpolation is calculated in the simulation)
*Note: This includes all possible inputs for all three simulation types. Refer to simulation types to see what would be required for any specific simulation.

## Simulation Types
There are three simulation types available. 
### hydraulic_simulation
The "main" simulation with the true hydraulic processing found in EPAnet is located in ```hydraulic_simulation```

This simulation type allows a user to insert a network, a temperature profile with daily temperature-at-surface max (TasMax), and failure curves for each of the four component populations.

The results output to a MySQL database contain:
* Pressures at the time-interval designated in the EPAnet network configuration file, for the duration of the simulation
* Component failure times, ID's, and incidence

*Note: This simulation scales with threads, but due to the nature of EPAnet, longer runs on full size networks (10,000+ components for 150 years) can take upwards of 5-7 days, running on c5d.24xlarge AWS instances)*

### diurnal_simulation
This simulation DOES NOT include hydraulic calculations, but rather just calculates component failures. It does this using a more realistic method than what is available in either ```hydraulic_simulation``` or ```statistical_simulation```, using a method to estimate hourly temperature based of daily min and max temperatures.

It will run SIGNIFIGANTLY faster than ```hydraulic_simulation``` due to not including the EPAnet calculations, with full 100,000 component runs taking sub 2 hours even on a 2016 15" MacBook Pro.

The required inputs are a component population, component failure CDF's, and a diurnal temperature profile.

The results output to a MySQL database contain:
* Component failure times, ID's, and incidence

*Note: This simulation is preferred over ```statistical_simulation```, as it is simply more accurate, given you have access to the compatible diurnal profiles.

### statistical_simulation
This simulation DOES NOT include hydraulic calculations, but rather just calculates component failures. This does not to intra-day resolution simulations, as it is based on the assumption of the user only having access to the daily temperature-at-surface max temperature distributions.

The required inputs are a component population, component failure CDF's, and a TasMax temperature profile.

The results output to a MySQL database contain:
* Component failure times, ID's, and incidence

## Running a Simulation
Running a simulation is simple assuming you have Python 3.7 installed.

The package dependencies can be installed by running ```pip install -r requirement.txt``` in whichever directory you're looking to run a simulation type of.

After that, instantiate an instance of the ```Controller``` class (or ```MultiThreadController```), define the required attributes for your simulation type, and run the simulation using ```Controller.run()```


*Note: All sensitive data has been removed, much of which is required to run the project. Contact austinmichne@gmail.com if running the project is something you'd like to pursue.*


