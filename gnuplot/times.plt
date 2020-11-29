set term png
set output "times.png"
plot "times.txt" using 1:2 title "bruteforce" with lines, "times.txt" using 1:3 title "hillclimb1" with lines, "times.txt" using 1:4 title "hillclimb2" with lines, "times.txt" using 1:5 title "tabu" with lines