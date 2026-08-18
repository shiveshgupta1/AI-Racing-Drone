import sys
import cv2
import pygame
import numpy as np

from tracker import HandTracker
from position import Position
from pipe import PipeManager

class Game:
    def __init__(self):
        pygame.init() 
        self.WIDTH, self.HEIGHT = 640, 480
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("CYBER-DODGE 3D")
        self.clock = pygame.time.Clock()
        
        self.font_big = pygame.font.SysFont("Courier", 28, bold=True)
        self.font_small = pygame.font.SysFont("Courier", 16, bold=True)

        self.hand_tracker = HandTracker()
        self.player = Position(self.WIDTH, self.HEIGHT)
        self.pipes = PipeManager(width=self.WIDTH, height=self.HEIGHT)
        self.flash_timer = 0
        self.touch_cooldown = 0

    def draw_hud(self, frame):
        cx, cy = self.WIDTH // 2, self.HEIGHT // 2
        grid_overlay = frame.copy()
        
        cv2.line(grid_overlay, (0, 0), (cx, cy), (80, 50, 20), 1)
        cv2.line(grid_overlay, (self.WIDTH, 0), (cx, cy), (80, 50, 20), 1)
        cv2.line(grid_overlay, (0, self.HEIGHT), (cx, cy), (80, 50, 20), 1)
        cv2.line(grid_overlay, (self.WIDTH, self.HEIGHT), (cx, cy), (80, 50, 20), 1)
        
        cv2.addWeighted(grid_overlay, 0.3, frame, 0.7, 0, frame)

    def draw_pygame_ui(self):
        card = pygame.Surface((200, 75), pygame.SRCALPHA)
        card.fill((10, 15, 30, 200))
        pygame.draw.rect(card, (0, 255, 200), card.get_rect(), 2)
        self.screen.blit(card, (15, 15))

        score_txt = self.font_big.render(f"SCORE: {self.pipes.score:03d}", True, (0, 255, 200))
        high_txt = self.font_small.render(f"BEST:  {self.pipes.high_score:03d}", True, (255, 200, 0))
        self.screen.blit(score_txt, (25, 22))
        self.screen.blit(high_txt, (25, 55))

        if self.flash_timer > 0:
            flash_surf = pygame.Surface((self.WIDTH, self.HEIGHT), pygame.SRCALPHA)
            flash_surf.fill((255, 0, 0, min(120, self.flash_timer * 15)))
            self.screen.blit(flash_surf, (0, 0))
            self.flash_timer -= 1

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                        running = False

            obj_x, obj_y, frame = self.hand_tracker.get_hand_position(self.WIDTH, self.HEIGHT)
            if frame is None:
                continue

            self.player.update(obj_x, obj_y)
            self.pipes.update()

            if self.touch_cooldown > 0:
                self.touch_cooldown -= 1

            # Checks front-face/opening rect collision instead of center point
            if self.pipes.check_front_face_collisions(self.player.get_rect()) and self.touch_cooldown == 0:
                self.pipes.score = max(0, self.pipes.score - 1)
                self.flash_timer = 4
                self.touch_cooldown = 5

            self.draw_hud(frame)
            self.pipes.draw(frame)

            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame_surface = pygame.surfarray.make_surface(np.rot90(frame_rgb))
            self.screen.blit(frame_surface, (0, 0))

            self.player.draw(self.screen)
            self.draw_pygame_ui()

            pygame.display.flip()
            self.clock.tick(60)

        self.hand_tracker.release()
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()