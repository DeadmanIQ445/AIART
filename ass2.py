from PIL import Image
import pygame
import classes
import sys
import copy

print('What is the source image path? (e.g "./photo.png")')
input_path = input()
print("Where to store resulting images? (e.g. \"./folder/\" or leave empty if in current folder)")
output_path = input()

target = Image.open(input_path)

width = target.size[0]
height = target.size[1]

classes.target = target
classes.width = width
classes.height = height

n_population = 5
classes.n_pop = n_population
pygame.init()
display_pygame = pygame.display.set_mode((width, height))
classes.display = display_pygame
pygame.display.set_caption('Art')


WHITE = (255, 255, 255, 255)
BLACK = (0, 0, 0)

display_pygame.fill(WHITE)

population = []
for _ in range(classes.n_pop):
    population.append(classes.Drawing())
    population[len(population)-1].calc_fitness()
gen = 0

record = []

while True:
    print("Generation " + str(gen))
    count = 1
    for d in population:
        # prints fitness scores (bigger is worse)
        print(str(count) + ": " + str(d.fitness))
        count += 1
    # Selection
    best = min(population, key=classes.min_fit)
    record.append(best.fitness)
    display_pygame.fill(WHITE)
    for x in best.figures:
        surface = pygame.Surface((width, height))
        surface.set_colorkey((0, 0, 0))
        surface.set_alpha(x.alpha)
        pygame.draw.polygon(surface, x.color, x.points)
        display_pygame.blit(surface, (0, 0))

    pygame.display.update()

    # Composing future generation and mutating it
    st = best.figures
    population = [best]
    for i in range(n_population):
        c = classes.Drawing()
        for j in range(classes.n_pent):
            c.figures[j] = copy.deepcopy(st[j])
        c.mutate()
        population.append(c)

    population = classes.crossover(population)

    if gen % 100 == 0:
        pygame.image.save(display_pygame, output_path + str(gen) + ".jpeg")

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    gen += 1
