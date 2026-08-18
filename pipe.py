import pygame
import random
import cv2
import numpy as np

#ts will be used to manage the pipes/obstacles in the game
class PipeManager:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.score = 0
        self.high_score = 0
        self.reset()

    def reset(self):
        self.z = 0.2
        self.target_x = random.randint(int(self.width * 0.25), int(self.width * 0.75))
        self.target_y = random.randint(int(self.height * 0.25), int(self.height * 0.75))
        self.speed = 0.22

    def update(self):
        self.z += self.speed
        if self.z > 15.0:
            self.score += 1
            if self.score > self.high_score:
                self.high_score = self.score
            self.reset()
            self.speed = min(0.65, 0.22 + (self.score * 0.025))

    def draw(self, frame):
        base_size = 18
        size = int(base_size * self.z)
        center_x = self.width // 2 + int((self.target_x - self.width // 2) * (self.z / 10.0))
        center_y = self.height // 2 + int((self.target_y - self.height // 2) * (self.z / 10.0))
        
        x1, y1 = center_x - size // 2, center_y - size // 2
        x2, y2 = center_x + size // 2, center_y + size // 2

        danger_ratio = min(1.0, max(0.0, (self.z - 1.0) / 10.0))
        b = int((1 - danger_ratio) * 255)
        g = int((1 - danger_ratio) * 200)
        r = int(danger_ratio * 255)
        color = (b, g, r)

        overlay = frame.copy()
        cv2.rectangle(overlay, (x1, y1), (x2, y2), (0, 0, 50), -1)
        cv2.addWeighted(overlay, 0.35, frame, 0.65, 0, frame)
        cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
        cv2.rectangle(frame, (x1 - 2, y1 - 2), (x2 + 2, y2 + 2), (255, 255, 255), 1)

        cx, cy = self.width // 2, self.height // 2
        alpha_line = (color[0], color[1], color[2])
        cv2.line(frame, (x1, y1), (cx, cy), alpha_line, 1, cv2.LINE_AA)
        cv2.line(frame, (x2, y1), (cx, cy), alpha_line, 1, cv2.LINE_AA)
        cv2.line(frame, (x1, y2), (cx, cy), alpha_line, 1, cv2.LINE_AA)
        cv2.line(frame, (x2, y2), (cx, cy), alpha_line, 1, cv2.LINE_AA)
        if self.z > 8.0:
            cv2.putText(frame, "! WARNING !", (x1 - 10, max(20, y1 - 10)), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2, cv2.LINE_AA)

    def get_rect(self):
        base_size = 18
        size = int(base_size * self.z)
        center_x = self.width // 2 + int((self.target_x - self.width // 2) * (self.z / 10.0))
        center_y = self.height // 2 + int((self.target_y - self.height // 2) * (self.z / 10.0))
        return pygame.Rect(center_x - size // 2, center_y - size // 2, size, size)

    def check_collisions(self, player_rectangle):
        if self.z > 9.5:
            return player_rectangle.colliderect(self.get_rect())
        return False 
