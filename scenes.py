import pygame
pygame.init()
from objects import *
from values import *

def menuold(game):
    clock = pygame.time.Clock()
    buttons = [Button((CENTER[0], CENTER[1] - 200), "Начать"), Button((CENTER[0], CENTER[1]), "Настройки"), Button((CENTER[0], CENTER[1] + 200), "Выйти нахуй")]
    click = False
    while 1:
        game.win.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    exit()
                if event.key == pygame.K_r:
                    restart(game)
                    return
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == pygame.BUTTON_LEFT:
                    click = True
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == pygame.BUTTON_LEFT:
                    click = False
        for obj in buttons:
            if type(obj) == Button:
                if obj.update(click):
                    if obj.text == "Начать":
                        return
                    if obj.text == "Настройки":
                        settings(game.win)
                    if obj.text == "Выйти нахуй":
                        exit()
            else:
                obj.update()
            if type(obj) == Button:
                obj.draw(game.win)
        pygame.display.flip()
        clock.tick(60)

def settingsold(win):
    clock = pygame.time.Clock()
    buttons = [Button((CENTER[0], CENTER[1] - 100), "Яркость"), Button((CENTER[0], CENTER[1] + 100), "Назад")]
    click = False
    while 1:
        win.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == pygame.BUTTON_LEFT:
                    click = True
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == pygame.BUTTON_LEFT:
                    click = False
        for obj in buttons:
            if type(obj) == Button:
                if obj.update(click):
                    if obj.text == "Яркость":
                        pass
                    if obj.text == "Назад":
                        return
            else:
                obj.update()
            if type(obj) == Button:
                obj.draw(win)
        pygame.display.flip()
        clock.tick(60)

def settings(game):
    game.objects = [Button((CENTER[0], CENTER[1] + 300), "Назад"), CheckBox((CENTER[0] - 150, CENTER[1] - 60), game.fallen_particles, "Падающие частицы", "fallen_particles"),
                    CheckBox((CENTER[0] - 150, CENTER[1]), game.click_particles, "Частицы после клика", "click_particles"), CheckBox((CENTER[0] - 150, CENTER[1] - 120), game.play_sounds, "Звук", "sounds"),
                    CheckBox((CENTER[0] - 150, CENTER[1] + 60), game.troll_mode, "Troll mode", "troll_mode", blocked=True), ChooseList((CENTER[0], CENTER[1] + 140), ["Default", "Blind", "Dark", "Shapes"], game.current_background, "background")]
    game.current_background = game.current_background
    game.state = "settings"

def menu(game):
    game.objects = [Button((CENTER[0], CENTER[1] - 200), "Играть"), Button((CENTER[0], CENTER[1]), "Настройки"), Button((CENTER[0], CENTER[1] + 200), "Выйти")]
    game.current_background = game.current_background
    game.state = "menu"

def return_to_game(game):
    game.state = "play"
    game.objects = game.all_objects

def restart(game):
    if game.play_sounds:
        if game.troll_mode:
            pass
        else:
            pass
    return_to_game(game)
    shuffle(game.questions)
    for que in game.questions:
        que.shuffle_buttons()
    game.current_question = 0
    game.scores = 0
    game.question_progress_bar.remove_progress(9999999)

def end(game):
    if game.play_sounds:
        if game.troll_mode:
            pygame.mixer.music.load("sounds/troll_full_scores_end_sound.mp3")
            pygame.mixer.music.play()
        elif game.scores == len(game.questions):
            pygame.mixer.music.load("sounds/full_scores_end_sound.mp3")
            pygame.mixer.music.play()
            pass
    game.objects = [Button((CENTER[0], CENTER[1] + 60), "restart" ,size=(100, 100), image="images/back_button.png", visible_text=False),
                    Button((CENTER[0], CENTER[1] - 60), "exit" ,size=(100, 100), image="images/cross_button.png", visible_text=False),
                    Text((CENTER[0], 150), 100, f"Ваши очки: {game.scores}")]
    game.current_background = game.current_background
    game.state = "end"
