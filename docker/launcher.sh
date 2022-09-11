#!/bin/bash
export CITKSNAP_URI=$@

export USER=$(whoami)
# are we over engineering??

# #option 1 do simple prep work in sh file only
# itksnap -g $image_file -s $segmentation_file

# #option 2 do prep work in py file then launch itksnap
#python3 launcher.py $CITKSNAP_URI

# option 3 add additional gui for addon user-interaction outside itksnap
python3 gui.py ${CITKSNAP_URI}
