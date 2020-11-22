import sys
import problems
import solutions
import presets
import utils

def fun(problem, filename):
    solver1 = solutions.Solver("bruteforce", solutions.bruteforce)
    solver2 = solutions.Solver("hillclimb1", solutions.hillclimb_ver1)
    solver3 = solutions.Solver("hillclimb2", solutions.hillclimb_ver2)
    solver4 = solutions.Solver("tabu", solutions.tabu)
    solver1.solve(problem, output_to_file=True, output_file=filename+"_bruteforce.txt", measure_time=True)
    solver2.solve(problem, 1000, output_to_file=True, output_file=filename+"_hillclimb1.txt", measure_time=True)
    solver3.solve(problem, 1000, output_to_file=True, output_file=filename+"_hillclimb2.txt", measure_time=True)
    solver4.solve(problem, 1000, 100, output_to_file=True, output_file=filename+"_tabu.txt", measure_time=True)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "random":
            problem = problems.get_problem("random", int(sys.argv[2]))
            fun(problem, sys.argv[3])
        elif sys.argv[1] == "read_file":
            problem = problems.get_problem("read_file", sys.argv[2])
            fun(problem, sys.argv[3])
            
    else:
    
        problem_list = []
        problem_list.append(problems.get_problem("random", 8))
        problem_list.append(problems.get_problem("read_file", "problems/size7_000.txt"))
        #problems.append(problems.get_problem("random", 10))
    
        solver1 = solutions.Solver("bruteforce", solutions.bruteforce)
        solver2 = solutions.Solver("hillclimb1", solutions.hillclimb_ver1)
        solver3 = solutions.Solver("hillclimb2", solutions.hillclimb_ver2)
        solver4 = solutions.Solver("tabu", solutions.tabu)
        
        for i, problem in enumerate(problem_list):
            print("########################")
            print(f'Problem #{i}')
            print("########################")
            print()
            
            solver1.solve(problem, output_to_terminal=True, measure_time=True)
            solver2.solve(problem, 1000, output_to_terminal=True, measure_time=True)
            solver3.solve(problem, 1000, output_to_terminal=True, measure_time=True)
            solver4.solve(problem, 1000, 100, output_to_terminal=True, measure_time=True)
    
    
    