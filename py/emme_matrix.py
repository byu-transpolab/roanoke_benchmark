#Create an empty EMME network

import pandas as pd
import numpy as np
import time
import inro.emme.desktop.app as _app
import inro.modeller as _m
import inro.emme.matrix as matrix




# Define paths
emme_project = r"C:\Users\kmsquire\source\EMME networks\Roanoke\Roanoke.emp"
nodes_file = r"C:\Users\kmsquire\source\repos\roanoke_benchmark\network\node.csv"
links_file = r"C:\Users\kmsquire\source\repos\roanoke_benchmark\network\link.csv"
use_group_file = r"C:\Users\kmsquire\source\repos\roanoke_benchmark\network\use_group.csv"

# Start EMME session
my_desktop = _app.start_dedicated(project=emme_project, visible=True, user_initials="KMS")
my_modeller = _m.Modeller(my_desktop)


# Get active scenario and network
my_scenario = my_modeller.scenario
network = my_scenario.get_network()


#Set Emmebank and zones
emmebank = my_modeller.emmebank
zones = my_scenario.zone_numbers


def create_network(links_file, nodes_file, use_group_file):
    start_time = time.time()
    # Load CSV data
    nodes_df = pd.read_csv(nodes_file)
    links_df = pd.read_csv(links_file)
    modes_df = pd.read_csv(use_group_file)

    #Delete any existing links, nodes, and modes.
    for i, row in nodes_df.iterrows():
        if network.node(row['node_id']):  # Check if the node exists
            network.delete_node(id=row['node_id'], cascade=True)

    for i, row in modes_df.iterrows():
        if network.mode(row['mode']):  # Check if the mode exists
            network.delete_mode(id=row['mode'], cascade=True)

    for i, row in links_df.iterrows():
        if network.link(row['from_node_id'], row['to_node_id']):  # Check if the link exists
            network.delete_link(i_node_id=row['from_node_id'], j_node_id=row['to_node_id'], cascade=True)


    #Create Modes table
    for _, row in modes_df.iterrows():
        mode = network.create_mode(id=row['mode'], type=row['type'])
        mode['description'] = row['description']  # Set description separately


    #Create Nodes
    for i, row in nodes_df.iterrows():
        node = network.create_node(id=row['node_id'],  is_centroid= row['is_centroid']) 
        node['x'] = row['x_coord']
        node['y'] = row['y_coord']
        node['data1'] = row['zone_id']


    #Turn NaN values into a string
    links_df['facility_type'] = links_df['facility_type'].fillna('').astype(str).str.strip()

    #Map the link_type if it is in a string in the link.csv file
    link_type_map = {
        'interstate_principal_freeway': 1,
        'minor_freeway': 2,
        'principal_arterial': 3,
        'major_arterial': 4,
        'minor_arterial': 5,
        'major_collector': 6,
        'minor_collector': 7,
        'local': 8,
        'highspeed_ramp': 9,
        'lowspeed_ramp': 10,
        'centroid_connector': 11,
        'external_station_connector': 12,
        'unknown_type': 13,
        'bus': 14,
        '': 15}

    #Create Links
    for _, row in links_df.iterrows():
        link = network.create_link(i_node_id=row['from_node_id'],j_node_id=row['to_node_id'],modes=row['allowed_uses'])
        link['num_lanes']=row['lanes']
        link['length']=row['length']
        link['type'] = link_type_map.get(row['facility_type'])
        link['data1'] = (row['length'] / row['free_speed'])* 60  #calculates fftt for imperial units


    #Publish the network
    my_scenario.publish_network(network)
    print ("Network succesfully imported!")
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Elapsed time: {elapsed_time:.2f} seconds")
    print("\n")

# ==== CREATE TRAVEL TIME MATRIX ====
def create_empty_matrix(emme_matrix_id):

    # Create index for matrix
    indices = [zones,zones]

    # Create matrix with 0s
    new_mat = matrix.MatrixData (indices, default_value=0, type='f')

    #print("New matrix indices=%s" % str(new_mat.indices))
    print("\n")
    #print("The new matrix value at O-D=(5,6) is %s " % str(new_mat.get(5,6)))
    
    existing_matrix = emmebank.matrix(emme_matrix_id)
    if existing_matrix is not None:
        print(f"Matrix with ID '{emme_matrix_id}' already exists. Over writting")
        existing_matrix.set_data(new_mat)
    else:
        matrix_new = emmebank.create_matrix(emme_matrix_id, 0)
        matrix_new.name = "zero_matrix"
        print(f"Matrix with ID '{emme_matrix_id}' created.")
        matrix_new.set_data(new_mat)

