import path4gmns as pg

network_file =    'hwy' # 'data/ASU' #

#pg.download_sample_data_sets()
'''
from_node = 1
to_node =2




###### Find Shortest Path between two nodes ########

network = pg.read_network(length_unit='mi', speed_unit='mph', input_dir=network_file)
# node path from node 1 to node 2
print('\nshortest path (node id) from node to node , '
      +network.find_shortest_path(from_node, to_node))
# link path from node 1 to node 2
print('\nshortest path (link id) from node to node , '
      +network.find_shortest_path(from_node, to_node, seq_type='link'))
'''


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