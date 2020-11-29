import sys
import problems
import solutions
import presets
import utils
import argparse


def check_positive(value):
    ivalue = int(value)
    if ivalue <= 0:
        raise argparse.ArgumentTypeError("%s is an invalid positive int value" % value)
    return ivalue


if __name__ == "__main__":
    if len(sys.argv) > 1:
        parser = argparse.ArgumentParser()
        parser.add_argument("--problem_source", type=str)
        parser.add_argument("--random_problem_size", type=check_positive, default=5)
        parser.add_argument("--problem_file", type=str, default="")
        parser.add_argument("--solver", type=str)
        parser.add_argument("--iterations", type=check_positive, default=1000)
        parser.add_argument("--tabu_size", type=check_positive, default=100)
        parser.add_argument("--output_results_to_terminal", action="store_true")
        parser.add_argument("--output_results_to_file", action="store_true")
        parser.add_argument("--results_output_file", type=str, default="")
        parser.add_argument("--output_plot_data_to_file", action="store_true")
        parser.add_argument("--plot_data_output_file", type=str, default="")
        parser.add_argument("--plotting_step", type=check_positive, default=1)
        args = parser.parse_args()
        
        if args.problem_source == "random":
            problem = problems.get_problem("random", args.random_problem_size)
        elif args.problem_source == "file":
            problem = problems.get_problem("file", args.problem_file)
        else:
            print("Invalid problem source.")
            sys.exit()
        
        solver = solutions.Solver(args.solver, solutions.get_solver(args.solver))
        if args.solver == "bruteforce":
            solver.solve(problem,
                         output_results_to_terminal=args.output_results_to_terminal,
                         output_results_to_file=args.output_results_to_file,
                         results_output_file=args.results_output_file,
                         output_plot_data_to_file=args.output_plot_data_to_file,
                         plot_data_output_file=args.plot_data_output_file,
                         plotting_step=args.plotting_step
                         )
        elif args.solver == "hillclimb1" or args.solver == "hillclimb2":
            solver.solve(problem,
                         args.iterations,
                         output_results_to_terminal=args.output_results_to_terminal,
                         output_results_to_file=args.output_results_to_file,
                         results_output_file=args.results_output_file,
                         output_plot_data_to_file=args.output_plot_data_to_file,
                         plot_data_output_file=args.plot_data_output_file,
                         plotting_step=args.plotting_step
                         )
        elif args.solver == "tabu":
            solver.solve(problem,
                         args.iterations,
                         args.tabu_size,
                         output_results_to_terminal=args.output_results_to_terminal,
                         output_results_to_file=args.output_results_to_file,
                         results_output_file=args.results_output_file,
                         output_plot_data_to_file=args.output_plot_data_to_file,
                         plot_data_output_file=args.plot_data_output_file,
                         plotting_step=args.plotting_step
                         )
    
    else:
        pass
    
