set xdata time
set timefmt "%s"
set format x "%H:%M:%S"
set xlabel "Time"
set ylabel "Power (W)"
set key off
set ytics nomirror
set tics out
set autoscale y
set xtics rotate by -40
plot "plot1.data" using 1:4 with filledcurve x1
pause mouse close