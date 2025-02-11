import path4gmns as pg

network_file = 'hwy' # 'data/ASU' #

#pg.download_sample_data_sets()

from_node = 1399
to_node = 1102




''' Find Shortest Path between two nodes'''
network = pg.read_network(length_unit='mi', speed_unit='mph', input_dir=network_file)
# node path from node 1 to node 2
print('\nshortest path (node id) from node to node , '
      +network.find_shortest_path(from_node, to_node))
# link path from node 1 to node 2
print('\nshortest path (link id) from node to node , '
      +network.find_shortest_path(from_node, to_node, seq_type='link'))




