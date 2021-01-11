import ga
import itertools
import sys
import numpy as np


if __name__ == "__main__":
    
    experiments = 5
    
    selections = ["tournament", "roulette"]
    crossovers = ["one_point", "two_point"]
    #prob_cross = list(np.linspace(0,1,11))
    #prob_mut = list(np.linspace(0,1,11))
    prob_cross = [0, 0.3, 0.6, 0.8]
    prob_mut = [0, 0.01, 0.02, 0.1]
    pop_sizes = [20, 40, 100]
    
    termination = "iterations"
    iterations = 100
    
    arguments = list(itertools.product(selections, crossovers, prob_cross,
                                        prob_mut, pop_sizes))
    
    best_result = float("inf")
    best_selection = arguments[0][0]
    best_crossover = arguments[0][1]
    best_prob_cross = arguments[0][2]
    best_prob_mut = arguments[0][3]
    best_pop_size = arguments[0][4]
    
    for arg in arguments:   
        results = []
        for i in range(experiments):
            _, result = ga.run(arg[0], arg[1], arg[2], arg[3], termination,
                                iterations, arg[4])
            if result != 0:
                results.append(result)
        if len(results) == 0:
            continue
        
        avg_result = sum(results) / len(results)
        
        print(avg_result)
        
        if avg_result < best_result:
            best_result = avg_result
            best_selection = arg[0]
            best_crossover = arg[1]
            best_prob_cross = arg[2]
            best_prob_mut = arg[3]
            best_pop_size = arg[4]
        
    print(best_result)
    print(best_selection)
    print(best_crossover)
    print(best_prob_cross)
    print(best_prob_mut)
    print(best_pop_size)
    
    
    # arguments = [
    #     #0
    #     ["tournament","one_point",0.5,0.01,"iterations",100],
    #     #1
    #     ["tournament","one_point",0.5,0.01,"fitness_goal",0.0000015],
    #     #2
    #     ["tournament","one_point",0.5,0.01,"std_deviation",0.001],
    #     #3
    #     ["tournament","two_point",0.5,0.01,"iterations",100],
    #     #4
    #     ["roulette","one_point",0.5,0.01,"iterations",100],
    #     #5
    #     ["roulette","two_point",0.5,0.01,"iterations",100],
    #     #6
    #     ]
    
    # for exp, a in enumerate(arguments):
    #     result = 0
    #     for i in range(experiments):
    #         x, r = ga.run(*a)
    #         result += r
    #     result = result / experiments
    #     print(exp, result)
        
        