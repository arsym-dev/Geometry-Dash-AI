import pygame
from pygame.locals import *

SCREENRECT = Rect(0, 0, 640, 480)

class Textsprite(pygame.sprite.Sprite):
    def __init__(self, text):
        pygame.sprite.Sprite.__init__(self)
        self.text = text
        self.pos = 0
        self.update()
    def update(self):
        self.image = pygame.font.Font(None, 36).render(self.text, 1, (0, 0, 0))
        self.highlight = pygame.font.Font(None, 36).render(self.text[:self.pos], 1, (0, 0, 255))
        self.image.blit(self.highlight, (0, 0))
        self.rect = self.image.get_rect()
        self.rect.center = pygame.display.get_surface().get_rect().center
    def keyin(self, key):
        if key == self.text[self.pos]:
            self.pos = self.pos + 1
        if len(self.text) == self.pos:
            self.pos = 0

def main():
    pygame.init()

    screen = pygame.display.set_mode(SCREENRECT.size)

    # make background
    background = pygame.Surface(SCREENRECT.size).convert()
    background.fill((255, 255, 255))
    screen.blit(background, (0, 0))
    pygame.display.update()

    # keep track of sprites
    all = pygame.sprite.RenderUpdates()

    # keep track of time
    clock = pygame.time.Clock()

    textsprite = Textsprite('The quick brown fox jumps over the lazy dog')
    all.add(textsprite)

    # game loop
    while 1:

        # get input
        for event in pygame.event.get():
            if event.type == QUIT:
                return
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    return
                else:
                    textsprite.keyin(event.unicode)

        # clear sprites
        all.clear(screen, background)

        # update sprites
        all.update()

        # redraw sprites
        dirty = all.draw(screen)
        pygame.display.update(dirty)

        # maintain frame rate
        clock.tick(30)

if __name__ == '__main__': main()
