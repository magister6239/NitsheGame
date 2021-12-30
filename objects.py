import pygame
pygame.init()
from values import *
from random import shuffle

class Button:
    def __init__(self, cor, text, image="images/button.png", size=(300,60), visible_text=True):
        self.font_size = 50
        self.font = pygame.font.Font("fonts/Second.ttf", self.font_size)
        self.text = text
        self.center = cor
        self.size = size
        self.image = pygame.transform.scale(pygame.image.load(image).convert(), size)
        self.image_rect = self.image.get_rect(center=cor)
        self.text_image = self.font.render(text, 1, (255, 255, 255))
        self.text_image_rect = self.text_image.get_rect(center=cor)
        self.visible_text = visible_text
        self.border_width = 2
        self.border_color = (255, 255, 255)
        self.blocked = False
        self.sound = pygame.mixer.Sound("sounds/button_click.wav")

    def update(self, click, play_sound):
        self.__check_text_size()
        if self.image_rect.collidepoint(pygame.mouse.get_pos()):
            self.border_color = (0, 0, 255)
            if click:
                self.border_color = (0, 255, 0)
                if play_sound:
                    pygame.mixer.Sound.play(self.sound)
                return True
        else:
            self.border_color = (255, 255, 255)

    def draw(self, win):
        win.blit(self.image, self.image_rect)
        pygame.draw.rect(win, self.border_color, (self.image_rect.topleft[0] - self.border_width, self.image_rect.topleft[1] - self.border_width,
                                                  self.size[0] + self.border_width, self.size[1] + self.border_width), width=2)
        if self.visible_text:
            win.blit(self.text_image, self.text_image_rect)

    def __check_text_size(self):
        if self.text_image.get_width() > self.image.get_width():
            self.font_size -= 1
            self.font = self.font = pygame.font.Font("fonts/Second.ttf", self.font_size)
            self.text_image = self.font.render(self.text, 1, (255, 255, 255))
            self.text_image_rect = self.text_image.get_rect(center=self.image_rect.center)

class CheckBox:
    def __init__(self, cor, start_value, text=None, name=None, size=(50, 50), blocked=False):
        self.font = pygame.font.Font("fonts/Second.ttf", size[0])
        self.size = size
        self.checkbox_true_image = pygame.transform.scale(pygame.image.load("images/checkbox_true.png").convert(), size)
        self.checkbox_false_image = pygame.transform.scale(pygame.image.load("images/checkbox_false.png").convert(), size)
        self.checkbox_blocked_image = pygame.transform.scale(pygame.image.load("images/cross_button.png").convert(), size)
        self.image = self.checkbox_false_image
        self.image_rect = self.checkbox_true_image.get_rect(center=cor)
        self.text_image = self.font.render(text, 1, (255, 255, 255))
        self.text_image_rect = self.text_image.get_rect(center=cor)
        self.text_image_rect.center = (cor[0] + self.image_rect.width + self.text_image_rect.width / 2, cor[1])
        self.border_color = (0, 0, 0)
        self.border_width = 2
        self.value = start_value
        self.name = name
        self.blocked = blocked
        self.sound = pygame.mixer.Sound("sounds/button_click.wav")
        self.blocked_sound = pygame.mixer.Sound("sounds/access_denied.mp3")

    def update(self, click, play_sound):
        if self.image_rect.collidepoint(pygame.mouse.get_pos()):
            self.border_color = (0, 0, 255)
            if click:
                if not self.blocked:
                    self.border_color = (0, 255, 0)
                    self.value = not self.value
                    if play_sound:
                        pygame.mixer.Sound.play(self.sound)
                else:
                    if play_sound:
                        pygame.mixer.Sound.play(self.blocked_sound)
        else:
            self.border_color = (255, 255, 255)
        if not self.blocked:
            if self.value:
                self.image = self.checkbox_true_image
                return True
            else:
                self.image = self.checkbox_false_image
                return False
        else:
            self.image = self.checkbox_blocked_image

    def draw(self, win):
        win.blit(self.image, self.image_rect)
        pygame.draw.rect(win, self.border_color, (self.image_rect.topleft[0] - self.border_width, self.image_rect.topleft[1] - self.border_width,
                                                  self.size[0] + self.border_width, self.size[1] + self.border_width), width=2)
        win.blit(self.text_image, self.text_image_rect)

