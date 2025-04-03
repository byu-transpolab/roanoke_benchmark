# Archived Read.me information

## Using the Dockerfile/Container
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

## Aequilibrae Notes
- link types must have unique first letters, or the project creation will fail using create_from_gmns.
- Centroid_conntectors will fail to import, causing a unique constraint error. Rename the connectors to something else, following the above constraint. 
- Use group is requiried currently, not optional. 