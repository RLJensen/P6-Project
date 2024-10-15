# P6-Project

## Generateing Docker image
In order to create the docker image will a few environment variables be declared which is listed below, the ".env" file should be located in the root folder for the repository: <br />
GRAFANACLOUD_URL="your grafana URL" <br />
GRAGANACLOUD_USERNAME="your grafana username" <br />
GRAFANACLOUD_PASSWORD="your grafana password" <br />

#### Whisper Workload Specifics
The whisper workload uses an AI model which can be downloaded from their website, it is important to download a copy of the model into the repository in order to run the cluster offline except from communication to grafana cloud but that is handled by the fog node in our case anyways. Furthermore, can any whisper model be used larger models may produce more accurate results, but in our case the model size is used as a "tweaking method" for the complexity of the workload itself.

#### Operating System and CPU Architecture
We have used Ubuntu server as the operating system for each node, furthermore is the CPU architecture important for the docker file aswell depending on which IoT device the image will be containerized on, in our case we build the image to be containerized on an ARM architecture which will have to be declared the "docker build command". 
