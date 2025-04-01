FROM python:3.11.10-bullseye

#When building the image from this dockerfile using:
#      docker build -t IMAGENAME  .
#the "." will set the location of this dockerfile as where it will copy it's files.


#set the working directory
WORKDIR /app

#Install Dependencies
RUN pip install aequilibrae
RUN apt update -y      
RUN apt install -y libsqlite3-mod-spatialite
RUN apt install -y libspatialite-dev

#These are not a dependencies, but helps for visualization/ other processes in aequilibrae.
RUN pip install folium
RUN pip install matplotlib
RUN pip install mapclassify
RUN pip install timer

#Adds from working Directory to this file path.
COPY . /app

#Runs intro script at start up. To be utilized latter?
RUN chmod +x introduction.sh





# Code to build Continaer and code to run to start continer from an image. 
# docker build -t IMAGENAME .
# docker run -d -it --name CONTAINDERNAME --mount type=bind,source=/FILE/PATH/TO/DATA,target=/userdata IMAGENAME

#docker run -d -it --name linkrenumbering --mount type=bind,source=/Users/willicon/Desktop/test,target=/app/userdata test1 
# docker build -t test1 .