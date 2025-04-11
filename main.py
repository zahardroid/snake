import pygame
import sys
import random
from pygame.locals import *

# Константы
WIDTH = 640
HEIGHT = 480
CELL_SIZE = 20
FPS = 10

# Цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Направления
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)


class Snake:
    def __init__(self):
        self.body = [(5, 5)]
        self.direction = RIGHT
        self.color = GREEN
        self.grow = False

    def move(self):
        head_x, head_y = self.body[0]
        dx, dy = self.direction
        new_head = (head_x + dx, head_y + dy)

        self.body.insert(0, new_head)
        if not self.grow:
            self.body.pop()
        else:
            self.grow = False

    def change_direction(self, new_dir):
        # Запрет разворота на 180 градусов
        if (new_dir[0] * -1, new_dir[1] * -1) != self.direction:
            self.direction = new_dir

    def check_collision(self):
        head = self.body[0]
        # Проверка столкновения с границами
        if (head[0] < 0 or head[0] >= WIDTH // CELL_SIZE or
                head[1] < 0 or head[1] >= HEIGHT // CELL_SIZE):
            return True
        # Проверка столкновения с телом
        if head in self.body[1:]:
            return True
        return False

    def draw(self, surface):
        for segment in self.body:
            x, y = segment
            rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(surface, self.color, rect)


class Food:
    def __init__(self):
        self.position = (0, 0)
        self.color = RED
        self.generate()

    def generate(self):
        x = random.randint(0, (WIDTH // CELL_SIZE) - 1)
        y = random.randint(0, (HEIGHT // CELL_SIZE) - 1)
        self.position = (x, y)

    def draw(self, surface):
        x, y = self.position
        rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(surface, self.color, rect)


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Змейка")
        self.clock = pygame.time.Clock()
        self.snake = Snake()
        self.food = Food()
        self.score = 0
        self.running = True

    def check_food_collision(self):
        if self.snake.body[0] == self.food.position:
            self.snake.grow = True
            self.food.generate()
            self.score += 10

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                self.running = False
            elif event.type == KEYDOWN:
                if event.key == K_UP:
                    self.snake.change_direction(UP)
                elif event.key == K_DOWN:
                    self.snake.change_direction(DOWN)
                elif event.key == K_LEFT:
                    self.snake.change_direction(LEFT)
                elif event.key == K_RIGHT:
                    self.snake.change_direction(RIGHT)

    def game_over(self):
        font = pygame.font.SysFont(None, 72)
        text = font.render(f"Game Over! Score: {self.score}", True, WHITE)
        self.screen.blit(text, (WIDTH // 2 - 200, HEIGHT // 2 - 50))
        pygame.display.flip()
        pygame.time.wait(3000)
        self.running = False

    def run(self):
        while self.running:
            self.handle_input()

            self.snake.move()

            if self.snake.check_collision():
                self.game_over()
                break

            self.check_food_collision()

            # Отрисовка
            self.screen.fill(BLACK)
            self.snake.draw(self.screen)
            self.food.draw(self.screen)

            # Отображение счета
            font = pygame.font.SysFont(None, 36)
            text = font.render(f"Score: {self.score}", True, WHITE)
            self.screen.blit(text, (10, 10))

            pygame.display.flip()
            self.clock.tick(FPS)

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    game = Game()
    game.run()