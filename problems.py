import random as rand
import utils


def validate_problem(problem):
    locations = problem[0]
    distances = problem[1]
    facilities = problem[2]
    flows = problem[3]
    size = len(locations)
    if len(facilities) != size:
        return False
    pairs = utils.generate_pairs(size)
    if len(pairs) != len(distances):
        return False
    if len(distances) != len(flows):
        return False
    distances_keys = list(distances.keys())
    flows_keys = list(flows.keys())
    for i, pair in enumerate(utils.generate_pairs(size)):
        if pair != distances_keys[i] or pair != flows_keys[i]:
            return False
    return True


def print_problem(problem):
    locations = problem[0]
    distances = problem[1]
    facilities = problem[2]
    flows = problem[3]
    for key, value in distances.items():
        print("Distance between {} and {} is {}".format(locations[key[0]],locations[key[1]],value))
    for key, value in flows.items():
        print("Flow between {} and {} is {}".format(facilities[key[0]],facilities[key[1]],value))


def read_problem_from_file(filename):
    locations = []
    distances = {}
    facilities = []
    flows = {}
    with open(filename, "r") as file:
        lines = file.read().splitlines()
    size = int(lines[0])
    cnt = 1
    pairs = utils.generate_pairs(size)
    for i in range(size):
        locations.append(lines[cnt])
        cnt += 1
    for pair in pairs:
        distances[pair] = int(lines[cnt])
        cnt += 1
    for i in range(size):
        facilities.append(lines[cnt])
        cnt += 1
    for pair in pairs:
        flows[pair] = int(lines[cnt])
        cnt += 1
    file.close()
    return [locations, distances, facilities, flows]


def get_output_for_writing_problem_to_file(problem):
    locations = problem[0]
    distances = problem[1]
    facilities = problem[2]
    flows = problem[3]
    size = len(problem[0])
    output = []
    cnt = 1
    output.append(str(size)+'\n')
    pairs = utils.generate_pairs(size)
    for i in range(size):
        output.append(locations[i]+'\n')
        cnt += 1
    for pair in pairs:
        output.append(str(distances[pair])+'\n')
        cnt += 1
    for i in range(size):
        output.append(facilities[i]+'\n')
        cnt += 1
    for pair in pairs:
        output.append(str(flows[pair])+'\n')
        cnt += 1
    return output


def write_problem_to_file(filename, problem):
    file = open(filename, "w")
    file.writelines(get_output_for_writing_problem_to_file(problem))
    file.close()
    return 0


def generate_example_problem():
    locations = ["Szczecin","Cracow","Lublin","Gdansk"]
    distances = {
        (0, 1):973,
        (0, 2):463,
        (0, 3):134,
        (1, 2):430,
        (1, 3):828,
        (2, 3):201,
        }
    facilities = ["Car factory","Coal mine","Port","Shipyard"]
    flows = {
        (0, 1):29,
        (0, 2):69,
        (0, 3):98,
        (1, 2):45,
        (1, 3):14,
        (2, 3):33,
        }
    return [locations, distances, facilities, flows]


def generate_random_problem(size):
    locations = []
    distances = {}
    facilities = []
    flows = {}
    location_names = ["Warsaw","Cracow","Lodz","Wroclaw","Poznan","Gdansk","Szczecin","Bydgoszcz","Lublin","Bialystok","Katowice","Gdynia"]
    facility_names = ["Phone factory","Refinery","Coal mine","Hospital","Car factory","Missle silo","Centrifuge","Shipyard","Port","Power plant","5G tower","Airport"]
    rand.shuffle(location_names)
    rand.shuffle(facility_names)
    #size = rand.randint(3, 10)
    for i in range(size):
        locations.append(location_names[i])
        facilities.append(facility_names[i])
    for pair in utils.generate_pairs(size):
        distances[pair] = rand.randint(50,1000)
        flows[pair] = rand.randint(0,100)
    return [locations, distances, facilities, flows]


def get_problem(method, *argv):
    if method == "example":
        return generate_example_problem()
    if method == "random":
        return generate_random_problem(argv[0])
    if method == "read_file":
        return read_problem_from_file(argv[0])
    if method == "read_files":
        problems = []
        for arg in argv:
            problems.append(read_problem_from_file(arg))
        return problems

