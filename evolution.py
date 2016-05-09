# -*- coding: utf-8 -*-
# pylint: disable=
"""
Created on Tue May  3 18:34:45 2016

@author: P. Rodriguez-Mier and T. Teijeiro
"""

import random
import invaders

class Evolution:
    def __init__(self, population, prob_crossover=0.8, prob_mutation=0.1):
        self.population = population
        self.prob_crossover = prob_crossover
        self.prob_mutation = prob_mutation

    @classmethod
    def random(cls, size=30):
        pass

    def mutate(self, individual):
        pass
