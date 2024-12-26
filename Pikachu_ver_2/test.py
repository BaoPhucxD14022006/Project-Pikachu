# INSTRUCTION: Just need to change this path and can run game
PATH = 'E:\Project\Pikachu' 

import pygame, sys, random, copy, time, collections, os
from pygame.locals import *
from PIL import Image
from moviepy import VideoFileClip
import os
import numpy as np
import threading
import json

FPS = 10
WINDOWWIDTH = 1060
WINDOWHEIGHT = 600
BOXSIZE = 55
BOARDWIDTH = 10
BOARDHEIGHT = 7
NUMHEROES_ONBOARD = 21
NUMSAMEHEROES = 4
TIMEBAR_LENGTH = 300
TIMEBAR_WIDTH = 30
LEVELMAX = 5
LIVES = 10
GAMETIME = 240
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

# ??nh ngh?a l?p InputBox (h?p nh?p li?u)
class InputBox:
    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = GRAY
        self.text = text
        self.txt_surface = FONT.render(text, True, WHITE)
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)
            self.color = WHITE if self.active else GRAY
        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                self.text += event.unicode
            self.txt_surface = FONT.render(self.text, True, WHITE)

    def draw(self, screen):
        screen.blit(self.txt_surface, (self.rect.x + 9, self.rect.y - 5))
        pygame.draw.rect(screen, self.color, self.rect, 2)

#t?o n�t b?m
class Button:
    def __init__(self, x, y, w, h, COLOR = WHITE, font = FONT, text = "Sign up"):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = COLOR
        self.font = font
        self.text = text
        self.txt_surface = font.render(self.text, True, BLACK)
        
    def draw(self, screen):
        #v? n�t b?m
        pygame.draw.rect(screen, self.color, self.rect)
        text_x = self.rect.x + (self.rect.w - self.txt_surface.get_width()) // 2
        text_y = self.rect.y + (self.rect.h - self.txt_surface.get_height()) // 2
        screen.blit(self.txt_surface, (text_x, text_y))
        
    def updateNodeNode(self, new_text):
        self.text = new_text
        self.txt_surface = self.font.render(self.text, True, BLACK) 
        
    def isClicked(self, event):
        rec = pygame.Rect(self.rect)  # Chuy?n self.rect th�nh ??i t??ng Rect
        mouse_pos = event.pos # Vi tri cua chuot
        if event.type == pygame.MOUSEMOTION:
            if rec.collidepoint(mouse_pos):
                self.color = BLUE
            else:
                self.color = BLACK
        # Ki?m tra n?u s? ki?n l� nh?n chu?t v� t?a ?? chu?t n?m trong h�nh ch? nh?t
        if event.type == pygame.MOUSEBUTTONDOWN:
            if rec.collidepoint(mouse_pos):  # Ki?m tra n?u chu?t trong v�ng n�t
                self.color = GRAY
                return True
                 
# H�m x? l� video
def play_video(video_surface):
    # Load video clip
    clip = VideoFileClip("video_intro/Pokemon_opening.mp4")
    clip = clip.subclip(0, 34)  # Ch? ph�t trong 344 gi�y
    clip = clip.resize(height=600)
    clip = clip.rotate(90)  # L?t d?c video

    while True:  # Ch?y video li�n t?c
        for frame in clip.iter_frames(fps=24, dtype='uint8'):
            frame = np.flipud(frame)  # ??o chi?u d?c m?ng
            frame_surface = pygame.surfarray.make_surface(frame)
            video_surface.blit(frame_surface, (0, 0))

        clip = clip.subclip(0, 34)  # Reset l?i video t? ??u
        
# T?o m?t Surface cho video
video_surface = pygame.Surface((1060, 600))

# T?o m?t thread ri�ng ?? ph�t video
def video_thread_func():
    play_video(video_surface)

# Kh?i t?o thread video
video_thread = threading.Thread(target=video_thread_func)
video_thread.daemon = True  # Cho ph�p thread k?t th�c khi ch??ng tr�nh ch�nh k?t th�c
video_thread.start()

