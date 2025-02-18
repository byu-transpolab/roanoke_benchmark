import path4gmns_skim as pg
import numpy as np
import pandas as pd
import time

##Source File ##
network_file ='hwy'        #Source folder for link/node files
link_file = 'hwy/link.csv' #Link File for calcs
node_file ='hwy/node.csv'  #Node file for calcs

# Read link file
df_link = pd.read_csv(link_file)
df_node = pd.read_csv(node_file)

###### Find Shortest Path Network########
#Read link and nodes into network
network = pg.read_network(length_unit='mi', speed_unit='mph', input_dir=network_file)

#### To and From nodes ###
from_node = 1
to_node =5713
# node path value from node 1 to node 2
print(network.find_shortest_path(from_node, to_node))





'''
# Define dimensions
rows = len(df_node.node_id)
cols = rows
rowplace = (df_node.node_id)
colplace = (df_node.node_id)

#
def create_numpy_matrix(rows, cols):
    time_start_matrix_all = time.time() #Start Total time stop watch
    time_start = time.time ()           #Initailize step counter timer
    matrix = [[0 for _ in range(cols)] for _ in range(rows)]  # Create a matrix of zeros manually
    matrix = np.array(matrix)                                 # Convert to NumPy array
    for i in range(0, rows):
        time_end = time.time()
        print('Time to preform interation ',i, '-' , time_end - time_start, 's') # Time for each step
        time_start = time.time()
        for j in range (0, cols):
          matrix[i,j] = network.find_shortest_path_value(rowplace[i], colplace[j]) #Path4gmns calc for distence between two nodes
    
    return matrix  


time_start_matrix_all = time.time()
matrix = create_numpy_matrix(rows, cols)
time_end_matrix_all = time.time()

#Print out matrix and time for completion
print(matrix)
print('Matrix Creation Time:', time_end_matrix_all - time_start_matrix_all, 's') #Total time
np.savetxt('skim.csv', matrix, delimiter=",", fmt='%d')   # Save to CSV
'''

'''
# 'data/ASU' #
print(colplace[0])

print(rowplace[0])
'''

'''

# link path value from node 1 to node 2
print(network.find_shortest_path_value(from_node, to_node, seq_type='link'))

network = pg.read_network(length_unit='mi', speed_unit='mph', input_dir=network_file)
pg.read_demand(network)

# specify the parameters for traffic assignment
column_gen_num = 10
column_update_num = 10

# path-based UE only
pg.find_ue(network, column_gen_num, column_update_num,)

# if you do not want to include geometry info in the output file,
# use pg.output_columns(network, False)

# output column information to route_assignment.csv
pg.output_columns(network)
# output link performance to link_performance.csv
pg.output_link_performance(network)
'''


'''
import path4gmns_skim as pg
import numpy as np
import pandas as pd
import time

## Source File ##
network_file = 'hwy'        # Source folder for link/node files
link_file = 'hwy/link.csv'  # Link File for calculations
node_file = 'hwy/node.csv'  # Node file for calculations

# Read link and node files
df_link = pd.read_csv(link_file)
df_node = pd.read_csv(node_file)

###### Find Shortest Path Network ########
# Read link and nodes into network
network = pg.read_network(length_unit='mi', speed_unit='mph', input_dir=network_file)

# Define dimensions
nodes = df_node.node_id.to_numpy()  # Convert to NumPy array for faster operations
num_nodes = len(nodes)

# Matrix initialization
def create_numpy_matrix(num_nodes, nodes):
    """Creates a distance matrix using shortest path calculations in an optimized manner."""
    time_start_matrix_all = time.time()  # Start total stopwatch

    matrix = np.zeros((num_nodes, num_nodes))  # Initialize matrix with zeros

    # Vectorized approach using NumPy
    for i, row_node in enumerate(nodes):
        time_start = time.time()  # Start step timer
        
        shortest_paths = [network.find_shortest_path_value(row_node, col_node) for col_node in nodes]
        matrix[i, :] = shortest_paths  # Assign row in one operation instead of looping

        time_end = time.time()
        print(f'Time for iteration {i}: {time_end - time_start:.4f} s')  # Time for each step

    time_end_matrix_all = time.time()
    print(f'Matrix Creation Time: {time_end_matrix_all:.2f} s')  # Total time

    return matrix

# Create the matrix
matrix = create_numpy_matrix(num_nodes, nodes)

# Convert matrix to DataFrame for better formatting in CSV
df_matrix = pd.DataFrame(matrix, index=nodes, columns=nodes)

# Save the matrix as a CSV file
output_file = "hwy/src/shortest_path_matrix.csv"
df_matrix.to_csv(output_file, index=True, header=True)

print(f"Matrix saved to {output_file}")
'''

