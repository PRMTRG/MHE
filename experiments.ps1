[System.Collections.ArrayList]$problems = @()
for ($i = 3; $i -lt 11; $i++){
    $problems.Add("size$i") > $null
}
$solvers = ( "bruteforce", "hillclimb1", "hillclimb2", "tabu" )
$experiments = 5
$iterations = 1000
$tabuSize = 100

foreach ( $solver in $solvers ){
    foreach ( $problem in $problems ){
        for ( $i = 0; $i -lt $experiments; $i++ ){
            $expression = 'python main.py --problem_source "file" --problem_file "{0}"' -f ("problems/" + $problem + ".txt")
            $expression += ' --solver "{0}" --iterations {1}' -f $solver, $iterations
            if ($solver -eq "tabu"){
                $expression += ' --tabu_size {0}' -f $tabuSize
            }
            $filename = "plot_data/{0}_{1}_run{2}.txt" -f $solver, $problem, $i
            $expression += ' --output_plot_data_to_file --plot_data_output_file "{0}"' -f $filename
            if ( $problem -eq "size9" -and $solver -eq "bruteforce" ){
                $expression += ' --plotting_step 100'
            }
            if ( $problem -eq "size10" -and $solver -eq "bruteforce" ){
                $expression += ' --plotting_step 1000'
            }
            #Invoke-Expression $expression
        }
    }
}

[System.Collections.ArrayList]$listSolverTimes = @()
[System.Collections.ArrayList]$listSolverResults = @()

foreach ( $solver in $solvers ){
    $outputFile = "experiment_data/average_results/$solver.txt"
    if ([System.IO.File]::Exists($outputFile)){
        Clear-Content $outputFile
    }
    [System.Collections.ArrayList]$solverTimes = @()
    [System.Collections.ArrayList]$solverResults = @()
    foreach ( $problem in $problems ){
        [System.Collections.ArrayList]$timeTaken = @()
        [System.Collections.ArrayList]$result = @()
        for ( $i = 0; $i -lt $experiments; $i++ ){
            $inputFile = "plot_data/{0}_{1}_run{2}.txt" -f $solver, $problem, $i
            $data = Get-Content $inputFile
            $lastLine = $data[-1].Split(" ")
            $timeTaken.Add($lastLine[0]) > $null
            $result.Add($lastLine[1]) > $null
        }
        $averageTimeTaken = [math]::Round(($timeTaken | Measure-Object -Average).Average, 2)
        $averageResult = [math]::Round(($result | Measure-Object -Average).Average)
        $solverTimes.Add($averageTimeTaken) > $null
        $solverResults.Add($averageResult) > $null
        "$solver $($problem[4..$problem.Length]-join'') $averageTimeTaken $averageResult" | Add-Content $outputFile
    }
    $listSolverTimes.Add($solverTimes) > $null
    $listSolverResults.Add($solverResults) > $null
}

$outputFile1 = "experiment_data/plots/times.txt"
$outputFile2 = "experiment_data/plots/results.txt"
if ([System.IO.File]::Exists($outputFile1)){
    Clear-Content $outputFile1
}
if ([System.IO.File]::Exists($outputFile2)){
    Clear-Content $outputFile2
}
for ($i = 0; $i -lt $problems.Count; $i++){
    $line1 = "$($problems[$i][4..$problems[$i].Length]-join'')"
    $line2 = "$($problems[$i][4..$problems[$i].Length]-join'')"
    for ($j = 0; $j -lt $solvers.Count; $j++){
        $line1 += " $($listSolverTimes[$j][$i])"
        $line2 += " $($listSolverResults[$j][$i])"
    }
    $line1 | Add-Content $outputFile1
    $line2 | Add-Content $outputFile2
}

Set-Location -Path "experiment_data/plots"
Invoke-Expression "gnuplot times.plt"
Set-Location -Path "../.."