# H�m ??ng k� t�i kho?n
def register(username, password):
    try:
        with open("users.json", "r", encoding="utf-8") as in_file:
            users = json.load(in_file)
    except FileNotFoundError:
        users = {}
    except json.JSONDecodeError:
        users = {}
    
    if username in list(users.keys()):
        return f"T�i kho?n ?� t?n t?i!"
    
    users[username] = password
    with open("users.json", "w", encoding="utf-8") as out_file:
        json.dump(users, out_file)
    return f"??ng k� th�nh c�ng!"

# H�m ??ng nh?p
def login(username, password):
    try:
        with open("users.json", "r", encoding="utf-8") as file:
            users = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return "Kh�ng t�m th?y d? li?u ng??i d�ng!"

    if username in users and users[username] == password:
        global INTRO
        INTRO = False  # C?p nh?t tr?ng th�i ?? chuy?n sang tr� ch?i
        return "??ng nh?p th�nh c�ng!"
    return "Sai t�i kho?n ho?c m?t kh?u!"


def LogIn(screen):
    pygame.key.set_repeat(0)
    # Kh?i t?o c�c h?p nh?p li?u
    username_box = InputBox(430, 180, 200, 40)
    password_box = InputBox(430, 280, 200, 40)
    input_boxes = [username_box, password_box]

    #hien nut
    register_button = Button(700, 500, 150, 50)
    login_button = Button(455, 350, 150, 40, WHITE, FONT, "Log In")
    
    # Ch? ?? (Login ho?c Register)
    mode = "Login"
    message = ""
    
    running1 = True
    returnColor = False
    MousePressed = False
    msgPressed = False  
    loginButtonPress = False
    while running1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running1 = False
                pygame.quit()
            for box in input_boxes:
                box.handle_event(event)
                
        # V? video l�n m�n h�nh
        screen.blit(video_surface, (0, 0))
        
        # X? l� n�t b?mb?m
        if event.type == pygame.MOUSEBUTTONDOWN:
            if not loginButtonPress:
                if login_button.isClicked(event):
                    loginButtonPress = True
                    msgPressed = True
                    username = username_box.text
                    password = password_box.text
                    username_box.text = ""
                    password_box.text = ""
                    if mode == "Login":
                        message = login(username, password)
                    else:
                        message = register(username, password) 
            if not MousePressed:        
                if register_button.isClicked(event):
                    returnColor = False
                    MousePressed = True
                    username = username_box.text
                    password = password_box.text
                    username_box.text = ""
                    password_box.text = ""
                    username_box.txt_surface = FONT.render("", True, WHITE)
                    password_box.txt_surface = FONT.render("", True, WHITE) 

        if mode == "Register":
            login_button.updateNodeNode("Confirm")
            register_button.updateNodeNode("Log In")
        else:
            login_button.updateNodeNode("Log In")
            register_button.updateNodeNode("Sign up")
            
        if event.type == pygame.MOUSEBUTTONUP:
            returnColor = True
            if MousePressed:
                if mode == "Login":
                    mode = "Register"
                else:
                    mode = "Login"
                message = ""
            MousePressed = False
            loginButtonPress = False
        # V? c�c ph?n giao di?n kh�c
        title = FONT.render(f"{mode.upper()}", True, WHITE)
        if mode == "Login":
            screen.blit(title, (475, 100))
        else:
            screen.blit(title, (450, 100))
        if message == "??ng nh?p th�nh c�ng!":
            return showStartScreen()
        # Hi?n th? th�ng b�o
        register_button.draw(screen)
        login_button.draw(screen)
        msg = FONT.render(message, True, WHITE)
        if msgPressed:
            if mode == "Login":
                screen.blit(msg, (300, 420))
            else:
                screen.blit(msg, (370, 420))
        # V? h?p nh?p li?u
        for box in input_boxes:
            box.draw(screen)
            
        if returnColor:
            register_button.color = WHITE
            login_button.color = WHITE

        pygame.display.flip()  # C?p nh?t m�n h�nh
        
