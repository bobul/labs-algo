import random
import matplotlib.pyplot as plt

P = 250
num_items = 100
max_value = 20
max_weight = 10
population_size = 100
crossover_probability = 0.8
mutation_probability = 0.05
iterations = 1000

population = [random.choices([0, 1], k=num_items) for _ in range(population_size)]


def fitness(solution):
    total_value = sum(
        value * solution[i] for i, value in enumerate(random.choices(range(2, max_value + 1), k=num_items)))
    total_weight = sum(
        weight * solution[i] for i, weight in enumerate(random.choices(range(1, max_weight + 1), k=num_items)))

    if total_weight > P:
        return 0
    else:
        return total_value


def one_point_crossover(parent1, parent2):
    crossover_point = random.randint(0, num_items - 1)
    child1 = parent1[:crossover_point] + parent2[crossover_point:]
    child2 = parent2[:crossover_point] + parent1[crossover_point:]
    return child1, child2


def mutation(solution):
    mutation_point = random.randint(0, num_items - 1)
    solution[mutation_point] = 1 - solution[mutation_point]


def local_search(solution):
    for i in range(num_items):
        modified_solution = solution.copy()
        modified_solution[i] = 1 - modified_solution[i]
        modified_quality = fitness(modified_solution)

        if modified_quality > fitness(solution):
            solution = modified_solution

    return solution


quality_history = []
solution_values = []

for iteration in range(1, iterations + 1):
    scores = [fitness(solution) for solution in population]

    selected_parents = random.choices(population, weights=scores, k=population_size)

    new_population = []
    for i in range(0, population_size, 2):
        if random.random() < crossover_probability:
            child1, child2 = one_point_crossover(selected_parents[i], selected_parents[i + 1])
            new_population.extend([child1, child2])
        else:
            new_population.extend([selected_parents[i], selected_parents[i + 1]])

    for solution in new_population:
        if random.random() < mutation_probability:
            mutation(solution)

    best_solutions = sorted(zip(new_population, scores), key=lambda x: x[1], reverse=True)[:10]
    for solution, _ in best_solutions:
        solution = local_search(solution)

    population = new_population

    if iteration % 20 == 0:
        best_solution = max(zip(population, scores), key=lambda x: x[1])
        print(f"Iteration {iteration}: Best Solution - {best_solution[1]}")
        quality_history.append(best_solution[1])
        solution_values.append(best_solution[1])

iterations_list = list(range(20, iterations + 1, 20))
plt.plot(iterations_list, quality_history, marker='o')
plt.title('Залежність якості розв\'язку від числа ітерацій')
plt.xlabel('Число ітерацій')
plt.ylabel('Якість розв\'язку')
plt.savefig("graphics_iteration_quality.png")
plt.show()

print("Значення цільової функції для кожної ітерації:")
for iteration, value in enumerate(solution_values, start=1):
    print(f"Iteration {iteration}: {value}")
