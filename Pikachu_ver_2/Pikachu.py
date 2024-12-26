# INSTRUCTION: Just need to change this path and can run game
from tkinter import messagebox
import tkinter as tk
import pygame, sys, random, copy, time, collections, os
from pygame.locals import *
from PIL import Image
from PIL import ImageTk
from moviepy import VideoFileClip
import json 
import os
import json
from tkinter import *
from tkinter import messagebox
from PIL import ImageTk  # For displaying images
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

def game_menu():
    pygame.init()

    # Khởi tạo màn hình
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Game Menu Example")

    # Tải hình ảnh
    menu_image = pygame.image.load("menu_icon.png").convert_alpha()
    settings_image = pygame.image.load("settings_icon.png").convert_alpha()
    trophy_image = pygame.image.load("trophy_icon.png").convert_alpha()

    # Tạo nút
    menu_button = Button(50, 50, menu_image, 0.5)
    settings_button = Button(150, 50, settings_image, 0.5)
    trophy_button = Button(250, 50, trophy_image, 0.5)

    # Vòng lặp chính
    running = True
    while running:
        screen.fill((255, 255, 255))  # Màu nền trắng

        # Vẽ các nút
        menu_button.draw(screen)
        settings_button.draw(screen)
        trophy_button.draw(screen)

        # Xử lý sự kiện
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Kiểm tra click
        if menu_button.is_clicked():
            print("Menu button clicked!")
        if settings_button.is_clicked():
            print("Settings button clicked!")
        if trophy_button.is_clicked():
            print("Trophy button clicked!")

        pygame.display.update()

    pygame.quit()

# Load background
startBG = pygame.image.load('image_background/introduction_image.jpg')
startBG = pygame.transform.scale(startBG, (WINDOWWIDTH, WINDOWHEIGHT))

listBG = [pygame.image.load('image_background/image_game_{}.jpg'.format(i)) for i in range(1, 8)]
for i in range(len(listBG)):
    listBG[i] = pygame.transform.scale(listBG[i], (WINDOWWIDTH, WINDOWHEIGHT))

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
    font = pygame.font.SysFont("Arial", 20)

    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption('Pikachu in Dota 1 style')
    BASICFONT = pygame.font.SysFont('comicsansms', 70)
    LIVESFONT = pygame.font.SysFont('comicsansms', 45)

    # Tính toán lề ban đầu dựa trên giá trị mặc định
    XMARGIN = (WINDOWWIDTH - (BOXSIZE * BOARDWIDTH)) // 2
    YMARGIN = (WINDOWHEIGHT - (BOXSIZE * BOARDHEIGHT)) // 2
    pygame.event.clear(pygame.MOUSEBUTTONUP)

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

            # Kiểm tra nếu giá trị thay đổi
            if (new_board_width != BOARDWIDTH or 
                new_board_height != BOARDHEIGHT or 
                new_box_size != BOXSIZE):
                BOARDWIDTH, BOARDHEIGHT, BOXSIZE = new_board_width, new_board_height, new_box_size
                XMARGIN = (WINDOWWIDTH - (BOXSIZE * BOARDWIDTH)) // 2
                YMARGIN = (WINDOWHEIGHT - (BOXSIZE * BOARDHEIGHT)) // 2

            # Tải lại hình ảnh sau khi thay đổi tùy chọn
            load_heroes_images()

            pygame.event.clear(pygame.MOUSEBUTTONUP)  # Xóa sự kiện chuột sau khi đóng option
            continue  # Quay lại màn hình Start sau khi chỉnh Option

        # Xử lý hành động từ màn hình chính
        if action == "LOG OUT":
            return "LOG OUT"  # Trả về trạng thái LOG OUT cho ứng dụng
        elif action == "NEW GAME":
            LEVEL = 1
            TIMEBONUS = 0
            STARTTIME = time.time()
            mainBoard = getRandomizedBoard()
            flag = 0
        elif action == "CONTINUE":
            saved_state = load_game_state(email)
            if saved_state:
                LEVEL = saved_state["level"]
                mainBoard = saved_state["board"]

                # Kiểm tra và tự động điều chỉnh kích thước nếu không khớp
                if len(mainBoard) != BOARDHEIGHT or len(mainBoard[0]) != BOARDWIDTH:
                    print("Adjusting saved game size to match current settings.")
                    flag = 0
                else:
                    flag = 1
            else:
                pygame.event.clear(pygame.MOUSEBUTTONUP)  # Xóa sự kiện chuột nếu không có trạng thái lưu
                continue  # Nếu không có trạng thái lưu, quay lại màn hình chính

        # Vòng lặp chơi game
        while LEVEL <= LEVELMAX:
            result = runGame(email, flag)
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


