# -*- coding: utf-8 -*-
# pylint: disable=
"""
Created on Tue May  3 18:34:45 2016

@author: P. Rodriguez-Mier and T. Teijeiro
"""

import random
import objects

def mating_pool(population, num_of_children=10):
    pool = []
    # Sort the population
    sorted_population = sorted(population, objects.Invader.compare_fitness)
    # Get the maximum fitness
    max_fitness = sorted_population[-1].steps
    while len(pool) < num_of_children*2:
        # Generate a random uniform number between [0, max_fitness]
        r = random.uniform(0, max_fitness)
        # Select the one according to the accumulative probability
        for i in population:
            if i.steps >= r:
                pool.append(i)
                break

    random.shuffle(pool)
    return pool
