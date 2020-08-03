import pygame
import neat


class Bird:

    MAX_ROTATION = 25
    ROT_VEL = 20
    ANIMATION_TIME = 5

    def __init__(self, x, y, bird_imgs):
        self.x = x
        self.y = y
        self.tilt = 0
        self.tick_count = 0
        self.velocity = -10
        self.image_count = 0
        self.jumped_at = 0
        self.IMGS = bird_imgs
        self.img = self.IMGS[0]

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
            center=self.img.get_rect(topleft=(self.x, self.y)).center)
        win.blit(tilted_image, new_rect.topleft)

    def get_mask(self):
        return pygame.mask.from_surface(self.img)
