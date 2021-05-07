set xdata time
set timefmt "%s"
set format x "%H:%M:%S"
set xlabel "Time"
set ylabel "Voltage (V)"
set y2label "Current (A)"
set key off
set ytics nomirror
set y2tics
set tics out
set autoscale y
set autoscale y2
set pointsize 0.5
set xtics rotate by -40
plot "plot1.data" using 1:2 axes x1y1 with points pointtype 8, "plot1.data" using 1:3 axes x1y2 with points pointtype 8
pause mouse close