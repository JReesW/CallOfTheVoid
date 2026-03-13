import pygame

from game.levelSelectPage import LevelSelectPage
from game.levelNode import LevelNode

from engine import colors, image


class LateCaveSelectPage(LevelSelectPage):
    def __init__(self):
        nodes = [
            LevelNode("Independence", "independence", 15, (80, 230)),
            LevelNode("Imprisoned", "imprisoned", 16, (360, 250)),
            LevelNode("Spike Pit", "spike_pit", 17, (670, 285)),
            LevelNode("Pole Vault", "pole_vault", 18, (870, 420)),
            LevelNode("Drop Chute", "drop_chute", 19, (895, 610)),
            LevelNode("Crystal Maze", "crystal_maze", 20, (1030, 750)),
            LevelNode("Last Jumps", "last_jumps", 21, (1295, 765)),
            LevelNode("Ending", ":end_game:", 22, (1570, 795))
        ]
        super().__init__(nodes)
    
    def handle_events(self, events):
        super().handle_events(events)
    
    def render(self, surface):
        # render world specific background
        surface.blit(image.load_image("world3"))

        startNode = self.nodes[0]
        lineColor = colors.white

        startPosition = (startNode.position[0] - 400, startNode.position[1])

        pygame.draw.line(surface, lineColor, startPosition, startNode.position, 5)

        super().render(surface)