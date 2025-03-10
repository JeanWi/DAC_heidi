import adopt_net0 as adopt
import json
from pathlib import Path
import pandas as pd

# Create folder for results
results_data_path = Path("./userData")
results_data_path.mkdir(parents=True, exist_ok=True)
# Create input data path and optimization templates
input_data_path = Path("./caseStudies/dac")
input_data_path.mkdir(parents=True, exist_ok=True)
adopt.create_optimization_templates(input_data_path)

# Load json template
with open(input_data_path / "Topology.json", "r") as json_file:
    topology = json.load(json_file)
# Nodes
topology["nodes"] = ["n1"]
# Carriers:
topology["carriers"] = ["electricity", "heat", "CO2captured"]
# Investment periods:
topology["investment_periods"] = ["period1"]
# Save json template
with open(input_data_path / "Topology.json", "w") as json_file:
    json.dump(topology, json_file, indent=4)


# Load json template
with open(input_data_path / "ConfigModel.json", "r") as json_file:
    configuration = json.load(json_file)
# Change objective
configuration["optimization"]["objective"]["value"] = "costs_emissionlimit"
# Set emission limit:
configuration["optimization"]["emission_limit"]["value"] = -1000
# Set time aggregation settings:
# configuration["optimization"]["typicaldays"]["N"]["value"] = 30
# configuration["optimization"]["typicaldays"]["method"]["value"] = 1
# Set MILP gap
configuration["solveroptions"]["mipgap"]["value"] = 0.02
# Save json template
with open(input_data_path / "ConfigModel.json", "w") as json_file:
    json.dump(configuration, json_file, indent=4)

adopt.create_input_data_folder_template(input_data_path)

# Define node locations (here an exemplary location in the Netherlands)
node_locations = pd.read_csv(input_data_path / "NodeLocations.csv", sep=";", index_col=0)
node_locations.loc["n1", "lon"] = 5.5
node_locations.loc["n1", "lat"] = 52.5
node_locations.loc["n1", "alt"] = 10
node_locations.to_csv(input_data_path / "NodeLocations.csv", sep=";")

# Add DAC as a new technology
with open(input_data_path / "period1" / "node_data" / "n1" / "Technologies.json", "r") as json_file:
    technologies = json.load(json_file)
technologies["new"] = ["DAC_Adsorption"]
technologies["existing"] = {"PermanentStorage_CO2_simple": 1001}

with open(input_data_path / "period1" / "node_data" / "n1" / "Technologies.json", "w") as json_file:
    json.dump(technologies, json_file, indent=4)

# Copy over technology files
adopt.copy_technology_data(input_data_path)

# Define climate data
adopt.load_climate_data_from_api(input_data_path)

adopt.fill_carrier_data(input_data_path, value_or_data=10000, columns=['Import limit'], carriers=['electricity', 'heat'], nodes=["n1"])

#
# m = adopt.ModelHub()
# m.read_data(input_data_path)
# m.quick_solve()