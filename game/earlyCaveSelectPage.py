import pygame
from game.levelSelectPage import LevelSelectPage
from game.levelNode import LevelNode
from engine import colors, image

class EarlyCaveSelectPage(LevelSelectPage):
    def __init__(self):
        nodes = [
            LevelNode("Cave Entrance", "cave_entrance", 1, (400, 260)),
            LevelNode("Mind the Gap", "mind_gap", 2, (1065, 260)),
            LevelNode("Projected Weight", "projected_weight", 3, (1380, 350)),
            LevelNode("Boxing Day", "boxing_day", 4, (1060, 495)),
            LevelNode("Just Out of Reach", "out_of_reach", 5, (735, 650)),
            LevelNode("Climbing the Gate", "climb_gate", 6, (785, 900)),
            LevelNode("The Climb", "the_climb", 7, (1400, 925))
        ]
        super().__init__(nodes)
    
    def handle_events(self, events):
        super().handle_events(events)
    
    def render(self, surface):
        # render world specific background
        surface.blit(image.load_image("world1"))

        endNode = self.nodes[-1]
        lineColor = colors.white if endNode.completed else colors.gray

        endPosition = (endNode.position[0] + 800, endNode.position[1])

        pygame.draw.line(surface, lineColor, endNode.position, endPosition, 5)


        super().render(surface)