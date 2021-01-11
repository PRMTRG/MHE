import random
import math
import solutions
import problems
import utils
import argparse
import sys
import numpy as np


class GA:
    def __init__(self, gen_starting_pop_f, fitness_f, selection_f, crossover_f,
                 mutation_f, termination_f, prob_crossover, prob_mutation, problem_size):
        self.gen_starting_pop_f = gen_starting_pop_f
        self.fitness_f = fitness_f
        self.selection_f = selection_f
        self.crossover_f = crossover_f
        self.mutation_f = mutation_f
        self.termination_f = termination_f
        self.prob_crossover = prob_crossover
        self.prob_mutation = prob_mutation
        self.population = self.gen_starting_pop_f()
        self.problem_size = problem_size
    def get_best_specimen_index(self):
        return self.population_fitness.index(max(self.population_fitness))
    def run(self):
        pop_size = len(self.population)
        self.population_fitness = []
        for i in range(pop_size):
            self.population_fitness.append(self.fitness_f(self.population[i]))
        while not self.termination_f(self):
            # calculating fitness
            for i in range(pop_size):
                self.population_fitness[i] = self.fitness_f(self.population[i])
            
            # selection
            parents = []
            for i in range(pop_size):
                parents.append(self.selection_f(self.population, self.population_fitness))
            
            # crossing
            parents_idx = 1
            children = []            
            while len(children) < pop_size and parents_idx < pop_size:
                for child in self.crossover_f(self.prob_crossover, parents[parents_idx], parents[parents_idx - 1]):
                    children.append(child)
                parents_idx += 2
            if len(children) > pop_size:
                children = children[:pop_size]
            
            # mutation
            for i in range(pop_size):
                children[i] = self.mutation_f(children[i], self.prob_mutation)
            
            # fix genotype
            for i in range(pop_size):
                children[i] = fix_genotype(children[i], self.problem_size)
            
            self.population = children
        
        for i in range(pop_size):
            
            #self.population[i] = fix_genotype(self.population[i], self.problem_size)            
            
            self.population_fitness[i] = self.fitness_f(self.population[i])
            #print("{} = {}".format(self.population_fitness[i], self.population[i]))
        return self.population[self.get_best_specimen_index()].copy()


def gen_gen_starting_pop(population_size, genotype_size, problem_size, only_valid):
    def gen_starting_pop():
        population = []
        for i in range(population_size):
            while True:
                specimen = [ random.getrandbits(1) for j in range(genotype_size) ]
                solution = decode_genotype(specimen, problem_size)
                if solutions.validate_solution(solution, problem_size) or not only_valid:
                    break
            population.append(specimen)
        return population
    return gen_starting_pop


def tournament_selection(pop, pop_fit):
    tournament_size = 2
    tournament = []
    for i in range(tournament_size):
        tournament.append(random.randint(0, len(pop) - 1))
    best = tournament[0]
    for i in range(1, tournament_size):
        if pop_fit[tournament[i]] > pop_fit[best]:
            best = tournament[i]
    return pop[best].copy()


def roulette_selection(pop, pop_fit):
    s = 0
    for i in range(len(pop)):
        s += pop_fit[i]
    r = random.uniform(0, s)
    p_sum = 0
    for i in range(len(pop)):
        p_sum += pop_fit[i]
        if r <= p_sum:
            return pop[i].copy()
    raise Exception("roulette_selection")


def one_point_crossover(prob_crossover, parent_a, parent_b):
    if random.random() > prob_crossover:
        return parent_a, parent_b
    child_a = parent_a.copy()
    child_b = parent_b.copy()
    pp = random.randint(0, len(parent_a))
    for i in range(pp, len(parent_a)):
        child_a[i], child_b[i] = child_b[i], child_a[i]
    return child_a, child_b


def two_point_crossover(prob_crossover, parent_a, parent_b):
    if random.random() > prob_crossover:
        return parent_a, parent_b
    child_a = parent_a.copy()
    child_b = parent_b.copy()
    pp1 = random.randint(0, len(parent_a))
    pp2 = random.randint(0, len(parent_a))
    if pp2 < pp1:
        pp1, pp2 = pp2, pp1
    for i in range(pp1, pp2):
        child_a[i], child_b[i] = child_b[i], child_a[i]
    return child_a, child_b


def mutation(genotype, prob):
    new_genotype = genotype.copy()
    for i in range(len(new_genotype)):
        if random.random() < prob:
            new_genotype[i] = 1 - new_genotype[i]
    return new_genotype


def gen_terminate_after_iterations(iterations):
    def terminate_after_iterations(self):
        try:
            self.iteration += 1
        except:
            if iterations == 0:
                return True
            self.iteration = 1
            return False
        if self.iteration >= iterations:
            return True
        return False
    return terminate_after_iterations


def gen_terminate_after_fitness_goal(goal):
    def terminate_after_fitness_goal(self):
        try:
            if sum(self.population_fitness) / len(self.population_fitness) >= goal:
                return True
        except:
            return False
        return False
    return terminate_after_fitness_goal


def gen_terminate_after_std_dev_goal(goal):
    def terminate_after_std_dev_goal(self):
        try:
            if np.std(self.population_fitness) <= goal:
                return True
        except:
            return False
        return False
    return terminate_after_std_dev_goal


def gen_terminate_immediately():
    def terminate_immediately(self):
        return True
    return terminate_immediately


