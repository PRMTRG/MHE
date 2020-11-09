import numpy as np
import utils

def printSolution(solution, problem):
    locations = problem[0]
    facilities = problem[2]
    for i in range(len(solution)):
        print("{} will be in {}".format(facilities[solution[i]], locations[i]))

def rateSolution(solution, problem):
    distances = problem[1]
    flows = problem[3]
    result = 0
    for pair in utils.generatePairs(len(solution)):
        distance = distances[pair]
        flow = flows[utils.correctPair((solution[pair[0]],solution[pair[1]]))]
        result += distance * flow
    return result

def generateRandomSolution(problem):
    solution = []
    for i in list(np.random.permutation(len(problem[0]))):
        solution.append(i)
    return solution

def bruteforceSolution(problem):
    size = len(problem[0])
    permutations = utils.generatePermutations(size)
    bestSolution = list(permutations[0])
    bestRating = rateSolution(bestSolution, problem)
    for i in range(1, len(permutations)):
        solution = list(permutations[i])
        rating = rateSolution(solution, problem)
        if rating < bestRating:
            bestSolution = solution
            bestRating = rating
    return bestSolution

def generateNextSolution(solution):
    return utils.nextPermutation(solution)

def generateSolution(problem, method):
    if method == "random":
        return generateRandomSolution(problem)
    if method == "bruteforce":
        return bruteforceSolution(problem)