# TIMEBAR setup
barPos = (WINDOWWIDTH // 2 - TIMEBAR_LENGTH // 2, YMARGIN // 2 - TIMEBAR_WIDTH // 2)
barSize = (TIMEBAR_LENGTH, TIMEBAR_WIDTH)
borderColor = WHITE
barColor = BOLDGREEN

# Make a dict to store scaled images
LISTHEROES = os.listdir(PATH + '/images_icon')
NUMHEROES = len(LISTHEROES)
HEROES_DICT = {}

for i in range(len(LISTHEROES)):
    HEROES_DICT[i + 1] = pygame.transform.scale(pygame.image.load('images_icon/' + LISTHEROES[i]), (BOXSIZE, BOXSIZE))

# Load pictures
# SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
# screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
# pygame.display.set_caption("GIF as Icon")

# Load frames t? th? m?c
def load_frames(folder):
    frames = []
    for filename in sorted(os.listdir(folder)):
        if filename.endswith(".gif"):
            frames.append(pygame.image.load(os.path.join(folder, filename)))
    return frames

frames = load_frames("icon_gif")

# V? tr� icon tr�n m�n h�nh
ICON_X, ICON_Y = 10, 10  # G�c tr�i tr�n

# V�ng l?p ch�nh
clock = pygame.time.Clock()

aegis = pygame.image.load('icon_gif/pikachu_run.gif')
aegis = pygame.transform.scale(aegis, (45, 45))

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

INTRO = True
def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT, LIVESFONT, LEVEL, INTRO
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption('Pikachu')
    BASICFONT = pygame.font.SysFont('comicsansms', 70)
    LIVESFONT = pygame.font.SysFont('comicsansms', 45)
    


    while True:
        random.shuffle(listBG)
        random.shuffle(listMusicBG)
        LEVEL = 1
        # showStartScreen()
        LogIn(DISPLAYSURF)
        while LEVEL <= LEVELMAX:
            runGame()
            LEVEL += 1
            pygame.time.wait(1000)
        showGameOverScreen()

def showStartScreen():
    startScreenSound.play()
    while True:
        DISPLAYSURF.blit(startBG, (0, 0))
        newGameSurf = BASICFONT.render('NEW GAME', True, WHITE)
        newGameRect = newGameSurf.get_rect()
        newGameRect.center = (WINDOWWIDTH // 2, WINDOWHEIGHT // 2)
        DISPLAYSURF.blit(newGameSurf, newGameRect)
        pygame.draw.rect(DISPLAYSURF, WHITE, newGameRect, 4)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                if newGameRect.collidepoint((mousex, mousey)):
                    # If click to New Game rect, the game starts
                    return

        pygame.display.update()
        FPSCLOCK.tick(FPS)

def runGame():
    mainBoard = getRandomizedBoard()
    clickedBoxes = [] # stores the (x, y) of clicked boxes
    firstSelection = None # stores the (x, y) of the first box clicked
    mousex = 0 # used to store x coordinate of mouse event
    mousey = 0 # used to store y coordinate of mouse event
    lastTimeGetPoint = time.time()
    hint = getHint(mainBoard)

    global GAMETIME, LEVEL, LIVES, TIMEBONUS, STARTTIME
    STARTTIME = time.time()
    TIMEBONUS = 0

    randomBG = listBG[LEVEL - 1]
    randomMusicBG = listMusicBG[LEVEL - 1]
    pygame.mixer.music.load(randomMusicBG)
    pygame.mixer.music.play(-1, 0.0)

    while True:
        mouseClicked = False

        DISPLAYSURF.blit(randomBG, (0, 0))
        drawBoard(mainBoard)
        drawClickedBox(mainBoard, clickedBoxes)
        drawTimeBar()
        drawLives()

        if time.time() - STARTTIME > GAMETIME + TIMEBONUS:
            LEVEL = LEVELMAX + 1
            return
        if time.time() - lastTimeGetPoint >= GETHINTTIME:
            drawHint(hint)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEMOTION:
                mousex, mousey = event.pos
            elif event.type == MOUSEBUTTONUP:
                mousex, mousey == event.pos
                mouseClicked = True
            if event.type == KEYUP:
                if event.key == K_n:
                    boxy1, boxx1 = hint[0][0], hint[0][1]
                    boxy2, boxx2 = hint[1][0], hint[1][1]
                    mainBoard[boxy1][boxx1] = 0
                    mainBoard[boxy2][boxx2] = 0
                    TIMEBONUS += 1
                    alterBoardWithLevel(mainBoard, boxy1, boxx1, boxy2, boxx2, LEVEL)

                    if isGameComplete(mainBoard):
                        drawBoard(mainBoard)
                        pygame.display.update()
                        return

                    if not(mainBoard[boxy1][boxx1] != 0 and bfs(mainBoard, boxy1, boxx1, boxy2, boxx2)):
                        hint = getHint(mainBoard)
                        while not hint:
                            pygame.time.wait(100)
                            resetBoard(mainBoard)
                            LIVES += -1
                            if LIVES == 0:
                                LEVEL = LEVELMAX + 1
                                return

                            hint = getHint(mainBoard)

        boxx, boxy = getBoxAtPixel(mousex, mousey)

        if boxx != None and boxy != None and mainBoard[boxy][boxx] != 0:
            # The mouse is currently over a box
            drawHighlightBox(mainBoard, boxx, boxy)

        if boxx != None and boxy != None and mainBoard[boxy][boxx] != 0 and mouseClicked == True:
            # The mouse is clicking on a box
            clickedBoxes.append((boxx, boxy))
            drawClickedBox(mainBoard, clickedBoxes)
            mouseClicked = False

            if firstSelection == None:
                firstSelection = (boxx, boxy)
                clickSound.play()
            else:
                path = bfs(mainBoard, firstSelection[1], firstSelection[0], boxy, boxx)
                if path:
                    # if random.randint(0, 100) < 20:
                        # soundObject = random.choice(LIST_SOUNDEFFECT)
                        # soundObject.play()
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
                    if not(mainBoard[hint[0][0]][hint[0][1]] != 0 and bfs(mainBoard, hint[0][0], hint[0][1], hint[1][0], hint[1][1])):
                        hint = getHint(mainBoard)
                        while not hint:
                            pygame.time.wait(500)
                            resetBoard(mainBoard)
                            LIVES += -1
                            if LIVES == 0:
                                LEVEL = LEVELMAX + 1
                                return

                            hint = getHint(mainBoard)
                else:
                    clickSound.play()

                clickedBoxes = []
                firstSelection = None

        pygame.display.update()
        FPSCLOCK.tick(FPS)
    pygame.mixer.music.stop()

def getRandomizedBoard():
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

def drawBoard(board):
    for boxx in range(BOARDWIDTH):
        for boxy in range(BOARDHEIGHT):
            if board[boxy][boxx] != 0:
                left, top = leftTopCoordsOfBox(boxx, boxy)
                boxRect = pygame.Rect(left, top, BOXSIZE, BOXSIZE)
                DISPLAYSURF.blit(HEROES_DICT[board[boxy][boxx]], boxRect)

def drawHighlightBox(board, boxx, boxy):
    left, top = leftTopCoordsOfBox(boxx, boxy)
    pygame.draw.rect(DISPLAYSURF, HIGHLIGHTCOLOR, (left - 2, top - 2,
                                                   BOXSIZE + 4, BOXSIZE + 4), 2)

def drawClickedBox(board, clickedBoxes):
    for boxx, boxy in clickedBoxes:
        left, top = leftTopCoordsOfBox(boxx, boxy)
        boxRect = pygame.Rect(left, top, BOXSIZE, BOXSIZE)
        image = HEROES_DICT[board[boxy][boxx]].copy()

        # Darken the clicked image
        image.fill((60, 60, 60), special_flags=pygame.BLEND_RGB_SUB)
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

def getCenterPos(pos): # pos is coordinate of a box in mainBoard
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
    DISPLAYSURF.blit(aegis, aegisRect)
    livesSurf = LIVESFONT.render(str(LIVES), True, WHITE)
    livesRect = livesSurf.get_rect()
    livesRect.topleft = (65, 0)
    DISPLAYSURF.blit(livesSurf, livesRect)

if __name__ == '__main__':
    main()



