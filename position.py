import pygame
from collections import deque

#ts class will be used to track the position 
class Position:
    def __init__(self, width, height):
        self.x = width // 2
        self.y = height // 2
        self.radius = 22
        self.trail = deque(maxlen=8)

    def update(self, x, y):
        if x is not None and y is not None:
            self.x = x
            self.y = y
            self.trail.appendleft((int(self.x), int(self.y)))

    def draw(self, screen):
        for i, pos in enumerate(self.trail):
            alpha_radius = max(2, self.radius - (i * 2))
            glow_surf = pygame.Surface((alpha_radius * 2 + 4, alpha_radius * 2 + 4), pygame.SRCALPHA)
            alpha = max(0, 180 - (i * 22))
            pygame.draw.circle(glow_surf, (0, 255, 200, alpha), (alpha_radius + 2, alpha_radius + 2), alpha_radius)
            screen.blit(glow_surf, (pos[0] - alpha_radius - 2, pos[1] - alpha_radius - 2))

        px, py = int(self.x), int(self.y)
        pygame.draw.circle(screen, (0, 255, 200), (px, py), self.radius, 2)
        pygame.draw.circle(screen, (255, 255, 255), (px, py), 4)

        len_b = 8
        pygame.draw.line(screen, (0, 255, 255), (px - self.radius, py - self.radius), (px - self.radius + len_b, py - self.radius), 2)
        pygame.draw.line(screen, (0, 255, 255), (px - self.radius, py - self.radius), (px - self.radius, py - self.radius + len_b), 2)

        pygame.draw.line(screen, (0, 255, 255), (px + self.radius, py - self.radius), (px + self.radius - len_b, py - self.radius), 2)
        pygame.draw.line(screen, (0, 255, 255), (px + self.radius, py - self.radius), (px + self.radius, py - self.radius + len_b), 2)

        pygame.draw.line(screen, (0, 255, 255), (px - self.radius, py + self.radius), (px - self.radius + len_b, py + self.radius), 2)
        pygame.draw.line(screen, (0, 255, 255), (px - self.radius, py + self.radius), (px - self.radius, py + self.radius - len_b), 2)

        pygame.draw.line(screen, (0, 255, 255), (px + self.radius, py + self.radius), (px + self.radius - len_b, py + self.radius), 2)
        pygame.draw.line(screen, (0, 255, 255), (px + self.radius, py + self.radius), (px + self.radius, py + self.radius - len_b), 2)

    def get_rect(self):
        return pygame.Rect(int(self.x) - self.radius, int(self.y) - self.radius, self.radius * 2, self.radius * 2)

    def reset(self, width, height):
        pass