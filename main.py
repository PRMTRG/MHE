import sys
import problems
import solutions
import presets



if len(sys.argv) > 1:
    if sys.argv[1] == "random":
        presets.getRandomProblemAndBruteforceSolutionAndWriteProblemAndResultToFile(int(sys.argv[2]), sys.argv[3])
else:
    #presets.readProblemFromFileAndBruteforceSolutionAndWriteResultToFile("problems/size7_000.txt", "out1.txt")
    #presets.getRandomProblemAndBruteforceSolutionAndWriteResultToFile(8, "out2.txt")
    presets.getRandomProblemAndBruteforceSolutionAndWriteProblemAndTimeAndResultToFile(9, "out3.txt")













