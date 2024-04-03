# Programmer: Connor Fricke (fricke.59@osu.edu)
# Gnuplot Script file for testing command line functionality of GNUPLOT in Powershell
# on Windows 10/11.
# To run script:
# PS > gnuplot --persist 'test.plt'

set terminal windows

set timestamp
set title 'test'
set xlabel 'X'
set ylabel 'Y'

set xrange[0:2*pi]
set yrange [-1.2:1.2]

plot sin(x) title 'Hello Professor Bundschuh'