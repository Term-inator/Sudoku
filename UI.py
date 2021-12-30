import pygame
from os import path
from time import perf_counter
from random import randint
from math import pi, sqrt

import Sudoku
import Theme


def str_to_tuple(string):
    string_list = string.split(' ')
    for i in range(0, len(string_list)):
        string_list[i] = int(string_list[i])
    return tuple(string_list)


def tuple_to_str(para_tuple):
    string = ""
    for i in range(0, len(para_tuple)):
        string += str(para_tuple[i])
        if i != len(para_tuple) - 1:
            string += " "
    return string


def touch(file_name):
    if path.exists(file_name):
        return
    file = open(file_name, "w")
    file.close()


def between(a, x, b):
    if a <= x <= b:
        return True
    return False


class UI:
    def __init__(self, origin_x, origin_y, length):
        pygame.init()

        # 创建窗口
        self.size = (width, height) = (800, 590)
        screen = pygame.display.set_mode(self.size, pygame.SRCALPHA)
        self.screen = screen
        self.back = 0

        self.start_screen = pygame.Surface(self.size, pygame.SRCALPHA)
        self.solution_num = 0
        self.single_solution = 0
        self.multiple_solution = 0
        self.theme_button = 0
        self.record_button = 0

        self.choose_screen = pygame.Surface(self.size, pygame.SRCALPHA)
        self.given = ""
        self.easy = 0
        self.middle = 0
        self.hard = 0

        self.main_screen = pygame.Surface(self.size, pygame.SRCALPHA)
        self.pause = 0
        self.clear_board = 0
        self.new_game = 0

        self.record_screen = pygame.Surface(self.size, pygame.SRCALPHA)
        self.single = []
        self.multiple = []

        self.theme_screen = pygame.Surface(self.size, pygame.SRCALPHA)
        self.theme_page = (len(Theme.theme_list) - 1) // 4 + 1
        self.theme_now_page = 1  # 初始默认第一页
        self.pre_button = 0
        self.next_button = 0

        self.transparent_screen = self.screen.convert_alpha()
        self.rect = 0

        self.bubble_screen = self.screen.convert_alpha()
        self.bubble = 0
        self.bubble_button = []
        self.button_clear = 0

        self.button_height = 35
        self.button_gap = 5

        # 窗口标题
        pygame.display.set_caption("数独")

        self.origin_x = origin_x  # 左上角x
        self.origin_y = origin_y  # 左上角y
        self.length = length  # 最大矩形的大小
        self.lattice = int(length / 9)  # 小格大小
        self.color = Theme.Color()
        self.theme = Theme.Theme().winter

        self.mouse_press = (0, 0, 0)
        self.mouse_down_position = (0, 0)

        self.mouse_move_position = (0, 0)

        self.start = 0
        self.paused = False
        self.pause_duration = 0
        self.pause_begin = 0
        self.duration = (0, 0, 0)

        self.win = False
        self.play_again = 0
        self.quit_button = 0
        self.quit = False

        self.class_sudoku = Sudoku.sudoku()
        self.sudoku = 0

        self.activity_stack = [self.start_screen]

    def on_range(self, range_left, range_top, range_width, range_height):
        if between(range_left, self.mouse_move_position[0], range_left + range_width) and \
                between(range_top, self.mouse_move_position[1], range_top + range_height):
            return True
        return False

    def in_range(self, range_left, range_top, range_width, range_height):
        if between(range_left, self.mouse_down_position[0], range_left + range_width) and \
                between(range_top, self.mouse_down_position[1], range_top + range_height):
            return True
        return False

    def on_rect(self, rect):
        if rect == 0:
            return False
        return self.on_range(rect.left, rect.top, rect.width, rect.height)

    def in_rect(self, rect):
        if rect == 0:
            return False
        return self.in_range(rect.left, rect.top, rect.width, rect.height)

    def on_circle(self, circle):
        if circle == 0:
            return False
        center = ((circle.left + circle.right) / 2, (circle.top + circle.bottom) / 2)
        radius = (circle.right - circle.left) / 2
        if (self.mouse_move_position[0] - center[0]) ** 2 + (
                self.mouse_move_position[1] - center[1]) ** 2 <= radius ** 2:
            return True
        return False

    def in_circle(self, circle):
        if circle == 0:
            return False
        center = ((circle.left + circle.right) / 2, (circle.top + circle.bottom) / 2)
        radius = (circle.right - circle.left) / 2
        if (self.mouse_down_position[0] - center[0]) ** 2 + (
                self.mouse_down_position[1] - center[1]) ** 2 <= radius ** 2:
            return True
        return False

    def draw_cell(self, x, y, length, width, depth):
        if depth == 2:
            return
        pygame.draw.rect(self.main_screen, self.theme["line"], ((x, y), (length, length)), width)
        for i in range(x, x + length, int(length / 3)):
            for j in range(y, y + length, int(length / 3)):
                pygame.draw.rect(self.main_screen, self.theme["line"], ((i, j), (length / 3, length / 3)), width)
                self.draw_cell(i, j, int(length / 3), 1, depth + 1)

    def in_cells(self, x, y):
        if between(self.origin_x, x, self.origin_x + self.length) and \
                between(self.origin_y, y, self.origin_y + self.length):
            return True
        return False

    def draw_mask(self, x, y):
        pygame.draw.rect(self.transparent_screen, self.theme["secondary"],
                         ((x, y), (self.lattice, self.lattice)), 0)  # 0表示填充矩形

    def draw_text(self, screen, font, color, string, x, y):
        text = font.render(string, 1, color)
        text_position = text.get_rect(center=(x, y))
        screen.blit(text, text_position)

    def draw_button(self, screen, x, y, width, height, font, string, theme, first_state, border, border_radius):
        state = first_state
        if self.on_range(x, y, width, height):
            state = "hover"

        button = pygame.draw.rect(screen, theme[state]["button"], ((x, y), (width, height)),
                                  0, border_radius=border_radius)
        if border:
            border = pygame.draw.rect(screen, theme[state]["border"], ((x, y), (width, height)),
                                      2, border_radius=border_radius)
        center_x = x + width / 2
        center_y = y + height / 2
        self.draw_text(screen, font, theme[state]["font"], string, center_x, center_y)
        return button

    def draw_back_button(self, screen, x, y, width, height, margin):
        first_state = "hover_on_parent"
        back_color = self.theme["primary"]
        if self.on_range(x - margin[3], y - margin[0], width + 2 * margin[1], height + 2 * margin[2]):
            first_state = "hover"
            back_color = self.theme["hover"]["border"]
        line_color = self.theme[first_state]["font"]
        pygame.draw.lines(screen, line_color, False,
                          [(x + width, y), (x, y + height / 2), (x + width, y + height)], 4)

        self.back = pygame.draw.rect(screen, back_color,
                                     ((x - margin[3], y - margin[0]),
                                      (width + margin[1] + margin[3], height + margin[0] + margin[2])),
                                     1, border_radius=5)

    def destroy_back_button(self):
        self.back = 0

    def draw_numbers(self):
        font_number = pygame.font.Font("assets/freesansbold.ttf", 40)
        font_center_x = self.origin_x + self.lattice / 2
        font_center_y = self.origin_y + self.lattice / 2
        mask_x = self.origin_x
        mask_y = self.origin_y
        for row in self.sudoku:
            for number in row:

                number_color = self.theme["number"]
                if number[2][0] == -1 or number[2][1] == -1 or number[2][2] == -1:
                    number_color = self.theme["wrong"]

                if number[0] != 0 and not self.paused:
                    self.draw_text(self.main_screen, font_number, number_color,
                                   str(number[0]), font_center_x, font_center_y)
                if number[1] == 1:
                    self.draw_mask(mask_x, mask_y)
                font_center_x += self.lattice
                mask_x += self.lattice
            font_center_x = self.origin_x + self.lattice / 2
            font_center_y += self.lattice
            mask_x = self.origin_x
            mask_y += self.lattice

    def rect_initialized(self):
        if self.rect != 0:
            return True
        return False

    def choose(self, x, y):
        # 界面坐标和数独相反
        row = (y - self.origin_y) // self.lattice
        column = (x - self.origin_x) // self.lattice

        rect_left = self.origin_x + column * self.lattice
        rect_top = self.origin_y + row * self.lattice

        if self.sudoku[row][column][1] == 0 or self.sudoku[row][column][1] == -1:
            self.rect = pygame.draw.rect(self.transparent_screen, self.theme["emphasize"],
                                         ((rect_left, rect_top), (self.lattice, self.lattice)), 0)  # 0表示填充矩形
            return True
        else:
            if self.rect_initialized():  # rect已初始化
                pygame.draw.rect(self.transparent_screen, self.color.transparent, self.rect, 0)  # 0表示填充矩形
            return False

    def draw_bubble(self, x, y, width, height):
        self.bubble_screen.fill(self.color.transparent)

        bubble_color = self.theme["normal"]["bubble"]
        border_color = self.theme["normal"]["border"]
        if self.on_rect(self.bubble):
            bubble_color = self.theme["hover"]["bubble"]
            border_color = self.theme["hover"]["border"]
        bubble = pygame.draw.rect(self.bubble_screen, bubble_color,
                                  ((x, y), (width, height)), 0, border_radius=5)
        border = pygame.draw.rect(self.bubble_screen, border_color,
                                  ((x, y), (width, height)), 1, border_radius=5)
        self.bubble = bubble
        self.draw_bubble_button(self.bubble_screen, self.button_height, self.button_height, self.button_gap, 5)
        self.main_screen.blit(self.bubble_screen, (0, 0))

    def draw_bubble_button(self, bubble_screen, button_width, button_height, button_radius, gap):
        self.bubble_button.clear()
        font_number = pygame.font.Font("assets/freesansbold.ttf", 22)
        for number in range(1, 10):
            i = (number - 1) // 3
            j = number - i * 3 - 1
            x = self.bubble.left + gap + (button_width + gap) * j
            y = self.bubble.top + gap + (button_width + gap) * i

            first_state = "normal"
            if self.on_rect(self.bubble):
                first_state = "hover_on_parent"

            button = self.draw_button(bubble_screen, x, y, button_width, button_height, font_number,
                                      str(number), self.theme, first_state, True, button_radius)

            self.bubble_button.append(button)

        font_clear = pygame.font.Font("assets/方正粗黑宋简体.ttf", 16)
        clear_x = self.bubble.left + gap
        clear_y = self.bubble.top + 4 * gap + 3 * button_width
        clear_width = 3 * button_width + 2 * gap

        self.button_clear = self.draw_button(bubble_screen, clear_x, clear_y, clear_width, button_width,
                                             font_clear, "清除", self.theme, first_state, True, button_radius)

    def in_bubble_button(self, x, y):
        if self.bubble == 0:
            return 0

        number = 1
        for button in self.bubble_button:
            if self.in_range(button.left, button.top, button.width, button.height):
                return number
            number += 1
        return 0

    def destroy_bubble(self):
        self.bubble = 0

    def draw_panel(self):
        font = pygame.font.Font("assets/方正粗黑宋简体.ttf", 20)
        button_width = 128
        button_height = 35
        button_radius = 5
        button_gap = 5
        panel_x = self.origin_x + self.length + 2.5 * self.lattice - button_width / 2
        panel_y = self.origin_y + self.length - button_gap - button_height
        self.new_game = self.draw_button(self.main_screen, panel_x, panel_y, button_width, button_height,
                                         font, "新游戏", self.theme, "hover_on_parent", True, button_radius)

        panel_y -= (button_gap + button_height)
        self.clear_board = self.draw_button(self.main_screen, panel_x, panel_y, button_width, button_height,
                                            font, "清空数独", self.theme, "hover_on_parent", True, button_radius)

        panel_y -= (button_gap + button_height)
        if self.paused:
            self.pause = self.draw_button(self.main_screen, panel_x, panel_y, button_width, button_height,
                                          font, "继续", self.theme, "hover_on_parent", True, button_radius)
        else:
            self.pause = self.draw_button(self.main_screen, panel_x, panel_y, button_width, button_height,
                                          font, "暂停", self.theme, "hover_on_parent", True, button_radius)

    def draw_main_screen(self):
        self.main_screen.fill(self.theme["primary"])
        self.main_screen.blit(self.transparent_screen, (0, 0))
        self.transparent_screen.fill(self.color.transparent)

        self.draw_cell(self.origin_x, self.origin_y, self.length, 3, 0)
        self.draw_numbers()

        self.draw_time()
        self.draw_panel()

    def draw_start_screen(self):
        self.start_screen.fill(self.theme["primary"])
        font = pygame.font.Font("assets/方正粗黑宋简体.ttf", 20)
        button_width = 300
        button_height = 40
        button_radius = 5
        button_gap = 15
        button_x = self.size[0] / 2 - button_width / 2
        button_y = self.size[1] / 2 - button_gap / 2 - button_height - 100
        self.single_solution = self.draw_button(self.start_screen, button_x, button_y, button_width, button_height,
                                                font, "单解数独", self.theme, "hover_on_parent", True, button_radius)

        button_y += (button_height + button_gap)
        self.multiple_solution = self.draw_button(self.start_screen, button_x, button_y, button_width, button_height,
                                                  font, "多解数独", self.theme, "hover_on_parent", True, button_radius)

        button_y += 2 * (button_height + button_gap)
        self.theme_button = self.draw_button(self.start_screen, button_x, button_y, button_width, button_height,
                                             font, "主题", self.theme, "hover_on_parent", True, button_radius)

        button_y += (button_height + button_gap)
        self.record_button = self.draw_button(self.start_screen, button_x, button_y, button_width, button_height,
                                              font, "记录", self.theme, "hover_on_parent", True, button_radius)

    def draw_choose_screen(self):
        self.choose_screen.fill(self.theme["primary"])
        font = pygame.font.Font("assets/方正粗黑宋简体.ttf", 20)

        back_x = 50
        back_y = 50
        back_width = 20
        back_height = 25
        self.draw_back_button(self.choose_screen, back_x, back_y, back_width, back_height, (7, 9, 7, 9))

        button_width = 300
        button_height = 40
        button_radius = 5
        button_gap = 15
        button_x = self.size[0] / 2 - button_width / 2
        button_y = self.size[1] / 2 - button_gap / 2 - button_height - 100
        self.hard = self.draw_button(self.choose_screen, button_x, button_y, button_width, button_height,
                                     font, "提供30-34个数字", self.theme, "hover_on_parent", True, button_radius)

        button_y += (button_height + button_gap)
        self.middle = self.draw_button(self.choose_screen, button_x, button_y, button_width, button_height,
                                       font, "提供35-39个数字", self.theme, "hover_on_parent", True, button_radius)

        button_y += (button_height + button_gap)
        self.easy = self.draw_button(self.choose_screen, button_x, button_y, button_width, button_height,
                                     font, "提供40-49个数字", self.theme, "hover_on_parent", True, button_radius)

    def draw_record_screen(self):
        self.record_screen.fill(self.theme["primary"])
        title_font = pygame.font.Font("assets/方正粗黑宋简体.ttf", 28)
        text_font = pygame.font.Font("assets/simkai.ttf", 18)

        back_x = 50
        back_y = 50
        back_width = 20
        back_height = 25
        self.draw_back_button(self.record_screen, back_x, back_y, back_width, back_height, (7, 9, 7, 9))

        record_center_x = self.size[0] / 2
        record_center_y = self.size[1] / 2 - 160
        self.draw_text(self.record_screen, title_font, self.theme["font"], "单解数独", record_center_x, record_center_y)
        record_center_y += 45
        for i in range(0, len(self.single)):
            string = ""
            if i == 0:
                string = "提供30-34个数字   "
            elif i == 1:
                string = "提供35-39个数字   "
            elif i == 2:
                string = "提供40-49个数字   "
            self.draw_text(self.record_screen, text_font, self.theme["font"], string,
                           record_center_x - 80, record_center_y)
            if self.single[i] == "":
                string = "暂无记录"
            else:
                string = self.duration_to_time(self.single[i])
            self.draw_text(self.record_screen, text_font, self.theme["font"], string,
                           record_center_x + 90, record_center_y)
            record_center_y += 25

        record_center_y += 45
        self.draw_text(self.record_screen, title_font, self.theme["font"], "多解数独", record_center_x, record_center_y)
        record_center_y += 50
        for i in range(0, len(self.multiple)):
            string = ""
            if i == 0:
                string = "提供30-34个数字   "
            elif i == 1:
                string = "提供35-39个数字   "
            elif i == 2:
                string = "提供40-49个数字   "
            self.draw_text(self.record_screen, text_font, self.theme["font"], string,
                           record_center_x - 80, record_center_y)
            if self.multiple[i] == "":
                string = "暂无记录"
            else:
                string = self.duration_to_time(self.multiple[i])
            self.draw_text(self.record_screen, text_font, self.theme["font"], string,
                           record_center_x + 90, record_center_y)
            record_center_y += 25

    def get_theme(self):
        touch("theme.txt")
        file = open("theme.txt", "r")
        theme_name = file.readline()
        file.close()
        if theme_name == "":
            self.theme = Theme.theme_list[0]
        for theme in Theme.theme_list:
            if theme["name"] == theme_name:
                self.theme = theme
                return

    def set_theme(self, theme):
        file = open("theme.txt", "r")
        theme_name = file.readline()
        file.close()
        if theme_name == theme["name"]:
            return
        file = open("theme.txt", "w+")
        if theme_name == "":
            file.write(theme["name"])
        else:
            file.write(theme["name"])
        self.theme = theme
        file.close()

    def draw_theme_screen(self):
        self.theme_screen.fill(self.theme["primary"])
        title_font = pygame.font.Font("assets/方正粗黑宋简体.ttf", 28)
        font = pygame.font.Font("assets/方正粗黑宋简体.ttf", 20)

        back_x = 50
        back_y = 50
        back_width = 20
        back_height = 25
        self.draw_back_button(self.theme_screen, back_x, back_y, back_width, back_height, (7, 9, 7, 9))

        theme_list = Theme.theme_list
        list_width = 300
        list_height = 40
        list_radius = 5
        list_gap = -1
        list_x = self.size[0] / 2 - list_width / 2
        list_y = self.size[1] / 2 - 3 * list_gap / 2 - 2 * list_height

        frame_width = list_width
        frame_height = 4 * list_height + 3 * list_gap
        frame_radius = 5
        frame_x = list_x
        frame_y = list_y
        margin = (80, 60, 20, 60)
        pygame.draw.rect(self.theme_screen, self.theme["line"],
                         ((frame_x - margin[3], frame_y - margin[0]),
                          (frame_width + margin[1] + margin[3], frame_height + margin[0] + margin[2])),
                         2, border_radius=frame_radius)

        title_y = list_y - 40
        self.draw_text(self.theme_screen, title_font, self.theme["font"], "主题", self.size[0] / 2, title_y)

        radius = 20
        ratio = 0.5
        pre_x = frame_x - margin[3] + radius + 18
        pre_y = list_y + list_height + list_height / 2
        if self.theme_now_page != 1:
            first_state = "hover_on_parent"
            if self.on_circle(self.pre_button):
                first_state = "hover"
            self.pre_button = pygame.draw.circle(self.theme_screen, self.theme[first_state]["border"],
                                                 (pre_x, pre_y), radius, 2)
            pygame.draw.lines(self.theme_screen, self.theme[first_state]["border"], False,
                              [(pre_x + 1 / 2 * ratio * radius, pre_y - sqrt(3) / 2 * ratio * radius),
                               (pre_x - ratio * radius, pre_y),
                               (pre_x + 1 / 2 * ratio * radius, pre_y + sqrt(3) / 2 * ratio * radius)], 2)

        next_x = self.size[0] - pre_x
        next_y = pre_y
        if self.theme_now_page != self.theme_page:
            first_state = "hover_on_parent"
            if self.on_circle(self.next_button):
                first_state = "hover"
            self.next_button = pygame.draw.circle(self.theme_screen, self.theme[first_state]["border"],
                                                  (next_x, next_y), radius, 2)
            pygame.draw.lines(self.theme_screen, self.theme[first_state]["border"], False,
                              [(next_x - 1 / 2 * ratio * radius, next_y - sqrt(3) / 2 * ratio * radius),
                               (next_x + ratio * radius, next_y),
                               (next_x - 1 / 2 * ratio * radius, next_y + sqrt(3) / 2 * ratio * radius)], 2)

        start = (self.theme_now_page - 1) * 4
        end = self.theme_now_page * 4
        if end > len(theme_list):
            end = len(theme_list)
        for i in range(start, end):
            first_state = "hover_on_parent"
            if self.theme == theme_list[i]:
                first_state = "click"

            button = self.draw_button(self.theme_screen, list_x, list_y, list_width, list_height,
                                      font, theme_list[i]["name"], self.theme, first_state, False, list_radius)
            if self.in_rect(button):
                self.set_theme(theme_list[i])

            list_y += (list_gap + list_height)

    def draw_win_bubble(self):
        win_bubble_screen = self.screen.convert_alpha()
        win_bubble_width = 300
        win_bubble_height = 180
        win_bubble_x = (self.size[0] - win_bubble_width) / 2
        win_bubble_y = (self.size[1] - win_bubble_height) / 2

        win_bubble_color = self.theme["normal"]["bubble"]
        win_border_color = self.theme["normal"]["border"]
        win_font_color = self.theme["normal"]["font"]
        first_state = "normal"
        if self.on_range(win_bubble_x, win_bubble_y, win_bubble_width, win_bubble_height):
            win_bubble_color = self.theme["hover"]["bubble"]
            win_border_color = self.theme["hover"]["border"]
            win_font_color = self.theme["hover"]["font"]
            first_state = "hover_on_parent"
        win_bubble = pygame.draw.rect(win_bubble_screen, win_bubble_color,
                                      ((win_bubble_x, win_bubble_y), (win_bubble_width, win_bubble_height)),
                                      0, border_radius=5)
        win_border = pygame.draw.rect(win_bubble_screen, win_border_color,
                                      ((win_bubble_x, win_bubble_y), (win_bubble_width, win_bubble_height)),
                                      1, border_radius=5)

        win_font = pygame.font.Font("assets/方正粗黑宋简体.ttf", 25)
        win_font_x = win_bubble_x + win_bubble_width / 2
        win_font_y = win_bubble_y + 35
        self.draw_text(win_bubble_screen, win_font, win_font_color, "完成", win_font_x, win_font_y)
        if self.new_record():
            font = pygame.font.Font("assets/simkai.ttf", 18)
            win_font_y += 28
            self.draw_text(win_bubble_screen, font, self.theme["emphasize"], " 新纪录！", win_font_x, win_font_y)

        button_width = 0.8 * win_bubble_width
        button_x = win_bubble_x + (win_bubble_width - button_width) / 2
        button_radius = 5
        button_font = pygame.font.Font("assets/方正粗黑宋简体.ttf", 20)

        button_new_game_y = win_bubble_y + win_bubble_height - 5 * self.button_gap - 2 * self.button_height
        self.play_again = self.draw_button(win_bubble_screen, button_x, button_new_game_y,
                                           button_width, self.button_height,
                                           button_font, "再玩一次", self.theme, first_state,
                                           True, button_radius)

        button_quit_y = win_bubble_y + win_bubble_height - 3 * self.button_gap - self.button_height
        self.quit_button = self.draw_button(win_bubble_screen, button_x, button_quit_y,
                                            button_width, self.button_height,
                                            button_font, "退出", self.theme, first_state,
                                            True, button_radius)

        self.screen.blit(win_bubble_screen, (0, 0))

    def get_record(self):
        self.single.clear()
        self.multiple.clear()
        touch("record_single.txt")
        touch("record_multiple.txt")
        record = open("record_single.txt", "r")
        text_lines = record.readlines()
        record.close()
        for line in text_lines:
            time = line.strip("\n").split(" ")
            if len(time) != 1:
                time = str_to_tuple(line.strip('\n'))
            else:
                time = time[0]

            self.single.append(time)

        while len(self.single) < 3:
            self.single.append("")

        record = open("record_multiple.txt", "r")
        text_lines = record.readlines()
        record.close()
        for line in text_lines:
            time = line.strip("\n").split(" ")
            if len(time) != 1:
                time = str_to_tuple(line.strip('\n'))
            else:
                time = time[0]

            self.single.append(time)

        while len(self.multiple) < 3:
            self.multiple.append("")

    def new_record(self):
        if self.solution_num == 1:
            if self.given == "easy":
                record = self.single[2]
            elif self.given == "middle":
                record = self.single[1]
            elif self.given == "hard":
                record = self.single[0]
        elif self.solution_num == 2:
            if self.given == "easy":
                record = self.multiple[2]
            elif self.given == "middle":
                record = self.multiple[1]
            elif self.given == "hard":
                record = self.multiple[0]
        if record == "":
            return True

        if self.duration < record:
            return True
        return False

    def record(self):
        if self.solution_num == 1:
            file_name = "record_single.txt"
            hard = self.single[0]
            middle = self.single[1]
            easy = self.single[2]
        elif self.solution_num == 2:
            file_name = "record_multiple.txt"
            hard = self.multiple[0]
            middle = self.multiple[1]
            easy = self.multiple[2]

        if self.given == "easy":
            if easy == "":
                easy = self.duration
            else:
                if self.duration < easy:
                    easy = self.duration
        elif self.given == "middle":
            if middle == "":
                middle = self.duration
            else:
                if self.duration < middle:
                    middle = self.duration
        elif self.given == "hard":
            if hard == "":
                hard = self.duration
            else:
                if self.duration < hard:
                    hard = self.duration

        string = tuple_to_str(hard) + "\n" + tuple_to_str(middle) + "\n" + tuple_to_str(easy)
        record = open(file_name, "w+")
        record.write(string)
        record.close()

    def click(self, screen):
        x, y = self.mouse_down_position

        if self.win:
            if self.in_rect(self.quit_button):
                self.record()
                self.quit = True

            if self.in_rect(self.play_again):
                self.win = False
                self.sudoku = self.class_sudoku.reset_sudoku()
                self.paused = False
                self.pause_duration = 0
                self.record()
                self.mouse_down_position = (0, 0)
                self.activity_stack = [self.start_screen]
                self.get_record()

            return
        if self.mouse_press[0] == 1:
            if self.in_rect(self.back):
                self.mouse_down_position = (0, 0)
                self.activity_stack.pop()
                self.destroy_back_button()

            if screen == self.start_screen:
                if self.in_rect(self.single_solution):
                    self.solution_num = 1
                    self.mouse_down_position = (0, 0)
                    self.activity_stack.append(self.choose_screen)
                    return

                if self.in_rect(self.multiple_solution):
                    self.solution_num = 2
                    self.mouse_down_position = (0, 0)
                    self.activity_stack.append(self.choose_screen)
                    return

                if self.in_rect(self.theme_button):
                    self.mouse_down_position = (0, 0)
                    self.activity_stack.append(self.theme_screen)

                if self.in_rect(self.record_button):
                    self.mouse_down_position = (0, 0)
                    self.activity_stack.append(self.record_screen)

            if screen == self.choose_screen:
                if self.in_rect(self.easy):
                    self.given = "easy"
                    given = randint(40, 49)
                    if self.solution_num == 1:
                        self.sudoku = self.class_sudoku.generate_sudoku_single(given)
                    else:
                        self.sudoku = self.class_sudoku.generate_sudoku_multiple(given)
                    self.start = perf_counter()
                    self.activity_stack.append(self.main_screen)

                if self.in_rect(self.middle):
                    self.given = "middle"
                    given = randint(35, 39)
                    if self.solution_num == 1:
                        self.sudoku = self.class_sudoku.generate_sudoku_single(given)
                    else:
                        self.sudoku = self.class_sudoku.generate_sudoku_multiple(given)
                    self.start = perf_counter()
                    self.activity_stack.append(self.main_screen)

                if self.in_rect(self.hard):
                    self.given = "hard"
                    given = randint(30, 34)
                    if self.solution_num == 1:
                        self.sudoku = self.class_sudoku.generate_sudoku_single(given)
                    else:
                        self.sudoku = self.class_sudoku.generate_sudoku_multiple(given)
                    self.start = perf_counter()
                    self.activity_stack.append(self.main_screen)

                self.mouse_down_position = (0, 0)

            if screen == self.theme_screen:
                if self.in_circle(self.pre_button):
                    self.theme_now_page -= 1

                if self.in_circle(self.next_button):
                    self.theme_now_page += 1

                self.mouse_down_position = (0, 0)

            if screen == self.main_screen:
                if self.in_rect(self.pause):
                    if self.paused:
                        self.paused = False
                        self.pause_duration += (perf_counter() - self.pause_begin)
                    else:
                        self.paused = True
                        self.pause_begin = perf_counter()
                    self.mouse_down_position = (0, 0)

                if self.in_rect(self.new_game):
                    self.paused = False
                    self.pause_duration = 0
                    self.activity_stack = [self.start_screen]
                    self.mouse_down_position = (0, 0)

                if not self.paused:
                    if self.in_rect(self.clear_board):
                        self.sudoku = self.class_sudoku.reset_sudoku()
                        self.mouse_down_position = (0, 0)

                    if self.bubble != 0:
                        number = self.in_bubble_button(x, y)
                        if number != 0 or self.in_rect(self.button_clear):
                            row = (self.rect.top - self.origin_y) // self.lattice
                            column = (self.rect.left - self.origin_x) // self.lattice
                            self.sudoku[row][column][0] = number
                            self.class_sudoku.check_sudoku(row, column, number)
                            self.mouse_down_position = (0, 0)
                            self.destroy_bubble()
                            return

                    if self.in_rect(self.bubble):  # 有bubble就意味着rect一定已经初始化
                        pygame.draw.rect(self.transparent_screen, self.theme["emphasize"], self.rect, 0)  # 0表示填充矩形
                        self.draw_bubble(self.bubble.left, self.bubble.top, self.bubble.width, self.bubble.height)
                        return
                    else:
                        if not self.in_rect(self.rect):
                            self.destroy_bubble()

                    if self.in_cells(x, y):
                        if self.choose(x, y):
                            rect_left = self.rect.left
                            rect_top = self.rect.top
                            if (rect_left, rect_top) != (-1, -1):
                                bubble_width = self.lattice * 2 + 25
                                bubble_height = self.lattice * 3 + 15
                                bubble_x = rect_left - bubble_width / 2 + self.lattice / 2
                                offset = 10
                                bubble_y = rect_top + self.lattice + offset
                                if bubble_y - offset > self.origin_y + 6 * self.lattice:
                                    bubble_y = rect_top - bubble_height - offset
                                self.draw_bubble(bubble_x, bubble_y, bubble_width, bubble_height)

    def calculate_time(self):
        if self.paused or self.win:
            return self.duration

        now = perf_counter()
        duration = int(now - self.start - self.pause_duration)
        day = duration // (3600 * 24)
        hour = (duration - 3600 * 24 * day) // 3600
        minute = (duration - 3600 * 24 * day - 3600 * hour) // 60
        second = duration - 3600 * hour - 60 * minute
        return day, hour, minute, second

    def duration_to_time(self, duration):
        time = ""
        for i in range(0, len(duration)):
            if (i == 0 or i == 1) and duration[i] == 0:
                continue
            t = str(duration[i])
            if len(t) == 1:
                t = "0" + t
            if i == 0:
                t += "天"
            elif i == 1:
                t += "时"
            elif i == 2:
                t += "分"
            elif i == 3:
                t += "秒"
            time += t
        return time

    def draw_time(self):
        self.duration = self.calculate_time()
        font_time = pygame.font.Font("assets/方正粗黑宋简体.ttf", 20)
        time = self.duration_to_time(self.duration)
        time_x = self.origin_x + self.length + 2.5 * self.lattice
        time_y = self.origin_y + 0.5 * self.lattice

        self.draw_text(self.main_screen, font_time, self.theme["number"], time, time_x, time_y)

    def launch(self):
        self.get_theme()
        self.get_record()
        while True:
            if self.quit:
                break
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.mouse_press = pygame.mouse.get_pressed()  # 返回元组(左键，中键，右键)，bool
                    self.mouse_down_position = pygame.mouse.get_pos()
                elif event.type == pygame.MOUSEMOTION:
                    self.mouse_move_position = pygame.mouse.get_pos()

            self.screen.fill(self.theme["primary"])
            if self.activity_stack[-1] == self.start_screen:
                self.draw_start_screen()
            elif self.activity_stack[-1] == self.choose_screen:
                self.draw_choose_screen()
            elif self.activity_stack[-1] == self.main_screen:
                self.draw_main_screen()
            elif self.activity_stack[-1] == self.theme_screen:
                self.draw_theme_screen()
            elif self.activity_stack[-1] == self.record_screen:
                self.draw_record_screen()
            self.click(self.activity_stack[-1])
            self.screen.blit(self.activity_stack[-1], (0, 0))

            if self.class_sudoku.correct():
                self.win = True
                self.draw_win_bubble()
            pygame.display.flip()

        pygame.quit()


def main():
    ui = UI(70, 70, 450)
    try:
        ui.launch()
    except pygame.error:
        pass


if __name__ == "__main__":
    main()
