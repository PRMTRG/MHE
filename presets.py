import time
import problems
import solutions

def readProblemFromFileAndBruteforceSolutionAndWriteResultToFile(inputFile, outputFile):
    problem = problems.getProblem("readFile", inputFile)
    solution = solutions.generateSolution(problem, "bruteforce")
    score = solutions.rateSolution(solution, problem)
    file = open(outputFile, "w")
    file.write(str(solution)+'\n')
    file.write(str(score)+'\n')
    file.close()

def getRandomProblemAndBruteforceSolutionAndWriteResultToFile(size, outputFile):
    problem = problems.getProblem("random", size)
    solution = solutions.generateSolution(problem, "bruteforce")
    score = solutions.rateSolution(solution, problem)
    file = open(outputFile, "w")
    file.write(str(solution)+'\n')
    file.write(str(score)+'\n')
    file.close()

def getRandomProblemAndBruteforceSolutionAndWriteProblemAndResultToFile(size, outputFile):
    problem = problems.getProblem("random", size)
    solution = solutions.generateSolution(problem, "bruteforce")
    score = solutions.rateSolution(solution, problem)
    file = open(outputFile, "w")
    file.writelines(problems.getOutputForWritingProblemToFile(problem))
    file.write('\n')
    file.write(str(solution)+'\n')
    file.write(str(score)+'\n')
    file.close()

def getRandomProblemAndBruteforceSolutionAndWriteProblemAndTimeAndResultToFile(size, outputFile):
    problem = problems.getProblem("random", size)
    startTime = time.time()
    solution = solutions.generateSolution(problem, "bruteforce")
    timeTaken = time.time() - startTime
    score = solutions.rateSolution(solution, problem)
    file = open(outputFile, "w")
    file.writelines(problems.getOutputForWritingProblemToFile(problem))
    file.write('\n')
    file.write(str(timeTaken)+'\n')
    file.write(str(solution)+'\n')
    file.write(str(score)+'\n')
    file.close()




