import traceback

import pygame
from pygame import mixer

from fighter import Fighter
import threading
from button import *

player = 0
def receive(client_socket, SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter_1, fighter_2, round_over, chat_dialog, ):
  global player
  while True:
    try:
      key = client_socket.recv(1024).decode("utf-8")
      if (key.startswith("__P") and player == 0):
        player = key[3]
      elif (key.startswith("__1")):
        fighter_1.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter_2, round_over, key)
      elif (key.startswith("__2")):
        fighter_2.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter_1, round_over, key)
      else:
        chat_dialog.append(key)
    except:
      break

  client_socket.close()
  
def run(client_socket, player_name):
  global player
  mixer.init()
  pygame.init()

  #create game window
  systemInfo = pygame.display.Info()
  SCREEN_WIDTH = 1280
  SCREEN_HEIGHT = 720

  screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
  pygame.display.set_caption(f"Brawler {player}")

  #set framerate
  clock = pygame.time.Clock()
  FPS = 60

  #define colours
  RED = (255, 0, 0)
  YELLOW = (255, 255, 0)
  WHITE = (255, 255, 255)

  #define game variables
  intro_count = 3
  last_count_update = pygame.time.get_ticks()
  score = [0, 0]#player scores. [P1, P2]
  round_over = False
  ROUND_OVER_COOLDOWN = 2000

  #define fighter variables
  WARRIOR_SIZE = 162
  WARRIOR_SCALE = 4
  WARRIOR_OFFSET = [72, 56]
  WARRIOR_DATA = [WARRIOR_SIZE, WARRIOR_SCALE, WARRIOR_OFFSET]
  WIZARD_SIZE = 250
  WIZARD_SCALE = 3
  WIZARD_OFFSET = [112, 107]
  WIZARD_DATA = [WIZARD_SIZE, WIZARD_SCALE, WIZARD_OFFSET]

  #load music and sounds
  pygame.mixer.music.load("assets/audio/music.mp3")
  pygame.mixer.music.set_volume(9.5)
  pygame.mixer.music.play(-1, 0.0, 5000)
  sword_fx = pygame.mixer.Sound("assets/audio/sword.wav")
  sword_fx.set_volume(0.5)
  magic_fx = pygame.mixer.Sound("assets/audio/magic.wav")
  magic_fx.set_volume(0.75)

  #load background image
  bg_image = pygame.image.load("assets/bggame.jpg").convert_alpha()

  #load spritesheets
  warrior_sheet = pygame.image.load("assets/images/warrior/Sprites/warrior.png").convert_alpha()
  wizard_sheet = pygame.image.load("assets/images/wizard/Sprites/wizard.png").convert_alpha()

  #load vicory image
  victory_img = pygame.image.load("assets/images/icons/victory.png").convert_alpha()

  #define number of steps in each animation
  WARRIOR_ANIMATION_STEPS = [10, 8, 1, 7, 7, 3, 7]
  WIZARD_ANIMATION_STEPS = [8, 8, 1, 8, 8, 3, 7]

  #define font
  count_font = pygame.font.Font("assets/fonts/turok.ttf", 80)
  score_font = pygame.font.Font("assets/fonts/turok.ttf", 40)
  chat_font = pygame.font.Font("assets/fonts/CascadiaCode.ttf", 18)
  
  #define chat elements
  chat_dialog = []
  chat_input = []
  chat_flag = False
  chat_bg_rect = pygame.Rect(40, SCREEN_HEIGHT - 40, 445, 30)
  input_color = (127,127,127)
  show = False

  #function for drawing text
  def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

  #function for drawing background
  def draw_bg():
    scaled_bg = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.blit(scaled_bg, (0, 0))

  #function for drawing fighter health bars
  def draw_health_bar(health, x, y):
    ratio = health / 100
    width = SCREEN_WIDTH // 2 - 40
    pygame.draw.rect(screen, WHITE, (x - 2, y - 2, width + 4, 34))
    pygame.draw.rect(screen, RED, (x, y, width, 30))
    pygame.draw.rect(screen, YELLOW, (x, y, width * ratio, 30))    
  
  def is_special_key(key):
    special = [pygame.K_INSERT, pygame.K_HOME, pygame.K_END, pygame.K_PAGEUP, pygame.K_PAGEDOWN, pygame.K_F1, pygame.K_F2, pygame.K_F3,
               pygame.K_F4, pygame.K_F5, pygame.K_F6, pygame.K_F7, pygame.K_F8, pygame.K_F9, pygame.K_F10, pygame.K_F11, pygame.K_F12,
               pygame.K_F13, pygame.K_F14, pygame.K_F15, pygame.K_NUMLOCK, pygame.K_CAPSLOCK, pygame.K_SCROLLOCK, pygame.K_RSHIFT, pygame.K_LSHIFT,
               pygame.K_RCTRL, pygame.K_LCTRL, pygame.K_RALT, pygame.K_LALT, pygame.K_RMETA, pygame.K_LMETA, pygame.K_LSUPER, pygame.K_RSUPER,
               pygame.K_MODE, pygame.K_HELP, pygame.K_PRINT, pygame.K_SYSREQ, pygame.K_BREAK, pygame.K_MENU, pygame.K_POWER, pygame.K_AC_BACK]
    return key in special

  #Tạo 2 fighter với tọa độ x y
  fighter_1 = Fighter(1, SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT * 13 // 22, False, WARRIOR_DATA, warrior_sheet, WARRIOR_ANIMATION_STEPS, sword_fx)
  fighter_2 = Fighter(2, SCREEN_WIDTH // 2 + 200, SCREEN_HEIGHT * 13 // 22, True, WIZARD_DATA, wizard_sheet, WIZARD_ANIMATION_STEPS, magic_fx)
  # fighter_1.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter_2, round_over)
  # fighter_2.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter_1, round_over)
  
  receive_thread = threading.Thread(target=receive, args=(client_socket, SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter_1, fighter_2, round_over, chat_dialog))
  receive_thread.start()

  global update_allowed2
  #game loop
  isRun = True
  while isRun:
    MOUSE_POS = pygame.mouse.get_pos()
    clock.tick(FPS)

    #draw background
    draw_bg()

    #show player stats
    draw_health_bar(fighter_1.health, 20, 140)
    draw_health_bar(fighter_2.health, SCREEN_WIDTH // 2 + 20, 140)
    draw_text("P1: " + str(score[0]), score_font, RED, 20, 60)
    draw_text("P2: " + str(score[1]), score_font, RED, SCREEN_WIDTH - 100, 60)
    
    #move fighters
    # fighter_1.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter_2, round_over)
    # fighter_2.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter_1, round_over)

    #update countdown
    if intro_count <= 0:
      if round_over == False and chat_flag == False:
        key = pygame.key.get_pressed()
        if (key[pygame.K_a]): client_socket.send(f"__{player}A".encode("utf-8"))
        if (key[pygame.K_d]): client_socket.send(f"__{player}D".encode("utf-8"))
        #if (key[pygame.K_w]): client_socket.send(f"__{player}W".encode("utf-8"))
        if (key[pygame.K_r]): client_socket.send(f"__{player}R".encode("utf-8"))
        if (key[pygame.K_t]): client_socket.send(f"__{player}T".encode("utf-8"))

    else:
      #display count timer
      draw_text(str(intro_count), count_font, RED, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 3)
      #update count timer
      if (pygame.time.get_ticks() - last_count_update) >= 1000:
        intro_count -= 1
        last_count_update = pygame.time.get_ticks()

    #update fighters
    fighter_1.update()
    fighter_2.update()

    #draw fighters
    fighter_1.draw(screen)
    fighter_2.draw(screen)

    """
    ---------------------------------------------------------------------------------
    """
    #check for player defeat
    if round_over == False:
      if fighter_1.alive == False:
        score[1] += 1
        round_over = True
        round_over_time = pygame.time.get_ticks()
      elif fighter_2.alive == False:
        score[0] += 1
        round_over = True
        round_over_time = pygame.time.get_ticks()
    else:
      #display victory image
      screen.blit(victory_img, (SCREEN_WIDTH // 2 - 140, 200)) #width of victory_img is 280px
      if pygame.time.get_ticks() - round_over_time > ROUND_OVER_COOLDOWN:
        round_over = False
        intro_count = 3
        fighter_1.reset(1, SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT * 13 // 22, False, WARRIOR_DATA, warrior_sheet, WARRIOR_ANIMATION_STEPS, sword_fx)
        fighter_2.reset(2, SCREEN_WIDTH // 2 + 200, SCREEN_HEIGHT * 13 // 22, True, WIZARD_DATA, wizard_sheet, WIZARD_ANIMATION_STEPS, magic_fx)
        receive_thread = threading.Thread(target=receive, args=(client_socket, SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter_1, fighter_2, round_over,))

    #draw chat input
    CHAT_INPUT_TEXT = chat_font.render("Chat here" if chat_input == [] else "".join(chat_input[-31:]), True, input_color)
    CHAT_INPUT_RECT = CHAT_INPUT_TEXT.get_rect(topleft=(50, SCREEN_HEIGHT - 37))
    #draw chat input background
    pygame.draw.rect(screen, (40,40,40), chat_bg_rect)

    #draw conversation (shown or not)
    CHAT_SHOW = ImageButton(screen=screen, pos=(10, SCREEN_HEIGHT - 40), path="assets/images/icons/up.png")
    CHAT_SHOW.update(screen)

    #create Send button
    CHAT_BUTTON = Button(pos=(455, SCREEN_HEIGHT - 40), text_input="Send", font=chat_font, base_color=(255, 255, 255), hovering_color=(0, 200, 200))
    CHAT_BUTTON.text_rect = CHAT_BUTTON.text.get_rect(topleft=(423, SCREEN_HEIGHT - 37))
    CHAT_BUTTON.update(screen)

    if show:
      i = 0
      CHAT_SHOW.setPath(screen, "assets/images/icons/down.png")
      show_surf = pygame.Surface((475,480))
      show_surf.set_alpha(128)
      show_surf.fill((40,40,40))
      screen.blit(show_surf, (10,SCREEN_HEIGHT - 520))
      for dialog in chat_dialog[-16:]:
        CHAT_TEXT = chat_font.render(dialog, True, (255,255,255), None)
        CHAT_RECT = CHAT_TEXT.get_rect(topleft=(10,(SCREEN_HEIGHT - 520) + 30*i))
        i += 1
        screen.blit(CHAT_TEXT, CHAT_RECT)
    
    screen.blit(CHAT_INPUT_TEXT, CHAT_INPUT_RECT)

    #event handler
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        isRun = False
        client_socket.close()

      if event.type == pygame.MOUSEBUTTONDOWN:
        if (CHAT_BUTTON.checkForInput(MOUSE_POS)):
          CHAT_BUTTON.changeColor(MOUSE_POS)
        if (chat_bg_rect.collidepoint(MOUSE_POS)):
          chat_flag = True
        else:
          chat_flag = False
      
      if event.type == pygame.MOUSEBUTTONDOWN:
        if CHAT_BUTTON.checkForInput(MOUSE_POS):
          if ("".join(chat_input) == ""): continue
          dialog = player_name + ": " + "".join(chat_input)
          for i in range(0,len(dialog),35):
            client_socket.send(dialog[i:i+35].encode("utf-8"))
          chat_input = []
          input_color = (127, 127, 127)
          continue
        if CHAT_SHOW.checkForInput(MOUSE_POS):
            show = not show

      if event.type == pygame.KEYDOWN and chat_flag:
        if event.key == pygame.K_BACKSPACE:
          if (len(chat_input) > 0):
            chat_input.pop()
            if len(chat_input) == 0: input_color = (127,127,127)
        elif event.key == pygame.K_RETURN:
          if ("".join(chat_input) == ""): continue
          dialog = player_name + ": " + "".join(chat_input)
          for i in range(0,len(dialog),35):
            client_socket.send(dialog[i:i+35].encode("utf-8"))
          chat_input = []
          input_color = (127, 127, 127)
          continue
        elif (not is_special_key(event.key)):
          input_color = (255, 255, 255)
          chat_input.append(event.unicode)

    #update display
    pygame.display.update()

  #exit pygame
  pygame.quit()
