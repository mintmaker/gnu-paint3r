import pygame
import numpy as np


class Drawing:

    def __init__(self,
                 window,
                 rect,
                 size=(300, 300),
                 default_color=(255, 255, 255),
                 zoom_factor=4,
                 autocompletion=True
                 ):

        self.window = window
        self.rect = rect
        self.size = size
        self.default_color = default_color
        self.zoom_factor = zoom_factor
        self.autocompletion = autocompletion

        if self.autocompletion:
            self.MODES = {'d': self.drawing_draw_autocomplete, 'e': self.drawing_erase, 'f': self.drawing_fill,
                          'r': self.drawing_replace, 'c': self.drawing_clear}
        else:
            self.MODES = {'d': self.drawing_draw, 'e': self.drawing_erase, 'f': self.drawing_fill,
                          'r': self.drawing_replace, 'c': self.drawing_clear}

        self.rect = (rect[0], rect[1], self.size[0] * self.zoom_factor, self.size[1] * self.zoom_factor)

        self.drawing = np.full((self.size[0], self.size[1], 3), -1)
        self.shown_drawing = self.drawing
        self.shown_drawing[self.shown_drawing == -1] = 255

        self.last_point = False

    def handle_events(self,
                      events,
                      mouse_pos,
                      mouse_click,
                      mode,
                      color,
                      brushsize):
        if mouse_click[0]:
            if self.rect[0] < mouse_pos[0] < self.rect[0] + self.rect[2]:
                mouse_pos = self.calculate_relative_pos(mouse_pos)
                self.MODES[mode](mouse_pos, color, brushsize)
                if mode != 'd':
                    self.last_point = False
                return False
        elif mode == 'c':
            self.MODES['c'](mouse_pos, color, brushsize)
        elif mode == 'd':
            self.last_point = False
        return True

    def calculate_relative_pos(self, mouse_pos):
        return (mouse_pos[0] - self.rect[0]) // self.zoom_factor, (mouse_pos[1] - self.rect[1]) // self.zoom_factor

    def drawing_draw_brush_size(self, pos, brushsize, color):
        self.drawing[pos] = color
        for i in range(-brushsize + 1, brushsize - 1):
            for j in range(-brushsize + 1, brushsize - 1):
                self.drawing[
                    max(0, min(pos[0] + i, self.size[0] - 1)), max(0, min(pos[1] + j, self.size[1] - 1))] = color

    def drawing_draw_autocomplete(self, mouse_pos, color, brushsize):
        if self.last_point:
            pos = (mouse_pos[0] - self.last_point[0], mouse_pos[1] - self.last_point[1])
            pre = (1 if abs(pos[0]) == pos[0] else -1, 1 if abs(pos[1]) == pos[1] else -1)
            if pos[0] == 0 and pos[1] != 0:
                for i in range(0, pos[1], pre[1]):
                    self.drawing_draw_brush_size((self.last_point[0], self.last_point[1] + i), brushsize, color)
            elif pos[1] == 0 and pos[0] != 0:
                for i in range(0, pos[0], pre[0]):
                    self.drawing_draw_brush_size((self.last_point[0] + i, self.last_point[1]), brushsize, color)
            elif pos[1] != 0 and pos[0] != 0:
                if abs(pos[1]) > abs(pos[0]):
                    ratio = pos[1] / pos[0]
                    for i in range(0, pos[1], pre[1]):
                        self.drawing_draw_brush_size(
                            (int(self.last_point[0] + (i // ratio)), int(self.last_point[1] + i)), brushsize, color)
                else:
                    ratio = pos[0] / pos[1]
                    for i in range(0, pos[0], pre[0]):
                        self.drawing_draw_brush_size(
                            (int(self.last_point[0] + i), int(self.last_point[1] + i // ratio)), brushsize, color)

        self.drawing_draw_brush_size(mouse_pos, brushsize, color)
        self.last_point = mouse_pos

    def drawing_draw(self, mouse_pos, color, brushsize):
        self.drawing_draw_brush_size(mouse_pos, brushsize, color)

    def drawing_erase(self, mouse_pos, color, brushsize):
        if self.autocompletion:
            self.drawing_draw_autocomplete(mouse_pos, -1, brushsize)
        else:
            self.drawing_draw_brush_size(mouse_pos, brushsize, color)

    def drawing_fill(self, mouse_pos, color, brushsize):  # hardest part, needs to be implemented later

        f_color = self.drawing[mouse_pos].copy()
        self.drawing[mouse_pos] = color

        up_list = []
        down_list = []
        left_list = []
        right_list = []

        dones = []

        done = False
        while not done:
            smth = False
            up_old_list = up_list.copy()
            down_old_list = down_list.copy()
            left_old_list = left_list.copy()
            right_old_list = right_list.copy()

            if len(right_list) == len(left_list) == len(down_list) == len(up_list) == 0:

                if np.array_equal(self.drawing[mouse_pos[0], mouse_pos[1] - 1], f_color):
                    up_list.append((mouse_pos[0], mouse_pos[1] - 1))
                    smth = True
                    self.drawing[mouse_pos[0], mouse_pos[1] - 1] = color

                if np.array_equal(self.drawing[mouse_pos[0], mouse_pos[1] + 1], f_color):
                    smth = True
                    down_list.append((mouse_pos[0], mouse_pos[1] + 1))
                    self.drawing[mouse_pos[0], mouse_pos[1] + 1] = color

                if np.array_equal(self.drawing[mouse_pos[0] - 1, mouse_pos[1]], f_color):
                    smth = True
                    left_list.append((mouse_pos[0] - 1, mouse_pos[1]))
                    self.drawing[mouse_pos[0] - 1, mouse_pos[1]] = color

                if np.array_equal(self.drawing[mouse_pos[0] + 1, mouse_pos[1]], f_color):
                    smth = True
                    right_list.append((mouse_pos[0] + 1, mouse_pos[1]))
                    self.drawing[mouse_pos[0] + 1, mouse_pos[1]] = color

                second_up_list = []
                second_down_list = []
                second_right_list = []
                second_left_list = []
                for idx, i in enumerate(up_list):
                    if not i in dones and not (i[0] + 1 >= self.size[0] or i[1] + 1 >= self.size[1] or i[0] == 0 or i[1] == 0):
                        dones.append(i)
                        second_up_list.append(i)
                for idx, i in enumerate(down_list):
                    if not i in dones and not (i[0] + 1 >= self.size[0] or i[1] + 1 >= self.size[1] or i[0] == 0 or i[1] == 0):
                        dones.append(i)
                        second_down_list.append(i)
                for idx, i in enumerate(right_list):
                    if not i in dones and not (i[0] + 1 >= self.size[0] or i[1] + 1 >= self.size[1] or i[0] == 0 or i[1] == 0):
                        dones.append(i)
                        second_right_list.append(i)
                for idx, i in enumerate(left_list):
                    if not i in dones and not (i[0] + 1 >= self.size[0] or i[1] + 1 >= self.size[1] or i[0] == 0 or i[1] == 0):
                        dones.append(i)
                        second_left_list.append(i)

                up_list = second_up_list
                down_list = second_down_list
                right_list = second_right_list
                left_list = second_left_list

                if len(right_list) == len(left_list) == len(down_list) == len(up_list) == 0:
                    done = True
                    return
            else:

                up_list = []
                down_list = []
                left_list = []
                right_list = []
                for i in up_old_list:

                    if i[1] - 1 > -1:
                        if np.array_equal(self.drawing[i[0], i[1] - 1], f_color):
                            up_list.append((i[0], i[1] - 1))
                            self.drawing[i[0], i[1] - 1] = color

                    if i[0] - 1 > -1:
                        if np.array_equal(self.drawing[i[0] - 1, i[1]], f_color):
                            left_list.append((i[0] - 1, i[1]))
                            self.drawing[i[0] - 1, i[1]] = color

                    if i[0] + 1 < self.size[0]:
                        if np.array_equal(self.drawing[i[0] + 1, i[1]], f_color):
                            right_list.append((i[0] + 1, i[1]))
                            self.drawing[i[0] + 1, i[1]] = color

                for i in down_old_list:

                    if i[1] + 1 < self.size[1]:
                        if np.array_equal(self.drawing[i[0], i[1] + 1], f_color):
                            down_list.append((i[0], i[1] + 1))
                            self.drawing[i[0], i[1] + 1] = color

                    if i[0] - 1 > -1:
                        if np.array_equal(self.drawing[i[0] - 1, i[1]], f_color):
                            left_list.append((i[0] - 1, i[1]))
                            self.drawing[i[0] - 1, i[1]] = color

                    if i[0] + 1 < self.size[0]:
                        if np.array_equal(self.drawing[i[0] + 1, i[1]], f_color):
                            right_list.append((i[0] + 1, i[1]))
                            self.drawing[i[0] + 1, i[1]] = color

                for i in left_old_list:

                    if i[1] - 1 > -1:
                        if np.array_equal(self.drawing[i[0], i[1] - 1], f_color):
                            up_list.append((i[0], i[1] - 1))
                            self.drawing[i[0], i[1] - 1] = color

                    if i[1] + 1 < self.size[1]:
                        if np.array_equal(self.drawing[i[0], i[1] + 1], f_color):
                            down_list.append((i[0], i[1] + 1))
                            self.drawing[i[0], i[1] + 1] = color

                    if  i[0] - 1 > -1:
                        if np.array_equal(self.drawing[i[0] - 1, i[1]], f_color):
                            left_list.append((i[0] - 1, i[1]))
                            self.drawing[i[0] - 1, i[1]] = color


                for i in right_old_list:
                    if i[1] - 1 > -1:
                        if np.array_equal(self.drawing[i[0], i[1] - 1], f_color):
                            up_list.append((i[0], i[1] - 1))
                            self.drawing[i[0], i[1] - 1] = color


                    if i[1] + 1 < self.size[1]:
                        if np.array_equal(self.drawing[i[0], i[1] + 1], f_color):
                            down_list.append((i[0], i[1] + 1))
                            self.drawing[i[0], i[1] + 1] = color

                    if i[0] + 1 < self.size[0]:
                        if np.array_equal(self.drawing[i[0] + 1, i[1]], f_color):
                            right_list.append((i[0] + 1, i[1]))
                            self.drawing[i[0] + 1, i[1]] = color

                second_up_list = []
                second_down_list = []
                second_right_list = []
                second_left_list = []
                for idx, i in enumerate(up_list):
                    if not i in dones:
                        dones.append(i)
                        second_up_list.append(i)
                for idx, i in enumerate(down_list):
                    if not i in dones:
                        dones.append(i)
                        second_down_list.append(i)
                for idx, i in enumerate(right_list):
                    if not i in dones:
                        dones.append(i)
                        second_right_list.append(i)
                for idx, i in enumerate(left_list):
                    if not i in dones:
                        dones.append(i)
                        second_left_list.append(i)

                up_list = second_up_list.copy()
                down_list = second_down_list.copy()
                right_list = second_right_list.copy()
                left_list = second_left_list.copy()

                if len(right_list) == len(left_list) == len(down_list) == len(up_list) == 0:
                    done = True
                    return

    def drawing_replace(self, mouse_pos, color, brushsize):
        r_color = self.drawing[mouse_pos].copy()
        for i in range(self.size[0]):
            for j in range(self.size[1]):
                if np.array_equal(self.drawing[i, j], r_color):
                    self.drawing[i, j] = color

    def drawing_clear(self, mouse_pos, color, brushsize):
        self.drawing = np.full((self.size[0], self.size[1], 3), -1)

    def draw(self, mouse_pos):
        self.shown_drawing = self.drawing
        self.shown_drawing[self.shown_drawing == -1] = 255
        # self.showed_drawing = Image.fromarray(self.showed_drawing, 'RGB').resize((1200,1200))
        self.window.blit(pygame.transform.scale(pygame.surfarray.make_surface(self.shown_drawing),
                                                ((self.size[0] * self.zoom_factor), (self.size[1] * self.zoom_factor))),
                         self.rect[:2])
