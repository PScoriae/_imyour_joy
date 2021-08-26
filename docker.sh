#!/bin/bash

# automates docker image creation and push to local registry.

docker build -t imyourjoy .
docker tag push imyourjoy 192.168.0.154:5000/imyourjoy
docker push 192.168.0.154:5000/imyourjoy