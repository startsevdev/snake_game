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

    def game_over(self):
        if self.score > 0:
            print("Score: {}".format(self.score))

        pygame.time.delay(1000)
        pygame.event.clear(pygame.KEYDOWN)
        main()


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
        self.vector = (1, 0)
        self.speed = 20
        self.window = window
        self.surface = window.surface
        self.side_length = side_length
        self.segments = [Segment(window)]

    def draw(self):
        for segment in self.segments:
            pygame.draw.rect(self.surface, GREEN, (segment.x, segment.y, self.side_length, self.side_length))

    def move(self, window, food):
        new_segments = []

        x = self.segments[0].x + self.vector[0] * self.speed
        y = self.segments[0].y + self.vector[1] * self.speed

        self.check_self_eating(self.window, x, y)
        self.check_collision(food, window)

        new_segments.append(Segment(self.window, x, y))

        for i in range(1, len(self.segments)):
            x = self.segments[i - 1].x
            y = self.segments[i - 1].y
            new_segments.append(Segment(self.window, x, y))

        self.segments = new_segments

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

    def check_self_eating(self, window, x, y):
        for segment in self.segments[1:]:
            if abs(segment.x - x) < 20 and abs(segment.y - y) < 20:
                window.game_over()
            else:
                pass

    def check_collision(self, food, window):
        if (not (-1 < self.segments[0].x < 581)) or (not (-1 < self.segments[0].y < 581)):
            self.window.game_over()

        if abs(food.x - self.segments[0].x) < 20 and abs(food.y - self.segments[0].y) < 20:
            food.new()
            self.grow()
            window.change_score()

    def grow(self):
        last_segment = self.segments[-1]
        self.segments.append(Segment(self.window, last_segment.x, last_segment.y))


def main():
    window = Window()
    food = Food(window)
    snake = Snake(window)

    while True:
        food.draw()
        snake.draw()
        window.update()
        # snake.check_collision(food, window)

        window.clear()
        snake.move(window, food)

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                snake.change_vector(event.key)
            elif event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.time.delay(40)


if __name__ == "__main__":
    main()
