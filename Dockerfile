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

#These are not a dependencies, but helps for visualization.
RUN pip install folium
RUN pip install matplotlib
RUN pip install mapclassify

#Adds from working Directory to this file path.
COPY . /app

RUN chmod +x introduction.sh

# An file that gives instructions on start up.
CMD ["./introduction.sh"]

# docker run -d -it --name CONTAINDERNAME --mount type=bind,source=/FILE/PATH/TO/DATA,target=/userdata CONTAINERNAME