# INSTRUCTION: Just need to change this path and can run game
import tkinter as tk
import pygame, sys, random, copy, time, collections, os
from pygame.locals import *
import json 
import os
import json
from tkinter import *
import time

PATH = os.path.dirname(os.path.abspath(__file__))

FPS = 144
WINDOWWIDTH = 1000
WINDOWHEIGHT = 570
BOXSIZE = 55
BOARDWIDTH = 14
BOARDHEIGHT = 9
NUMHEROES_ONBOARD = (BOARDWIDTH - 2) * (BOARDHEIGHT - 2) // 4
NUMSAMEHEROES = 4
XMARGIN = (WINDOWWIDTH - (BOXSIZE * BOARDWIDTH)) // 2
YMARGIN = (WINDOWHEIGHT - (BOXSIZE * BOARDHEIGHT)) // 2
TIMEBAR_LENGTH = 300
TIMEBAR_WIDTH = 30
LEVELMAX = 5
LIVES = random.randrange(5, 10, 1)
GAMETIME = random.randrange(240, 361, 10)
GETHINTTIME = 20

XMARGIN = (WINDOWWIDTH - (BOXSIZE * BOARDWIDTH)) // 2
YMARGIN = (WINDOWHEIGHT - (BOXSIZE * BOARDHEIGHT)) // 2

# set up the colors
GRAY = (100, 100, 100)
NAVYBLUE = ( 60, 60, 100)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = ( 0, 255, 0)
BOLDGREEN = (0, 175, 0)
BLUE = ( 0, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 128, 0)
PURPLE = (255, 0, 255)
CYAN = ( 0, 255, 255)
BLACK = (0, 0, 0)
BGCOLOR = NAVYBLUE
HIGHLIGHTCOLOR = BLUE
BORDERCOLOR = RED

