import numpy as np
import utils
import random as rand
import time
import problems
import math


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
    def output_results_to_terminal(self, problem, solution, rating,
                           measure_time=False, time_taken=0):
        # print(self.solver_name)
        # print("Solution:", solution)
        # print("Rating:", rating)
        # print("Rater calls:", self.solution_rater.counter)
        # if measure_time:
        #     print("Time taken:", time_taken)
        # print()
        if measure_time:
            print("{} {}".format(time_taken, rating))
        else:
            print(rating)
    def output_results_to_file(self, output_file, problem, solution, rating,
                               measure_time=False, time_taken=0):
        file = open(output_file, "w")
        file.writelines(problems.get_output_for_writing_problem_to_file(problem))
        file.write('\n')
        if measure_time:
            file.write(str(time_taken)+'\n')
        file.write(str(solution)+'\n')
        file.write(str(rating)+'\n')
        file.close()
    def output_plot_data_to_file(self, plot_data_output_file, plot_time, plot_result):
        file = open(plot_data_output_file, "w")
        for i in range(len(plot_time)):
            file.write(str(plot_time[i]) + " " + str(plot_result[i]) + "\n")
        file.close()
    def solve(self, problem, *argv, output_results_to_terminal=False,
              output_results_to_file=False, results_output_file="",
              output_plot_data_to_file=False, plot_data_output_file="",
              plotting_step=1, measure_time=True):
        time_taken = 0
        if measure_time:
            start_time = time.time()
        if output_plot_data_to_file:
            solution, plot_time, plot_result = self.solver_algorithm(self.solution_rater,
                            problem, *argv, save_data_for_plot=True, plotting_step=plotting_step)
            self.output_plot_data_to_file(plot_data_output_file, plot_time, plot_result)
        else:
            solution = self.solver_algorithm(self.solution_rater, problem, *argv)
        rating = rate_solution(solution.copy(), problem)
        if measure_time:
            time_taken = time.time() - start_time
        if output_results_to_file and results_output_file != "":
            self.output_results_to_file(results_output_file, problem, solution,
                                        rating, measure_time, time_taken)
        if output_results_to_terminal:
            self.output_results_to_terminal(problem, solution, rating,
                                            measure_time, time_taken)
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


def validate_solution(solution, size):
    sol = solution.copy()
    if len(sol) != size:
        return False
    sol.sort()
    if sol[0] != 0:
        return False
    for i in range(1, size):
        if sol[i-1] != (sol[i] - 1):
            return False
    return True


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


def bruteforce(solution_rater, problem,
               save_data_for_plot=False, plotting_step=1):
    size = len(problem[0])
    permutations = utils.generate_permutations(size)
    best_solution = list(permutations[0])
    best_result = solution_rater.rate(best_solution.copy(), problem)
    if save_data_for_plot:
        plot_time = []
        plot_time.append(0)
        plot_result = []
        plot_result.append(best_result)
        start_time = time.perf_counter()
    iterations = len(permutations)
    for i in range(1, iterations):
        solution = list(permutations[i])
        result = solution_rater.rate(solution.copy(), problem)
        if result < best_result:
            best_solution = solution
            best_result = result
        if save_data_for_plot and (i % plotting_step == 0 or i == iterations - 1):
            plot_time.append(time.perf_counter() - start_time)
            plot_result.append(best_result)
    if save_data_for_plot:
        return best_solution, plot_time, plot_result 
    else:
        return best_solution


def hillclimb_ver1(solution_rater, problem, iterations,
                   save_data_for_plot=False, plotting_step=1):
    best_solution = generate_random_solution(problem)
    size = len(best_solution)
    best_result = solution_rater.rate(best_solution.copy(), problem)
    if save_data_for_plot:
        plot_time = []
        plot_time.append(0)
        plot_result = []
        plot_result.append(best_result)
        start_time = time.perf_counter()
    for i in range(iterations):
        neighbors = generate_neighboring_solutions(best_solution.copy())
        new_best_solution = neighbors[0].copy()
        new_best_result = solution_rater.rate(new_best_solution.copy(), problem)
        for j in range(1, size):
            solution = neighbors[j].copy()
            result = solution_rater.rate(solution.copy(), problem)
            if result < new_best_result:
                new_best_solution = solution.copy()
                new_best_result = result
        end = False
        if best_result < new_best_result:
            end = True
        else:
            best_solution = new_best_solution.copy()
            best_result = new_best_result
        if save_data_for_plot and (i % plotting_step == 0 or i == iterations - 1 or end):
            plot_time.append(time.perf_counter() - start_time)
            plot_result.append(best_result)
        if end:
            break
    if save_data_for_plot:
        return best_solution, plot_time, plot_result
    else:
        return best_solution


