# roanoke_benchmark
Data for a benchmark or sandbox travel model scenario in Roanoke, Virginia

## Motivation
The travel modeling community has long needed a benchmark scenario on which to implement and compare
model frameworks in a quantitative manner. For example, agencies often wish to know how improvements to
model sensitivity will affect model run time. This repository is intended to push us towards that
goal.

The focus of this exercise is specifically on *demand* models, and as such we are less concerned with 
the highway assignment steps. But these steps are critical for the interpretation and implementation of 
the demand model, so they cannot be ignored completely. Researchers who implement their models in this 
sandbox may use whichever of the several network engines that they have available.

## Contents
This repository contains several files that researchers can draw upon to generate their own scenarios. 
The files are compiled from and for the trip-based model developed by WSP for the Roanoke Valley Transportation 
Planning Organization (RVTPO), which oversees transportation planning efforts in the Roanoke, Virginia
metropolitan area. The files are provided courtesy of the Virginia Department of Transportation 
and the RVTPO.

The first set of files are drawn from the inputs to the travel model:
  - A **Highway network** labeled with vehicle counts as well as the trip-based model vehicle forecasts. This is stored in `network/` as a gmns-compliant network. The source files for this network (exports from the RVTPO model) are in `hwy/src`, and are created with the `py/network_creator.py` script.
  - A **Transit network** with accompanying ridership measures. The network is stored in `network/` as a gmns-compliant network. The source file for the GTFS routes is included in `transit/src`, and the script to convert the GTFS to GMNS is in the submodule `gtfs2gmns/`. `py/network.py` automatically adds the transit network into the highway network.
  - A topologically connected **Bicyle network**. This is included in the highway network.
  - A **Socioeconomic data** file with employment and aggregate household characteristics by TAZ, stored in `se/zones.csv`. (Under Development)
  - A **Traffic Analysis Zone** geojson file (Under Development)

A second set of files are outputs of the travel model:
  - **Travel time matrices**, saved in `skims/`, both as .omx and .csv files. Created using `py/network_skimmer.py`
  - **Passenger origin-destination matrices**(Under Development)
  - **Freight origin-destination matrices** (Under Development)
  - **Internal/External trip matrices** (Under Development)

These output files may be useful if researchers optionally wish to --- for example --- include freight
processes in the model steps or simply include them as background traffic.

### File formats
In general, tabular data is provided as plain text with comma-separated values and names in a header; a data
dictionary supplied with the file provides more attributes.
Geospatial data are provided as geojson files, and matrix files are provided in an OMX format. 
Network files are given as node / link tables formated to GMNS specifications.

## Report

If you implement the a model in this sandbox, we would kindly request for you to send us a report with the following information:
  - The name of the model and the organization behind the implementation.
  - The basic design of your model, including which elements are held constant with the Cache Valley model and
    any necessary information from the network or supply model.
  - Total model run time, broken down by model step and feedback cycle.
  - A report of model failure statistics
  - Assigned highway volumes at counted locations in a CSV file.
An example report is provided in this repository. 


# Applications

## Network skims from dbf and gtfs files.
1. Download this repository.
2. Add hwy dbf files into the `hwy` folder. The current file are for the Roanoke benchmark
3. Add gtfs files for the transit network in `transit`. Details on how to obtain these file is below.
4. Run the following code displayed here and or in `py/test.py`.

```
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
```

## Network_Creator.py
The network creator will convert dbf and gtfs formated files into gmns netowrk of link and node files. 

### Converting gtfs data to gmns
Thanks to [the ASU transportation lab](https://github.com/asu-trans-ai-lab/GTFS2GMNS/tree/main), gtfs transit data may be converted into gmns data. Network Creator handles the conversion at time of network creation. 

### Obtaining gtfs data
Transit authorities freely offer thier routes for any who would want it. 
Websites such as [Mobility Database](https://mobilitydatabase.org), [Transit Feeds](https://transitfeeds.com), and [Transit Land](https://www.transit.land/feeds) are good places to find this data. 
Learn more about gtfs [here](https://gtfs.org)

## Network_Skimmer
This simple python code will run the path4gmns submodule to create network skims based off of modes in the network. 

## EMME_netowrk
Creation of a EMME network from gmns data. Under Development

# API
Under Development

## Acknowledgements
Li, P. and Zhou, X. (2024, November 26). Path4GMNS. Forked from https://github.com/jdlph/Path4GMNS
Mr. Xiangyong Luo, Mrs. Fang Tang,  Dr. Xuesong Simon Zhou. gtfs2gmns. Forked from https://github.com/asu-trans-ai-lab/GTFS2GMNS.git 