import pygame
pygame.init()
from random import randrange
from objects import *
from values import *
from scenes import *
from sys import exit

class Game:
    def __init__(self, WIN_SIZE=(pygame.display.Info().current_w, pygame.display.Info().current_h), FPS=60):
        self.clock = pygame.time.Clock()
        self.FPS = FPS
        self.win = pygame.display.set_mode(WIN_SIZE)
        self.backgrounds = [pygame.transform.scale(pygame.image.load("images/background.png").convert(), (WIN_SIZE)),
                            pygame.transform.scale(pygame.image.load("images/background2.png").convert(), (WIN_SIZE)),
                            pygame.transform.scale(pygame.image.load("images/background3.png").convert(), (WIN_SIZE)),
                            pygame.transform.scale(pygame.image.load("images/background4.png").convert(), (WIN_SIZE))]
        self.current_background = 2
        self.troll_questions = [Question("2 + 2???", ["А может без спойлеров?", "4", "22", "?"], "22"),
                              Question("Кем будешь?", ["Иллюминат", "Мафиозник", "?", "My name is Van..."],
                                       "My name is Van..."), Question("Когда мы сделаем проект по Ницше?",
                                                                      ["Вчера", "Никогда", "А мы не сделали!?",
                                                                       "Да пох**"], "Никогда")]
        self.normal_questions = [Question("Кто брат Ницше?", ["Людвиг Йозеф", "Паулем Ре", "Франц Овербек", "Вильгельм Нестле"], "Людвиг Йозеф"),
                                 Question("Где родился Ницше?", ["Рёккен", "Бланкенбург", "Вернигероде", "Штендаль"], "Рёккен"),
                                 Question("В какой гимназии учился Ницше?", ["Школа Пфорта", "Йенская гимназия", "Берлинская гемназия", "Школа св. Николая"], "Школа Пфорта"),
                                 Question("Что не является книгой Ницше?", ["'Так говорил Заратустра'", "'Утренняя заря'", "'Человеческое слишком человеческое'", "'Степной король лир'"], "'Степной король лир'"),
                                 Question("Один из друзей Ницше?", ["Рихард Вагнер", "Пауль Дойссен", "Карл-Фридрих", "Иоганн Герман"], "Рихард Вагнер"),
                                 Question("В какой войне учавствовал Ницше?", ["Не учавствовал", "Первая мировая война", "Франко-германская война", "Война пятой коалиции"], "Не учавствовал"),
                                 Question("Как зовут сестру Ницше?", ["Элизабет", "Мейзенбуг", "Фрейлейн", "Нет сестры"], "Элизабет"),
                                 Question("Сколько длилась дружба Ницше с Вагнером? ", ["Около трёх лет", "Около года", "Окола двух лет", "Около четырёх лет"], "Около трёх лет"),
                                 Question("Что изучал Ницше в Боннском университете?", ["Теологию и филологию", "Математику и физику", "Философию", "Богословие и историю"], "Теологию и филологию"),
                                 Question("Кто был наставником Ницше?", ["Фридрих Ричль", "Байрон", "Иоганн Вольфганг", "Вильгельм Ине"], "Фридрих Ричль"),
                                 Question("Где Ницше познакомился с Лу Саломе?", ["Рим", "Рёккен", "Кёльн", "Флоренция"], "Рим"),
                                 Question("Где был похоронен Ницше?", ["Рёккен", "Рим", "Цербст", "Кётен"], "Рёккен"),
                                 Question("Кого Ницше считал своим учителем?", ["Шопенгауэр", "Гильдебрандт", "Хелене фон", "Рудольф Леман"], "Шопенгауэр"),
                                 Question("Какой религии придерживался Ницше?", ["Не придерживался", "Христианство", "Ислам", "Буддизм"], "Не придерживался"),
                                 Question("Где преподавал Ницше?", ["Базельский университет", "Тюбингенский университет", "Ростокский университет", "Берлинский университет"], "Базельский университет")]
        self.questions = self.normal_questions
        shuffle(self.questions)
        self.objects = [Button((WIN_SIZE[0] - 230, 52), "restart" ,size=(50, 50), image="images/back_button.png", visible_text=False), Button((WIN_SIZE[0] - 102, 52), "Меню", size=(100, 50)),
                        Text((30, 30), 40, name="scores")]
        self.question_progress_bar = ProgressBar((WIN_SIZE[0] / 2, 50), len(self.questions), "images/progress_bar_shell2.png")
        self.all_objects = self.objects
        self.current_question = 0
        self.current_particles = []
        self.click = False
        self.press = False
        self.scores = 0
        self.state = "play"
        self.version = Text((WIN_SIZE[0] - 180, WIN_SIZE[1] - 30), 50, "Удачи кстати")
        self.fallen_particles = True
        self.click_particles = True
        self.play_sounds = False
        self.click_particles_color = (255, 255, 255)
        self.troll_mode = False

        # Sounds
        self.right_answer_sound = pygame.mixer.Sound("sounds/right_answer_sound.mp3")
        self.wrong_answer_sound = pygame.mixer.Sound("sounds/access_denied.mp3")
        self.troll_wrong_answer_sound = pygame.mixer.Sound("sounds/troll_wrong_answer_sound.mp3")

        self.loop()

    def loop(self):
        menu(self)
        while 1:
            self.handle_events()
            self.update()
            self.draw()

    def handle_events(self):
        self.click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.state == "play":
                        menu(self)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == pygame.BUTTON_LEFT:
                    self.click = True
                    self.press = True

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == pygame.BUTTON_LEFT:
                    self.press = False

    def update(self):
        self.click_particles_color = (255, 255, 255)
        for obj in self.objects:

            # update all
            if type(obj) == CheckBox or type(obj) == Button or type(obj) == ChooseList:

                # update checkboxes
                if type(obj) == CheckBox:
                    obj.update(self.click, self.play_sounds)
                    if obj.name == "fallen_particles":
                        self.fallen_particles = obj.value
                    if obj.name == "sounds":
                        self.play_sounds = obj.value
                    if obj.name == "click_particles":
                        self.click_particles = obj.value
                    if obj.name == "troll_mode":
                        self.troll_mode = obj.value

                # update choose lists
                if type(obj) == ChooseList:
                    obj.update(self.click, self.play_sounds)
                    if obj.name == "background":
                        self.current_background = obj.index

                # update buttons
                if type(obj) == Button:
                    if self.state == "play":
                        if obj.update(self.click, self.play_sounds):
                            if obj.text == "restart":
                                restart(self)
                            if obj.text == "Меню":
                                menu(self)
                    if self.state == "menu":
                        if obj.update(self.click, self.play_sounds):
                            if obj.text == "Играть":
                                return_to_game(self)
                            if obj.text == "Настройки":
                                settings(self)
                            if obj.text == "Выйти":
                                exit()
                    if self.state == "settings":
                        if obj.update(self.click, self.play_sounds):
                            if obj.text == "Назад":
                                menu(self)
                    if self.state == "end":
                        if obj.update(self.click, self.play_sounds):
                            if obj.text == "restart":
                                restart(self)
                            if obj.text == "exit":
                                exit()
                    obj.update(self.click, self.play_sounds)

            # update all without buttons, checkboxes and choose lists
            else:
                obj.update()

        # update questions
        if self.state == "play":
            self.update_questions()

        # update question progress bar
        if self.state == "play":
            self.question_progress_bar.update()
            self.question_progress_bar.set_progress(self.current_question)
        elif self.state == "end":
            self.question_progress_bar.add_progress()

        # update particles
        self.update_particles()
        if self.fallen_particles and self.state == "play" or self.state == "end":
            self.generate_particles(1)

        # update click
        if self.click and self.click_particles:
            self.make_click_particles(10)

        self.clock.tick(self.FPS)

    def draw(self):

        # draw background and version
        self.win.blit(self.backgrounds[self.current_background], ZERO)
        self.version.draw(self.win)

        # draw all objects
        for obj in self.objects:
            if type(obj) == Text:
                if obj.name == "scores":
                    obj.draw(self.win, self.scores)
                else:
                    obj.draw(self.win)
            else:
                obj.draw(self.win)

        # draw questions
        if self.state == "play":
            self.draw_questions()

        # draw question progress bar
        if self.state == "play" or self.state == "end":
            self.question_progress_bar.draw(self.win)

        # draw particles
        if self.state == "play" or self.state == "end":
            self.draw_particles()
        else:
            self.clear_particles()
        pygame.display.flip()

    def update_questions(self):
        for but in self.questions[self.current_question].buttons:
            if but.update(self.click, 0):
                if but.text == self.questions[self.current_question].answer:
                    if self.play_sounds:
                        pygame.mixer.Sound.play(self.right_answer_sound)
                    self.click_particles_color = (0, 255, 0)
                    self.answer(1)
                else:
                    if self.play_sounds:
                        if self.troll_mode:
                            pygame.mixer.Sound.play(self.troll_wrong_answer_sound)
                        else:
                            pygame.mixer.Sound.play(self.wrong_answer_sound)
                    self.click_particles_color = (0, 255, 0)
                    self.click_particles_color = (255, 0, 0)
                    self.answer()

    def draw_questions(self):
        for but in self.questions[self.current_question].buttons:
            but.draw(self.win)
        self.questions[self.current_question].text.draw(self.win)

    def answer(self, add_scores=0):
        try:
            pygame.display.flip()
            self.scores += add_scores
            if self.current_question + 1 == len(self.questions):
                end(self)
            else:
                self.current_question += 1
        except:
            end(self)

    def generate_particles(self, amount):
        for i in range(amount):
            if randrange(1, 10) == 7:
                self.current_particles.append(Particle((randrange(0, WIN_SIZE[0]), -3),
                                                       (randrange(200, 255), randrange(200, 255), randrange(200, 255)), randrange(10, 100) / 10, randrange(-50, 50) / 10, randrange(1, 5)))

    def update_particles(self):
        for particle in self.current_particles:
            if particle.update():
                self.current_particles.remove(particle)

    def draw_particles(self):
        for particle in self.current_particles:
            self.win.blit(particle.image, particle.rect)

    def make_click_particles(self, amount):
        for i in range(amount):
            self.current_particles.append(ClickParticle(pygame.mouse.get_pos(), self.click_particles_color, randrange(1, 10),
                                                        randrange(-50, 50) / 10, randrange(-100, 10) / 10, 0.2))

    def clear_particles(self):
        self.current_particles = []

game = Game()
