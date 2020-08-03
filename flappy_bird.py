import pygame
import neat

import time
import os
import random

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
BASE_IMG = load_image('base.png')

STAT_FONT = pygame.font.SysFont('comicsans', 50)
STAT_FONT_SMALL = pygame.font.SysFont('comicsans', 35)


class Bird:
    IMGS = BIRD_IMGS
    MAX_ROTATION = 25
    ROT_VEL = 20
    ANIMATION_TIME = 5

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.tilt = 0
        self.tick_count = 0
        self.velocity = -10
        self.image_count = 0
        self.img = self.IMGS[0]
        self.jumped_at = 0

    def jump(self):
        self.vel = -10.5
        self.tick_count = 0
        self.jumped_at = self.y

    def move(self):
        self.tick_count += 1
        d = self.velocity*self.tick_count + 1.5*self.tick_count**2
        if d >= 16:
            d = (d/abs(d)) * 16
        # s = ut + (1/2)a(t*t) lol
        if d < 0:
            d -= 2
        self.y = self.y + d

        if d < 0 or (self.y < self.jumped_at + 50):
            if self.tilt < self.MAX_ROTATION:
                self.tilt = self.MAX_ROTATION
        else:
            if self.tilt > -90:
                self.tilt -= self.ROT_VEL
        # print(self.x, self.y, d, self.tick_count)

    def draw(self, win):
        self.image_count += 1
        cycle_pos = self.image_count // self.ANIMATION_TIME
        # print(self.image_count, cycle_pos)
        if cycle_pos == 3:
            if self.image_count % self.ANIMATION_TIME == 1:
                self.img = self.IMGS[0]
                self.image_count = 0
            else:
                self.img = self.IMGS[1]
        else:
            self.img = self.IMGS[cycle_pos]
        # if self.image_count < self.ANIMATION_TIME:
        #     self.img = self.IMGS[0]
        # elif

        if self.tilt <= -80:
            self.img = self.IMGS[1]
            self.image_count = self.ANIMATION_TIME*2

        tilted_image = pygame.transform.rotate(self.img, self.tilt)
        new_rect = tilted_image.get_rect(
            center=self.img.get_rect(topleft=(int(self.x), int(self.y))).center)
        win.blit(tilted_image, new_rect.topleft)

    def get_mask(self):
        return pygame.mask.from_surface(self.img)


class Pipe:
    GAP = 200
    VEL = 5

    def __init__(self, x):
        self.x = x
        self.height = 0
        # self.gap = 100
        self.top = 0
        self.bottom = 0
        self.PIPE_BOTTOM = PIPE_IMG
        self.PIPE_TOP = pygame.transform.flip(PIPE_IMG, False, True)

        self.passed = False
        self.set_height()

    def set_height(self):
        self.height = random.randrange(50, 450)
        self.top = self.height - self.PIPE_TOP.get_height()
        self.bottom = self.height + self.GAP

    def move(self):
        self.x -= self.VEL

    def draw(self, win):
        win.blit(self.PIPE_TOP, (self.x, self.top))
        win.blit(self.PIPE_BOTTOM, (self.x, self.bottom))

    def collide(self, bird):
        bird_mask = bird.get_mask()
        top_mask = pygame.mask.from_surface(self.PIPE_TOP)
        bottom_mask = pygame.mask.from_surface(self.PIPE_BOTTOM)
        top_offset = (self.x - bird.x, self.top - round(bird.y))
        bottom_offset = (self.x - bird.x, self.bottom - round(bird.y))

        b_point = bird_mask.overlap(bottom_mask, bottom_offset)
        t_point = bird_mask.overlap(top_mask, top_offset)

        if t_point or b_point:
            return True
        else:
            return False


class Ground:
    VEL = 5
    WIDTH = BASE_IMG.get_width()
    IMG = BASE_IMG

    def __init__(self, y):
        self.y = y
        self.x1 = 0
        self.x2 = self.WIDTH

    def move(self):
        self.x1 -= self.VEL
        self.x2 -= self.VEL

        if self.x1 + self.WIDTH == 0:
            self.x1 = self.WIDTH

        if self.x2 + self.WIDTH == 0:
            self.x2 = self.WIDTH

    def draw(self, win):
        win.blit(self.IMG, (self.x1, self.y))
        win.blit(self.IMG, (self.x2, self.y))


def draw_window(win, bird, pipes, ground, score, msg=""):
    win.blit(BG_IMG, (0, 0))
    bird.draw(win)
    for pipe in pipes:
        pipe.draw(win)
    text = STAT_FONT.render("Score: " + str(score), 1, (255, 255, 255))
    win.blit(text, (WINDOW_W - 10 - text.get_width(), 10))
    text = STAT_FONT_SMALL.render(msg, 1, (255, 255, 255))
    win.blit(text, (WINDOW_W - 10 - text.get_width(), 50))

    ground.draw(win)
    # win.blit(PIPE_IMG,(200,700))
    pygame.display.update()


def main():
    bird = Bird(230, 350)
    ground = Ground(730)
    pipes = [Pipe(600)]
    # print(PIPE_IMG.get_height())
    score = 0
    win = pygame.display.set_mode((WINDOW_W, WINDOW_H))

    run = True
    i = 0
    clock = pygame.time.Clock()
    draw_window(win, bird, pipes, ground, score)
    text = STAT_FONT.render("Press Space Bar To Start", 1, (255, 255, 255))
    win.blit(text, (50, bird.y-80))
    pygame.display.update()
    start = False
    while not start:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird.jump()
                    start = True

    while run:
        clock.tick(25)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird.jump()
                if event.key == pygame.K_ESCAPE:
                    pause = True
                    draw_window(win, bird, pipes, ground, score,
                                msg="Press JUMP to resume")
                    while pause:
                        for event in pygame.event.get():
                            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                                bird.jump()
                                pause = False
        bird.move()
        rem = []
        add_pipe = False
        for pipe in pipes:
            if pipe.collide(bird):
                # print('colliding'+str(i))
                i += 1
                run = False

            if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                rem.append(pipe)

            if not pipe.passed and pipe.x < bird.x:
                pipe.passed = True
                add_pipe = True

            pipe.move()

        for r in rem:
            pipes.remove(r)

        if bird.y + bird.img.get_height() >= 730:
            # print('hit the g')
            run = False
        if add_pipe:
            score += 1
            pipes.append(Pipe(600))
        draw_window(win, bird, pipes, ground, score, msg="Press ESC to pause")
        # draw_window(win, pipe)

    # pygame.quit()
    print('-'*20)
    print('GAME OVER')
    print('YOUR SCORE : '+str(score))
    print('-'*20)


main()
