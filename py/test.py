import network_creator as nt
import py.network_skimmer as ns

#Directories
hwy_src = 'hwy/src'     # hwy network dbf files
tran_src ='transit/src' # Transit network gtfs files
network_dir = 'network' # Location for saved network. 
output_dir = "skims"

# Output type
output_type = ".omx"  # Choose between ".csv", ".omx"

#Travel Time Cost Type
cost_type = "time" # Either time or distance

# Unit types
length_unit = 'mi'
speed_unit = "mph"

# Creates gmns netowrk from dbf file in hwy and gtfs files in transit
nt.create_network(hwy_src,tran_src, network_dir )

# Creates network skims based off modes in network
ns.skim_network(length_unit,speed_unit,network_dir,output_dir,output_type,cost_type)