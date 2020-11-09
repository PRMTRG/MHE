import random as rand
import utils

def validateProblem(problem):
    locations = problem[0]
    distances = problem[1]
    facilities = problem[2]
    flows = problem[3]
    size = len(locations)
    if len(facilities) != size:
        return False
    pairs = utils.generatePairs(size)
    if len(pairs) != len(distances):
        return False
    if len(distances) != len(flows):
        return False
    distancesKeys = list(distances.keys())
    flowsKeys = list(flows.keys())
    for i, pair in enumerate(utils.generatePairs(size)):
        if pair != distancesKeys[i] or pair != flowsKeys[i]:
            return False
    return True

def printProblem(problem):
    locations = problem[0]
    distances = problem[1]
    facilities = problem[2]
    flows = problem[3]
    for key, value in distances.items():
        print("Distance between {} and {} is {}".format(locations[key[0]],locations[key[1]],value))
    for key, value in flows.items():
        print("Flow between {} and {} is {}".format(facilities[key[0]],facilities[key[1]],value))

def readProblemFromFile(filename):
    locations = []
    distances = {}
    facilities = []
    flows = {}
    with open(filename, "r") as file:
        lines = file.read().splitlines()
    size = int(lines[0])
    cnt = 1
    pairs = utils.generatePairs(size)
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

def getOutputForWritingProblemToFile(problem):
    locations = problem[0]
    distances = problem[1]
    facilities = problem[2]
    flows = problem[3]
    size = len(problem[0])
    output = []
    cnt = 1
    output.append(str(size)+'\n')
    pairs = utils.generatePairs(size)
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

def writeProblemToFile(filename, problem):
    file = open(filename, "w")
    file.writelines(getOutputForWritingProblemToFile(problem))
    file.close()
    return 0

def generateExampleProblem():
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

def generateRandomProblem(size):
    locations = []
    distances = {}
    facilities = []
    flows = {}
    locationNames = ["Warsaw","Cracow","Lodz","Wroclaw","Poznan","Gdansk","Szczecin","Bydgoszcz","Lublin","Bialystok","Katowice","Gdynia"]
    facilityNames = ["Phone factory","Refinery","Coal mine","Hospital","Car factory","Missle silo","Centrifuge","Shipyard","Port","Power plant","5G tower","Airport"]
    rand.shuffle(locationNames)
    rand.shuffle(facilityNames)
    #size = rand.randint(3, 10)
    for i in range(size):
        locations.append(locationNames[i])
        facilities.append(facilityNames[i])
    for pair in utils.generatePairs(size):
        distances[pair] = rand.randint(50,1000)
        flows[pair] = rand.randint(5,100)
    return [locations, distances, facilities, flows]

def getProblem(method, *argv):
    if method == "example":
        return generateExampleProblem()
    if method == "random":
        return generateRandomProblem(argv[0])
    if method == "readFile":
        return readProblemFromFile(argv[0])
    if method == "readFiles":
        problems = []
        for arg in argv:
            problems.append(readProblemFromFile(arg))
        return problems

