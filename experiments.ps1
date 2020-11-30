[System.Collections.ArrayList]$problems = @()
for ($i = 3; $i -lt 10; $i++){
    $problems.Add("size$i") > $null
}
$solvers = ( "bruteforce", "hillclimb1", "hillclimb2", "tabu" )
$experiments = 5
$iterationCounts = ( 100, 300, 500, 1000, 2000 )
$tabuSize = 100

foreach ( $solver in $solvers ){
    foreach ( $iterationCount in $iterationCounts ){
        foreach ( $problem in $problems ){
            for ( $i = 0; $i -lt $experiments; $i++ ){
                $expression = 'python main.py --problem_source "file" --problem_file "{0}"' -f ("problems/" + $problem + ".txt")
                $expression += ' --solver "{0}" --iterations {1}' -f $solver, $iterationCount
                if ($solver -eq "tabu"){
                    $expression += ' --tabu_size {0}' -f $tabuSize
                }
                $filename = "plot_data/{0}_{1}_{2}_run{3}.txt" -f $solver, $iterationCount, $problem, $i
                $expression += ' --output_plot_data_to_file --plot_data_output_file "{0}"' -f $filename
                if ( $problem -eq "size9" -and $solver -eq "bruteforce" ){
                    $expression += ' --plotting_step 100'
                }
                if ( $problem -eq "size10" -and $solver -eq "bruteforce" ){
                    $expression += ' --plotting_step 1000'
                }
                Invoke-Expression $expression
            }
        }
    }
}

[System.Collections.ArrayList]$listSolverTimes = @()
[System.Collections.ArrayList]$listSolverResults = @()

foreach ( $solver in $solvers ){
    [System.Collections.ArrayList]$listSolverTimesPerArgs = @()
    [System.Collections.ArrayList]$listSolverResultsPerArgs = @()
    foreach ( $iterationCount in $iterationCounts ){
        $outputFile = "experiment_data/average_results/{0}_{1}.txt" -f $solver, $iterationCount
        if ([System.IO.File]::Exists($outputFile)){
            Clear-Content $outputFile
        }
        [System.Collections.ArrayList]$solverTimes = @()
        [System.Collections.ArrayList]$solverResults = @()
        foreach ( $problem in $problems ){
            [System.Collections.ArrayList]$timeTaken = @()
            [System.Collections.ArrayList]$result = @()
            for ( $i = 0; $i -lt $experiments; $i++ ){
                $inputFile = "plot_data/{0}_{1}_{2}_run{3}.txt" -f $solver, $iterationCount, $problem, $i
                $data = Get-Content $inputFile
                $lastLine = $data[-1].Split(" ")
                $timeTaken.Add($lastLine[0]) > $null
                $result.Add($lastLine[1]) > $null
            }
            $averageTimeTakenInExperiments = [math]::Round(($timeTaken | Measure-Object -Average).Average, 2)
            $averageResultInExperiments = [math]::Round(($result | Measure-Object -Average).Average)
            $solverTimes.Add($averageTimeTakenInExperiments) > $null
            $solverResults.Add($averageResultInExperiments) > $null
            "$solver $($problem[4..$problem.Length]-join'') $averageTimeTakenInExperiments $averageResultInExperiments" | Add-Content $outputFile
        }
        $listSolverTimesPerArgs.Add($solverTimes) > $null
        $listSolverResultsPerArgs.Add($solverResults) > $null        
    }
    [System.Collections.ArrayList]$averageProblemTimeForSolver = @()
    [System.Collections.ArrayList]$averageProblemResultForSolver = @()
    for ( $i = 0; $i -lt $problems.Count; $i++ ){
        $sumTime = 0
        $sumResult = 0
        for ( $j = 0; $j -lt $iterationCounts.Count; $j++ ){
            $sumTime += $listSolverTimesPerArgs[$j][$i]
            $sumResult += $listSolverResultsPerArgs[$j][$i]
        }
        $averageProblemTimeForSolver.Add( $sumTime / $iterationCounts.Count ) > $null
        $averageProblemResultForSolver.Add( $sumResult / $iterationCounts.Count ) > $null
    }
    $listSolverTimes.Add($averageProblemTimeForSolver) > $null
    $listSolverResults.Add($averageProblemResultForSolver) > $null
}

for ( $i = 0; $i -lt $solvers.Count; $i++ ){
    $outputFile = "experiment_data/average_results/{0}.txt" -f $solvers[$i]
    if ([System.IO.File]::Exists($outputFile)){
        Clear-Content $outputFile
    }
    for ( $j = 0; $j -lt $problems.Count; $j++ ){
        "$($solvers[$i]) $($problems[$j][4..$problem.Length]-join'') $($listSolverTimes[$i][$j]) $($listSolverResults[$i][$j])" | Add-Content $outputFile
    }
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


