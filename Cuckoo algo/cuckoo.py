import random
import copy
import matplotlib.pyplot as plt

GRID_SIZE = 50
NUM_SENSORS = 10
RADIUS = 8

NUM_NESTS = 25
MAX_ITER = 100
PA = 0.25

w1 = 1
w2 = 0.3


def evaluate_solution(solution):

    grid = [[0]*GRID_SIZE for _ in range(GRID_SIZE)]

    for (cx, cy) in solution:
        for x in range(GRID_SIZE):
            for y in range(GRID_SIZE):
                if (x-cx)**2 + (y-cy)**2 <= RADIUS**2:
                    grid[x][y] += 1

    covered = 0
    overlap = 0

    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            if grid[i][j] > 0:
                covered += 1
            if grid[i][j] > 1:
                overlap += grid[i][j] - 1

    total_points = GRID_SIZE * GRID_SIZE
    uncovered = total_points - covered

    fitness = w1 * uncovered + w2 * overlap
    coverage_percent = (covered / total_points) * 100

    return fitness, coverage_percent, covered


def random_solution():

    sol = []

    for _ in range(NUM_SENSORS):
        x = random.randint(0, GRID_SIZE-1)
        y = random.randint(0, GRID_SIZE-1)
        sol.append((x,y))

    return sol


def levy_flight(solution):

    new_solution = copy.deepcopy(solution)

    i = random.randint(0, NUM_SENSORS-1)

    step_x = int(random.gauss(0,5))
    step_y = int(random.gauss(0,5))

    x = new_solution[i][0] + step_x
    y = new_solution[i][1] + step_y

    x = max(0, min(GRID_SIZE-1, x))
    y = max(0, min(GRID_SIZE-1, y))

    new_solution[i] = (x,y)

    return new_solution


nests = []
fitness = []

for _ in range(NUM_NESTS):

    sol = random_solution()

    f,_,_ = evaluate_solution(sol)

    nests.append(sol)
    fitness.append(f)


best_index = fitness.index(min(fitness))
best_solution = nests[best_index]
best_fitness = fitness[best_index]

history = []


for iteration in range(MAX_ITER):

    for i in range(NUM_NESTS):

        new_sol = levy_flight(nests[i])

        new_fit,_,_ = evaluate_solution(new_sol)

        if new_fit < fitness[i]:
            nests[i] = new_sol
            fitness[i] = new_fit


    for i in range(NUM_NESTS):

        if random.random() < PA:
            nests[i] = random_solution()
            fitness[i],_,_ = evaluate_solution(nests[i])


    current_best = min(fitness)
    history.append(current_best)

    if current_best < best_fitness:

        best_fitness = current_best
        best_solution = nests[fitness.index(current_best)]

    print("Iteration", iteration+1, "Best fitness =", current_best)


fitness_val, coverage_percent, covered_tiles = evaluate_solution(best_solution)

print("\nFinal Best Fitness:", fitness_val)
print("Coverage Area (tiles):", covered_tiles)
print("Coverage Percentage:", coverage_percent)
print("\nSensor Positions:")
for s in best_solution:
    print(s)


plt.plot(history)
plt.xlabel("Iteration")
plt.ylabel("Best Fitness")
plt.title("Cuckoo Search Convergence")
plt.show()