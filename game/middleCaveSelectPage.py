import pygame

from game.levelSelectPage import LevelSelectPage
from game.levelNode import LevelNode

from engine import colors, image


class MiddleCaveSelectPage(LevelSelectPage):
    def __init__(self):
        nodes = [
            LevelNode("Teleport", "teleport", 8, (125, 195)),
            LevelNode("Little Help", "little_help", 9, (415, 275)),
            LevelNode("Snatch", "snatch", 10, (475, 515)),
            LevelNode("Elevator", "elevator", 11, (685, 730)),
            LevelNode("Jugglin'", "jugglin", 12, (950, 580)),
            LevelNode("Descent", "descent", 13, (1290, 610)),
            LevelNode("Back Track", "back_track", 14, (1585, 850))
        ]
        super().__init__(nodes)
    
    def handle_events(self, events):
        super().handle_events(events)
    
    def render(self, surface):
        # render world specific background
        surface.blit(image.load_image("world2"))

        startNode = self.nodes[0]
        endNode = self.nodes[-1]
        lineColor = colors.white

        startPosition = (startNode.position[0] - 400, startNode.position[1])
        endPosition = (endNode.position[0] + 800, endNode.position[1] + 200)

        pygame.draw.line(surface, lineColor, startPosition, startNode.position, 5)
        pygame.draw.line(surface, lineColor, endNode.position, endPosition, 5)

        super().render(surface)