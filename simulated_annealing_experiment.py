import problems
import solutions
import matplotlib.pyplot as plt

if __name__ == "__main__":
    experiments = 10
    problem_files = [
        "problems/size5.txt",
        "problems/size7.txt",
        "problems/size9.txt"
        ]
    iterations_counts = [ 500, 1000, 2000 ]
    f1_args = [ 
        [], 
        [], 
        [] 
        ]
    f2_args = [ 
        [], 
        [], 
        [] 
        ]
    f3_args = [ 
        [ 500 ], 
        [ 1000 ], 
        [ 2000 ] 
        ]
    function_names = [ "f1", "f2", "f3" ]
    functions_arguments = {
        function_names[0]: f1_args,
        function_names[1]: f2_args,
        function_names[2]: f3_args,
        }
    def f1(k, iterations, args):
        return 0.1
    def f2(k, iterations, args):
        return 1000.0 * iterations / k;
    def f3(k, iterations, args):
        x = args[0]
        return x * iterations / k;
    functions = {
        function_names[0]: f1,
        function_names[1]: f2,
        function_names[2]: f3,        
        }
    solution_rater = solutions.SolutionRater("simulated_annealing", False)
    best_result = float("inf")
    
    
    for iterations_count in iterations_counts:
        for function_name in function_names:
            for function_arguments in functions_arguments[function_name]:
                r1 = []
                for problem_file in problem_files:
                    r2 = []
                    problem = problems.get_problem("file", problem_file)
                    for experiment in range(experiments):
                        sol_list, res_list = solutions.simulated_annealing(solution_rater, 
                                                                           problem, iterations_count, 
                                                                           functions[function_name],
                                                                           function_arguments)
                        if function_name == "f3" and \
                            iterations_count == 1000 and \
                            experiment == 0:
                            plt.plot(res_list)
                            plt.title(function_arguments)
                            plt.show()
                            
                        r2.append(res_list[-1])
                    r1.append(sum(r2) / len(r2))
                result = sum(r1) / len(r1)
                if result < best_result:
                    best_result = result
                    best_iterations_count = iterations_count
                    best_function = function_name
                    best_function_arguments = function_arguments
                print("===")
                print("Iterations =", iterations_count)
                print("Function =", function_name)
                print("Arguments =", function_arguments)
                print("Result =", result)
                print("===")
                print()
                
    print("===BEST===")
    print("Iterations =", best_iterations_count)
    print("Function =", best_function)
    print("Arguments =", best_function_arguments)
    print("Result =", best_result)
    print("===")
    print()
    