def handle_settings(screen, settings):
    """Xử lý logic và vẽ giao diện Settings."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:  # Nhấn S để hiển thị menu Settings
                settings.toggle_visibility()
        settings.handle_event(event)

    # Vẽ game bình thường
    if not settings.visible:
        DISPLAYSURF.fill((0, 0, 0))  # Tạm placeholder cho màn hình game
    else:
        settings.draw()  # Vẽ giao diện Settings
    pygame.display.update()
    
def showStartScreen(email):
    startScreenSound.play()
    pygame.event.clear()
    while True:
        DISPLAYSURF.blit(startBG, (0, 0))
        button_texts = ['NEW GAME', 'CONTINUE', 'RANK', 'OPTION', 'LOG OUT', 'QUIT']
        button_rects = []
        button_surfs = []

        smallFont = pygame.font.SysFont('comicsansms', 50)

        for i, text in enumerate(button_texts):
            button_surf = smallFont.render(text, True, WHITE)
            button_rect = button_surf.get_rect()
            button_rect.center = (WINDOWWIDTH // 2, WINDOWHEIGHT // 2 - 250 + i * 80)
            button_surfs.append(button_surf)
            button_rects.append(button_rect)

        for surf, rect in zip(button_surfs, button_rects):
            DISPLAYSURF.blit(surf, rect)
            pygame.draw.rect(DISPLAYSURF, WHITE, rect, 2)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONUP:
                pygame.event.clear(pygame.MOUSEBUTTONUP)  # Xóa sự kiện chuột còn lại trước khi xử lý
                mousex, mousey = event.pos
                for i, rect in enumerate(button_rects):
                    if rect.collidepoint((mousex, mousey)):
                        if i == 0:  # NEW GAME
                            return "NEW GAME"
                        elif i == 1:  # CONTINUE
                            saved_state = load_game_state(email)
                            if saved_state:
                                return "CONTINUE"
                            else:
                                print("No saved game found!")
                        elif i == 2:  # RANK
                            print("Rank selected")
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

def runGame(email, flag):
    global font
    font = pygame.font.Font(None, 36)

    # Tải trạng thái hoặc khởi tạo mặc định
    saved_state = load_game_state(email)
    global mainBoard, LEVEL, LIVES, GAMETIME, TIMEBONUS, STARTTIME

    settings = Settings(DISPLAYSURF)
    settings.save_callback = lambda: save_game_state(email, mainBoard, LEVEL, LIVES, GAMETIME, TIMEBONUS, STARTTIME)
    
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

    if saved_state and flag == 1:
        mainBoard = saved_state["board"]
        LEVEL = saved_state["level"]
        LIVES = saved_state["lives"]
        GAMETIME = saved_state["game_time"]
        TIMEBONUS = saved_state["time_bonus"]
        STARTTIME = time.time() - saved_state["start_time"]
    else:
        print(f"No saved game found for account: {email}. Starting with default settings.")
        mainBoard = getRandomizedBoard()
        LEVEL = 1
        LIVES = 3
        TIMEBONUS = 0
        STARTTIME = time.time()

    clickedBoxes = []
    firstSelection = None
    mousex, mousey = 0, 0
    lastTimeGetPoint = time.time()
    hint = getHint(mainBoard)

    randomBG = listBG[LEVEL - 1]
    randomMusicBG = listMusicBG[LEVEL - 1]
    pygame.mixer.music.load(randomMusicBG)
    pygame.mixer.music.play(-1, 0.0)

    while not restart_flag:  # Vòng lặp chính sẽ thoát khi restart_flag được bật
        mouseClicked = False

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
                mouseClicked = True

        # Nếu Settings bị đóng, xóa các sự kiện chuột dư thừa
        if not settings.visible and mouseClicked:
            pygame.event.clear(pygame.MOUSEBUTTONUP)  # Xóa sự kiện chuột dư thừa

        # Vẽ nền và các thành phần chính
        DISPLAYSURF.blit(randomBG, (0, 0))
        drawBoard(mainBoard)
        drawClickedBox(mainBoard, clickedBoxes)
        drawTimeBar()
        drawLives()

        # Kiểm tra thời gian hoặc trạng thái game
        if not settings.visible:
            if time.time() - STARTTIME > GAMETIME + TIMEBONUS:
                LEVEL = LEVELMAX + 1
                return
            if time.time() - lastTimeGetPoint >= GETHINTTIME:
                drawHint(hint)

            # Phần logic game
            boxx, boxy = getBoxAtPixel(mousex, mousey)
            boxx, boxy = getBoxAtPixel(mousex, mousey)
            if (
                boxx is not None and boxy is not None
                and 0 <= boxy < len(mainBoard)
                and 0 <= boxx < len(mainBoard[boxy])
                and mainBoard[boxy][boxx] != 0
            ):
                drawHighlightBox(mainBoard, boxx, boxy)  # Vẽ khung nổi bật quanh ô
                if mouseClicked:
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
                            alterBoardWithLevel(mainBoard, firstSelection[1], firstSelection[0], boxy, boxx, LEVEL)

                            if isGameComplete(mainBoard):
                                drawBoard(mainBoard)
                                pygame.display.update()
                                return
                        else:  # Nếu không tìm được đường nối
                            clickSound.play()

                        # Reset trạng thái sau lần click thứ hai
                        clickedBoxes = []
                        firstSelection = None

            
        # Vẽ menu Settings nếu mở
        settings.draw()

        pygame.display.update()
        FPSCLOCK.tick(FPS)

    pygame.mixer.music.stop()
    pygame.event.clear(pygame.MOUSEBUTTONUP)
    pygame.event.clear()
    return "MAIN_MENU" 

#Lưu game và load game
def save_game_state(email, mainBoard, LEVEL, LIVES, GAMETIME, TIMEBONUS, STARTTIME):
    """Lưu trạng thái hiện tại của trò chơi vào tệp JSON cho tài khoản cụ thể."""
    game_state = {
        "board": mainBoard,
        "level": LEVEL,
        "lives": LIVES,
        "game_time": GAMETIME,
        "time_bonus": TIMEBONUS,
        "start_time": time.time() - STARTTIME  # Thời gian đã trôi qua
    }

    # Đảm bảo thư mục lưu trữ game tồn tại
    save_folder = "saves"
    if not os.path.exists(save_folder):
        os.makedirs(save_folder)

    # Tạo tệp lưu dựa trên email tài khoản
    save_file_path = os.path.join(save_folder, f"{email}_saved_game.json")

    try:
        with open(save_file_path, "w") as save_file:
            json.dump(game_state, save_file, indent=4)
        print("Game saved successfully for account:", email)
    except Exception as e:
        print(f"Error saving game for account {email}: {e}")
        
def load_game_state(email):
    """Tải trạng thái trò chơi từ tệp JSON của tài khoản cụ thể."""
    save_file_path = os.path.join("saves", f"{email}_saved_game.json")

    try:
        with open(save_file_path, "r") as save_file:
            print(f"Game loaded successfully for account: {email}")
            return json.load(save_file)
    except FileNotFoundError:
        print(f"No saved game found for account: {email}")
        return None
    except Exception as e:
        print(f"Error loading game for account {email}: {e}")
        return None
    
def load_saved_game(email):
    """Tải trạng thái đã lưu của tài khoản hiện tại hoặc khởi tạo mặc định."""
    saved_state = load_game_state(email)
    if saved_state:
        mainBoard = saved_state["board"]
        LEVEL = saved_state["level"]
        LIVES = saved_state["lives"]
        GAMETIME = saved_state["game_time"]
        TIMEBONUS = saved_state["time_bonus"]
        STARTTIME = time.time() - saved_state["start_time"]
        print(f"Game state restored for account: {email}")
        return True
    else:
        # Trạng thái mặc định khi không có tệp lưu
        mainBoard = getRandomizedBoard()  # Tạo bảng mặc định
        LEVEL = 1
        LIVES = 3
        TIMEBONUS = 0
        STARTTIME = time.time()
        print(f"No saved game found for account {email}. Starting with default settings.")
        return False

def getRandomizedBoard():
    NUMHEROES_ONBOARD = (BOARDWIDTH - 2) * (BOARDHEIGHT - 2) // 4
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

def drawLives():
    aegisRect = pygame.Rect(10, 10, BOXSIZE, BOXSIZE)
    # DISPLAYSURF.blit(aegis, aegisRect)
    livesSurf = LIVESFONT.render(str(LIVES), True, WHITE)
    livesRect = livesSurf.get_rect()
    livesRect.topleft = (65, 0)
    DISPLAYSURF.blit(livesSurf, livesRect)

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
        self.settings_button_rect = pygame.Rect(10, 10, 100, 40)  # Vị trí nút "Settings"

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
        if not self.visible:
            pygame.draw.rect(self.screen, GREEN, self.settings_button_rect, border_radius=5)
            text = font.render("Settings", True, BLACK)
            self.screen.blit(text, (self.settings_button_rect.x + 10, self.settings_button_rect.y + 10))
        else:
            # Vẽ box settings
            pygame.draw.rect(self.screen, self.box_color, self.box_rect, border_radius=10)
            pygame.draw.rect(self.screen, self.box_border_color, self.box_rect, width=2, border_radius=10)

            # Vẽ các nút bên trong box settings
            for button in self.buttons:
                pygame.draw.rect(self.screen, BLUE, button["rect"], border_radius=10)
                text = font.render(button["text"], True, WHITE)
                self.screen.blit(text, (button["rect"].x + 20, button["rect"].y + 10))