class ChooseList:
    def __init__(self, cor, list_of_choose, start_index, name=None, image="images/button.png", size=(200, 60), font_size=60):
        self.list = list_of_choose
        self.index = start_index
        self.current_choose = self.list[self.index]
        self.image = pygame.transform.scale(pygame.image.load(image).convert(), size)
        self.image_rect = self.image.get_rect(center=cor)
        self.size = size
        self.cor = cor
        self.border_width = 2
        self.border_color = (0, 0, 0)
        self.font = pygame.font.Font("fonts/Second.ttf", font_size)
        self.font_size = font_size
        self.text_image = self.font.render(self.current_choose, 1, (255, 255, 255))
        self.text_image_rect = self.text_image.get_rect(center=cor)
        self.text = ""
        self.name = name
        self.sound = pygame.mixer.Sound("sounds/switch_choose_list_sound.mp3")

    def update(self, click, play_sound):
        self.__check_text_size()
        if self.image_rect.collidepoint(pygame.mouse.get_pos()):
            self.border_color = (0, 0, 255)
            if click:
                if play_sound:
                    pygame.mixer.Sound.play(self.sound)
                self.border_color = (0, 255, 0)
                self.index += 1
                if self.index == len(self.list):
                    self.index = 0
                self.current_choose = self.list[self.index]
                self.text_image = self.font.render(self.current_choose, 1, (255, 255, 255))
                self.text_image_rect = self.text_image.get_rect(center=self.cor)
        else:
            self.border_color = (255, 255, 255)

    def draw(self, win):
        win.blit(self.image, self.image_rect)
        pygame.draw.rect(win, self.border_color, (self.image_rect.topleft[0] - self.border_width, self.image_rect.topleft[1] - self.border_width,
                                                  self.size[0] + self.border_width, self.size[1] + self.border_width), width=2)
        win.blit(self.text_image, self.text_image_rect)

    def __check_text_size(self):
        if self.text_image.get_width() > self.image.get_width():
            self.font_size -= 3
            self.font = self.font = pygame.font.Font("fonts/Second.ttf", self.font_size)
            self.text_image = self.font.render(self.current_choose, 1, (255, 255, 255))
            self.text_image_rect = self.text_image.get_rect(center=self.image_rect.center)

class Text(pygame.sprite.Sprite):
    def __init__(self, cor, size, text=None, name=None):
        self.font = pygame.font.Font("fonts/Second.ttf", size)
        self.cor = cor
        self.text = text
        self.name = name

    def draw(self, win, text=None):
        if text != None:
            self.text = text
        self.image = self.font.render(str(self.text), 1, (255, 255, 255))
        self.image_rect = self.image.get_rect(center=self.cor)
        win.blit(self.image, self.image_rect)

class Question:
    def __init__(self, text, buttons, answer):
        self.list_of_buttons = buttons
        shuffle(buttons)
        self.button_image = "images/button2.png"
        self.text = Text((CENTER[0], CENTER[1] - 100), 50, text)
        self.buttons = [Button((CENTER[0] - 300, WIN_SIZE[1] - 300), buttons[0], self.button_image), Button((CENTER[0] + 300, WIN_SIZE[1] - 300), buttons[1], self.button_image),
                        Button((CENTER[0] + 300, WIN_SIZE[1] - 150), buttons[2], self.button_image), Button((CENTER[0] - 300, WIN_SIZE[1] - 150), buttons[3], self.button_image)]
        self.answer = answer

    def light_answer(self):
        for but in self.buttons:
            if but.text == self.answer:
                but.border_color = (0, 255, 0)
            else:
                but.border_color = (255, 0, 0)

    def shuffle_buttons(self):
        shuffle(self.list_of_buttons)
        self.buttons = [Button((CENTER[0] - 300, WIN_SIZE[1] - 300), self.list_of_buttons[0], self.button_image),
                        Button((CENTER[0] + 300, WIN_SIZE[1] - 300), self.list_of_buttons[1], self.button_image),
                        Button((CENTER[0] + 300, WIN_SIZE[1] - 150), self.list_of_buttons[2], self.button_image),
                        Button((CENTER[0] - 300, WIN_SIZE[1] - 150), self.list_of_buttons[3], self.button_image)]

class Particle:
    def __init__(self, pos, color, size, speed_x, speed_y):
        self.image = pygame.Surface((size, size))
        self.image.fill(color)
        self.rect = self.image.get_rect(center=pos)
        self.speed_x = speed_x
        self.speed_y = speed_y

    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        if self.rect.centerx <= -10 or self.rect.centerx >= WIN_SIZE[0] + 10:
            return True
        if self.rect.centery <= -10 or self.rect.centery >= WIN_SIZE[1] + 10:
            return True

class ClickParticle(Particle):
    def __init__(self, pos, color, size, speed_x, speed_y, acceleration=1):
        super().__init__(pos, color, size, speed_x, speed_y)
        self.acceleration = acceleration

    def update(self):
        super().update()
        self.speed_y += self.acceleration

class ProgressBar:
    def __init__(self, pos, max, progress_bar_shell_image="images/progress_bar_shell.png", progress_bar_line_image="images/progress_bar_line.png" ,name=None):
        self.image = pygame.transform.scale(pygame.image.load(progress_bar_shell_image), (300, 100))
        self.image_line = pygame.transform.scale(pygame.image.load(progress_bar_line_image), (250, 100))
        self.rect = self.image.get_rect(center=pos)
        self.rect_line = self.image_line.get_rect(center=pos)
        self.progress = 0
        self.progress_max = max
        self.one_chunk = 250 / self.progress_max
        self.start_pos = 10
        self.name = name

    def update(self):
        pass

    def draw(self, win):
        win.blit(self.image, self.rect)
        win.blit(self.image_line, self.rect_line, (0, 0, self.progress * self.one_chunk, 100))

    def add_progress(self, count=1):
        self.progress += count
        self.progress = min(self.progress, self.progress_max)

    def remove_progress(self, count=1):
        self.progress -= count
        self.progress = max(self.progress, 0)

    def set_progress(self, value):
        self.progress = value
