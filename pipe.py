import pygame
import random
import cv2

class Pipe:
    def __init__(self, width, height, scale_factor=1.0):
        self.width = width
        self.height = height
        self.z = 0.2
        self.target_x = random.randint(int(self.width * 0.2), int(self.width * 0.8))
        self.target_y = random.randint(int(self.height * 0.2), int(self.height * 0.8))
        self.speed = random.uniform(0.18, 0.26)
        self.base_size = random.randint(6, 14) * scale_factor
        self.passed = False
        self.counted_score = False
        self.hit_counted = False

    def update(self):
        self.z += self.speed
        if self.z > 14.0:
            self.passed = True

    def get_rect(self):
        size = int(self.base_size * self.z)
        center_x = self.width // 2 + int((self.target_x - self.width // 2) * (self.z / 10.0))
        center_y = self.height // 2 + int((self.target_y - self.height // 2) * (self.z / 10.0))
        rect = pygame.Rect(center_x - size // 2, center_y - size // 2, size, size)
        return rect.inflate(15, 15)

    def draw(self, frame):
        size = int(self.base_size * self.z)
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
        cv2.line(frame, (x1, y1), (cx, cy), color, 1, cv2.LINE_AA)
        cv2.line(frame, (x2, y1), (cx, cy), color, 1, cv2.LINE_AA)
        cv2.line(frame, (x1, y2), (cx, cy), color, 1, cv2.LINE_AA)
        cv2.line(frame, (x2, y2), (cx, cy), color, 1, cv2.LINE_AA)

        if self.z > 8.0:
            cv2.putText(frame, "! WARNING !", (x1 - 10, max(20, y1 - 10)), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 255), 1, cv2.LINE_AA)


class PipeManager:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.score = 0
        self.high_score = 0
        self.pipes = []
        self.spawn_timer = 0
        self.reset()

    def reset(self):
        self.score = 0
        self.pipes = [Pipe(self.width, self.height)]
        self.spawn_timer = 0

    def update(self):
        self.spawn_timer += 1
        if self.spawn_timer > 45 and len(self.pipes) < 4:
            self.pipes.append(Pipe(self.width, self.height))
            self.spawn_timer = 0

        for pipe in self.pipes:
            pipe.update()

            if pipe.z > 11.5 and not pipe.counted_score and not pipe.passed:
                pipe.counted_score = True
                self.score += 1
                if self.score > self.high_score:
                    self.high_score = self.score

        self.pipes = [pipe for pipe in self.pipes if not pipe.passed]

    def draw(self, frame):
        for pipe in self.pipes:
            pipe.draw(frame)

    def check_collisions(self, player_rect):
        hit_detected = False
        for pipe in self.pipes:
            if 0.5 <= pipe.z <= 12.0 and not pipe.hit_counted:
                target_rect = pipe.get_rect()
                
                if player_rect.colliderect(target_rect):
                    pipe.hit_counted = True
                    hit_detected = True
                    self.score = max(0, self.score - 1)
                    print(f"COLLISION DETECTED! Score deducted. Current Score: {self.score}")
                    break
        return hit_detected

    def check_front_face_collisions(self, player_rect):
        hit_detected = False
        for pipe in self.pipes:
            if 8.0 <= pipe.z <= 12.0 and not pipe.hit_counted:
                target_rect = pipe.get_rect()
                
                if player_rect.colliderect(target_rect):
                    pipe.hit_counted = True
                    hit_detected = True
                    self.score = max(0, self.score - 1)
                    print(f"FRONT FACE COLLISION DETECTED! Current Score: {self.score}")
                    break
        return hit_detected