def decode_genotype(genotype, size):
    if len(genotype) % size != 0:
        raise Exception("decode_genotype")
    n = len(genotype) // size
    enc_positions = [ genotype[i:i + n] for i in range(0, len(genotype), n) ]
    solution = []
    for pos in enc_positions:
        res = 0
        for i, v in enumerate(pos):
            if v:
                res += 2 ** i
        solution.append(res)
    return solution


def encode_genotype(solution):
    size = len(solution)
    bits_per_position = get_genotype_size(size) // size
    genotype = []
    for p in solution:
        pos = [int(x) for x in list('{0:0b}'.format(p))]
        pos.reverse()
        if len(pos) < bits_per_position:
            for i in range(bits_per_position - len(pos)):
                pos.append(0)
        genotype += pos
    return genotype


def gen_fitness(problem):
    size = len(problem[0])
    def fitness(genotype):
        solution = decode_genotype(genotype, size)
        if not solutions.validate_solution(solution.copy(), size):
            return 0
        rating = solutions.rate_solution(solution.copy(), problem)
        return 1000000 / ( rating + 1 )
    return fitness


def get_genotype_size(problem_size):
    return math.ceil(np.log(problem_size) / np.log(2)) * problem_size


def fix_genotype(genotype, size):
    pos_pos = [ i for i in range(size) ]
    solution = decode_genotype(genotype, size)
    
    for i in range(size):
        if solution[i] not in solution[:i] and solution[i] < size:
            continue
        for pp in pos_pos:
            if pp not in solution:
                solution[i] = pp
                break
    return encode_genotype(solution)


def run(selection="tournament", crossover="one_point", prob_crossover=0.3,
        prob_mutation=0.1, termination="iterations", termination_arg=100,
        pop_size=40):
    problem = problems.read_problem_from_file("problems/size9.txt")
    problem_size = len(problem[0])
    solution_rater = solutions.SolutionRater("", False)
    if selection == "tournament":
        selection_f = tournament_selection
    elif selection == "roulette":
        selection_f = roulette_selection
    if crossover == "one_point":
        crossover_f = one_point_crossover
    elif crossover == "two_point":
        crossover_f = two_point_crossover
    if termination == "iterations":
        termination_f = gen_terminate_after_iterations(int(termination_arg))
    elif termination == "fitness_goal":
        termination_f = gen_terminate_after_fitness_goal(float(termination_arg))
    elif termination == "std_deviation":
        termination_f = gen_terminate_after_std_dev_goal(float(termination_arg))
    solution_rater = solutions.SolutionRater("", False)
    ga = GA(gen_gen_starting_pop(pop_size, get_genotype_size(problem_size), problem_size, False),
            gen_fitness(problem), selection_f, crossover_f, mutation,
            termination_f, prob_crossover, prob_mutation, problem_size)
    
    ga_best_genotype = ga.run()
    ga_best_solution = decode_genotype(ga_best_genotype, problem_size)
    if solutions.validate_solution(ga_best_solution, problem_size):
        ga_best_rating = solution_rater.rate(ga_best_solution, problem)
    else:
        ga_best_rating = 0
    return ga_best_solution, ga_best_rating


def main():
    problem = problems.read_problem_from_file("problems/size9.txt")
    problem_size = len(problem[0])
    pop_size = 100
    
    selection_f = tournament_selection
    crossover_f = two_point_crossover
    prob_crossover = 0.3
    prob_mutation = 0.01
    termination_f = gen_terminate_after_iterations(10000)
    
    if len(sys.argv) > 1:
        parser = argparse.ArgumentParser()
        parser.add_argument("--selection", type=str)
        parser.add_argument("--crossover", type=str)
        parser.add_argument("--prob_crossover", type=float)
        parser.add_argument("--prob_mutation", type=float)
        parser.add_argument("--termination", type=str)
        parser.add_argument("--termination_arg", type=str)
        args = parser.parse_args()
        if args.selection == "tournament":
            selection_f = tournament_selection
        elif args.selection == "roulette":
            selection_f = roulette_selection
        if args.crossover == "one_point":
            crossover_f = one_point_crossover
        elif args.crossover == "two_point":
            crossover_f = two_point_crossover
        prob_crossover = args.prob_crossover
        prob_mutation = args.prob_mutation
        if args.termination == "iterations":
            termination_f = gen_terminate_after_iterations(int(args.termination_arg))
        elif args.termination == "fitness_goal":
            termination_f = gen_terminate_after_fitness_goal(float(args.termination_arg))
        elif args.termination == "std_deviation":
            termination_f = gen_terminate_after_std_dev_goal(float(args.termination_arg))
    
    solution_rater = solutions.SolutionRater("", False)
    ga = GA(gen_gen_starting_pop(pop_size, get_genotype_size(problem_size), problem_size, False),
            gen_fitness(problem), selection_f, crossover_f, mutation,
            termination_f, prob_crossover, prob_mutation, problem_size)

    # bf_best_solution = solutions.bruteforce(solution_rater, problem)
    # bf_best_rating = solution_rater.rate(bf_best_solution, problem)
    # print("BF = {} = {}".format(bf_best_solution, bf_best_rating))    
    ga_best_genotype = ga.run()
    ga_best_solution = decode_genotype(ga_best_genotype, problem_size)
    if solutions.validate_solution(ga_best_solution, problem_size):
        ga_best_rating = solution_rater.rate(ga_best_solution, problem)
    else:
        ga_best_rating = 0
    print("GA = {} = {}".format(ga_best_solution, ga_best_rating))
    

if __name__ == "__main__":
    main()
    
    
    
    
    