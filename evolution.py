# -*- coding: utf-8 -*-
# pylint: disable=
"""
Created on Tue May  3 18:34:45 2016

@author: P. Rodriguez-Mier and T. Teijeiro
"""

import random


def recombinate(pairs, gene_props, mutation_probability=0.1):
    offspring = []
    for p1, p2 in pairs:
        children_genes = {}
        for gen in p1.genes.keys():
            values = [p1.genes[gen], p2.genes[gen]]
            children_genes[gen] = random.uniform(min(values), max(values))
            if random.random() < mutation_probability:
                min_v = gene_props[gen]['min']
                max_v = gene_props[gen]['max']
                rv = random.gauss(children_genes[gen], (max_v - min_v)*0.1)
                children_genes[gen] = min(max(min_v, rv), max_v)
        offspring.append(children_genes)
    return offspring


def mating_pool(population, num_of_pairs=10, evaluator=lambda x: x.fitness):
    evaluated_population = evaluate(population, evaluator=evaluator)
    return zip(roulette_wheel(evaluated_population, k=num_of_pairs),
               roulette_wheel(evaluated_population, k=num_of_pairs))


def evaluate(population, evaluator=lambda x: x.fitness):
    return map(lambda x: (x, evaluator(x)), population)


def roulette_wheel(evaluated_population, k=10):
    sum_fitness = sum([v[1] for v in evaluated_population])
    selected = []
    while len(selected) < k:
        r = random.uniform(0, sum_fitness)
        for i in evaluated_population:
            r -= i[1]
            if r < 0:
                selected.append(i[0])
                break
    return selected


if __name__ == '__main__':
    pop = [15, 18, 30, 100, 120, 60, 35, 40, 42]
    print mating_pool(pop, evaluator=lambda x: x)