def read_into_emme(matrix_id, cost_matrix):
    emme_matrix = emmebank.matrix(matrix_id)
    emme_matrix.name = "skim"
    emme_matrix.set_numpy_data(cost_matrix)
    print("Travel skim saved to emme")
    

def network_skim(network, zones, link_costs, emme_matrix_id, excluded_links, id_mode):
    """ Creates network skim between all zones. 

    Args:
       
    """
    start_time = time.time()
    # Create empty matrix the size of the centorids.
    cost_matrix = np.full((len(zones), len(zones)), np.nan)
    print("Creating travel skim")

    for origin_idx, origin in enumerate(zones):

        if origin not in zones:
            continue

        # Don't know if you will work before I do again. It looks liek excluded nodes is ignored by the shortesttree function
        # Don't know why. The bit of code below deletes the links manually from the network
        # And then the network is recreated every time with a new mode. Don't know if this will acually work. SO far it doesn't
        # I also realized i have not impremented the different different fftt for the different modes
        # They all use the car speed at the moment. So that's a problem. 
        # You can try to implement that if you want, or I can next week.
        # You can look in path4gmns/path.py function find_shortest_path_network to see how I implemented it there


        #Deletes links in the network from the excluded_links list
        for link in excluded_links:
            if network.link(link.i_node,link.j_node) is not None:
                network.delete_link(link.i_node,link.j_node)
        

        #How many links remain in network.
        total_links = 0
        for link in network.links():
            total_links += 1
        print(total_links)


        network_tree = network.shortest_path_tree(origin, link_costs, excluded_links ) # Excluded links is not doing what it's suppose to. Wrong format???? The function ignores it.

        
        for dest_idx, dest in enumerate(zones):
            if dest == origin:
                cost_matrix[origin_idx, dest_idx] = 0 # Sets a zero time for zones going to themselves.
                continue

            try:
                node_cost = network_tree.cost_to_node(dest)
                cost_matrix[origin_idx, dest_idx] = node_cost  # Save cost in the matrix
            except KeyError:
                cost_matrix[origin_idx, dest_idx] = 0
                continue

    #Save matrix into EMME
    #read_into_emme(emme_matrix_id, cost_matrix)

    #Save the matrix to a csv file
    cost_df = pd.DataFrame(cost_matrix, index=zones, columns=zones)
    cost_df = cost_df.round(2) # Round Results to 2 decimal places
    output_file_name = "\cost_matrix_" + id_mode + ".csv" 
    cost_df.to_csv(output_dir + output_file_name , index=False)
    print(f"Saving travel skim to {output_file_name} ")
    
    # Print the elapsed time
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"\nElapsed time: {elapsed_time:.2f} seconds")
    print("\n")


def network_skim_by_modes(network, zones, link_costs, emme_matrix_id):
    # Find total number of links
    total_links = 0
    for link in network.links():
        total_links += 1

    # Initialize a list for each mode
    all_modes = list(network.modes())

    excluded_links = {}
    for mode in all_modes:
        excluded_links[mode] = []

    # Loop through all links in the network. Create exclusion lists
    for link in network.links():
        link_modes = list(link.modes)

        for mode in all_modes:  # Iterate over all modes
            if mode.id == "t" and mode not in link_modes: # For t, keeps the p mode links.
                if mode not in link_modes and not any(m.id == "p" for m in link_modes):
                    excluded_links[mode].append(link)
            elif mode not in link_modes:
                    excluded_links[mode].append(link)        

    # Print the number of excluded links for each mode
    for mode in excluded_links:
        num_links = len(excluded_links[mode])  # Get the number of excluded links for this mode
        print(f"-------- MODE {mode}--------")
        print(f"Number links for mode '{mode}': {total_links - num_links}") # Print out total links for this mode.
        print("\n")
        #print(excluded_links[mode])
        ex_links = excluded_links[mode]
        id_mode = mode.id
        create_network(links_file, nodes_file, use_group_file)
        network_skim(network, zones, link_costs, emme_matrix_id, ex_links, id_mode)

if __name__ == "__main__":
    matrix_number = 4
    output_dir =  r"C:\Users\kmsquire\source\repos\roanoke_benchmark\skims"

    emme_matrix_id = f"mf{matrix_number}"
    link_costs = "data1"  #Which column it is taking the cost from. data1 is the fftt

    #create_empty_matrix(emme_matrix_id)
    #create_network(links_file, nodes_file, use_group_file)

    network_skim_by_modes(network, zones, link_costs, emme_matrix_id)

    
    