import random
import numpy
import pygame
n_pent = 50
mutation_var = 0.5  # determines,in which favour will mutation go (in favour of color, or shape)
n_pop = 5

mutation_rate = 1  # how many polygons will be mutated at once
target = 0
display = 0

WHITE = (255, 255, 255, 255)
BLACK = (0, 0, 0)

width = 0
height = 0


def crossover(population):
    # Crossovering each specimen with each other and also selecting the n_pop best of them, that will compose next
    # generation, by sorting population by fitness score
    arr = [population[0]]
    arr[0].calc_fitness()
    for i in range(1, len(population)):
        for j in range(i+1, len(population)):
            arr.append(crossover_func(population[i], population[j]))
            arr[-1].calc_fitness()
    arr2 = sorted(arr, key=min_fit)
    return arr2[0:n_pop]


def crossover_func(one, two):
    # It goes through every figure and randomly selects the ones that will be compoising a child
    child = Drawing()
    for j in range(n_pent):
        child.figures[j] = random.choice([one.figures[j], two.figures[j]])

    return child


class Figures:
    # Figure is a thing that composes my art
    # Here my figure is pentagon
    def __init__(self):
        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        self.alpha = random.randint(0, 255)
        self.points = [(random.randint(0, width), random.randint(0, height)),
                       (random.randint(0, width), random.randint(0, height)),
                       (random.randint(0, width), random.randint(0, height)),
                       (random.randint(0, width), random.randint(0, height)),
                       (random.randint(0, width), random.randint(0, height))]


def to_array(display):
    arr = []
    for i in range(width):
        arr.append([])
        for j in range(height):
            arr[i].append(display.get_at((i,j))[:3])
    return arr

class Drawing:

    # I decided to place here methods that I use for genetic algorithm( fitness, crossover, mutation)
    # so that code could be readable

    def __init__(self):
        self.figures = []
        for _ in range(n_pent):
            t = Figures()
            self.figures.append(t)
        self.calc_fitness()


    def calc_fitness(self):
        # Calculates fitness by comparing each pixel's color to ideal (input)
        display.fill(WHITE)
        for x in self.figures:
            surface = pygame.Surface((width, height))
            surface.set_colorkey((0, 0, 0))
            surface.set_alpha(x.alpha)
            pygame.draw.polygon(surface, x.color, x.points)
            display.blit(surface, (0, 0))
        one = to_array(display)
        two = numpy.array(target)
        five = numpy.square(one)
        six = numpy.square(two)
        three = five - six
        four = numpy.sum(
            three
        )
        fitness_score = numpy.sqrt(numpy.abs(four))
        self.fitness = fitness_score

    def mutate(self):
        # It randomly chooses whether to change color or shape and then randomly changes it
        for _ in range(mutation_rate):
            pick_index = random.randint(0, n_pent - 1)

            if random.random() < mutation_var:
                index = random.randint(0, 3)
                change = random.randint(0, 255)
                if index == 3:
                    self.figures[pick_index].alpha = change
                else:
                    colors = list(self.figures[pick_index].color)
                    colors[index] = change
                    self.figures[pick_index].color = tuple(colors)

            else:
                index = random.randint(0, 2)
                p1 = self.figures[pick_index].points[0]
                p2 = self.figures[pick_index].points[1]
                p3 = self.figures[pick_index].points[2]
                p4 = self.figures[pick_index].points[3]
                p5 = self.figures[pick_index].points[4]
                dx = random.randint(0, width)
                dy = random.randint(0, height)
                change = [p1, p2, p3, p4, p5]
                change[index] = (dx, dy)
                self.figures[pick_index].points = change


# this function is purly for using in sort and min
def min_fit(drawing):
    return drawing.fitness
