import pygame
from game.levelSelectPage import LevelSelectPage
from game.levelNode import LevelNode
from engine import colors

class EarlyCaveSelectPage(LevelSelectPage):
    def __init__(self):
        nodes = [
            LevelNode("Cave 1", "cave1", True, True, (100, 200)),
            LevelNode("Cave 2", "cave2", True, False, (300, 800)),
            LevelNode("Cave 3", "cave3", False, False, (500, 500))
        ]
        super().__init__(nodes)
    
    def handle_events(self, events):
        super().handle_events(events)
    
    def render(self, surface):
        # render world specific background

        endNode = self.nodes[-1]
        lineColor = colors.white if endNode.completed else colors.gray

        endPosition = (endNode.position[0] + 400, endNode.position[1] + 1080)

        pygame.draw.line(surface, lineColor, endNode.position, endPosition, 5)


        super().render(surface)