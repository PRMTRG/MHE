import numpy as np
import utils
import random as rand
import time
import problems


class SolutionRater:
    def __init__(self, solver_name, enable_print):
        self.solver_name = solver_name
        self.enable_print = enable_print
        self.counter = 0
    def rate(self, solution, problem):
        self.counter += 1
        rating = rate_solution(solution.copy(), problem)
        if self.enable_print:
            print(f'{self.solver_name} #{self.counter:03d} = {solution} = {rating}')
        return rating


class Solver:
    def __init__(self, solver_name, solver_algorithm, enable_print=False):
        self.solver_name = solver_name
        self.solver_algorithm = solver_algorithm
        self.enable_print = enable_print
        self.solution_rater = SolutionRater(self.solver_name, self.enable_print)
    def solve(self, problem, *argv, output_to_terminal=False, output_to_file=False, 
              output_file="", measure_time=False):
        if measure_time:
            start_time = time.time()
        solution = self.solver_algorithm(self.solution_rater, problem, *argv)
        rating = rate_solution(solution.copy(), problem)
        if measure_time:
            time_taken = time.time() - start_time
        if output_to_file and output_file != "":
            file = open(output_file, "w")
            file.writelines(problems.get_output_for_writing_problem_to_file(problem))
            file.write('\n')
            if measure_time:
                file.write(str(time_taken)+'\n')
            file.write(str(solution)+'\n')
            file.write(str(rating)+'\n')
            file.close()
        elif output_to_terminal:
            print(self.solver_name)
            print("Solution:", solution)
            print("Rating:", rating)
            print("Rater calls:", self.solution_rater.counter)
            if measure_time:
                print("Time taken:", time_taken)
            print()
        self.solution_rater.counter = 0


def print_solution(solution, problem):
    locations = problem[0]
    facilities = problem[2]
    for i in range(len(solution)):
        print("{} will be in {}".format(facilities[solution[i]], locations[i]))


def rate_solution(solution, problem):
    distances = problem[1]
    flows = problem[3]
    result = 0
    for pair in utils.generate_pairs(len(solution)):
        distance = distances[pair]
        flow = flows[utils.correct_pair((solution[pair[0]],solution[pair[1]]))]
        result += distance * flow
    return result


def generate_random_solution(problem):
    solution = []
    for i in list(np.random.permutation(len(problem[0]))):
        solution.append(i)
    return solution


def generate_next_solution(solution):
    return utils.next_permutation(solution)


def generate_previous_solution(solution):
    return utils.previous_permutation(solution)


def add_axis(solution, axis):
    if axis > len(solution) - 1:
        return
    new_solution = solution
    old_value = new_solution[axis]
    if old_value + 2 > len(new_solution):
        new_value = 0
    else:
        new_value = old_value + 1
    for i in range(len(new_solution)):
        if new_solution[i] == new_value:
            new_solution[i] = old_value
    new_solution[axis] = new_value
    return new_solution


def sub_axis(solution, axis):
    if axis > len(solution) - 1:
        return
    new_solution = solution
    old_value = new_solution[axis]
    if old_value == 0:
        new_value = len(new_solution) - 1
    else:
        new_value = old_value - 1
    for i in range(len(new_solution)):
        if new_solution[i] == new_value:
            new_solution[i] = old_value
    new_solution[axis] = new_value
    return new_solution


def generate_random_neighbour(solution):
    size = len(solution)
    index = rand.randint(0, size - 1)
    new_solution = add_axis(solution.copy(), index)
    return new_solution


def generate_neighboring_solutions(solution):
    size = len(solution)
    neighbors = []
    for i in range(size):
        neighbors.append(add_axis(solution.copy(), i))
    return neighbors


def bruteforce(solution_rater, problem):
    size = len(problem[0])
    permutations = utils.generate_permutations(size)
    best_solution = list(permutations[0])
    best_rating = solution_rater.rate(best_solution.copy(), problem)
    for i in range(1, len(permutations)):
        solution = list(permutations[i])
        rating = solution_rater.rate(solution.copy(), problem)
        if rating < best_rating:
            best_solution = solution
            best_rating = rating
    return best_solution


def hillclimb_ver1(solution_rater, problem, attempts):
    best_solution = generate_random_solution(problem)
    size = len(best_solution)
    best_rating = solution_rater.rate(best_solution.copy(), problem)
    for i in range(attempts):
        neighbors = generate_neighboring_solutions(best_solution.copy())
        new_best_solution = neighbors[0].copy()
        new_best_rating = solution_rater.rate(new_best_solution.copy(), problem)
        for j in range(1, size):
            solution = neighbors[i].copy()
            rating = solution_rater.rate(solution.copy(), problem)
            if rating < new_best_rating:
                new_best_solution = solution.copy()
                new_best_rating = rating
        if best_rating < new_best_rating:
            break
        else:
            best_solution = new_best_solution.copy()
            best_rating = new_best_rating
    return best_solution


def hillclimb_ver2(solution_rater, problem, attempts):
    best_solution = generate_random_solution(problem)
    best_rating = solution_rater.rate(best_solution.copy(), problem)
    for i in range(attempts):
        neighbour = generate_random_neighbour(best_solution.copy())
        rating = solution_rater.rate(neighbour.copy(), problem)
        if best_rating > rating:
            best_solution = neighbour.copy()
            best_rating = rating
    return best_solution


def tabu(solution_rater, problem, attempts, tabu_size):
    tabu_list = []
    best_solution = generate_random_solution(problem)
    tabu_list.append(best_solution.copy())
    size = len(tabu_list[0])
    for i in range(attempts):
        neighbours = []
        for i in range(size):
            new_solution = add_axis(tabu_list[-1].copy(), i)
            found = False
            for s in tabu_list:
                if s == new_solution:
                    found = True
            if not found:
                neighbours.append(new_solution.copy())
        neighbours.sort(key=lambda x: solution_rater.rate(x.copy(), problem), reverse=True)
        tabu_list.append(neighbours[-1].copy())
        if solution_rater.rate(tabu_list[-1], problem) < solution_rater.rate(best_solution.copy(), problem):
            best_solution = tabu_list[-1].copy()
        if len(tabu_list) > tabu_size:
            tabu_list.pop(0)
    return best_solution

