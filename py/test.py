import network_creator as nt
import py.network_skimmer as ns
import path4gmns as pg
from GTFS2GMNSII import gtfs2gmns as gg

#Directories
hwy_src = 'src/roanoke/hwy'     # hwy network dbf files
tran_src ='src/roanoke/transit' # Transit network gtfs files
network_dir = 'network/roanoke' # Location for saved network. 
output_dir = "skims/roanoke"

# Output type
output_type = ".csv"  # Choose between ".csv", ".omx"

#Travel Time Cost Type
cost_type = "time" # Either time or distance
transit_time_period = '0000_2359' 

# Unit types
length_unit = 'mi'
speed_unit = "mph"

#network = pg.read_network(length_unit, speed_unit, network_dir)
#print(network.find_shortest_path(1,2, "node", "distance"))

gg.gtfs2gmns(tran_src, f"{network_dir}/transit", transit_time_period)

# Creates gmns netowrk from dbf file in hwy and gtfs files in transit
#nt.create_network(hwy_src,tran_src, network_dir ) 

# Creates network skims based off modes in network
#ns.skim_network(length_unit,speed_unit,f"{network_dir}/hwy",output_dir,output_type,cost_type)
#ns.skim_network(length_unit,speed_unit,f"{network_dir}/transit",output_dir,output_type,cost_type)
