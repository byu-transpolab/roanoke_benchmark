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
  - A **Highway network** labeled with vehicle counts as well as the trip-based model vehicle forecasts. This is stored in `hwy/` as a gmns-compliant network. The source files for this network (exports from the RVTPO model) are in `hwy/src`, and are created with the `py/network.py` script.
  - A **Transit network** with accompanying ridership measures. This is stored in `transit/` as a gmns-compliant network. The source file for the GTFS routes is included in `transit/gtfs`, and the script to convert the GTFS to GMNS is in `py/gtfs2gmns_conversion.py`
  - A topologically connected **Bicyle network**. This is included in the highway network.
  - A **Socioeconomic data** file with employment and aggregate household characteristics by TAZ, stored in `se/zones.csv`.
  - A **Traffic Analysis Zone** geojson file

A second set of files are outputs of the travel model:
  - **Travel time matrices** 
  - **Passenger origin-destination matrices**
  - **Freight origin-destination matrices** 
  - **Internal/External trip matrices** 

These output files may be useful if researchers optionally wish to --- for example --- include freight
processes in the model steps or simply include them as background traffic.

### File formats
In general, tabular data is provided as plain text with comma-separated values and names in a header; a data
dictionary supplied with the file provides more attributes.
Geospatial data are provided as geojson files, and matrix files are provided in an OMX format. Network files 
are given as node / link tables but will be supplied as GMNS files in the future.

## Report

If you implement the a model in this sandbox, we would kindly request for you to send us a report with the following information:
  - The name of the model and the organization behind the implementation.
  - The basic design of your model, including which elements are held constant with the Cache Valley model and
    any necessary information from the network or supply model.
  - Total model run time, broken down by model step and feedback cycle.
  - A report of model failure statistics
  - Assigned highway volumes at counted locations in a CSV file.
An example report is provided in this repository. 


# Using the Dockerfile/Container
Docker runs a small computer on top of your operating OS, allowing you to run a machine isolated from your computer. This machine is linux based and should have no problem running on Linux, Mac, or Window OS. 
A basic understanding of linux and bash commands are needed to run these programs. [Here](https://www.freecodecamp.org/news/linux-command-line-bash-tutorial/) is a good place to start.

### Creating an Image from the Dockerfile
~~~
docker build -t IMAGENAME .
~~~

Here is the outline code for running a docker image. Run it in the terminal. Replace IMAGENAME with your own name for the docker image. The "." designates the current folder as the place that the dockerfile reads from. This file will also be pulled into the virtual machine, so leaving the dockerfile within the downloaded file will ensure all needed code will be present. 

### Running Containers and Mounting Data
To run the network analysis', your image needs to be turned into a contianer and your data needs to be linked to your container. This code is an outline for running the container. Below is an explanation of each piece and what needs to be changed. 
~~~
  docker run -it --name CONTAINERNAME --mount type=bind,source=/FILE/PATH/TO/DATA,target=/app/userdata IMAGENAME
~~~

"-d" may be added before "-it" if you don't want the container to run in your current terminal. It can still be acessed elsewhere even without this tag.

"-it" allows you to interact with your container once running.

"--name CONTAINERNAME" designates the continer's name. Replace **CONTAINERNAME**.

"--mount type=bind"  tells the continer what type of binding. 

"Source=/FILE/PATH/TO/DATA" Replace **/FILE/PATH/TO/DATA** with the full file path to your input data. Do not use relative path.

"target=/app/userdata" In the continer, this will be the folder where your input data can be found. If one wishes, 'userdata' may be changed to any desired name. To make navigation simpler, /app is used so that userdata will be found with the other data. 

"IMAGENAME" Replace this with the image you want to use to build the container.

### Mounted Data File
The mounted file acts as intermediaty between the host computer and the container. Files may be written to it at will. You do not need to rerun a container if you need to add or remove data from this file. 

# Applications
These are the current processes able to be run within the container.

## Converting .dbf files to .cvs
1. Open network.py and scroll to the bottom
2. Replace **input_dbf** and **inputn_dbf**  with your DBF file paths from your input data file.
3. Replace **output_csv** and **outputn_csv** with your desired CSV file paths
4. Run Code. 

## Converting gtfs data to gmns
Thanks to the folks at [the ASU transportation lab](https://github.com/asu-trans-ai-lab/GTFS2GMNS/tree/main), gtfs transit data may be converted into gmns data. 

### Obtaining gtfs data
Transit authorities freely offer thier routes for any who would want it. 
Websites such as [Mobility Database](https://mobilitydatabase.org), [Transit Feeds](https://transitfeeds.com), and [Transit Land](https://www.transit.land/feeds) are good places to find this data. 

Learn more about gtfs [here](https://gtfs.org)

### Conversion Steps 
1. Open the gtfs2gmns_conversion.py and scroll to the bottom.
2. Modify **input_path**, **output_path**, **transit_node_name**, and **transit_link_name** as needed. **time_period** may also be modified if only a certain period is desired.
3. Run code.