
# Press windows+r, type cmd, and hit enter. To run the code using the EMME python, run "C:\Program Files\Bentley\OpenPaths\EMME 24.00.00\Python311\python.exe" "C:\Users\kmsquire\source\repos\roanoke_benchmark\py\Emme_network.py"


import pandas as pd
import inro.emme.desktop.app as _app
import inro.modeller as _m

# Define paths
emme_project = r"C:\Users\kmsquire\source\repos\roanoke_benchmark\EMME Network\Roanoke\Roanoke.emp"
nodes_file = r"C:\Users\kmsquire\source\repos\roanoke_benchmark\hwy\node.csv"
links_file = r"C:\Users\kmsquire\source\repos\roanoke_benchmark\hwy\link.csv"
use_group_file = r"C:\Users\kmsquire\source\repos\roanoke_benchmark\hwy\use_group.csv"

# Start EMME session
my_desktop = _app.start_dedicated(project=emme_project, visible=True, user_initials="KMS")
my_modeller = _m.Modeller(my_desktop)

# Load CSV data
nodes_df = pd.read_csv(nodes_file)
links_df = pd.read_csv(links_file)


#Do not delete any code above this

# Get active scenario and network
my_scenario = my_modeller.scenario
network = my_scenario.get_network()


# Create the modes table using the use_group_file

# Code
# Codey
# Coding
# Very nice code


# Create network fields if not already present
create_field = my_modeller.tool("inro.emme.data.network_field.create_network_field")

for column in nodes_df.columns:
    if column not in ["node_id"]:
        create_field(network_field_type="NODE", network_field_atype="REAL",
                     network_field_name=f"#{column}", network_field_description=column, overwrite=True)

for column in links_df.columns:
    if column not in ["link_id", "from_node_id", "to_node_id", "directed", "allowed_uses"]:
        create_field(network_field_type="LINK", network_field_atype="REAL",
                     network_field_name=f"#{column}", network_field_description=column, overwrite=True)

# Add nodes
for _, row in nodes_df.iterrows():
    node = network.create_node(row["node_id"], is_centroid=row["is_centroid"])
    for column in nodes_df.columns:
        if column not in ["node_id", "is_centroid"]:
            node[f"#{column}"] = row[column]

# Get valid mode IDs in scenario
defined_modes = {mode.id for mode in my_scenario.modes()}

# Add links
for _, row in links_df.iterrows():
    from_node = network.node(row["from_node_id"])
    to_node = network.node(row["to_node_id"])

    if from_node and to_node:  # Ensure both nodes exist
        modes = "".join([char for char in str(row["allowed_uses"]) if char in defined_modes])
        if not modes:
            modes = "a"  # Default mode if none valid

        link = network.create_link(row["from_node_id"], row["to_node_id"], modes=modes)
        
        for column in links_df.columns:
            if column not in ["link_id", "from_node_id", "to_node_id", "directed", "allowed_uses"]:
                link[f"#{column}"] = row[column]

# Save network
my_scenario.publish_network(network)
print("Network successfully created.")