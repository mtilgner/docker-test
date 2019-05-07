# docker-test
A small toy project to test communication between docker containers. One container receives a string and writes it to a database on another container.

## Installation

### Prerequisites
You need to have docker and docker-machine installed. To inspect the database you need mongodb.

### Getting the image 
The first container will be running a Python Flask app to receive the string and forward it to the database. To build the image yourself, start docker:
```
systemctl start docker
```
Then from the `container1` directory build the image:
```
docker build -t "string-forwarder" .
```
Alternatively you can get the image from [dockerhub](https://hub.docker.com/r/jmtilgner/string-forwarder).

## Setting up the containers
Now you can set up the containers and run the test.

**Note** It is important for the database container to have `mongo-host-container` as its name or hostname, otherwise the other container won't find it (this is hardcoded). It is also neccessary to create a user-defined network, otherwise the containers won't have name resolution within their network.

### Running both containers on the same host
This is achieved by using a bridge network. First create the network on the host:
```
docker network create --driver bridge docker-test-nw
```
Then you can create the containers attached to this network:
```
docker run -d -p 5000:5000 --network "docker-test-nw" --name "string-forwarder" jmtilgner/string-forwarder:0.0.1
docker run -d -p 27017:27017 -v ~/data/db:/data/db --network "docker-test-nw" --name "mongo-host-container" mongo
```
Now you can send strings using
```
curl "http://localhost:5000/receive?string=foo"
``` 
Inspect the database by running
```
mongo localhost/stringDB
```
Then from the mongo prompt:
```
db.strings.find()
```

### Running on different hosts
You need to create two hosts running docker. This can be done locally or on an external provider. Use docker-machine to manage your hosts. Instructions can be found [here](https://blog.codeship.com/docker-machine-compose-and-swarm-how-they-work-together/) or [here](https://docs.docker.com/machine/examples/ocean/)

Then both hosts have to be [configured](https://www.digitalocean.com/community/tutorials/how-to-create-a-cluster-of-docker-containers-with-docker-swarm-and-digitalocean-on-ubuntu-16-04) as a _swarm_.

Now you can create a network spanning both hosts. From the swarm manager node do
```
docker network create --driver overlay --attachable docker-test-nw
```

Finally you can run each container on their own host. The commands are exactly the same as above. Note that this time `docker-test-nw` is an attachable overlay network. To access the containers you have to replace `localhost` with their node's IP address, e.g.:
```
curl "http://node_address_here:5000/receive?string=foo"
```

