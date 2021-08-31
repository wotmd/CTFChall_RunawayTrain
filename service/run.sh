#!/bin/sh
docker build -t runtrain .
docker rm -f runtrain
docker run -d --name runtrain -p 31337:31337 runtrain