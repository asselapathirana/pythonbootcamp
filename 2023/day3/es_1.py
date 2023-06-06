import numpy as np

"""Fitness function to be minimized. 
   Example: minimize the sum of squares of the variables.
    x - a numpy array of values for the variables
    returns a single floating point value representing the fitness of the solution"""
def fitness_function(x):
    return np.sum(x**2)  # Example: minimize the sum of squares

"""Evolves a population of candidate solutions using the evolutionary strategy algorithm.
    fitness_function - the fitness function to be minimized
    num_variables - the number of variables in each candidate solution
    population_size - the number of candidate solutions in the population
    num_generations - the number of generations to evolve the population
    returns the best solution evolved"""
def evolutionary_strategy(fitness_function, num_variables, population_size, num_generations):
    # Initialize the population
    population = np.random.uniform(low=-5.0, high=5.0, size=(population_size, num_variables))

    for generation in range(num_generations):
        # Evaluate the fitness of each individual in the population
        fitness = np.array([fitness_function(individual) for individual in population])

        # Select the best individuals for the next generation
        elite_indices = np.argsort(fitness)[:int(population_size/2)]
        elite_population = population[elite_indices]

        # Create the next generation
        next_generation = []
        for _ in range(population_size):
            parent_indices = np.random.choice(range(len(elite_population)), size=2)
            parents = elite_population[parent_indices]
            child = np.mean(parents, axis=0) + np.random.normal(scale=0.1, size=num_variables)
            next_generation.append(child)

        population = np.array(next_generation)

        print(np.argmin(fitness), np.min(fitness))  # Print the best individual from each generation
    # Find the best individual in the final population
    fitness = np.array([fitness_function(individual) for individual in population])
    best_index = np.argmin(fitness)
    best_individual = population[best_index]

    return best_individual

# Example usage
num_variables = 5
population_size = 50
num_generations = 100

best_solution = evolutionary_strategy(fitness_function, num_variables, population_size, num_generations)
print("Best solution:", best_solution)
print("Fitness:", fitness_function(best_solution))
