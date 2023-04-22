#!/bin/bash

# remove png files generated with the 3dmodel/get_single_photo.py script
# from the 3dmodel directory

for i in {1..96}
do
    rm -f $i.png
done