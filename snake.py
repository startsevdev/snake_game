import pygame
import sys

# pygame.init()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
UP = (0, 1)
DOWN = (0, -1)
LEFT = (-1, 0)
RIGHT = (1, 0)


class Window(object):
    def __init__(self, width=600, height=600):
        self.surface = pygame.display.set_mode((width, height))
        self.clear()

    def clear(self):
        self.surface.fill(BLACK)

    def update(self):
        pygame.display.update()


class Snake(object):
    def __init__(self, window, side_length=20):
        self.x = 0
        self.y = 0
        self.vector = (1, 0)
        self.speed = 5
        self.window = window
        self.surface = window.surface
        self.side_length = side_length

        self.draw()

    def draw(self):
        pygame.draw.rect(self.surface, WHITE, (self.x, self.y, self.side_length, self.side_length))
        self.window.update()

    def move(self):
        self.x += self.vector[0] * self.speed
        self.y += self.vector[1] * self.speed
        self.draw()
        self.window.clear()

    def change_vector(self, key):
        if key == 273:
            self.vector = DOWN
        elif key == 274:
            self.vector = UP
        elif key == 275:
            self.vector = RIGHT
        elif key == 276:
            self.vector = LEFT


def main():
    window = Window()
    snake = Snake(window)

    while True:
        snake.move()

        for event in pygame.event.get():
            print(event)

            if event.type == pygame.KEYDOWN:
                snake.change_vector(event.key)

            elif event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.time.delay(20)


if __name__ == "__main__":
    main()
