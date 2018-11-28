import random
import pygame
import sys

# pygame.init()

CELL = 20

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

UP = (0, 1)
DOWN = (0, -1)
LEFT = (-1, 0)
RIGHT = (1, 0)


class Window(object):
    def __init__(self, width=600, height=600):
        self.score = -1
        self.surface = pygame.display.set_mode((width, height))
        self.change_score()
        self.clear()

    def clear(self):
        self.surface.fill(BLACK)

    def update(self):
        pygame.display.update()

    def change_score(self):
        self.score += 1
        pygame.display.set_caption("Score: {}".format(self.score))


class Segment(object):
    def __init__(self, window, x=0, y=0, side_length=CELL, color=GREEN):
        self.x = x
        self.y = y
        self.side_length = side_length
        self.color = color
        self.surface = window.surface

    def draw(self):
        pygame.draw.rect(self.surface, self.color, (self.x, self.y, self.side_length, self.side_length))


class Food(Segment):
    def __init__(self, window):
        Segment.__init__(self, window, side_length=CELL, color=RED)
        self.new()

    def new(self):
        self.x = random.randint(0, 580)
        self.y = random.randint(0, 580)


class Snake(object):
    def __init__(self, window, side_length=CELL):
        self.x = 0
        self.y = 0
        self.vector = (1, 0)
        self.speed = 10
        self.surface = window.surface
        self.side_length = side_length

    def draw(self):
        pygame.draw.rect(self.surface, GREEN, (self.x, self.y, self.side_length, self.side_length))

    def move(self):
        self.x += self.vector[0] * self.speed
        self.y += self.vector[1] * self.speed
        self.draw()

    def change_vector(self, key):
        if key == 273:
            self.vector = DOWN
        elif key == 274:
            self.vector = UP
        elif key == 275:
            self.vector = RIGHT
        elif key == 276:
            self.vector = LEFT

    def check_collision(self, food, window):
        if (not (-1 < self.x < 581)) or (not (-1 < self.y < 581)):
            pygame.quit()
            sys.exit()

        elif abs(food.x - self.x) < 20 and abs(food.y - self.y) < 20:
            food.new()
            window.change_score()


def main():
    window = Window()
    food = Food(window)
    snake = Snake(window)

    while True:
        food.draw()
        snake.draw()
        window.update()
        snake.check_collision(food, window)
        window.clear()
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
