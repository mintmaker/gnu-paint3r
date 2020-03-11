import pygame
import numpy as np

from buttons import TextButton, ColorButton
from drawing import Drawing

# TODO: clean up everything, make different lists for colorbuttons, modebuttons, brushsizebuttons and whatsoever
# TODO: make the buttons alright

pygame.init()


class PAINT3R:
    def __init__(self, drawing_size=(300, 300), window_size=(800, 600)):
        self.drawing_size = drawing_size
        self.window_size = window_size

        self.window = pygame.display.set_mode(window_size)
        pygame.display.set_caption('GNU PAINT3R')
        self.drawing = Drawing(window=self.window,
                               rect=(0,0),
                               size=self.drawing_size,
                               zoom_factor=2)
        self.clock = pygame.time.Clock()

        self.running = False

        self.MODE_BUTTONS = [TextButton(self.window, (self.window_size[0] - 50, 75), (75, 75), 'Draw'),
                             TextButton(self.window, (self.window_size[0] - 50, 150), (75, 75), 'Erase'),
                             TextButton(self.window, (self.window_size[0] - 50, 225), (75, 75), 'Fill'),
                             TextButton(self.window, (self.window_size[0] - 50, 300), (75, 75), 'Replace'),
                             TextButton(self.window, (self.window_size[0] - 50, 375), (75, 75), 'Clear')
                             ]
        self.MODE_BUTTONS[0].selected = True
        self.mode = 'd'
        self.modes = ['d', 'e', 'f', 'r', 'c']

        self.BRUSHSIZE_BUTTONS = [TextButton(self.window, (self.window_size[0] - 50, 425), (25, 25), '1'),
                             TextButton(self.window, (self.window_size[0] - 50, 450), (25, 25), '2'),
                             TextButton(self.window, (self.window_size[0] - 50, 475), (25, 25), '3'),
                             TextButton(self.window, (self.window_size[0] - 50, 500), (25, 25), '4'),
                             TextButton(self.window, (self.window_size[0] - 50, 525), (25, 25), '5')
                             ]
        self.BRUSHSIZE_BUTTONS[0].selected = True
        self.brushsize = 1

        self.colors = ((255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 255, 255), (0, 0, 0))

        self.COLOR_BUTTONS = [ColorButton(window=self.window,
                                          center=(self.window_size[0] - 170, 75),
                                          size=(50, 50),
                                          base_color=(225, 0, 0),
                                          light_color=(255, 0, 0)
                                          ),
                              ColorButton(window=self.window,
                                          center=(self.window_size[0] - 120, 75),
                                          size=(50, 50),
                                          base_color=(0, 225, 0),
                                          light_color=(0, 255, 0)
                                          ),
                              ColorButton(window=self.window,
                                          center=(self.window_size[0] - 120, 125),
                                          size=(50, 50),
                                          base_color=(0, 0, 225),
                                          light_color=(0, 0, 255)
                                          ),
                              ColorButton(window=self.window,
                                          center=(self.window_size[0] - 170, 125),
                                          size=(50, 50),
                                          base_color=(225, 225, 0),
                                          light_color=(255, 255, 0)
                                          ),
                              ColorButton(window=self.window,
                                          center=(self.window_size[0] - 120, 175),
                                          size=(50, 50),
                                          base_color=(225, 225, 225),
                                          light_color=(255, 255, 255)
                                          ),
                              ColorButton(window=self.window,
                                          center=(self.window_size[0] - 170, 175),
                                          size=(50, 50),
                                          base_color=(10, 10, 10),
                                          light_color=(20, 20, 20)
                                          ),
                              ]
        self.COLOR_BUTTONS[0].selected = True
        self.color = self.colors[0]

    def draw(self, mouse_pos, mouse_click):
        self.window.fill((0, 0, 0))

        for button in self.MODE_BUTTONS:
            button.draw(mouse_pos)

        for button in self.MODE_BUTTONS:
            if button.selected:
                button.draw(mouse_pos)

        for button in self.COLOR_BUTTONS:
            button.draw(mouse_pos)

        for button in self.COLOR_BUTTONS:
            if button.selected:
                button.draw(mouse_pos)

        for button in self.BRUSHSIZE_BUTTONS:
            button.draw(mouse_pos)

        for button in self.BRUSHSIZE_BUTTONS:
            if button.selected:
                button.draw(mouse_pos)

        self.drawing.draw(mouse_pos)

        pygame.display.update()

    @staticmethod
    def get_events():
        return pygame.event.get(), pygame.mouse.get_pos(), pygame.mouse.get_pressed()

    def handle_events(self, events, mouse_pos, mouse_click):
        for event in events:
            if event.type == pygame.QUIT:
                self.running = False

        if self.drawing.handle_events(events, mouse_pos, mouse_click, self.mode, self.color, self.brushsize):
            mode_ds = False
            for idx in range(len(self.MODE_BUTTONS)):
                self.MODE_BUTTONS[idx].handle_events(events, mouse_pos, mouse_click)
                if self.MODE_BUTTONS[idx].directly_selected:
                    mode_ds = True
                    self.mode = self.modes[idx]
                else:
                    mode_ds = False

            for idx in range(len(self.MODE_BUTTONS)):
                if self.modes[idx] != self.mode:
                    self.MODE_BUTTONS[idx].selected = False
            if not mode_ds:
                color_ds = False
                for idx in range(len(self.COLOR_BUTTONS)):
                    self.COLOR_BUTTONS[idx].handle_events(events, mouse_pos, mouse_click)
                    if self.COLOR_BUTTONS[idx].directly_selected:
                        self.color = self.colors[idx]
                        color_ds = True

                for idx in range(len(self.COLOR_BUTTONS)):
                    if self.colors[idx] != self.color:
                        self.COLOR_BUTTONS[idx].selected = False

                if not color_ds:
                    for idx in range(len(self.BRUSHSIZE_BUTTONS)):
                        self.BRUSHSIZE_BUTTONS[idx].handle_events(events, mouse_pos, mouse_click)
                        if self.BRUSHSIZE_BUTTONS[idx].directly_selected:
                            self.brushsize = idx+1

                    for idx in range(len(self.BRUSHSIZE_BUTTONS)):
                        if idx+1 != self.brushsize:
                            self.BRUSHSIZE_BUTTONS[idx].selected = False



    def main_loop(self):
        self.running = True
        while self.running:
            # Sense everything
            events, mouse_pos, mouse_click = self.get_events()

            # Handle them
            self.handle_events(events, mouse_pos, mouse_click)

            # And now draw it
            self.draw(mouse_pos, mouse_click)

            #self.clock.tick(10)

        pygame.quit()


if __name__ == '__main__':
    painter = PAINT3R()
    painter.main_loop()
