#!/bin/bash
#
# Generate Plot of results with gnuplot
#

# Generate the gnuplot input data file from the filename given at the command
python contrib/generate_gnuplot_from_single_result.py "$1" >/tmp/m2mlearning.tmp

gnuplot <<EOF
set terminal svg enhanced background rgb 'white' size 1920,1080 fname 'Verdana'
set output '/tmp/m2mlearning.svg'
set title "$2"
plot "/tmp/m2mlearning.tmp" using 1:2 with dots title "Measurements", "/tmp/m2mlearning.tmp" using 1:3 with lines title "Mean over 10", "/tmp/m2mlearning.tmp" using 1:4 with lines title "Mean over 100", "/tmp/m2mlearning.tmp" using 1:5 with lines title "Mean over 1000"
EOF
