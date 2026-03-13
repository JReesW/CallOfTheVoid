import pygame
from game.levelSelectPage import LevelSelectPage
from game.levelNode import LevelNode
from engine import colors, image

class EarlyCaveSelectPage(LevelSelectPage):
    def __init__(self):
        nodes = [
            LevelNode("Cave Entrance", "cave_entrance", 1, (360, 250)),
            LevelNode("Mind the Gap", "mind_gap", 2, (735, 260)),
            LevelNode("Projected Weight", "projected_weight", 3, (1065, 260)),
            LevelNode("Boxing Day", "boxing_day", 4, (1380, 350)),
            LevelNode("Just Out of Reach", "out_of_reach", 5, (1190, 450)),
            LevelNode("Climbing the Gate", "climb_gate", 6, (930, 570)),
            LevelNode("Cave 7", "cave3", 7, (735, 650)),
            LevelNode("Cave 8", "cave3", 8, (570, 870)),
            LevelNode("Cave 9", "cave3", 9, (1010, 940)),
            LevelNode("Cave 10", "cave3", 10, (1470, 930)),
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