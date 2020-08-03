import pygame
import neat

import time
import os
import random

from ground import Ground
from bird import Bird
from pipe import Pipe
pygame.font.init()

WINDOW_W = 500
WINDOW_H = 800


def asset_path(asset_name, asset_type="imgs"):
    return os.path.join(asset_type, asset_name)


def load_image(path):
    return pygame.transform.scale2x(pygame.image.load(asset_path(path)))


BIRD_IMGS = [
    load_image('bird1.png'),
    load_image('bird2.png'),
    load_image('bird3.png')
]

PIPE_IMG = load_image('pipe.png')
BG_IMG = load_image('bg.png')
GROUND_IMG = load_image('base.png')

STAT_FONT = pygame.font.SysFont('comicsans', 50)

GEN = 1


def draw_window(win, birds, pipes, ground, score, gen=1):
    win.blit(BG_IMG, (0, 0))
    # print(len(birds))
    for i, bird in enumerate(birds):
        # print('bird {}', i)
        bird.draw(win)

    text = STAT_FONT.render("Score: " + str(score), 1, (255, 255, 255))
    # win.blit(text, (WINDOW_W - 10 - text.get_width(), 10))
    win.blit(text, (15, 10))
    text = STAT_FONT.render("Generation: " + str(gen), 1, (255, 255, 255))
    win.blit(text, (15, 45))
    text = STAT_FONT.render("Alive: " + str(len(birds)), 1, (255, 255, 255))
    win.blit(text, (15, 80))
    for pipe in pipes:
        pipe.draw(win)
    ground.draw(win)
    # win.blit(PIPE_IMG,(200,700))
    pygame.display.update()


def main(genomes, config):
    global GEN
    birds = []
    nets = []
    ge = []
    # print(genomes, config)
    for _, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        birds.append(Bird(230, 350, BIRD_IMGS))
        g.fitness = 0
        ge.append(g)
    # print(len(birds))
    # Bird(230, 350)
    ground = Ground(730, GROUND_IMG)
    pipes = [Pipe(600, PIPE_IMG)]
    # print(PIPE_IMG.get_height())
    score = 0
    win = pygame.display.set_mode((WINDOW_W, WINDOW_H))
    pygame.display.set_caption('FLAPPY BIRD')
    run = True
    # i = 0
    clock = pygame.time.Clock()
    while run:
        clock.tick(50)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()

        pipe_ind = 0
        if len(birds) > 0:
            if len(pipes) > 1 and birds[0].x > pipes[0].x + pipes[0].PIPE_TOP.get_width():
                pipe_ind = 1
        else:
            run = False
            break
            # if event.type == pygame.KEYDOWN:
            #     if event.key == pygame.K_SPACE:
            #         bird.jump()

        for x, bird in enumerate(birds):
            bird.move()
            ge[x].fitness += 0.1
            output = nets[x].activate(
                (bird.y, abs(bird.y-pipes[pipe_ind].height), abs(bird.y-pipes[pipe_ind].bottom)))
            if output[0] > 0.5:
                bird.jump()
        # bird.move()
        rem = []
        add_pipe = False
        for pipe in pipes:
            for x, bird in enumerate(birds):
                if pipe.collide(bird):
                    # print('colliding'+str(i))
                    ge[x].fitness -= 1
                    birds.pop(x)
                    nets.pop(x)
                    ge.pop(x)
                    # i += 1
                    # run = False

                if not pipe.passed and pipe.x < bird.x:
                    pipe.passed = True
                    add_pipe = True

            if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                rem.append(pipe)
            pipe.move()

        for r in rem:
            pipes.remove(r)
        for x, bird in enumerate(birds):
            if bird.y + bird.img.get_height() >= 730 or bird.y < 0:
                # print('hit the g')
                # run = False
                birds.pop(x)
                nets.pop(x)
                ge.pop(x)

        if add_pipe:
            score += 1
            for g in ge:
                g.fitness += 5
            pipes.append(Pipe(600, PIPE_IMG))
        draw_window(win, birds, pipes, ground, score, gen=GEN)
        # draw_window(win, pipe)
    GEN += 1
    # pygame.quit()
    # print('GAME OVER')


# main()


def run(config_path):

    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)
    p = neat.Population(config)

    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    winner = p.run(main, 50)


if __name__ == "__main__":
    config_path = os.path.join(os.path.dirname(__file__), 'neat-config.txt')
    run(config_path)
