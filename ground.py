
class Ground:
    VEL = 5

    def __init__(self, y, ground_img):
        self.y = y
        self.WIDTH = ground_img.get_width()
        self.IMG = ground_img
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
