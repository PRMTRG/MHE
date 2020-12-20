import ga

if __name__ == "__main__":
    
    experiments = 50
    
    arguments = [
        #0
        ["tournament","one_point",0.5,0.01,"iterations",100],
        #1
        ["tournament","one_point",0.5,0.01,"fitness_goal",0.0000015],
        #2
        ["tournament","one_point",0.5,0.01,"std_deviation",0.001],
        #3
        ["tournament","two_point",0.5,0.01,"iterations",100],
        #4
        ["roulette","one_point",0.5,0.01,"iterations",100],
        #5
        ["roulette","two_point",0.5,0.01,"iterations",100],
        #6
        ]
    
    for exp, a in enumerate(arguments):
        result = 0
        for i in range(experiments):
            x, r = ga.run(*a)
            result += r
        result = result / experiments
        print(exp, result)
        
        