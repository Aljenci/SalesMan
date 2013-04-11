#-------------------------------------------------------------------------------
# Name:        SalesMan.py
# Purpose:     Python program that solves the Travelling Salesman Problem
#              with Genetic Algorithms
#
# Author:      Alejandro Jimenez Encinas
#
# Created:     11/04/2013
# Copyright:   (c) Alejandro Jimenez Encinas 2013
# Licence:     CC BY-NC-SA
#-------------------------------------------------------------------------------

from random import randint
from Tkinter import *

country = None
master = None
w = None
ga = None
iteration = 0

class Chromosome:
    def __init__(self, size, mutation_probability):
        self.data = [0]
        for i in range(size-1):
            index = randint(1, size-1)
            while index in self.data:
                index = randint(1, size-1)
            self.data.append(index)
        self.data.append(0)

        self.mutation_probability = mutation_probability

    def crossover(self, other):
        crossover_point = randint(1, len(self.data)-2)
        child1 = self.data[:crossover_point]
        for i in other.data:
            if i not in child1:
                child1.append(i)
        child1.append(0)
        child2 = other.data[:crossover_point]
        for i in self.data:
            if i not in child2:
                child2.append(i)
        child2.append(0)
        return child1, child2

    def mutation(self):
        if randint(0, 100) <= self.mutation_probability:
            index1 = randint(1, len(self.data)-2)
            index2 = randint(1, len(self.data)-2)
            aux = self.data[index1]
            self.data[index1] = self.data[index2]
            self.data[index2] = aux

    def adaptability(self):
        distance = 0
        for i in range(len(self.data)-1):
            distance += (country.cities[self.data[i+1]].x-country.cities[self.data[i]].x)**2 + (country.cities[self.data[i+1]].y-country.cities[self.data[i]].y)**2
        return distance

class GA:
    def __init__(self, country, max_generations, population_size):
        self.country = country
        self.max_generations = max_generations
        self.population = []
        for i in range(population_size):
            self.population.append(Chromosome(country.size(), 0.1))

    def step(self):
        self.sort()
        self.crossover()
        self.mutation()

    def sort(self):
        self.population = [p for (a, p) in sorted(zip(self.adaptability(), self.population))]

    def crossover(self):
        child1_best, child2_best = self.population[0].crossover(self.population[1])
        for i in range(2, len(self.population)-4, 2):
            self.population[i].data, self.population[i+1].data = self.population[i].crossover(self.population[i+1])
        self.population[-2].data = child1_best
        self.population[-1].data = child2_best

    def mutation(self):
        for i in self.population:
            i.mutation()

    def adaptability(self):
        adap = []
        for i in self.population:
            adap.append(i.adaptability())
        return adap

    def get_best(self):
        return [p for (a, p) in sorted(zip(self.adaptability(), self.population))][0]

class City:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return str(self.x) + ", " + str(self.y)

class Country:
    def __init__(self, w, h, rand = 0, cities = []):
        self.w = w
        self.h = h
        if rand == 0:
            self.cities = cities
        else:
            self.cities = []
            for i in range(rand):
                self.add_random_city()

    def add_city(self, c):
        self.cities.append(c)

    def add_random_city(self):
        self.cities.append(City(randint(0, self.w), randint(0, self.h)))

    def size(self):
        return len(self.cities)

    def __str__(self):
        s = ""
        for i in self.cities:
            s = s + "[" + str(i) + "]" + ", "
        return s[:-2]

def step():
    global iteration
    print iteration
    iteration += 1

    w.delete(ALL)
    for city in country.cities:
        w.create_oval(city.x-2, city.y-2, city.x+2, city.y+2)
    best = ga.get_best().data
    for i in range(len(best)-1):
        w.create_line(country.cities[best[i]].x, country.cities[best[i]].y, country.cities[best[i+1]].x, country.cities[best[i+1]].y)
    ga.step()

    master.after(1, step)

def main():
    global country, master, w, ga
    country = Country(1000, 1000, 10)
    master = Tk()
    w = Canvas(master, width=1000, height=1000)
    w.pack()

    ga = GA(country, 1000, 1000)

    master.after(1, step)
    master.mainloop()

if __name__ == '__main__':
    main()
