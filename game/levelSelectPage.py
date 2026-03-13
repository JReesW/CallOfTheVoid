import pygame
import pygame.freetype

from game.levelNode import LevelNode
from game import saveSystem
from scenes.game import GameScene
from scenes.complete import Completed

from engine import colors, director


class LevelSelectPage:
    def __init__(self, nodes : list[LevelNode]):
        self.nodes = nodes

        self.selected_node = 0
    
    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    nextNode = self.selected_node + 1

                    # switch page if we go past the last node, but only if the last node is completed
                    if nextNode >= len(self.nodes):
                        if not self.nodes[self.selected_node].completed:
                            continue
                        self.selected_node = nextNode
                        continue

                    # otherwise, just move to the next node if it's unlocked
                    if not self.nodes[nextNode].unlocked:
                        continue
                    self.selected_node = nextNode
                elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    nextNode = self.selected_node - 1

                    # switch page if we go before the first node
                    if nextNode < 0:
                        self.selected_node = nextNode
                        continue

                    if not self.nodes[nextNode].unlocked:
                        continue
                    self.selected_node = nextNode
                elif event.key == pygame.K_RETURN:
                    self.play_selected_node()
                elif event.key == pygame.K_BACKSPACE:
                    saveSystem.saveData["levelCleared"] = max(0, saveSystem.saveData["levelCleared"] - 1)
                    saveSystem.save_save_data(saveSystem.saveData)
    
    def should_switch_page(self):
        if self.selected_node < 0:
            return True, -1
        elif self.selected_node >= len(self.nodes):
            return True, 1
        else:
            return False, 0
    
    def play_selected_node(self):
        selected_level = self.nodes[self.selected_node].level
        if selected_level == ":end_game:":
            director.change_scene("Fadeout", self, Completed())
        else:
            director.change_scene("Fadeout", self, GameScene(selected_level))
    
    def render(self, surface):
        lineSurface = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
        lineSurface.fill(colors.transparent)

        levelSurface = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
        levelSurface.fill(colors.transparent)

        for i in range(len(self.nodes)):
            node = self.nodes[i]

            lineColor = colors.gray

            startPoint = node.position
            endPoint = (0, 0)
            if i < len(self.nodes) - 1:
                endPoint = self.nodes[i + 1].position
                if self.nodes[i + 1].unlocked:
                    lineColor = colors.white
                pygame.draw.line(lineSurface, lineColor, startPoint, endPoint, 5)
            
            # if we want automatic end lines, but i feel manually placing them looks better
            # else:
            #     if node.completed:
            #         lineColor = colors.white
            #     endPoint = node.position
            #     endPoint = (levelSurface.get_width(), endPoint[1])

            # pygame.draw.line(lineSurface, lineColor, startPoint, endPoint, 5)

            levelColor = colors.green if node.completed else colors.white if node.unlocked else colors.gray

            if i == self.selected_node:
                pygame.draw.circle(levelSurface, colors.yellow, node.position, 25)

            pygame.draw.circle(levelSurface, levelColor, node.position, 20)

        surface.blit(lineSurface, (0, 0))
        surface.blit(levelSurface, (0, 0))