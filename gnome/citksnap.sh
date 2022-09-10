#!/bin/bash
export CITKSNAP_URI=$@
echo ${CITKSNAP_URI}

xhost +
export LIBGL_ALWAYS_INDIRECT=1

docker volume create \
    --driver local \
    --opt type=none \
    --opt o=bind \
    --opt device=/home/${USER}/Downloads/itksnap-xdg-open/demo-image \
    --name demo-image

docker run -it --rm --privileged --net=host --ipc=host \
    -e DISPLAY -e QT_X11_NO_MITSHM=1 -v /tmp/.X11-unix \
    -u "$(id -u):$(id -g)" \
    -v /home/$USER:/home/$USER:rw \
    -v /etc/group:/etc/group:ro \
    -v /etc/passwd:/etc/passwd:ro \
    -v /etc/shadow:/etc/shadow:ro \
    -v demo-image:/demo-image \
    -e CITKSNAP_URI \
    citksnap:latest \
    bash launcher.sh ${CITKSNAP_URI}
