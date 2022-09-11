#!/bin/bash
export CITKSNAP_URI=citksnap://image_file=/mydownloads/2020-fibrosis/dcm,segmentation_file=/mydownloads/2020-fibrosis/nice.nii.gz

echo "run below in docker to debug"
echo bash launcher.sh "$"CITKSNAP_URI

xhost +
export LIBGL_ALWAYS_INDIRECT=1

docker volume create \
    --driver local \
    --opt type=none \
    --opt o=bind \
    --opt device=/home/${USER}/Downloads \
    --name mydownloads

docker run -it --rm --privileged --net=host --ipc=host \
    -e DISPLAY -e QT_X11_NO_MITSHM=1 -v /tmp/.X11-unix \
    -u "$(id -u):$(id -g)" \
    -v /home/$USER:/home/$USER:rw \
    -v /etc/group:/etc/group:ro \
    -v /etc/passwd:/etc/passwd:ro \
    -v /etc/shadow:/etc/shadow:ro \
    -v mydownloads:/mydownloads \
    -v ${PWD}:/opt/citksnap \
    -e CITKSNAP_URI \
    citksnap:latest \
    bash

