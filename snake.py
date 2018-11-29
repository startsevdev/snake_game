import random
import pygame
import sys

# pygame.init()

CELL = 20
SIZE = 740

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

UP = (0, 1)
DOWN = (0, -1)
LEFT = (-1, 0)
RIGHT = (1, 0)

print("\n\n\n– – – – – SNAKE GAME – – – – –\n")


class Window(object):
    def __init__(self, width=SIZE, height=SIZE):
        self.surface = pygame.display.set_mode((width, height))

    def update(self):
        pygame.display.update()
        self.surface.fill(BLACK)


class Segment(object):
    def __init__(self, x=0, y=0, side_length=CELL, color=GREEN):
        self.x = x
        self.y = y
        self.side_length = side_length
        self.color = color


class Food(Segment):
    def __init__(self):
        Segment.__init__(self, side_length=CELL, color=RED)
        self.new()

    def new(self):
        self.x = random.randint(0, SIZE - self.side_length)
        self.y = random.randint(0, SIZE - self.side_length)


class Snake(object):
    def __init__(self, side_length=CELL):
        self.vector = (1, 0)
        self.speed = 20
        self.side_length = side_length
        self.segments = [Segment()]

    def move(self):
        new_segments = []

        # new coords of snake's head
        x = self.segments[0].x + self.vector[0] * CELL
        y = self.segments[0].y + self.vector[1] * CELL
        new_segments.append(Segment(x, y))

        # new coords of snake's body
        for i in range(1, len(self.segments)):
            x = self.segments[i - 1].x
            y = self.segments[i - 1].y
            new_segments.append(Segment(x, y))

        # update snake's egments
        self.segments = new_segments

    def change_vector(self, key):
        if key == 273 and self.vector != UP:
            self.vector = DOWN
        elif key == 274 and self.vector != DOWN:
            self.vector = UP
        elif key == 275 and self.vector != LEFT:
            self.vector = RIGHT
        elif key == 276 and self.vector != RIGHT:
            self.vector = LEFT

    def grow(self):
        last_segment = self.segments[-1]
        self.segments.append(Segment(last_segment.x, last_segment.y))


class Game(object):
    def __init__(self):
        self.window = Window()
        self.food = Food()
        self.snake = Snake()
        self.score = -1
        self.change_score()

    def circle(self):
        self.snake.move()
        self.draw_frame()
        self.check_collision()

    def event_handler(self):
        for event in pygame.event.get():
            # controls
            if event.type == pygame.KEYDOWN:
                self.snake.change_vector(event.key)
            # Exit
            elif event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def change_score(self):
        self.score += 1
        pygame.display.set_caption("Score: {}".format(self.score))

    def draw_frame(self):
        # draw food
        pygame.draw.rect(self.window.surface, self.food.color,
                         (self.food.x, self.food.y, self.food.side_length, self.food.side_length))

        # draw snake
        for segment in self.snake.segments:
            pygame.draw.rect(self.window.surface, GREEN,
                             (segment.x, segment.y, self.snake.side_length, self.snake.side_length))

        self.window.update()

    def check_collision(self):
        for segment in self.snake.segments[1:]:
            if abs(segment.x - self.snake.segments[0].x) < 20 and abs(segment.y - self.snake.segments[0].y) < 20:
                self.over()

        if (not (0 <= self.snake.segments[0].x <= SIZE - self.snake.side_length)) or \
                (not (0 <= self.snake.segments[0].y <= SIZE - self.snake.side_length)):
            self.over()

        if abs(self.food.x - self.snake.segments[0].x) < 20 and abs(self.food.y - self.snake.segments[0].y) < 20:
            self.food.new()
            self.snake.grow()
            self.change_score()

    def over(self):
        if self.score > 0:
            print("Score: {}\n".format(self.score))

        pygame.time.delay(1000)
        pygame.event.clear(pygame.KEYDOWN)

        main()


def main():
    game = Game()

    while True:
        game.circle()
        game.event_handler()

        pygame.time.delay(40)


if __name__ == "__main__":
    main()