# TIMEBAR setup
barPos = (WINDOWWIDTH // 2 - TIMEBAR_LENGTH // 2, YMARGIN // 2 - TIMEBAR_WIDTH // 2)
barSize = (TIMEBAR_LENGTH, TIMEBAR_WIDTH)
borderColor = WHITE
barColor = BOLDGREEN

# Make a dict to store scaled images
LISTHEROES = os.listdir(PATH + '/images_icon/Gen1/')
NUMHEROES = len(LISTHEROES)
HEROES_DICT = {}

for i in range(len(LISTHEROES)):
    HEROES_DICT[i + 1] = pygame.transform.scale(pygame.image.load('images_icon/Gen1/' + LISTHEROES[i]), (BOXSIZE, BOXSIZE))

def Mouse_on_button(surface, rect):
    x,y,w,h = rect
    gray_transparent = (128, 128, 128, 100)
    transparent_surface = pygame.Surface((WINDOWWIDTH, WINDOWHEIGHT), pygame.SRCALPHA)
    pygame.draw.rect(transparent_surface, gray_transparent, (x,y,w,h))
    surface.blit(transparent_surface, (0, 0))

class Button:
    def __init__(self, x, y, image, scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False

    def draw(self, surface):
        # Hiển thị nút
        surface.blit(self.image, (self.rect.x, self.rect.y))

    def is_clicked(self):
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos) and pygame.mouse.get_pressed()[0]:
            if not self.clicked:
                self.clicked = True
                return True
        if not pygame.mouse.get_pressed()[0]:
            self.clicked = False
        return False

# Load background
startBG = pygame.image.load('image_background/introduction_image.jpg')
startBG = pygame.transform.scale(startBG, (WINDOWWIDTH, WINDOWHEIGHT))

listBG = ['image_background/image_game_{}.jpg'.format(i) for i in range(1, 5)]
# for i in range(len(listBG)):
#     listBG[i] = pygame.transform.scale(listBG[i], (WINDOWWIDTH, WINDOWHEIGHT))

# Load sound and music
pygame.mixer.pre_init()
pygame.mixer.init()
clickSound = pygame.mixer.Sound('beep4.ogg')
getPointSound = pygame.mixer.Sound('beep1.ogg')
startScreenSound = pygame.mixer.Sound('music_background/introduction.wav')
listMusicBG = [f"music_background/music_{i}.mp3" for i in range(1, 5)]

def main(email):
    global FPSCLOCK, DISPLAYSURF, BASICFONT, LIVESFONT, LEVEL, BOARDWIDTH, BOARDHEIGHT, BOXSIZE, XMARGIN, YMARGIN, HEROES_DICT

    # Khởi tạo Pygame và các tài nguyên cơ bản
    pygame.init()
    pygame.font.init()
    # font = pygame.font.SysFont("Arial", 20)

    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption('Pikachu')
    BASICFONT = pygame.font.SysFont('comicsansms', 70)
    LIVESFONT = pygame.font.SysFont('comicsansms', 45)

    # Tính toán lề ban đầu dựa trên giá trị mặc định
    XMARGIN = (WINDOWWIDTH - (BOXSIZE * BOARDWIDTH)) // 2
    YMARGIN = (WINDOWHEIGHT - (BOXSIZE * BOARDHEIGHT)) // 2
    pygame.event.clear(pygame.MOUSEBUTTONUP)

    global savemenu
    savemenu = SaveMenu(DISPLAYSURF, email)
    
    while True:
        random.shuffle(listBG)
        random.shuffle(listMusicBG)
        LEVEL = 1

        # Hiển thị màn hình bắt đầu
        action = showStartScreen(email)
        pygame.event.clear(pygame.MOUSEBUTTONUP)  # Xóa sự kiện chuột sau khi nhận hành động

        # Hiển thị màn hình Option khi người chơi yêu cầu
        if action == "OPTION":
            new_board_width, new_board_height, new_box_size = showOptionScreen()

            # # Kiểm tra nếu giá trị thay đổi
            # if (new_board_width != BOARDWIDTH or 
            #     new_board_height != BOARDHEIGHT or 
            #     new_box_size != BOXSIZE):
            #     BOARDWIDTH, BOARDHEIGHT, BOXSIZE = new_board_width, new_board_height, new_box_size
            #     XMARGIN = (WINDOWWIDTH - (BOXSIZE * BOARDWIDTH)) // 2
            #     YMARGIN = (WINDOWHEIGHT - (BOXSIZE * BOARDHEIGHT)) // 2

            # # Tải lại hình ảnh sau khi thay đổi tùy chọn
            # load_heroes_images()

            pygame.event.clear(pygame.MOUSEBUTTONUP)  # Xóa sự kiện chuột sau khi đóng option
            continue  # Quay lại màn hình Start sau khi chỉnh Option

        # Xử lý hành động từ màn hình chính
        if action == "LOG OUT":
            return "LOG OUT"  # Trả về trạng thái LOG OUT cho ứng dụng
        
        #Ai làm phần game thì để ý chỗ này
        elif action == "NEW GAME":
            new_game_option = NewGameOption(DISPLAYSURF)
            new_game_option.appear()
            while new_game_option.visible:
                new_game_option.handle_event()
            if new_game_option.return_home:
                continue
            if new_game_option.size_choose <= 2:
                size = ((8,8), (16,9), (20,12))[new_game_option.size_choose]
            else:
                size = (int(new_game_option.col_text), int(new_game_option.row_text))
            saved_state = None
            load_heroes_images(f'Gen{new_game_option.gen_choose + 1}')
            
            
        elif action == "LOAD GAME":
            savemenu.page = 1
            savemenu.appear()
            while savemenu.visible:
                for event in pygame.event.get():
                    saved_state = savemenu.load(event)
            if not saved_state:
                pygame.event.clear(pygame.MOUSEBUTTONUP)  # Xóa sự kiện chuột nếu không có trạng thái lưu
                continue  # Nếu không có trạng thái lưu, quay lại màn hình chính

        # Vòng lặp chơi game
        while LEVEL <= LEVELMAX:
            if not saved_state:
                result = runGame(email, saved_state, new_game_option.level_choose, new_game_option.gen_choose, new_game_option.device_choose, size, listBG[0])
            else:
                result = runGame(email, saved_state, None, None, None, None, None)
            if result == "MAIN_MENU":  # Nếu quay về StartScreen
                pygame.event.clear()
                pygame.event.clear(pygame.MOUSEBUTTONUP)
                break
            LEVEL += 1
            pygame.time.wait(1000)

        # Kiểm tra nếu quay lại màn hình chính
        pygame.event.clear(pygame.MOUSEBUTTONUP)
        if result == "MAIN_MENU":
            pygame.event.clear()
            pygame.time.wait(100)  # Xóa sự kiện chuột khi quay lại màn hình chính
            continue

        # Hiển thị màn hình Game Over sau khi hoàn thành
        showGameOverScreen()
        pygame.event.clear(pygame.MOUSEBUTTONUP)  # Xóa sự kiện chuột sau Game Over
        
class RunningBox:
    def __init__(self):
        self.runningbox = pygame.transform.scale(pygame.image.load('images/runningbox.png'), (BOXSIZE + 2, BOXSIZE + 2))
        self.x = 1
        self.y = 1
        self.mode = 'normal'
    def draw(self):
        left, top = leftTopCoordsOfBox(self.x, self.y)
        runningboxRect = pygame.Rect(left, top, BOXSIZE, BOXSIZE)
        DISPLAYSURF.blit(self.runningbox, runningboxRect)
    def active(self):
        return self.x, self.y
    def move_left(self, mainBoard = None):
        if mainBoard:
            self.x -= 1
            while mainBoard[self.y][self.x] == 0:
                if self.x <= 0:
                    self.x = BOARDWIDTH - 1
                self.x -= 1
        else:
            self.x -= 1
            if self.x <= 0:
                self.x = BOARDWIDTH - 2
    def move_right(self, mainBoard):
        if mainBoard:
            self.x += 1
            while mainBoard[self.y][self.x] == 0:
                if self.x >= BOARDWIDTH - 1:
                    self.x = 0
                self.x += 1
        else:
            self.x += 1
            if self.x >= BOARDWIDTH - 1:
                self.x = 1
    def move_down(self, mainBoard = None):
        if mainBoard:
            self.y += 1
            while mainBoard[self.y][self.x] == 0:
                if self.y >= BOARDHEIGHT - 1:
                    self.y = 0
                self.y += 1
        else:
            self.y += 1
            if self.y >= BOARDHEIGHT - 1:
                self.y = 1
    def move_up(self, mainBoard = None):
        if mainBoard:
            self.y -= 1
            while mainBoard[self.y][self.x] == 0:
                if self.y <= 0:
                    self.y = BOARDHEIGHT - 1
                self.y -= 1
        else:
            self.y -= 1
            if self.y <= 0:
                self.y = BOARDHEIGHT - 2
    def find_nearest(self, mainBoard):
        while mainBoard[self.y][self.x] == 0:
            self.x -= 1
            if self.x <= 0:
                self.y -= 1
                if self.y <= 0:
                    self.y = BOARDHEIGHT - 1
                self.x = BOARDWIDTH - 1
        self.draw()

class NewGameOption:
    def __init__(self, screen):
        self.font = pygame.font.Font('font_pixel.otf', 25)
        self.fonts = pygame.font.Font('font_pixel.otf', 20)
        self.visible = False
        self.screen = screen
        self.is_draw = False
        self.drawing_pos = None
        self.size_choose = None
        self.gen_choose = None
        self.level_choose = None
        self.device_choose = None
        self.play_able = False
        self.row_text = ''
        self.col_text = ''
        self.col_active = False
        self.row_active = False

    def playable(self):
        for i in (self.size_choose, self.gen_choose, self.level_choose, self.device_choose):
            if i == None:
                return False
        return True

    def appear(self):
        self.visible = True
        self.return_home = False
        self.size_rects = []
        self.gen_rects = []
        self.level_rects = []
        self.device_rects = []
        nen = pygame.image.load('images/new_game_background.png')
        self.screen.blit(nen, (0, 0))
        size = ('8x8', '9x16', '12x20')
        x, y = 100, 65
        self.screen.blit(self.font.render('SIZE', True, RED), (x + 40, y))
        for i in range(3):
            y += 70
            if i == self.size_choose:
                color = BLUE
            else:
                color = BLACK
            pygame.draw.rect(self.screen, color, (x, y, 150, 60), 2)
            self.size_rects.append(pygame.Rect(x, y, 150, 60))
            self.screen.blit(self.font.render(size[i], True, BLACK), (x + 75 - self.font.render(size[i], True, BLACK).get_width()/2, y + 7)) 
        x, y = 400, 65
        self.screen.blit(self.font.render('GEN', True, RED), (x + 70, y))
        for i in range(2):
            y += 80
            x = 340
            for j in range(2):
                pygame.draw.rect(self.screen, BLUE if self.gen_choose == 2 * i + j else BLACK, (x, y, 150, 60), 2)
                self.gen_rects.append(pygame.Rect(x, y, 150, 60))
                self.screen.blit(self.font.render(f'GEN{i*2 + j + 1}', True, BLACK), (x + 75 - self.font.render(f'GEN{i*2 + j + 1}', True, BLACK).get_width()/2, y + 7))
                x += 170
        x, y = 775, 65
        self.screen.blit(self.font.render('LEVEL', True, RED), (x + 25, y))
        for i in range(5):
            y += 55
            color = BLUE if i == self.level_choose else BLACK
            pygame.draw.rect(self.screen, color, (x, y, 120, 40), 2)
            self.level_rects.append(pygame.Rect(x, y, 120, 40))
            self.screen.blit(self.font.render(f'{i + 1}', True, BLACK), (x + 65 - self.font.render(f'{i + 1}', True, BLACK).get_width()/2, y - 2))
        
        self.screen.blit(self.font.render('DEVICE:', True, RED), (730, 400))
        device = ('MOUSE', 'KEYBOARD')
        x, y = 470, 450
        for i in range(2):
            x += 155
            color = BLUE if i == self.device_choose else BLACK
            pygame.draw.rect(self.screen, color, (x, y, 150, 50), 2)
            self.device_rects.append(pygame.Rect(x, y, 150, 50))
            self.screen.blit(self.font.render(device[i], True, BLACK), (x + 75 - self.font.render(device[i], True, BLACK).get_width()/2, y + 5))
        x, y = 70, 400
        
        pygame.draw.rect(self.screen, BLUE if self.size_choose == 3 else BLACK, (x, y, 200, 100), 2)
        self.screen.blit(self.fonts.render('COL', True, RED), (x + 10, y + 10))
        pygame.draw.rect(self.screen, BLUE if self.col_active else GRAY, (x + 60, y + 15, 120, 30), 2)
        self.col_rect = pygame.Rect(x + 60, y + 15, 120, 30)
        self.screen.blit(self.fonts.render('ROW', True, RED), (x + 10, y + 50))
        pygame.draw.rect(self.screen, BLUE if self.row_active else GRAY, (x + 60, y + 55, 120, 30), 2)
        self.row_rect = pygame.Rect(x + 60, y + 55, 120, 30)
        self.size_rects.append(pygame.Rect(x, y, 200, 100))
        self.screen.blit(self.fonts.render(self.col_text, True, BLACK), (x + 90, y + 13))
        self.screen.blit(self.fonts.render(self.row_text, True, BLACK), (x + 90, y + 53))
        
        home_button = pygame.image.load('images/home_button.png')
        home_button = pygame.transform.scale(home_button, (50,50))
        self.home_button_rect = (pygame.Rect(930, 20, 50, 50),)
        self.screen.blit(home_button, (930, 20))
        
        pygame.draw.rect(self.screen, GRAY, (460, 510, 80, 40), 2)
        self.play_button_rect = (pygame.Rect(460, 510, 80, 40),)
        self.screen.blit(self.font.render('PLAY', True, RED if self.playable() else GRAY), (465, 500))
        pygame.display.update()
    
    def handle_event(self):
        for event in pygame.event.get():
            self.is_draw = False
            if event.type == MOUSEMOTION:
                mousepos = event.pos
                
                for index, rect in enumerate((self.size_rects, self.gen_rects, self.level_rects, self.device_rects, self.home_button_rect, self.play_button_rect)):
                    for i in rect:
                        if i.collidepoint(mousepos):
                            if self.is_draw is False:
                                if  i != self.drawing_pos:
                                    if index != 5 or self.playable():
                                        Mouse_on_button(DISPLAYSURF, i)
                                        
                                        self.drawing_pos = i
                                        pygame.display.update()
                                
                                self.is_draw = True
                                
                if self.is_draw == False:
                    self.drawing_pos = None
                    self.appear()
            elif event.type == MOUSEBUTTONUP:
                self.row_active = False
                self.col_active = False
                mousepos = event.pos
                for index, rect in enumerate((self.size_rects, self.gen_rects, self.level_rects, self.device_rects, self.home_button_rect, self.play_button_rect)):
                    for i, box in enumerate(rect):
                        if box.collidepoint(mousepos):
                            if index == 0:
                                self.size_choose = i
                                if i == 3:
                                    if self.row_rect.collidepoint(mousepos):
                                        self.row_active = True
                                    elif self.col_rect.collidepoint(mousepos):
                                        self.col_active = True
                            elif index == 1:
                                self.gen_choose = i
                            elif index == 2:
                                self.level_choose = i
                            elif index == 3:
                                self.device_choose = i
                            elif index == 4:
                                self.visible = False
                                self.return_home = True
                                return
                            elif index == 5:
                                if self.playable():
                                    self.visible = False
                                    self.return_home = False
                                    return 
                
                self.appear()
            elif event.type == pygame.KEYDOWN:
                if self.row_active:
                    if event.key == pygame.K_RETURN:
                        self.row_active = False
                    elif event.key == pygame.K_BACKSPACE:
                        self.row_text = self.row_text[:-1]
                    else:
                        new_index = str(event.unicode)
                        if new_index.isnumeric() and 0 < int(self.row_text + new_index) <= 20:
                            self.row_text += new_index
                elif self.col_active:
                    if event.key == pygame.K_RETURN:
                        self.col_active = False
                    elif event.key == pygame.K_BACKSPACE:
                        self.col_text = self.col_text[:-1]
                    else:
                        new_index = str(event.unicode)
                        if new_index.isnumeric() and 0 < int(self.col_text + new_index) <= 20:
                            self.col_text += new_index
                self.appear()
                                
                                
def showStartScreen(email):
    cur_rect = None
    pixel_font = pygame.font.Font('font_pixel.otf', 30)
    startScreenSound.play()
    pygame.event.clear()
    button_folder = 'images'
    new_game_button = pygame.image.load(f'{button_folder}/new_game_button.png')
    load_game_button = pygame.image.load(f'{button_folder}/load_game_button.png')
    rank_button = pygame.image.load(f'{button_folder}/rank_button.png')
    setting_button = pygame.image.load(f'{button_folder}/setting_button.png')
    log_out_button = pygame.image.load(f'{button_folder}/log_out_button.png')
    quit_game_button = pygame.image.load(f'{button_folder}/quit_game_button.png')
    buttons = [new_game_button, load_game_button, rank_button, setting_button, log_out_button, quit_game_button]
    buttons_rect = []
    y = 30
    for i in range(4):
        buttons_rect.append((240,y,buttons[i].get_width(), buttons[i].get_height()))
        y += buttons[i].get_height() + 20
    buttons_rect.append((WINDOWWIDTH - (buttons[4].get_width() + 30), 90, buttons[4].get_width(), buttons[4].get_height()))
    buttons_rect.append((265, 450, buttons[5].get_width(), buttons[5].get_height()))
    buttons_Rect = tuple(pygame.Rect(i[0], i[1], i[2], i[3]) for i in buttons_rect)
    DISPLAYSURF.blit(startBG, (0, 0))
    for i in range(6):
        DISPLAYSURF.blit(buttons[i], (buttons_rect[i][0], buttons_rect[i][1]))
    DISPLAYSURF.blit(pixel_font.render('Welcome:', True, BLACK), (WINDOWWIDTH - (buttons[4].get_width() + 30), 1))
    email_render = pixel_font.render(email, True, RED)
    if (email_render.get_width() / 2) <= 105:
        email_render_x = 895 - email_render.get_width() // 2
    else:
        email_render_x = 1000 - email_render.get_width()
    DISPLAYSURF.blit(email_render, (email_render_x, 35))
    while True:
        for event in pygame.event.get():
            is_drawed = False
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEMOTION:
                mouse_pos = event.pos
                for i, rect in enumerate(buttons_Rect):
                    if rect.collidepoint(mouse_pos):
                        if is_drawed == False:
                            if cur_rect != rect:
                                Mouse_on_button(DISPLAYSURF, rect)
                                cur_rect = rect
                        is_drawed = True
                if is_drawed == False:
                    DISPLAYSURF.blit(startBG, (0, 0))
                    cur_rect = None
                    for i in range(6):
                        DISPLAYSURF.blit(buttons[i], (buttons_rect[i][0], buttons_rect[i][1]))
                    DISPLAYSURF.blit(pixel_font.render('Welcome:', True, BLACK), (WINDOWWIDTH - (buttons[4].get_width() + 30), 1))
                    email_render = pixel_font.render(email, True, RED)
                    if (email_render.get_width() / 2) <= 105:
                        email_render_x = 895 - email_render.get_width() // 2
                    else:
                        email_render_x = 1000 - email_render.get_width()
                    DISPLAYSURF.blit(email_render, (email_render_x, 35))
            elif event.type == MOUSEBUTTONUP:
                pygame.event.clear(pygame.MOUSEBUTTONUP)  # Xóa sự kiện chuột còn lại trước khi xử lý
                mousex, mousey = event.pos
                for i, rect in enumerate(buttons_Rect):
                    if rect.collidepoint((mousex, mousey)):
                        if i == 0:  # NEW GAME
                            return "NEW GAME"
                        elif i == 1:  # CONTINUE
                            return "LOAD GAME"
                        elif i == 2:  # RANK
                            print("Rank selected")
                            import RANKSCREEN
                            RANKSCREEN.main()
                        elif i == 3:  # OPTION
                            showOptionScreen()
                            pygame.event.clear(pygame.MOUSEBUTTONUP)  # Xóa sự kiện chuột sau khi thoát khỏi OPTION
                        elif i == 4:  # LOG OUT
                            return "LOG OUT"
                        elif i == 5:  # QUIT
                            pygame.quit()
                            sys.exit()


        pygame.display.update()
        FPSCLOCK.tick(FPS)

def showOptionScreen():
    """Hiển thị màn hình cài đặt Option và lưu giữ các giá trị đã chọn."""
    options_running = True
    selected_generation = "Gen1"  # Mặc định là Gen1
    selected_size = "8x8"

    global BOARDWIDTH, BOARDHEIGHT, BOXSIZE  # Sử dụng các biến toàn cục để lưu trạng thái

    while options_running:
        DISPLAYSURF.fill(BLACK)  # Background for option screen
        title_font = pygame.font.SysFont('comicsansms', 70)
        small_font = pygame.font.SysFont('comicsansms', 40)

        # Tiêu đề màn hình Options
        title_surf = title_font.render("OPTIONS", True, WHITE)
        title_rect = title_surf.get_rect(center=(WINDOWWIDTH // 2, 100))
        DISPLAYSURF.blit(title_surf, title_rect)

        # Các lựa chọn cài đặt
        option_texts = [
            f"1. Generation: {selected_generation}",
            f"2. Size: {selected_size}",
            f"3. Box Size: {BOXSIZE}px",
            "Back"
        ]
        option_rects = []
        for i, text in enumerate(option_texts):
            option_surf = small_font.render(text, True, WHITE)
            option_rect = option_surf.get_rect(center=(WINDOWWIDTH // 2, 200 + i * 80))
            DISPLAYSURF.blit(option_surf, option_rect)
            option_rects.append(option_rect)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                for i, rect in enumerate(option_rects):
                    if rect.collidepoint((mousex, mousey)):
                        if i == 0:  # Generation Option
                            if selected_generation == "Gen1":
                                selected_generation = "Gen2"
                            elif selected_generation == "Gen2":
                                selected_generation = "Gen3"
                            else:
                                selected_generation = "Gen1"
                        elif i == 1:  # Size Option
                            if selected_size == "8x8":
                                selected_size = "12x10"
                            elif selected_size == "12x10":
                                selected_size = "12x7"
                            else:
                                selected_size = "8x8"

                            # Cập nhật kích thước bảng dựa trên lựa chọn
                            if selected_size == "8x8":
                                BOARDWIDTH, BOARDHEIGHT = 10, 10
                            elif selected_size == "12x10":
                                BOARDWIDTH, BOARDHEIGHT = 14, 12
                            elif selected_size == "12x7":
                                BOARDWIDTH, BOARDHEIGHT = 14, 9
                        elif i == 2:  # Box Size Option
                            if BOXSIZE == 40:
                                BOXSIZE = 50
                            elif BOXSIZE == 50:
                                BOXSIZE = 30
                            else:
                                BOXSIZE = 40
                        elif i == 3:  # Back
                            options_running = False

        pygame.display.update()
        FPSCLOCK.tick(FPS)

    # Tải lại hình ảnh từ Generation đã chọn
    load_heroes_images(selected_generation)

    # Trả về các giá trị Board size đã chọn
    return BOARDWIDTH, BOARDHEIGHT, BOXSIZE

def load_heroes_images(gen_folder):
    """Tải danh sách ảnh từ thư mục tương ứng với Gen."""
    global HEROES_DICT, LISTHEROES, NUMHEROES, BOXSIZE
    path = PATH + f'/images_icon/{gen_folder}/'
    if not os.path.exists(path):
        raise FileNotFoundError(f"Folder {path} không tồn tại!")

    LISTHEROES = os.listdir(path)
    NUMHEROES = len(LISTHEROES)
    HEROES_DICT = {}

    for i in range(len(LISTHEROES)):
        HEROES_DICT[i + 1] = pygame.transform.scale(
            pygame.image.load(path + LISTHEROES[i]),
            (BOXSIZE, BOXSIZE)
        )
    print(f"Loaded {NUMHEROES} heroes from {gen_folder}.")

def runGame(email, saved_state, level, gen, device, size, randomBG):

    
    global font
    font = pygame.font.Font('font_pixel.otf', 30)

    # Tải trạng thái hoặc khởi tạo mặc định
    # saved_state = load_game_state(email)
    global mainBoard, LEVEL, LIVES, GAMETIME, TIMEBONUS, STARTTIME, lastTimeGetPoint, hint, mainBoard, firstSelection, clickedBoxes

    settings = Settings(DISPLAYSURF)
    
    settings.save_callback = lambda: save_game_state(settings, email, mainBoard, LEVEL, LIVES, GAMETIME, TIMEBONUS, STARTTIME, BG, gen, device, size)

    # Thêm cờ để báo hiệu quay về StartScreen
    restart_flag = False

    # Callback cho nút Main Menu trong Settings
    def go_to_main_menu():
        nonlocal restart_flag
        restart_flag = True
        settings.visible = False  # Đóng Settings
        pygame.event.clear(pygame.MOUSEBUTTONUP)

    settings.quit_callback = lambda: sys.exit()
    settings.main_menu_callback = go_to_main_menu
    
    def logic_game(boxx, boxy, mouseClicked, enterPress):
        global TIMEBONUS, lastTimeGetPoint, hint, mainBoard, firstSelection, clickedBoxes
        # Phần logic game
        if (
            boxx is not None and boxy is not None
            and 0 <= boxy < len(mainBoard)
            and 0 <= boxx < len(mainBoard[boxy])
            and mainBoard[boxy][boxx] != 0
        ):
            drawHighlightBox(mainBoard, boxx, boxy)  # Vẽ khung nổi bật quanh ô
            if mouseClicked or enterPress:
                # Nếu ô chưa được click, thêm vào danh sách clickedBoxes
                if (boxx, boxy) not in clickedBoxes:
                    clickedBoxes.append((boxx, boxy))
                drawBoard(mainBoard, clickedBoxes)  # Vẽ lại bảng với hiệu ứng nhạt màu
                pygame.display.update()  # Cập nhật màn hình

                if firstSelection is None:  # Lần click đầu tiên
                    firstSelection = (boxx, boxy)
                    clickSound.play()
                else:  # Lần click thứ hai
                    path = bfs(mainBoard, firstSelection[1], firstSelection[0], boxy, boxx)
                    if path:  # Nếu tìm được đường nối
                        getPointSound.play()
                        mainBoard[firstSelection[1]][firstSelection[0]] = 0
                        mainBoard[boxy][boxx] = 0
                        
                        drawPath(mainBoard, path)
                        TIMEBONUS += 1
                        lastTimeGetPoint = time.time()
                        mainBoard = alterBoardWithLevel(mainBoard, firstSelection[1], firstSelection[0], boxy, boxx, LEVEL)
                        hint = getHint(mainBoard)

                        if isGameComplete(mainBoard):
                            # drawBoard(mainBoard)
                            # pygame.display.update()
                            return "WIN"
                    else:  # Nếu không tìm được đường nối
                        clickSound.play()

                    # Reset trạng thái sau lần click thứ hai
                    clickedBoxes = []
                    firstSelection = None
    
    global BOARDHEIGHT, BOARDWIDTH, XMARGIN, YMARGIN, BOXSIZE
    size = saved_state["size"] if saved_state else size
    BOARDWIDTH, BOARDHEIGHT = size[0] + 2, size[1] + 2
    BOXSIZE = min(800 // BOARDWIDTH, 500 // BOARDHEIGHT)
    XMARGIN = (WINDOWWIDTH - (BOXSIZE * BOARDWIDTH)) // 2
    YMARGIN = (WINDOWHEIGHT - (BOXSIZE * BOARDHEIGHT)) // 2
    
    
    if saved_state:
        name = saved_state["name"]
        mainBoard = saved_state["board"]
        LEVEL = saved_state["level"]
        LIVES = saved_state["lives"]
        GAMETIME = saved_state["game_time"]
        TIMEBONUS = saved_state["time_bonus"]
        STARTTIME = time.time() - saved_state["start_time"] #Thời gian đã tốn
        BG = saved_state["bg"]
        device = saved_state["device"]
        gen = saved_state["gen"]
    else:
        name = None
        mainBoard = getRandomizedBoard()
        LEVEL = level
        LIVES = 3
        TIMEBONUS = 0
        STARTTIME = time.time()
        BG = randomBG
        device = device
        gen = gen
    load_heroes_images(f'Gen{int(gen) + 1}')


    Background = pygame.image.load(BG)
    Background = pygame.transform.scale(Background, (WINDOWWIDTH, WINDOWHEIGHT))
    clickedBoxes = []
    firstSelection = None
    mousex, mousey = 0, 0
    lastTimeGetPoint = time.time()
    hint = getHint(mainBoard)

    # randomBG = listBG[LEVEL - 1]
    randomMusicBG = listMusicBG[LEVEL - 1]
    pygame.mixer.music.load(randomMusicBG)
    pygame.mixer.music.play(-1, 0.0)
    running_box = RunningBox()
    while not restart_flag:  # Vòng lặp chính sẽ thoát khi restart_flag được bật
        mouseClicked = False
        enterPress = False
        # Vòng lặp sự kiện
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            # Chuyển sự kiện tới Settings
            settings.handle_event(event)

            # Nếu menu Settings mở, bỏ qua logic game
            if settings.visible:
                continue

            if time.time() - settings.last_close_time < 0.2:
                continue
            # Xử lý sự kiện game
            if event.type == MOUSEMOTION:
                mousex, mousey = event.pos
            elif event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                if device == 0:
                    mouseClicked = True
            elif event.type == KEYUP:
                # while event.type == KEYDOWN:
                #     pass
                if event.key == pygame.K_a:
                    running_box.move_left(mainBoard if running_box.mode == 'normal' else None)
                elif event.key == pygame.K_d:
                    running_box.move_right(mainBoard if running_box.mode == 'normal' else None)
                elif event.key == pygame.K_w:
                    running_box.move_up(mainBoard if running_box.mode == 'normal' else None)
                elif event.key == pygame.K_s:
                    running_box.move_down(mainBoard if running_box.mode == 'normal' else None)
                elif event.key in (pygame.K_LSHIFT, pygame.K_RSHIFT):
                    running_box.mode = 'pass' if running_box.mode == 'normal' else 'normal'
                    curx, cury = running_box.active()
                    if mainBoard[cury][curx] == 0:
                        running_box.find_nearest(mainBoard)
                elif event.key == pygame.K_RETURN:
                    enterPress = True
                print(running_box.x, running_box.y)

        # Nếu Settings bị đóng, xóa các sự kiện chuột dư thừa
        if not settings.visible and mouseClicked:
            pygame.event.clear(pygame.MOUSEBUTTONUP)  # Xóa sự kiện chuột dư thừa
        # Vẽ nền và các thành phần chính
        if settings.start_pause:
            STARTTIME += time.time() - settings.start_pause
            lastTimeGetPoint += time.time() - settings.start_pause
            settings.start_pause = None
        DISPLAYSURF.blit(Background, (0, 0))
        drawBoard(mainBoard)
        drawClickedBox(mainBoard, clickedBoxes)
        drawTimeBar()
        drawInfo(name, device, gen, level, size)
        # drawLives()
        # Kiểm tra thời gian hoặc trạng thái game
        if not settings.visible:
            settings.draw()
            ###
            if time.time() - STARTTIME > GAMETIME + TIMEBONUS:
                LEVEL = LEVELMAX + 1
                return
            if time.time() - lastTimeGetPoint >= GETHINTTIME:
                drawHint(hint)
            if device == 0:
                boxx, boxy = getBoxAtPixel(mousex, mousey)
                
            else:
                running_box.draw()
                boxx, boxy = running_box.active()
            logic_game(boxx, boxy, mouseClicked, enterPress)
                
        # Vẽ menu Settings nếu mở
        settings.draw()
    
        pygame.display.update()
        FPSCLOCK.tick(FPS)

    pygame.mixer.music.stop()
    pygame.event.clear(pygame.MOUSEBUTTONUP)
    pygame.event.clear()
    return "MAIN_MENU" 

#Lưu game và load game
def save_game_state(settings, email, mainBoard, LEVEL, LIVES, GAMETIME, TIMEBONUS, STARTTIME, BG, gen, device, size):
    """Lưu trạng thái hiện tại của trò chơi vào tệp JSON cho tài khoản cụ thể."""

    savemenu.page = 1
    savemenu.appear()
    while True:
        for event in pygame.event.get():
            savemenu.save(event, mainBoard, LEVEL, LIVES, GAMETIME, TIMEBONUS, STARTTIME, BG, gen, device, size)
        if savemenu.visible == False:
            settings.appear_again = True
            break

def drawInfo(name, device, gen, level, size):
    name_render = font.render(name if name else 'NO NAME MAP', True, BLUE if name else RED)
    DISPLAYSURF.blit(name_render, (500 - name_render.get_width() / 2,20))
    DISPLAYSURF.blit(font.render(f'Map size: {size[0]}x{size[1]}', True, RED), (50, 500))
    delta_x = font.render(f'Map size: {size[0]}x{size[1]}', True, RED).get_width()
    DISPLAYSURF.blit(font.render(f'Device: {'MOUSE' if device == 0 else 'KEYBOARD'}', True, RED), (50 + delta_x + 20, 500))
    delta_x += font.render(f'Device: {'MOUSE' if device == 0 else 'KEYBOARD'}', True, RED).get_width() + 20
    DISPLAYSURF.blit(font.render(f'Gen: {gen}', True, RED), (50 + delta_x + 20, 500))
    delta_x += font.render(f'Gen: {gen}', True, RED).get_width() + 20
    DISPLAYSURF.blit(font.render(f'Level: {level}', True, RED), (50 + delta_x + 20, 500))

def getRandomizedBoard():
    k_max = (BOARDHEIGHT - 2)*(BOARDWIDTH - 2)
    for i in range(2,k_max,2):
        if k_max // i <= len(HEROES_DICT):
            break
    NUMSAMEHEROES = i
    NUMHEROES_ONBOARD = (BOARDWIDTH - 2) * (BOARDHEIGHT - 2) // NUMSAMEHEROES
    list_pokemons = list(range(1, len(HEROES_DICT) + 1))
    random.shuffle(list_pokemons)
    list_pokemons = list_pokemons[:NUMHEROES_ONBOARD] * NUMSAMEHEROES
    random.shuffle(list_pokemons)
    board = [[0 for _ in range(BOARDWIDTH)] for _ in range(BOARDHEIGHT)]
    # We create a board of images surrounded by 4 arrays of zeroes
    k = 0
    for i in range(1, BOARDHEIGHT - 1):
        for j in range(1, BOARDWIDTH - 1):
            board[i][j] = list_pokemons[k]
            k += 1
    return board

def leftTopCoordsOfBox(boxx, boxy):
    left = boxx * BOXSIZE + XMARGIN
    top = boxy * BOXSIZE + YMARGIN
    return left, top

def getBoxAtPixel(x, y):
    if x <= XMARGIN or x >= WINDOWWIDTH - XMARGIN or y <= YMARGIN or y >= WINDOWHEIGHT - YMARGIN:
        return None, None
    return (x - XMARGIN) // BOXSIZE, (y - YMARGIN) // BOXSIZE

def drawBoard(board, clickedBoxes=[]):
    for boxx in range(len(board[0])):
        for boxy in range(len(board)):
            left, top = leftTopCoordsOfBox(boxx, boxy)
            if board[boxy][boxx] != 0:  # Nếu ô không trống
                DISPLAYSURF.blit(HEROES_DICT[board[boxy][boxx]], (left, top))
                
                # Áp dụng hiệu ứng nhạt màu nếu ô nằm trong clickedBoxes
                if (boxx, boxy) in clickedBoxes:
                    s = pygame.Surface((BOXSIZE, BOXSIZE))
                    s.set_alpha(100)  # Đặt độ trong suốt (0-255)
                    s.fill((255, 255, 255))  # Phủ màu trắng nhạt
                    DISPLAYSURF.blit(s, (left, top))

def drawHighlightBox(board, boxx, boxy):
    # Lấy tọa độ góc trên bên trái của ô
    left, top = leftTopCoordsOfBox(boxx, boxy)
    
    # Vẽ một khung chữ nhật màu đỏ đậm quanh ô (highlight)
    pygame.draw.rect(DISPLAYSURF, HIGHLIGHTCOLOR, 
                     (left - 2, top - 2, BOXSIZE + 4, BOXSIZE + 4), 4)  # Độ dày 4 pixel

def drawClickedBox(board, clickedBoxes):
    for boxx, boxy in clickedBoxes:
        left, top = leftTopCoordsOfBox(boxx, boxy)
        boxRect = pygame.Rect(left, top, BOXSIZE, BOXSIZE)
        image = HEROES_DICT[board[boxy][boxx]].copy()

        # Kiểm tra xem ảnh có alpha channel không, nếu chưa có thì thêm
        if image.get_alpha() is None:  
            image = image.convert_alpha()  # Chuyển ảnh sang RGBA nếu cần

        # Tối màu ảnh khi click
        image.fill((60, 60, 60), special_flags=pygame.BLEND_RGB_SUB)  # Tối ảnh
        DISPLAYSURF.blit(image, boxRect)

def bfs(board, boxy1, boxx1, boxy2, boxx2):
    def backtrace(parent, boxy1, boxx1, boxy2, boxx2):
        start = (boxy1, boxx1, 0, 'no_direction')
        end = 0
        for node in parent:
            if node[:2] == (boxy2, boxx2):
                end = node

        path = [end]
        while path[-1] != start:
            path.append(parent[path[-1]])
        path.reverse()

        for i in range(len(path)):
            path[i] = path[i][:2]
        return path

    if board[boxy1][boxx1] != board[boxy2][boxx2]:
        return []

    n = len(board)
    m = len(board[0])

    import collections
    q = collections.deque()
    q.append((boxy1, boxx1, 0, 'no_direction'))
    visited = set()
    visited.add((boxy1, boxx1, 0, 'no_direction'))
    parent = {}

    while len(q) > 0:
        r, c, num_turns, direction = q.popleft()
        if (r, c) != (boxy1, boxx1) and (r, c) == (boxy2, boxx2):
            return backtrace(parent, boxy1, boxx1, boxy2, boxx2)

        dict_directions = {(r + 1, c): 'down', (r - 1, c): 'up', (r, c - 1): 'left',
                           (r, c + 1): 'right'}
        for neiborX, neiborY in dict_directions:
            next_direction = dict_directions[(neiborX, neiborY)]
            if 0 <= neiborX <= n - 1 and 0 <= neiborY <= m - 1 and (
                    board[neiborX][neiborY] == 0 or (neiborX, neiborY) == (boxy2, boxx2)):
                if direction == 'no_direction':
                    q.append((neiborX, neiborY, num_turns, next_direction))
                    visited.add((neiborX, neiborY, num_turns, next_direction))
                    parent[(neiborX, neiborY, num_turns, next_direction)] = (
                    r, c, num_turns, direction)
                elif direction == next_direction and (
                        neiborX, neiborY, num_turns, next_direction) not in visited:
                    q.append((neiborX, neiborY, num_turns, next_direction))
                    visited.add((neiborX, neiborY, num_turns, next_direction))
                    parent[(neiborX, neiborY, num_turns, next_direction)] = (
                    r, c, num_turns, direction)
                elif direction != next_direction and num_turns < 2 and (
                        neiborX, neiborY, num_turns + 1, next_direction) not in visited:
                    q.append((neiborX, neiborY, num_turns + 1, next_direction))
                    visited.add((neiborX, neiborY, num_turns + 1, next_direction))
                    parent[
                        (neiborX, neiborY, num_turns + 1, next_direction)] = (
                    r, c, num_turns, direction)
    return []

def getCenterPos(pos):
    left, top = leftTopCoordsOfBox(pos[1], pos[0])
    return tuple([left + BOXSIZE // 2, top + BOXSIZE // 2])

def drawPath(board, path):
    for i in range(len(path) - 1):
        startPos = getCenterPos(path[i])
        endPos = getCenterPos(path[i + 1])
        pygame.draw.line(DISPLAYSURF, RED, startPos, endPos, 4)
    pygame.display.update()
    pygame.time.wait(300)

def drawTimeBar():
    progress = 1 - ((time.time() - STARTTIME - TIMEBONUS) / GAMETIME)

    pygame.draw.rect(DISPLAYSURF, borderColor, (barPos, barSize), 1)
    innerPos = (barPos[0] + 2, barPos[1] + 2)
    innerSize = ((barSize[0] - 4) * progress, barSize[1] - 4)
    pygame.draw.rect(DISPLAYSURF, barColor, (innerPos, innerSize))

def showGameOverScreen():
    playAgainFont = pygame.font.Font('freesansbold.ttf', 50)
    playAgainSurf = playAgainFont.render('Play Again?', True, PURPLE)
    playAgainRect = playAgainSurf.get_rect()
    playAgainRect.center = (WINDOWWIDTH // 2, WINDOWHEIGHT // 2)
    DISPLAYSURF.blit(playAgainSurf, playAgainRect)
    pygame.draw.rect(DISPLAYSURF, PURPLE, playAgainRect, 4)
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                if playAgainRect.collidepoint((mousex, mousey)):
                    return

def getHint(board):
    boxPokesLocated = collections.defaultdict(list)
    hint = []
    for boxy in range(BOARDHEIGHT):
        for boxx in range(BOARDWIDTH):
            if board[boxy][boxx] != 0:
                boxPokesLocated[board[boxy][boxx]].append((boxy, boxx))
    for boxy in range(BOARDHEIGHT):
        for boxx in range(BOARDWIDTH):
            if board[boxy][boxx] != 0:
                for otherBox in boxPokesLocated[board[boxy][boxx]]:
                    if otherBox != (boxy, boxx) and bfs(board, boxy, boxx, otherBox[0], otherBox[1]):
                        hint.append((boxy, boxx))
                        hint.append(otherBox)
                        return hint
    return []

def drawHint(hint):
    for boxy, boxx in hint:
        left, top = leftTopCoordsOfBox(boxx, boxy)
        pygame.draw.rect(DISPLAYSURF, GREEN, (left, top,
                                                       BOXSIZE, BOXSIZE), 2)

def resetBoard(board):
    pokesOnBoard = []
    for boxy in range(BOARDHEIGHT):
        for boxx in range(BOARDWIDTH):
            if board[boxy][boxx] != 0:
                pokesOnBoard.append(board[boxy][boxx])
    referencedList = pokesOnBoard[:]
    while referencedList == pokesOnBoard:
        random.shuffle(pokesOnBoard)

    i = 0
    for boxy in range(BOARDHEIGHT):
        for boxx in range(BOARDWIDTH):
            if board[boxy][boxx] != 0:
                board[boxy][boxx] = pokesOnBoard[i]
                i += 1
    return board

def isGameComplete(board):
    for boxy in range(BOARDHEIGHT):
        for boxx in range(BOARDWIDTH):
            if board[boxy][boxx] != 0:
                return False
    return True

def alterBoardWithLevel(board, boxy1, boxx1, boxy2, boxx2, level):

    # Level 2: All the pokemons move up to the top boundary
    if level == 2:
        for boxx in (boxx1, boxx2):
            # rearrange pokes into a current list
            cur_list = [0]
            for i in range(BOARDHEIGHT):
                if board[i][boxx] != 0:
                    cur_list.append(board[i][boxx])
            while len(cur_list) < BOARDHEIGHT:
                cur_list.append(0)

            # add the list into the board
            j = 0
            for num in cur_list:
                board[j][boxx] = num
                j += 1

    # Level 3: All the pokemons move down to the bottom boundary
    if level == 3:
        for boxx in (boxx1, boxx2):
            # rearrange pokes into a current list
            cur_list = []
            for i in range(BOARDHEIGHT):
                if board[i][boxx] != 0:
                    cur_list.append(board[i][boxx])
            cur_list.append(0)
            cur_list = [0] * (BOARDHEIGHT - len(cur_list)) + cur_list

            # add the list into the board
            j = 0
            for num in cur_list:
                board[j][boxx] = num
                j += 1

    # Level 4: All the pokemons move left to the left boundary
    if level == 4:
        for boxy in (boxy1, boxy2):
            # rearrange pokes into a current list
            cur_list = [0]
            for i in range(BOARDWIDTH):
                if board[boxy][i] != 0:
                    cur_list.append(board[boxy][i])
            while len(cur_list) < BOARDWIDTH:
                cur_list.append(0)

            # add the list into the board
            j = 0
            for num in cur_list:
                board[boxy][j] = num
                j += 1

    # Level 5: All the pokemons move right to the right boundary
    if level == 5:
        for boxy in (boxy1, boxy2):
            # rearrange pokes into a current list
            cur_list = []
            for i in range(BOARDWIDTH):
                if board[boxy][i] != 0:
                    cur_list.append(board[boxy][i])
            cur_list.append(0)
            cur_list = [0] * (BOARDWIDTH - len(cur_list)) + cur_list

            # add the list into the board
            j = 0
            for num in cur_list:
                board[boxy][j] = num
                j += 1

    return board

# def drawLives():
#     aegisRect = pygame.Rect(10, 10, BOXSIZE, BOXSIZE)
#     # DISPLAYSURF.blit(aegis, aegisRect)
#     livesSurf = LIVESFONT.render(str(LIVES), True, WHITE)
#     livesRect = livesSurf.get_rect()
#     livesRect.topleft = (65, 0)
#     DISPLAYSURF.blit(livesSurf, livesRect)

class SaveMenu:
    def __init__(self, screen, email):
        self.visible = False
        self.screen = screen
        self.height = WINDOWHEIGHT
        self.width = WINDOWWIDTH
        self.memory_rects = ((50 , 100, 250, 142), (375 , 100, 250, 142), (700 , 100, 250, 142), (50 , 300, 250, 142), (375 , 300, 250, 142), (700 , 300, 250, 142))
        self.maxpage = 3
        self.page = 1
        self.memories = [None for _ in range(6 * self.maxpage)]
        self.memory_boxes = []
        for i in range(6):
            x,y,w,h = self.memory_rects[i]
            self.memory_boxes.append(pygame.Rect(x,y,w,h))
        self.memory_boxes = tuple(self.memory_boxes)
        self.delete_rects = [None for _ in range(6)]
        self.email = email
        self.is_delete = False
        pygame.font.init()
        self.font = pygame.font.Font('font_pixel.otf', 25)
        self.fonts = pygame.font.Font('font_pixel.otf', 20)
        self.next_page = pygame.image.load('images/next_page.png')
        self.next_page = pygame.transform.scale(self.next_page, (50,50))
        self.next_page_rect = pygame.Rect(600, 505,50,50)
        self.prev_page = pygame.image.load('images/previous_page.png')
        self.prev_page = pygame.transform.scale(self.prev_page, (50,50))
        self.prev_page_rect = pygame.Rect(350, 505, 50, 50)
        self.is_drawed = False
        self.cur_rect = None
    def appear(self):
        self.visible = True
        self.BG = pygame.image.load('images/savemenu.png')
        self.BG = pygame.transform.scale(self.BG, (WINDOWWIDTH, WINDOWHEIGHT))
        self.screen.blit(self.BG, (0,0))
        with open(os.path.join("saves", f"{self.email}_saved_game.json"), "r") as save_file:
            saved_game = json.load(save_file)
            self.memories = [None for _ in range(6 * self.maxpage)]
            for i in saved_game:
                self.memories[int(i)] = f'saves/{self.email}_saved{i}.png'
        for i in range(6):
            x,y,w,h = self.memory_rects[i]
            pygame.draw.rect(self.screen, GRAY, pygame.Rect(x,y,w,h), border_radius=1)
        delete_icon = pygame.image.load('images/delete.png')
        delete_icon = pygame.transform.scale(delete_icon, (50,50))
        self.delete_rects = [None for _ in range(6)]
        for i in range(6 * (self.page - 1), 6 * self.page):
            if self.memories[i]:
                image = pygame.image.load(self.memories[i])
                image = pygame.transform.scale(image, (248,140))
                self.screen.blit(image, (self.memory_rects[i % 6][0] + 1, self.memory_rects[i % 6][1] + 1))
                delete_icon_rect = delete_icon.get_rect()
                delete_icon_rect.topleft = (self.memory_rects[i % 6][0], self.memory_rects[i % 6][1])
                self.screen.blit(delete_icon, delete_icon_rect)
                self.delete_rects[i % 6] = delete_icon_rect
                map_name = self.font.render(saved_game[str(i)]['name'], True, BLACK)
                self.screen.blit(map_name, (self.memory_rects[i % 6][0] + 125 - map_name.get_width()/2, self.memory_rects[i % 6][1] + 140))
        for i in range(6 * (self.page - 1), 6 * self.page):
            if self.memories[i]:
                color = RED
            else:
                color = BLACK
            number = self.font.render(str(i + 1), True, color)
            self.screen.blit(number, (self.memory_rects[i % 6][0] + 110, self.memory_rects[i % 6][1] + 50))
        if self.page > 1:
            self.screen.blit(self.prev_page, (350, 505))
        if self.page < self.maxpage:
            self.screen.blit(self.next_page, (600, 505))
                
        self.out = pygame.Rect(880,500,100,50)
        pygame.draw.rect(self.screen, BLUE, pygame.Rect(880,500,100,50))
        self.screen.blit(self.fonts.render('Home', True, BLACK), (900, 505))
        pygame.display.flip()
    
    def save(self, event,mainBoard, LEVEL, LIVES, GAMETIME, TIMEBONUS, STARTTIME, BG, gen, device, size):
        # Đảm bảo thư mục lưu trữ game tồn tại
        save_folder = "saves"
        if not os.path.exists(save_folder):
            os.makedirs(save_folder)
        temp_image = pygame.image.load('saves/temporary.png')
        delete_icon = pygame.image.load('images/delete.png')
        delete_icon = pygame.transform.scale(delete_icon, (50,50))
        if event.type == pygame.MOUSEMOTION:
            self.mouse_on(event)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            for i, box in enumerate(self.memory_boxes):
                if self.delete_rects[i] and self.delete_rects[i].collidepoint(mouse_pos):
                    
                    self.delete(i + (self.page - 1) * 6)
                    
                elif box and box.collidepoint(mouse_pos):
                    enter_map_name = EnterMapName(250, 160, 500, 250, DISPLAYSURF)
                    map_name = None
                    while not map_name:
                        map_name =  enter_map_name.appear()
                        if enter_map_name.visible == False:
                            break
                    if enter_map_name.visible:
                        pygame.image.save(temp_image, f'saves/{self.email}_saved{i + (self.page - 1) * 6}.png')
                        self.memories[i + (self.page - 1) * 6] = f'saves/{self.email}_saved{i + (self.page - 1) * 6}.png'
                        image = pygame.transform.scale(temp_image, (248,140))
                        self.screen.blit(image, (self.memory_rects[i][0] + 1, self.memory_rects[i][1] + 1))
                        delete_icon_rect = delete_icon.get_rect()
                        delete_icon_rect.topleft = (self.memory_rects[i][0], self.memory_rects[i][1])
                        self.delete_rects[i] = delete_icon_rect
                        self.screen.blit(delete_icon, delete_icon_rect)
                        pygame.display.flip()
                        
                        with open(f'saves/{self.email}_saved_game.json', 'r', encoding='utf_8', ) as file:
                            try:
                                game_state = json.load(file)
                            except:
                                game_state = {}
                                json.dump(game_state, file)
                        game_state[i + (self.page - 1) * 6] = {
                        "name": map_name,
                        "bg": BG,
                        "size":size,
                        "gen": gen,
                        "device":device,
                        "board": mainBoard,
                        "level": LEVEL,
                        "lives": LIVES,
                        "game_time": GAMETIME,
                        "time_bonus": TIMEBONUS,
                        "start_time": time.time() - STARTTIME  # Thời gian đã trôi qua
                    }
                        with open(f'saves/{self.email}_saved_game.json', "w") as save_file:
                            json.dump(game_state, save_file, indent=4)
                        self.appear()
                    else:
                        self.appear()
            if self.out.collidepoint(mouse_pos):
                self.visible = False
            if self.next_page_rect.collidepoint(mouse_pos) and self.page < self.maxpage:
                while pygame.event.get() == MOUSEBUTTONDOWN:
                    pass
                self.page += 1
                self.appear()
                if self.page < self.maxpage:
                    Mouse_on_button(self.screen, self.next_page_rect)
                pygame.display.update()
            if self.prev_page_rect.collidepoint(mouse_pos) and self.page > 1:
                while pygame.event.get() == MOUSEBUTTONDOWN:
                    pass
                self.page -= 1
                self.appear()
                if self.page > 0:
                    Mouse_on_button(self.screen, self.prev_page_rect)
                pygame.display.update()
        
    def mouse_on(self, event):
        mouse_pos = event.pos
        self.is_drawed = False
        for i, box in enumerate(self.memory_boxes):
            if self.delete_rects[i] and self.delete_rects[i].collidepoint(mouse_pos):
                if self.is_drawed == False:
                    if self.cur_rect != self.delete_rects[i]:
                        if self.cur_rect == box:
                            self.appear()
                        Mouse_on_button(self.screen, self.delete_rects[i])
                        self.cur_rect = self.delete_rects[i]
                self.is_drawed = True
            elif box and box.collidepoint(mouse_pos):
                if self.is_drawed == False:
                    if self.cur_rect != box:
                        if self.cur_rect == self.delete_rects[i]:
                            self.appear()
                        Mouse_on_button(self.screen, box)
                        self.cur_rect = box
                self.is_drawed = True
        if self.out.collidepoint(mouse_pos):
            if self.is_drawed == False:
                if self.cur_rect != self.out:
                    Mouse_on_button(self.screen, self.out)
                    self.cur_rect = self.out
            self.is_drawed = True
        if self.next_page_rect.collidepoint(mouse_pos):
            if self.page < self.maxpage:
                if self.is_drawed == False:
                    if self.cur_rect != self.next_page_rect:
                        Mouse_on_button(self.screen, self.next_page_rect)
                        self.cur_rect = self.next_page_rect
                self.is_drawed = True
        if self.prev_page_rect.collidepoint(mouse_pos):
            if self.page > 1:
                if self.is_drawed == False:
                    if self.cur_rect != self.prev_page_rect:
                        Mouse_on_button(self.screen, self.prev_page_rect)
                        self.cur_rect = self.prev_page_rect
                self.is_drawed = True
        if self.is_drawed == False:
            self.appear()
            self.cur_rect = None
        pygame.display.update()
    def delete(self, i):
        self.is_delete = True
        self.memories[i] = None
        self.delete_rects[i % 6] = None
        with open(os.path.join("saves", f"{self.email}_saved_game.json"), 'r') as save_file:
            saved_game = json.load(save_file)
            del saved_game[str(i)]
        with open(os.path.join("saves", f"{self.email}_saved_game.json"), 'w') as save_file:
            json.dump(saved_game, save_file, indent=4)
            print('len',len(saved_game))
        os.remove(f'saves/{self.email}_saved{i}.png')
        self.appear()
                    
    def load(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.mouse_on(event)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos 
            for i, box in enumerate(self.memory_boxes):
                 
                if self.delete_rects[i] and self.delete_rects[i].collidepoint(mouse_pos):
                    self.delete(i + (self.page - 1) * 6)
                    return None
                elif box and box.collidepoint(mouse_pos):
                    print('aaa')
                    save_file_path = os.path.join("saves", f"{self.email}_saved_game.json")
                    print('bbb')
                    with open(save_file_path, "r") as save_file:
                        saved_game = json.load(save_file)
                        if not saved_game or len(saved_game) == 0:
                            continue
                        if str(i + (self.page - 1) * 6) not in saved_game:
                            continue
                        self.visible = False
                        return saved_game[str(i + (self.page - 1) * 6)]

            if self.out.collidepoint(mouse_pos):
                self.visible = False
                return None
            if self.next_page_rect.collidepoint(mouse_pos) and self.page < self.maxpage:
                while pygame.event.get() == MOUSEBUTTONDOWN:
                    pass
                self.page += 1
                self.appear()
                if self.page < self.maxpage:
                    Mouse_on_button(self.screen, self.next_page_rect)
                pygame.display.update()
            if self.prev_page_rect.collidepoint(mouse_pos) and self.page > 1:
                while pygame.event.get() == MOUSEBUTTONDOWN:
                    pass
                self.page -= 1
                self.appear()
                if self.page > 1:
                    Mouse_on_button(self.screen, self.prev_page_rect)
                pygame.display.update()

class EnterMapName:
    def __init__(self, x,y,w,h, screen):
        self.x, self.y, self.w, self.h = x,y,w,h
        self.Rect = pygame.Rect(x,y,w,h)
        self.screen = screen
        pygame.font.init()
        self.font = pygame.font.Font(None, 32)
        self.visible = True
    def appear(self):
        enter_map_name = pygame.image.load('images/enter_map_name.png')
        self.screen.blit(enter_map_name, (self.x, self.y))
        close_button = pygame.transform.scale(pygame.image.load('images/close_button.png'), (50,50))
        self.screen.blit(close_button, (self.x + 8, self.y + 8))
        close_button_rect = pygame.Rect(self.x + 8, self.y + 8, 50, 50)
        
        # Ô nhập dữ liệu
        input_box = pygame.Rect(self.x + 100, self.y + 100, 300, 40)
        color_inactive = GRAY
        color_active = BLUE
        color = color_inactive
        active = False
        text = ''

        enter_button = pygame.image.load('images/enter_button.png')
        self.screen.blit(enter_button, (self.x + 175, self.y + 185))
        enter_rect = pygame.Rect(self.x + 175, self.y + 185, 150,35)
        # Vòng lặp chính
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    # Kiểm tra nếu nhấp vào ô nhập
                    if input_box.collidepoint(event.pos):
                        active = not active
                    else:
                        active = False
                    # Thay đổi màu sắc dựa trên trạng thái
                    color = color_active if active else color_inactive
                    if enter_rect.collidepoint(mouse_pos):
                        return text
                    if close_button_rect.collidepoint(mouse_pos):
                        self.visible = False
                        return None
                if event.type == pygame.KEYDOWN:
                    if active:
                        if event.key == pygame.K_RETURN:
                            return text
                        elif event.key == pygame.K_BACKSPACE:
                            text = text[:-1]
                        elif len(text) < 15:
                            text += event.unicode

            # Vẽ ô nhập dữ liệu
            pygame.draw.rect(self.screen, WHITE, input_box)
            pygame.draw.rect(self.screen, color, input_box, 2)
            
            # Render văn bản
            txt_surface = self.font.render(text, True, BLACK)
            if txt_surface.get_width() > 300:
                l = 300 // txt_surface.get_width() * len(text)
                txt_surface = self.font.render(text[-l:], True, BLACK)
            # Vẽ văn bản
            self.screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))

            # Cập nhật màn hình
            pygame.display.flip()
            
class Settings:
    def __init__(self, screen):
        self.screen = screen
        self.visible = False  # Initially hidden
        self.processing_click = False 
        self.last_close_time = 0
        # Box settings
        self.box_width = 400
        self.box_height = 400
        self.box_color = (50, 50, 50)  # Màu nền box settings
        self.box_border_color = (255, 255, 255)  # Màu viền box settings
        self.box_rect = pygame.Rect(
            (WINDOWWIDTH - self.box_width) // 2,
            (WINDOWHEIGHT - self.box_height) // 2,
            self.box_width,
            self.box_height,
        )


        # Nút Settings chính
        self.settings_button_rect = pygame.Rect(10, 10, 130, 40)  # Vị trí nút "Settings"

        # Các nút trong box settings (bao gồm nút Close)
        self.button_width = 200
        self.button_height = 50
        self.buttons = [
            {"text": "Toggle Sound", "action": self.toggle_sound, "rect": None},
            {"text": "Save Game", "action": self.save_game, "rect": None},
            {"text": "Quit Game", "action": self.quit_game, "rect": None},
            {"text": "Main Menu", "action": self.main_menu, "rect": None},
            {"text": "Close", "action": self.toggle_visibility, "rect": None},  # Nút Close
        ]

        self.sound_on = True  # Default sound state
        self.save_callback = None  # Save callback
        self.quit_callback = None  # Quit callback
        self.main_menu_callback = None  # Main menu callback

        # Tính toán vị trí các nút trong box settings
        self._update_button_positions()
        self.start_pause = None
        self.appear_again = False

    def _update_button_positions(self):
        """Căn chỉnh vị trí các nút nằm trong box settings."""
        start_x = self.box_rect.x + (self.box_width - self.button_width) // 2
        start_y = self.box_rect.y + 40  # Khoảng cách từ mép trên box đến nút đầu tiên
        gap = 20  # Khoảng cách giữa các nút

        for i, button in enumerate(self.buttons):
            button["rect"] = pygame.Rect(
                start_x,
                start_y + i * (self.button_height + gap),
                self.button_width,
                self.button_height,
            )

    def toggle_sound(self):
        """Toggle sound on/off."""
        self.sound_on = not self.sound_on
        if self.sound_on:
            pygame.mixer.music.unpause()  # Unpause music if sound is on
            print("Sound On")
        else:
            pygame.mixer.music.pause()  # Pause music if sound is off
            print("Sound Off")

    def save_game(self):
        """Call save callback."""
        if self.save_callback:
            self.save_callback()
            self.save_message_time = time.time()

    def quit_game(self):
        """Call quit callback."""
        if self.quit_callback:
            self.quit_callback()

    def main_menu(self):
        """Call main menu callback."""
        if self.main_menu_callback:
            self.main_menu_callback()

    def handle_event(self, event):
        """Handle mouse events."""
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos

            if not self.visible:
                # Kiểm tra nút Settings chính khi menu chưa hiển thị
                if self.settings_button_rect.collidepoint(mouse_pos):
                    self.toggle_visibility()  # Mở menu Settings
            else:
                if self.visible:
                    # Đảm bảo không xử lý sự kiện khi menu đã đóng
                    if not self.processing_click:
                        self.processing_click = True
                        # Xử lý các nút trong box settings khi menu hiển thị
                        for button in self.buttons:
                            if button["rect"].collidepoint(mouse_pos):
                                button["action"]()

        # Nếu đã xử lý xong sự kiện, reset trạng thái
        if self.processing_click and event.type == pygame.MOUSEBUTTONUP:
            self.processing_click = False


    def toggle_visibility(self):
        """Toggle visibility of the settings menu."""
        self.visible = not self.visible
        if not self.visible:  # Khi menu đóng
            self.last_close_time = time.time()  # Lưu thời gian menu đóng

    def draw(self):
        """Draw Settings menu and button."""
        # Nút Settings chính trên giao diện
        fonts = pygame.font.Font('font_pixel.otf', 20)
        if not self.visible:
            pygame.draw.rect(self.screen, GREEN, self.settings_button_rect, border_radius=5)
            text = fonts.render("Settings", True, BLACK)
            self.screen.blit(text, (self.settings_button_rect.x + self.settings_button_rect.w / 2 - text.get_width() / 2, self.settings_button_rect.y))
        else:
            # Vẽ box settings
            if not self.start_pause:
                self.start_pause = time.time()
            if not self.appear_again:
                pygame.image.save(DISPLAYSURF, 'saves/temporary.png')
            pygame.draw.rect(self.screen, self.box_color, self.box_rect, border_radius=3)
            pygame.draw.rect(self.screen, self.box_border_color, self.box_rect, width=2, border_radius=3)

            # Vẽ các nút bên trong box settings
            for button in self.buttons:
                pygame.draw.rect(self.screen, BLUE, button["rect"], border_radius=3)
                text = fonts.render(button["text"], True, WHITE)
                w = text.get_width()
                self.screen.blit(text, (button["rect"].x + button["rect"].w / 2 - w / 2, button["rect"].y + 7))