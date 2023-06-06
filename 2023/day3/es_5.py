import numpy as np
from matplotlib import pyplot as plt

"""Fitness function to be minimized. 
   Example: minimize the sum of squares of the variables.
    x - a numpy array of values for the variables
    returns a single floating point value representing the fitness of the solution"""
def fitness_function(x):
    return np.sum(x**2)   # Example: minimize the sum of squares, solution is all values are 0.0

"""Prints updates about the evolution of the population."""
def monitor_function(generation, population, fitness):
    if generation % 25 == 0:
        best_index = np.argmin(fitness)
        best_individual = population[best_index]
        best_fitness = fitness[best_index]
        print(f"Generation {generation:6d}: Best solution = {np.round(best_individual,5)}, Fitness = {best_fitness:10.6f}")
        
best_fitnesses = []

"""Real-time plotting of the best fitness over time."""
def monitor_function2(generation, population, fitness):
    monitor_function(generation, population, fitness)
    best_fitness = np.min(fitness)
    best_fitnesses.append(best_fitness)

    plt.clf()
    plt.plot(best_fitnesses)
    plt.xlabel('Generation')
    plt.ylabel('Best Fitness in the Population')
    plt.title('Progress')
    plt.pause(0.00001)


"""Evolutinoary strategy algorithm. Evolves a population of candidate solutions using the evolutionary strategy algorithm.
    fitness_function - the fitness function to be minimized
    num_variables - the number of variables in each candidate solution
    population_size - the number of candidate solutions in the population
    num_generations - the number of generations to evolve the population
    monitor_func - a function that is called after each generation, with the generation number, population, and fitness as parameters
    returns the best solution evolved."""
def evolutionary_strategy(fitness_function, num_variables, population_size, num_generations, monitor_func=None):
    # Initialize the population
    population = np.random.uniform(low=-5.0, high=5.0, size=(population_size, num_variables))

    for generation in range(num_generations):
        # Evaluate the fitness of each individual in the population
        fitness = np.array([fitness_function(individual) for individual in population])

        # Call the monitor function (if provided)
        if monitor_func is not None:
            monitor_func(generation, population, fitness)

        # Select the best individuals for the next generation 
        elite_indices = np.argsort(fitness)[:int(population_size/2)]
        elite_population = population[elite_indices]

        # Create the next generation with one elite individual
        next_generation = [elite_population[0]]

        # Create the rest of the next generation
        for _ in range(population_size - 1):
            parent_indices = np.random.choice(range(len(elite_population)), size=2)
            parents = elite_population[parent_indices]
            child = np.mean(parents, axis=0) + np.random.normal(scale=0.1, size=num_variables)
            next_generation.append(child)

        population = np.array(next_generation)

    # Find the best individual in the final population
    fitness = np.array([fitness_function(individual) for individual in population])
    best_index = np.argmin(fitness)
    best_individual = population[best_index]

    return best_individual

# Run the evolutionary strategy algorithm
num_variables = 3
population_size = 50
num_generations = 200

best_solution = evolutionary_strategy(fitness_function, num_variables, population_size, num_generations, monitor_func=monitor_function2)
plt.show(block=True)
