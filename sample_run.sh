#!/bin/bash
# python3 Tinysa_animate_waterfall_scanraw.py -s /dev/cu.usbmodem4001 -f 87e6:108e6:100e3 -N 200 -T 101
source ~/.venv/bin/activate
python3 Tinysa_animate_waterfall_scanraw.py -s /dev/ttyACM0 -f 50e6:250e6:100e3 -N 1024 -T 101 -D true
# python3 Tinysa_animate_waterfall_scanraw.py -s /dev/ttyACM0 -f 500e6:700e6:100e3 -N 1024 -T 101 -D true
deactivate
