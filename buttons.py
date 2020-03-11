import pygame


class Button:

    def __init__(self,
                 window,
                 center,
                 size,
                 base_color=(30, 30, 30),
                 light_color=(50, 50, 50)):
        self.window = window
        self.center = center
        self.size = size
        self.base_color = base_color
        self.light_color = light_color

        self.x = self.center[0]-0.5*self.size[0]
        self.y = self.center[1]-0.5*self.size[1]
        self.width = self.size[0]
        self.height = self.size[1]

        self.selected = False
        self.directly_selected = False

    def draw(self, mouse_pos):
        if self.x < mouse_pos[0] < self.x + self.width and self.y < mouse_pos[1] < self.y + self.height:
            pygame.draw.rect(self.window, self.light_color, (self.x, self.y, self.width, self.height))

        else:
            pygame.draw.rect(self.window, self.base_color, (self.x, self.y, self.width, self.height))


class SelectButton(Button):

    def __init__(self,
                 window,
                 center,
                 size,
                 base_color=(30, 30, 30),
                 light_color=(50, 50, 50),
                 selected_outline_color=(128, 128, 128),
                 selected_outline_width=1):
        self.window = window
        self.center = center
        self.size = size
        self.base_color = base_color
        self.light_color = light_color
        self.selected_outline_color = selected_outline_color
        self.selected_outline_width = selected_outline_width

        super().__init__(self.window, self.center, self.size, self.base_color, self.light_color)

    def handle_events(self, events, mouse_pos, mouse_click):
        self.is_selected(mouse_pos, mouse_click)

    def is_selected(self, mouse_pos, mouse_click):
        if mouse_click[0] == 1:
            if self.x < mouse_pos[0] < self.x + self.width and self.y < mouse_pos[1] < self.y + self.height:
                self.selected = True
                self.directly_selected = True
                return True
        else:
            self.directly_selected = False

        return False

    def draw(self, mouse_pos):
        super().draw(mouse_pos)
        if self.selected:
            pygame.draw.rect(self.window,
                             self.selected_outline_color,
                             (self.x, self.y, self.width, self.height),
                             self.selected_outline_width
                             )


class TextButton(SelectButton):

    def __init__(self,
                 window,
                 center,
                 size,
                 text,
                 base_color=(30, 30, 30),
                 light_color=(50, 50, 50),
                 text_color=(187, 187, 187),
                 selected_outline_color=(128, 128, 128),
                 selected_outline_width=1,
                 font_tuple=('comicsansms', 30),
                 antialiasing=True):
        self.window = window
        self.center = center
        self.size = size
        self.text = text
        self.base_color = base_color
        self.light_color = light_color
        self.text_color = text_color
        self.selected_outline_color = selected_outline_color
        self.selected_outline_width = selected_outline_width
        self.font_tuple = font_tuple
        self.antialiasing = antialiasing

        self.font = pygame.font.SysFont(self.font_tuple[0], self.font_tuple[1])

        self.surf = None
        self.rect = None
        
        super().__init__(self.window,
                         self.center,
                         self.size,
                         self.base_color,
                         self.light_color,
                         self.selected_outline_color,
                         self.selected_outline_width
                         )

    def draw(self, mouse_pos):
        super().draw(mouse_pos)
        self.surf = self.font.render(self.text, self.antialiasing, self.text_color)
        self.rect = self.surf.get_rect()
        self.rect.center = self.center

        self.window.blit(self.surf, self.rect)


class ColorButton(SelectButton):

    def __init__(self,
                 window,
                 center,
                 size,
                 base_color=(30, 30, 30),
                 light_color=(50, 50, 50),
                 selected_outline_color=(187, 187, 187),
                 selected_outline_width=2):
        self.window = window
        self.center = center
        self.size = size
        self.base_color = base_color
        self.light_color = light_color
        self.selected_outline_color = selected_outline_color
        self.selected_outline_width = selected_outline_width

        super().__init__(self.window,
                         self.center,
                         self.size,
                         self.base_color,
                         self.light_color,
                         self.selected_outline_color,
                         self.selected_outline_width
                         )
