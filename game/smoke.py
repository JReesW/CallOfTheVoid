import pygame
import random

class SmokeSystem:
    def __init__(self):
        self.particles = []

    def emit(self, pos, amount=2):
        """Spawn smoke particles at position"""
        for _ in range(amount):
            particle = {
                "x": pos[0] + random.uniform(-10, 10),
                "y": pos[1] + random.uniform(-3, 10),
                "vx": random.uniform(-15, 15),
                "vy": random.uniform(-120, -20),
                "size": random.uniform(2, 6),
                "alpha": 200
            }
            self.particles.append(particle)

    def update_draw(self, screen, dt):
        """Update and draw all particles"""
        for p in self.particles[:]:

            # movement
            p["x"] += p["vx"] * dt
            p["y"] += p["vy"] * dt

            # slow drift and expansion
            p["vx"] *= 0.97
            p["vy"] *= 0.97
            p["size"] += 8 * dt

            # fade
            p["alpha"] -= 70 * dt

            if p["alpha"] <= 0:
                self.particles.remove(p)
                continue

            surf = pygame.Surface((p["size"]*2, p["size"]*2), pygame.SRCALPHA)
            pygame.draw.circle(
                surf,
                (40, 40, 40, int(p["alpha"])),
                (p["size"], p["size"]),
                int(p["size"])
            )

            screen.blit(surf, (p["x"]-p["size"], p["y"]-p["size"]))