import pygame
from game.levelSelectPage import LevelSelectPage
from game.levelNode import LevelNode
from engine import colors

class LateCaveSelectPage(LevelSelectPage):
    def __init__(self):
        nodes = [
            LevelNode("Late Cave 1", "latecave1", 7, (200, 500)),
            LevelNode("Late Cave 2", "latecave2", 8, (700, 800)),
            LevelNode("Late Cave 3", "latecave3", 9, (1600, 800))
        ]
        super().__init__(nodes)
    
    def handle_events(self, events):
        super().handle_events(events)
    
    def render(self, surface):
        # render world specific background

        startNode = self.nodes[0]
        lineColor = colors.white

        startPosition = (startNode.position[0] - 400, startNode.position[1] - 1080)

        pygame.draw.line(surface, lineColor, startPosition, startNode.position, 5)

        super().render(surface)