import pygame
import sys
from button import Button

pygame.init()

SCREEN = pygame.display.set_mode((1920, 1080))
pygame.display.set_caption("Menu")

BG = pygame.image.load("assets/bg.jpg")

def get_font(size):
    return pygame.font.Font("assets/Atop-R99O3.ttf", size)

name_input = ""  # Khai báo biến name_input như một biến toàn cục

def play():
    global name_input  # Sử dụng biến name_input toàn cục

    while True:
        PLAY_MOUSE_POS = pygame.mouse.get_pos()

        bg = pygame.image.load("assets/play.jpg")
        SCREEN.blit(bg, (0,0))

        PLAY_TEXT = get_font(20).render("Enter Your Name: " + name_input, True, (255, 255, 255))
        PLAY_RECT = PLAY_TEXT.get_rect(center=(960, 540))
        SCREEN.blit(PLAY_TEXT, PLAY_RECT)

        OPTIONS_PLAY = Button(pos=(1080, 800),
                              text_input="CONTINUE", font=get_font(40), base_color=(255, 255, 255), hovering_color=(0, 255, 0))
        PLAY_BACK = Button(pos=(800, 800), 
                            text_input="BACK", font=get_font(40), base_color=(255, 255, 255), hovering_color=(0, 255, 0))
        PLAY_BACK.changeColor(PLAY_MOUSE_POS)
        OPTIONS_PLAY.changeColor(PLAY_MOUSE_POS)
        PLAY_BACK.update(SCREEN)
        OPTIONS_PLAY.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BACK.checkForInput(PLAY_MOUSE_POS):
                    main_menu()
                elif OPTIONS_PLAY.checkForInput(PLAY_MOUSE_POS):
                    wait_enermy()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    name_input = name_input[:-1]
                elif event.key == pygame.K_RETURN:
                    # Do something with the entered name, like storing it in a variable
                    print("Player name:", name_input)
                else:
                    name_input += event.unicode

        pygame.display.update()

def wait_enermy():
    while True:
        PLAY_MOUSE_POS = pygame.mouse.get_pos()
        bg = pygame.image.load("assets/waiting.jpg")
        SCREEN.blit(bg, (0,0))

        # Display player's name
        player_name_text = get_font(40).render("Player 1: " + name_input, True, (255, 255, 255))
        player_name_rect = player_name_text.get_rect(center=(960, 400))
        SCREEN.blit(player_name_text, player_name_rect)

        # Display "Waiting" text
        waiting_text = get_font(40).render("Waiting...", True, (255, 255, 255))
        waiting_rect = waiting_text.get_rect(center=(960, 500))
        PLAY_BACK = Button(pos=(960, 800), 
                            text_input="BACK", font=get_font(40), base_color=(255, 255, 255), hovering_color=(0, 255, 0))
        PLAY_BACK.changeColor(PLAY_MOUSE_POS)
        PLAY_BACK.update(SCREEN)
        SCREEN.blit(waiting_text, waiting_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BACK.checkForInput(PLAY_MOUSE_POS):
                    main_menu()
        pygame.display.update()

def options():
    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill((255, 255, 255))

        OPTIONS_TEXT = get_font(60).render("This is the OPTIONS screen.", True, (0, 0, 0))
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(960, 540))
        SCREEN.blit(OPTIONS_TEXT, OPTIONS_RECT)

        OPTIONS_BACK = Button(pos=(960, 800), 
                            text_input="BACK", font=get_font(75), base_color=(0, 0, 0), hovering_color=(0, 255, 0))

        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        
        OPTIONS_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    main_menu()

        pygame.display.update()

def main_menu():
    while True:
        SCREEN.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(100).render("MAIN MENU", True, (182, 143, 64))
        MENU_RECT = MENU_TEXT.get_rect(center=(960, 200))

        PLAY_BUTTON = Button(pos=(960, 400), 
                            text_input="PLAY", font=get_font(75), base_color=(215, 252, 212), hovering_color=(255, 255, 255))
        OPTIONS_BUTTON = Button(pos=(960, 600), 
                            text_input="OPTIONS", font=get_font(75), base_color=(215, 252, 212), hovering_color=(255, 255, 255))
        QUIT_BUTTON = Button(pos=(960, 800), 
                            text_input="QUIT", font=get_font(75), base_color=(215, 252, 212), hovering_color=(255, 255, 255))

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play()
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    options()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

main_menu()
