import pygame
from game.levelSelectPage import LevelSelectPage
from game.levelNode import LevelNode
from engine import colors

class MiddleCaveSelectPage(LevelSelectPage):
    def __init__(self):
        nodes = [
            LevelNode("Middle Cave 1", "middlecave1", 4, (200, 500)),
            LevelNode("Middle Cave 2", "middlecave2", 5, (700, 800)),
            LevelNode("Middle Cave 3", "middlecave3", 6, (1600, 800))
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