def hillclimb_ver2(solution_rater, problem, iterations,
                   save_data_for_plot=False, plotting_step=1):
    best_solution = generate_random_solution(problem)
    best_result = solution_rater.rate(best_solution.copy(), problem)
    if save_data_for_plot:
        plot_time = []
        plot_time.append(0)
        plot_result = []
        plot_result.append(best_result)
        start_time = time.perf_counter()
    for i in range(iterations):
        neighbour = generate_random_neighbour(best_solution.copy())
        result = solution_rater.rate(neighbour.copy(), problem)
        if best_result > result:
            best_solution = neighbour.copy()
            best_result = result
        if save_data_for_plot and (i % plotting_step == 0 or i == iterations - 1):
            plot_time.append(time.perf_counter() - start_time)
            plot_result.append(best_result)
    if save_data_for_plot:
        return best_solution, plot_time, plot_result
    else:
        return best_solution


def tabu(solution_rater, problem, iterations, tabu_size,
         save_data_for_plot=False, plotting_step=1):
    tabu_list = []
    best_solution = generate_random_solution(problem)
    tabu_list.append(best_solution.copy())
    size = len(tabu_list[0])
    if save_data_for_plot:
        plot_time = []
        plot_time.append(0)
        plot_result = []
        plot_result.append(rate_solution(best_solution, problem))
        start_time = time.perf_counter()
    for i in range(iterations):
        neighbours = []
        for i in range(size):
            new_solution = add_axis(tabu_list[-1].copy(), i)
            found = False
            for s in tabu_list:
                if s == new_solution:
                    found = True
            if not found:
                neighbours.append(new_solution.copy())
        if len(neighbours) == 0:
            break #got stuck
        neighbours.sort(key=lambda x: solution_rater.rate(x.copy(), problem), reverse=True)
        tabu_list.append(neighbours[-1].copy())
        if solution_rater.rate(tabu_list[-1], problem) < solution_rater.rate(best_solution.copy(), problem):
            best_solution = tabu_list[-1].copy()
        if len(tabu_list) > tabu_size:
            tabu_list.pop(0)
        if save_data_for_plot and (i % plotting_step == 0 or i == iterations - 1):
            plot_time.append(time.perf_counter() - start_time)
            plot_result.append(rate_solution(best_solution, problem))
    if save_data_for_plot:
        return best_solution, plot_time, plot_result
    else:
        return best_solution


def simulated_annealing(solution_rater, problem, iterations,
                         temperature_function, t_args, print_iterations=False):
    solutions = []
    results = []
    solutions.append(generate_random_solution(problem))
    results.append(solution_rater.rate(solutions[-1].copy(), problem))
    for k in range(1, iterations):
        neighbour = generate_random_neighbour(solutions[-1].copy())
        result = solution_rater.rate(neighbour.copy(), problem)
        if results[-1] >= result:
            solutions.append(neighbour.copy())
            results.append(result)
        else:
            u = rand.random()
            ep = math.exp(-1 * abs(result - results[-1]) / temperature_function(k, iterations, t_args))
            if (u < ep):
                solutions.append(neighbour.copy())
                results.append(result)
            else:
                solutions.append(solutions[-1])
                results.append(results[-1])
    if print_iterations:
        for k in range(len(results)):
            print("k = {} result = {}".format(k, results[k]))
    return solutions, results


def get_solver(solver_name):
    if solver_name == "bruteforce":
        return bruteforce
    elif solver_name == "hillclimb1":
        return hillclimb_ver1
    elif solver_name == "hillclimb2":
        return hillclimb_ver2
    elif solver_name == "tabu":
        return tabu