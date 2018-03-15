#!/bin/sh                                                                                                          


docker volume create  robin_docker_assignment_vol
docker build  -t="robin_ubuntu_docker" .

docker run  -v robin_docker_assignment_vol:/iozone --name my_docker  -d robin_ubuntu_docker
docker cp my_docker:/www.iozone.org/src/stable/iozone_report.xls .
docker stop my_docker
docker rm my_docker
cp /var/lib/docker/volumes/robin_docker_assignment_vol/_data/iozone_report.xls copied_from_docker_volume_iozone_re\
port.xls
