import path4gmns_skim as pg
import numpy as np
import pandas as pd
import time
from joblib import Parallel, delayed  # Parallel processing

## Source Files ##
network_file = 'hwy'            # Source folder for link/node files
link_file = 'hwy/link.csv'      # Link File for calculations
node_file = 'hwy/node.csv'      # Node file for calculations

# Read link and node files
df_link = pd.read_csv(link_file)
df_node = pd.read_csv(node_file)


###### Find Shortest Path Network ########
# Read link and nodes into network
network = pg.read_network(length_unit='mi', speed_unit='mph', input_dir=network_file)

# Convert node IDs to NumPy array for efficiency
nodes = df_node.node_id.to_numpy()
num_nodes = len(nodes)

# Function to compute shortest paths for a single row (parallelized)
def compute_row_distances(row_node, nodes):
    return [network.find_shortest_path_value(row_node, col_node) for col_node in nodes]

# Parallel computation of matrix rows
def create_numpy_matrix_parallel(num_nodes, nodes):
    time_start_matrix_all = time.time()  # Start total stopwatch

    # Use joblib to parallelize row-wise computation
    matrix = Parallel(n_jobs=-1)(delayed(compute_row_distances)(row_node, nodes) for row_node in nodes)

    time_end_matrix_all = time.time()
    print(f'Matrix Creation Time: {time_end_matrix_all - time_start_matrix_all:.2f} s')

    return np.array(matrix)

# Create the matrix using parallel processing
matrix = create_numpy_matrix_parallel(num_nodes, nodes)

# Convert matrix to DataFrame for structured output
df_matrix = pd.DataFrame(matrix, index=nodes, columns=nodes)

# Save the matrix as a CSV file
output_file = "hwy/shortest_path_matrix.csv"   #Output file path for matrix
df_matrix.to_csv(output_file, index=True, header=True, float_format="%.6f")  # Save with 6 decimal precision
print(f"Matrix saved to {output_file}")
