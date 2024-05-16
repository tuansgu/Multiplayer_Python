import pygame
import sys
import socket
import gameplay
from button import Button
import traceback

pygame.init()
#systemInfo = pygame.display.Info()
#SCREEN = pygame.display.set_mode((systemInfo.current_w, systemInfo.current_h))
SCREEN = pygame.display.set_mode((1280,720))
pygame.display.set_caption("Menu")
BG = pygame.image.load("assets/bg.jpg")

def get_font(size):
    return pygame.font.Font("assets/fonts/Atop-R99O3.ttf", size)

name_input = []  # Khởi tạo name_input như một list
ready_count = 0

def start_game1():
    global systemInfo
    screen = pygame.display.set_mode((systemInfo.current_w, systemInfo.current_h))
    pygame.display.set_caption("Stress Fight")
    bg_image = pygame.image.load("assets/bggame.jpg")
    screen.blit(bg_image, (0,0))

def start_game(client_socket, player_name):
    gameplay.run(client_socket, player_name)

def play():
    global name_input

    while True:
        PLAY_MOUSE_POS = pygame.mouse.get_pos()

        bg = pygame.image.load("assets/play.jpg")
        SCREEN.blit(bg, (0, 0))

        PLAY_TEXT = get_font(20).render("Enter Your Name: " + ''.join(name_input), True, (255, 255, 255))
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
                    # Kết nối đến server
                    connect_to_server(''.join(name_input))

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    name_input = name_input[:-1]
                elif event.key == pygame.K_RETURN:
                    # Làm gì đó với tên đã nhập, như lưu vào biến
                    print("Player name:", ''.join(name_input))
                    # Gửi ready signal đến server khi nhấn Enter
                    connect_to_server(''.join(name_input))
                else:
                    name_input.append(event.unicode)

        pygame.display.update()

def connect_to_server(player_name):
    # Kết nối đến server
    #HOST = '192.168.56.1'
    HOST = socket.gethostbyname(socket.gethostname())
    PORT = 5555

    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((HOST, PORT))
        client_socket.send(player_name.encode())
        print("Connected to the server as Player")
        #wait_enemy()
        start_game(client_socket, player_name)
    except Exception as e:
        print("Error:", e)
        traceback.print_exc()

def wait_enemy():
    global ready_count

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # Nhận sự kiện từ server và tăng biến ready_count
            if event.type == pygame.USEREVENT and event.message == "ready":
                ready_count += 1

        PLAY_MOUSE_POS = pygame.mouse.get_pos()
        bg = pygame.image.load("assets/waiting.jpg")
        SCREEN.blit(bg, (0, 0))

        # Hiển thị thông báo chờ
        wait_text = get_font(40).render("Waiting for other player...", True, (42, 231, 34))
        wait_rect = wait_text.get_rect(center=(960, 400))
        SCREEN.blit(wait_text, wait_rect)
        
        # Kiểm tra nếu đủ 2 người chơi thì hiển thị nút Start
        if ready_count >= 2:
            START_BUTTON = Button(pos=(960, 600), 
                                  text_input="START", font=get_font(75), base_color=(215, 252, 212), hovering_color=(255, 255, 255))
            START_BUTTON.changeColor(PLAY_MOUSE_POS)
            START_BUTTON.update(SCREEN)
            
            # Nếu đủ 2 người chơi thì gọi hàm start_game()
            start_game()

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

if __name__ == "__main__":
    connect_to_server("John")
    #main_menu()
