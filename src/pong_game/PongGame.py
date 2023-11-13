import pygame
from pygame.locals import *
import math
import time

class PongGame:
    def __init__(self):
        pygame.init()

        # Set constants
        self.WIDTH, self.HEIGHT = 800, 600
        self.BALL_RADIUS = 7
        self.PADDLE_WIDTH, self.PADDLE_HEIGHT = 10, 100
        self.BALL_SPEED = [5, 5]
        self.PADDLE_SPEED = 5
        self.SECTOR_HEIGHT = self.HEIGHT // 8

        # Colors
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)

        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption('Pong Simulator with Rate Coding')

        # Initialize ball and paddle positions
        self.ball = pygame.Rect(self.WIDTH // 2 - self.BALL_RADIUS, self.HEIGHT // 2 - self.BALL_RADIUS, self.BALL_RADIUS * 2, self.BALL_RADIUS * 2)
        self.paddle = pygame.Rect(10, self.HEIGHT // 2 - self.PADDLE_HEIGHT // 2, self.PADDLE_WIDTH, self.PADDLE_HEIGHT)

    def reset_game(self):
        self.ball.x = self.WIDTH // 2 - self.BALL_RADIUS
        self.ball.y = self.HEIGHT // 2 - self.BALL_RADIUS
        self.paddle.y = self.HEIGHT // 2 - self.PADDLE_HEIGHT // 2
        self.BALL_SPEED[0] = abs(self.BALL_SPEED[0])
        time.sleep(4)  # Wait for 4 seconds

    def move_paddle(self):
        keys = pygame.key.get_pressed()
        if keys[K_UP] and self.paddle.top > 0:
            self.paddle.move_ip(0, -self.PADDLE_SPEED)
        if keys[K_DOWN] and self.paddle.bottom < self.HEIGHT:
            self.paddle.move_ip(0, self.PADDLE_SPEED)

    def get_ball_region(self):
        return self.ball.centery // self.SECTOR_HEIGHT + 1

    def calculate_rate_coding(self):
        distance_from_paddle = abs(self.ball.centerx - self.paddle.centerx)
        max_distance = self.WIDTH
        normalized_distance = distance_from_paddle / max_distance
        return 4 + normalized_distance * 36  # Scale between 4 to 40

    def move_ball(self):
        # Move ball
        self.ball.move_ip(self.BALL_SPEED[0], self.BALL_SPEED[1])

        # Collision with top and bottom
        if self.ball.top <= 0 or self.ball.bottom >= self.HEIGHT:
            self.BALL_SPEED[1] = -self.BALL_SPEED[1]

        # Ball goes past the left wall (loss condition)
        if self.ball.left <= 0:
            self.reset_game()

        # Collision with right wall
        if self.ball.right >= self.WIDTH:
            self.BALL_SPEED[0] = -self.BALL_SPEED[0]

        # Collision with paddle
        if self.ball.colliderect(self.paddle):
            # Determine where the ball hit the paddle
            relative_intersect_y = (self.ball.centery - self.paddle.centery) / (self.PADDLE_HEIGHT/2)
            
            # Convert this to an angle (max of 45 degrees)
            bounce_angle = relative_intersect_y * (45 * (3.14 / 180))
            
            # Update ball speeds
            self.BALL_SPEED[0] = abs(self.BALL_SPEED[0])  # Always bounce to the right
            self.BALL_SPEED[1] = self.BALL_SPEED[0] * math.tan(bounce_angle)

    def run_game(self):
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    return

            self.move_paddle()
            self.move_ball()
            
            print(f"Ball Region: {self.get_ball_region()}")
            print(f"Rate Coding: {self.calculate_rate_coding()}")

            self.screen.fill(self.BLACK)
            pygame.draw.ellipse(self.screen, self.WHITE, self.ball)
            pygame.draw.rect(self.screen, self.WHITE, self.paddle)
            pygame.draw.aaline(self.screen, self.WHITE, (self.WIDTH // 2, 0), (self.WIDTH // 2, self.HEIGHT))
            pygame.display.flip()
            pygame.time.Clock().tick(60)

if __name__ == "__main__":
    pong_game = PongGame()
    pong_game.run_game()