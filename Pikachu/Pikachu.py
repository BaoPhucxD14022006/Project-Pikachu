import pygame, sys, random, copy, time, collections, os
from pygame.locals import *
import json 
import os
import json
from tkinter import *
import time
from PIL import Image
import pygame.locals
import re

PATH = os.path.dirname(os.path.abspath(__file__))
os.chdir(PATH)
FPS = 144
BASE_WINDOWWIDTH = 1920
BASE_WINDOWHEIGHT = 1080
WINDOWWIDTH = 1920
WINDOWHEIGHT = 1080
BOXSIZEX = 40
BOXSIZEY = 50
BOARDWIDTH = 14
BOARDHEIGHT = 9
NUMHEROES_ONBOARD = (BOARDWIDTH - 2) * (BOARDHEIGHT - 2) // 4
NUMSAMEHEROES = 4
XMARGIN = (WINDOWWIDTH - (BOXSIZEX * BOARDWIDTH)) // 2
YMARGIN = (WINDOWHEIGHT - (BOXSIZEY * BOARDHEIGHT)) // 2
TIMEBAR_LENGTH = 600
TIMEBAR_WIDTH = 60
LEVELMAX = 5
LIVES = 3
GAMETIME = 60
GETHINTTIME = 20

# Set up cho màu
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

# Setup cho TIMEBAR
barPos = (WINDOWWIDTH // 2 - TIMEBAR_LENGTH // 2, YMARGIN // 2 - TIMEBAR_WIDTH // 2)
barSize = (TIMEBAR_LENGTH, TIMEBAR_WIDTH)
borderColor = WHITE
barColor = BOLDGREEN

# Tạo danh sách lưu trữ địa chỉ Pokemon
LISTPOKES = os.listdir(PATH + '/images/images_icon/Gen1/')
POKES_DICT = dict()

# Thêm danh sách lưu trữ các cặp đã được thông báo
notified_pairs = set()

# Hàng đợi lưu thông báo
notifications = []

def add_notification(message, duration=3):
    """Thêm thông báo mới vào hàng đợi."""
    global notifications
    # Mỗi thông báo sẽ ghi lại nội dung và thời gian hết hạn
    notifications.append({"message": message, "end_time": time.time() + duration})

def draw_notifications(screen):
    """Hiển thị thông báo hiện tại."""
    global notifications
    if notifications:
        # Lấy thông báo đầu tiên trong hàng đợi
        current_notification = notifications[0]
        if time.time() > current_notification["end_time"]:
            notifications.pop(0)  # Xóa thông báo nếu đã hết thời gian hiển thị
        else:
            # Vẽ thông báo lên màn hình
            font = pygame.font.Font('font_pixel.otf', int(36*x_scale))
            text_surface = font.render(current_notification["message"], True, WHITE)
            text_rect = text_surface.get_rect()
            text_rect.bottomleft = (int(10*x_scale), WINDOWHEIGHT - text_surface.get_height() - int(5*y_scale))  # Góc dưới bên trái màn hình
            screen.blit(text_surface, text_rect)

for i in range(len(LISTPOKES)):
    POKES_DICT[i + 1] = pygame.transform.scale(pygame.image.load('images/images_icon/Gen1/' + LISTPOKES[i]), (BOXSIZEX, BOXSIZEY))

def Mouse_on_button(surface, rect):
    x,y,w,h = rect
    gray_transparent = (128, 128, 128, 100)
    transparent_surface = pygame.Surface((WINDOWWIDTH, WINDOWHEIGHT), pygame.SRCALPHA)
    pygame.draw.rect(transparent_surface, gray_transparent, (x,y,w,h))
    surface.blit(transparent_surface, (0, 0))

class Score:
    def __init__(self, font, path, initial_score=0):
        self.score = initial_score
        self.font = font
        self.position = (WINDOWWIDTH - int(150*x_scale), int(10*y_scale))
        self.last_action_time = time.time()  # Thời gian nối Pokémon gần nhất
        self.multiplier = 1  # Hệ số nhân mặc định
        self.combo_count = 0  # Số lần kết nối đúng liên tiếp
        self.multiplier_image = None  # Ảnh hệ số nhân
        self.image_display_time = 0  # Thời gian bắt đầu hiển thị ảnh hệ số nhân
        self.path = path
        self.flagx5 = True
        self.flagx10 = True

    def increase(self, base_points):
        """Tăng điểm với hệ số nhân."""
        global LIVES
        current_time = time.time()
        elapsed_time = current_time - self.last_action_time

        if elapsed_time <= 5:
            self.combo_count += 1

            # Gán hệ số nhân và đường dẫn ảnh tương ứng
            if self.combo_count >= 10:
                if self.flagx10:
                    if LIVES == 2:
                        LIVES += 1
                    elif LIVES == 1:
                        LIVES += 1
                    self.flagx10 = False
                self.multiplier = 10
                image_path = f"{self.path}/images/multiplier/x10.png"
            elif self.combo_count >= 5:
                if self.flagx5:
                    if LIVES < 3:
                        LIVES += 1
                    self.flagx5 = False
                self.multiplier = 5
                image_path = f"{self.path}/images/multiplier/x5.png"
            elif self.combo_count >= 2:
                self.multiplier = 2
                image_path = f"{self.path}/images/multiplier/x2.png"
            else:
                self.multiplier = 1
                image_path = None

            # Nếu có ảnh, tải và gán
            if image_path:
                self.multiplier_image = pygame.image.load(image_path)
                self.multiplier_image = pygame.transform.scale(self.multiplier_image, (int(100*x_scale), int(100*y_scale)))
                self.image_display_time = time.time()  # Đặt lại thời gian hiển thị
            else:
                self.multiplier_image = None
        else:
            # Nếu ngoài 5 giây, đặt lại combo và hệ số nhân về 1
            self.combo_count = 0
            self.multiplier = 1
            self.multiplier_image = None

        # Cập nhật điểm và thời gian nối Pokémon gần nhất
        self.score += base_points * self.multiplier
        self.last_action_time = current_time

    def reset_multiplier(self):
        """Đặt lại hệ số nhân và combo về 1 nếu đã quá 5 giây."""
        current_time = time.time()
        if current_time - self.last_action_time > 5:
            self.combo_count = 0
            self.multiplier = 1
            self.multiplier_image = None
            self.flagx5, self.flagx10 = True, True

    def decrease(self, amount):
        """Giảm điểm, không để âm."""
        self.score = max(0, self.score - amount)

    def reset(self):
        """Đặt lại điểm số, combo và hệ số nhân."""
        self.flagx5, self.flagx10 = True, True
        self.score = 0
        self.combo_count = 0
        self.multiplier = 1
        self.multiplier_image = None
        self.last_action_time = time.time()

    def draw(self, screen):
        """Hiển thị điểm số, hệ số nhân và combo lên màn hình."""
        score_text = f"Score: {self.score}"
        score_surf = self.font.render(score_text, True, WHITE)
        score_rect = score_surf.get_rect()
        score_rect.topright = (WINDOWWIDTH - int(10*x_scale), int(10*y_scale))  # Căn phải ở góc trên
        screen.blit(score_surf, score_rect)

        # Hiển thị ảnh hệ số nhân (nếu có và trong vòng 5 giây)
        if self.multiplier_image and time.time() - self.image_display_time <= 5:
            image_rect = self.multiplier_image.get_rect()
            image_rect.topright = (WINDOWWIDTH - int(10*x_scale), int(75*y_scale))  # Vị trí dưới ô điểm score
            screen.blit(self.multiplier_image, image_rect)
        elif self.multiplier_image and time.time() - self.image_display_time > 5:
            self.multiplier_image = None  # Xóa ảnh sau 5 giây

class LoadGif:
    def __init__(self, screen, WINDOWWIDTH, WINDOWHEIGHT, width=None, height=None):
        self.SCREEN_WIDTH, self.SCREEN_HEIGHT = WINDOWWIDTH, WINDOWHEIGHT
        self.screen = screen
        self.clock, self.last_update_time = pygame.time.Clock(), pygame.time.get_ticks()
        self.frame_counters = 0

        # Kích thước tùy chỉnh
        self.custom_width = width
        self.custom_height = height

        # Load các khung hình GIF
        self.frames, self.frame_delay = self.load_gif_frames(f"{PATH}/images/icon_gif/lastright.gif")


    def load_gif_frames(self, gif_path):
        gif = Image.open(gif_path)
        frames = []
        try:
            while True:
                frame = gif.convert("RGBA")  # Chuyển khung hình sang RGBA
                pygame_frame = pygame.image.fromstring(frame.tobytes(), frame.size, "RGBA")

                # Nếu có kích thước tùy chỉnh, thay đổi kích thước khung hình
                if self.custom_width and self.custom_height:
                    pygame_frame = pygame.transform.scale(pygame_frame, (self.custom_width, self.custom_height))
                
                frames.append(pygame_frame)
                gif.seek(gif.tell() + 1)  # Chuyển sang khung hình tiếp theo
        except EOFError:
            pass  # Kết thúc GIF
        return frames, gif.info["duration"]  # Trả về các khung hình và thời gian giữa các khung
    
    def playGif(self, posX=None, posY=None):
        # Xác định vị trí mặc định nếu không cung cấp
        self.frame = self.frames[self.frame_counters]
        if posX is None:
            posX = self.SCREEN_WIDTH - self.frame.get_width()
        if posY is None:
            posY = self.SCREEN_HEIGHT - self.frame.get_height()

        current_time = pygame.time.get_ticks()
        if current_time - self.last_update_time > self.frame_delay:
            self.last_update_time = current_time
            # Cập nhật bộ đếm frame
            self.frame_counters = (self.frame_counters + 1) % len(self.frames)

        # Hiển thị vẽ gif
        self.screen.blit(self.frame, (posX, posY))

        # Cập nhật màn hình
        pygame.display.flip()
        self.clock.tick(60)

class SettingMenu:
    def __init__(self, w, h, screen = None, muteSound = True, muteSFX = True, Volume = 0.5, dragging = False):
        self.w = w
        self.h = h
        self.muteSound = muteSound
        self.muteSFX = muteSFX
        self.volumeSound = 0.3
        self.volumeSFX = 1
        self.draggingSound = dragging
        self.draggingSFX = dragging
        self.screen = screen
        self.actived = False
        self.font = pygame.font.Font('font_pixel.otf', int(25*x_scale))
        self.gif = LoadGif(screen, w, h, int(400*x_scale), int(356*y_scale))
        self.handle_x_sfx = 0
        self.handle_y_sfx = 0
        self.handle_x_sound = 0
        self.handle_y_sound = 0
        self.flag = False

    def WriteMsg(self, text = "text", color = WHITE, posY = 130):
        msg = self.font.render(text, True, color)
        screen_width = self.screen.get_size()[0]
        text_width = msg.get_width()
        centerX = (screen_width - text_width) / 2
        self.screen.blit(msg, (centerX + int(5*x_scale), int(posY*y_scale)))
    
    def loadImages(self, linkImage,  posX = 0, posY = 0, W = WINDOWWIDTH, H = WINDOWHEIGHT):
        image = pygame.image.load(linkImage)
        image = pygame.transform.scale(image, (W, H))
        imageRect = image.get_rect(topleft = (posX, posY))
        return (image, imageRect)
    
    def drawImage(self, image):
        self.screen.blit(image[0], image[1].topleft)
    
    def Option(self):
        
        # Kích thước thanh trượt của âm thanh
        slider_x_sound = int(1200*x_scale)
        slider_y_sound = int(460*x_scale)
        slider_width_sound = int(400*x_scale)
        slider_height_sound = int(20*y_scale)
        handle_radius_sound = int(30*x_scale)

        # Vị trí nút điều chỉnh của âm thanh
        handle_x_sound = slider_x_sound + int(slider_width_sound * 0.3)
        handle_y_sound = slider_y_sound + slider_height_sound // 2
        
        # Kích thước thanh trượt của SFX
        slider_x_sfx = int(1200*x_scale)
        slider_y_sfx = int(660*x_scale) 
        slider_width_sfx = int(400*x_scale)
        slider_height_sfx = int(20*x_scale)
        handle_radius_sfx = int(30*x_scale)

        # Vị trí nút điều chỉnh của SFX
        handle_x_sfx = slider_x_sfx + slider_width_sfx
        handle_y_sfx = slider_y_sfx + slider_height_sfx // 2
        
        # Nút bấm về menu
        # ButtonExit = Button(50, 580, 200, 50, WHITE, , "Main Menu", 2)
        Gif = self.gif
        
        image_background = self.loadImages("images/image_background/backgroundSetting.jpg", 0, 0, self.w, self.h)
        image_sound_on = self.loadImages("images/image_button/on.png", int(1640*x_scale), int(370*y_scale), int(200*x_scale), int(200*y_scale))
        image_sound_off = self.loadImages("images/image_button/off.png", int(1640*x_scale), int(370*y_scale), int(200*x_scale), int(200*y_scale))
        image_sfx_on = self.loadImages("images/image_button/on.png", int(1640*x_scale), int(570*y_scale), int(200*x_scale), int(200*y_scale))
        image_sfx_off = self.loadImages("images/image_button/off.png", int(1640*x_scale), int(570*y_scale), int(200*x_scale), int(200*y_scale))
        image_back_home = self.loadImages("images/image_button/buttonbackhome.png", int(50*x_scale), self.h - int(200*y_scale), int(240*x_scale), int(160*y_scale))
        
        # Vẽ hình các nút bấm
        button_image_sound_rect = image_sound_on[1]
        button_image_sfx_rect = image_sfx_on[1]
        button_image_back_home = image_back_home[1]
        
        
        while True:
            
            self.drawImage(image_background)
            self.drawImage(image_back_home)
            if self.muteSound:
                self.drawImage(image_sound_on)
            else:
                self.drawImage(image_sound_off)
            if self.muteSFX:
                self.drawImage(image_sfx_on)
            else:
                self.drawImage(image_sfx_off)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # Kiểm tra nếu nhấn vào nút trượt
                    mouse_x, mouse_y = event.pos
                    if not self.flag:
                        distanceSound = ((mouse_x - handle_x_sound) ** 2 + (mouse_y - handle_y_sound) ** 2) ** 0.5
                        distanceSFX = ((mouse_x - handle_x_sfx) ** 2 + (mouse_y - handle_y_sfx) ** 2) ** 0.5
                    else:
                        distanceSound = ((mouse_x - self.handle_x_sound) ** 2 + (mouse_y - self.handle_y_sound) ** 2) ** 0.5
                        distanceSFX = ((mouse_x - self.handle_x_sfx) ** 2 + (mouse_y - self.handle_y_sfx) ** 2) ** 0.5
                    if distanceSound <= handle_radius_sound:
                        self.draggingSound = True
                    if distanceSFX <= handle_radius_sfx:
                        self.draggingSFX = True
                    if button_image_sound_rect.collidepoint((mouse_x, mouse_y)):
                        self.muteSound = not self.muteSound
                    if button_image_sfx_rect.collidepoint((mouse_x, mouse_y)):
                        self.muteSFX = not self.muteSFX
                    if button_image_back_home.collidepoint((mouse_x, mouse_y)):
                        if not self.flag:
                            self.volumeSound = (handle_x_sound - slider_x_sound) / slider_width_sound
                            self.volumeSFX = (handle_x_sfx - slider_x_sfx) / slider_width_sfx
                        else:
                            self.volumeSound = (self.handle_x_sound - slider_x_sound) / slider_width_sound
                            self.volumeSFX = (self.handle_x_sfx - slider_x_sfx) / slider_width_sfx
                        if not self.flag:
                            self.handle_x_sfx = handle_x_sfx
                            self.handle_y_sfx = handle_y_sfx
                            self.handle_x_sound = handle_x_sound
                            self.handle_y_sound = handle_y_sound
                        self.flag = True
                        return "MAIN_MENU"

                elif event.type == pygame.MOUSEBUTTONUP:
                    self.draggingSound = False
                    self.draggingSFX = False

                elif event.type == pygame.MOUSEMOTION:
                    mouse_x, mouse_y = event.pos
                    if button_image_sound_rect.collidepoint((mouse_x, mouse_y)):
                        image_sound_on[0].set_alpha(100)
                        image_sound_off[0].set_alpha(100)
                    else:
                        image_sound_on[0].set_alpha(255)
                        image_sound_on[0].set_alpha(255)
                    if button_image_sfx_rect.collidepoint((mouse_x, mouse_y)):
                        image_sfx_on[0].set_alpha(100)
                        image_sfx_off[0].set_alpha(100)
                    else:
                        image_sfx_on[0].set_alpha(255)
                        image_sfx_off[0].set_alpha(255)
                    if button_image_back_home.collidepoint((mouse_x, mouse_y)):
                        image_back_home[0].set_alpha(100)
                    else:
                        image_back_home[0].set_alpha(255)
                    if self.draggingSFX:
                        if not self.flag:
                            handle_x_sfx = max(slider_x_sfx, min(mouse_x, slider_x_sfx + slider_width_sfx))  # Giới hạn trong thanh nền
                        else:
                            self.handle_x_sfx = max(slider_x_sfx, min(mouse_x, slider_x_sfx + slider_width_sfx))  # Giới hạn trong thanh nền
                    if self.draggingSound:
                        if not self.flag:
                            handle_x_sound = max(slider_x_sound, min(mouse_x, slider_x_sound + slider_width_sound))  # Giới hạn trong thanh nền
                        else:
                            self.handle_x_sound = max(slider_x_sound, min(mouse_x, slider_x_sound + slider_width_sound))  # Giới hạn trong thanh nền
                
            # Tính toán âm lượng mới (0.0 - 1.0)
            if not self.flag:
                self.volumeSound = (handle_x_sound - slider_x_sound) / slider_width_sound
                self.volumeSFX = (handle_x_sfx - slider_x_sfx) / slider_width_sfx
            else:
                self.volumeSound = (self.handle_x_sound - slider_x_sound) / slider_width_sound
                self.volumeSFX = (self.handle_x_sfx - slider_x_sfx) / slider_width_sfx
            pygame.mixer.music.set_volume(self.volumeSound)  
            pygame.mixer.music.set_volume(self.volumeSFX)  
            
            # Vẽ thanh nền
            pygame.draw.rect(self.screen, GRAY, (slider_x_sound, slider_y_sound, slider_width_sound, slider_height_sound))
            pygame.draw.rect(self.screen, GRAY, (slider_x_sfx, slider_y_sfx, slider_width_sfx, slider_height_sfx))
            
            # Vẽ nút điều chỉnh
            if not self.flag:
                pygame.draw.circle(self.screen, GREEN, (handle_x_sound, handle_y_sound), handle_radius_sound)
                pygame.draw.circle(self.screen, GREEN, (handle_x_sfx, handle_y_sfx), handle_radius_sfx)
            else:
                pygame.draw.circle(self.screen, GREEN, (self.handle_x_sound, self.handle_y_sound), handle_radius_sound)
                pygame.draw.circle(self.screen, GREEN, (self.handle_x_sfx, self.handle_y_sfx), handle_radius_sfx)

            # Hiển thị giá trị âm lượng
            volume_text_sound = self.font.render(f"SOUND: {int(self.volumeSound * 100)}%", True, WHITE)
            volume_text_sfx = self.font.render(f"SFX:       {int(self.volumeSFX * 100)}%", True, WHITE)
            self.screen.blit(volume_text_sound, (slider_x_sound, slider_y_sound - int(50*y_scale)))
            self.screen.blit(volume_text_sfx, (slider_x_sfx, slider_y_sfx - int(50*y_scale)))
            
            Gif.playGif()
            # Cập nhật màn hình
            pygame.display.flip()

# Load background
listBG = ['images/image_background/image_game_{}.jpg'.format(i) for i in range(1, 5)]

# Load âm thanh
pygame.mixer.pre_init()
pygame.mixer.init()
clickSound = pygame.mixer.Sound('sound_effect/beep4.ogg')
getPointSound = pygame.mixer.Sound('sound_effect/beep1.ogg')
wrongSound = pygame.mixer.Sound('sound_effect/wrong.mp3')
startScreenSound = pygame.mixer.Sound('sound_effect/music_background/introduction.wav')
TimeOutSound = pygame.mixer.Sound('sound_effect/ClockTick.mp3')
less_time = False
RingRingSound = pygame.mixer.SoundType('sound_effect/ringring.mp3')
listMusicBG = [f"sound_effect/music_background/music_{i}.mp3" for i in range(1, 5)]

def main(email):
    global WINDOWHEIGHT, WINDOWWIDTH, FPSCLOCK, DISPLAYSURF, BASICFONT, LIVESFONT, LEVEL, BOARDWIDTH, BOARDHEIGHT, BOXSIZEX, BOXSIZEY, XMARGIN, YMARGIN, unlocked_pokemon, x_scale, y_scale
    with open(f'{PATH}/saves/save_game/{email}_saved_collection.json', 'r') as file:
        unlocked_pokemon = json.load(file)

    # Khởi tạo Pygame và các tài nguyên cơ bản
    pygame.init()
    pygame.font.init()

    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    WINDOWWIDTH = pygame.display.Info().current_w
    WINDOWHEIGHT = pygame.display.Info().current_h
    x_scale = WINDOWWIDTH / BASE_WINDOWWIDTH
    y_scale = WINDOWHEIGHT / BASE_WINDOWHEIGHT

    print(WINDOWWIDTH, WINDOWHEIGHT)
    
    pygame.display.set_caption('Pikachu')
    BASICFONT = pygame.font.SysFont('comicsansms', 70)
    LIVESFONT = pygame.font.SysFont('comicsansms', int(45*x_scale))

    pygame.event.clear(pygame.MOUSEBUTTONUP)

    global savemenu, SettingGame, score_manager
    savemenu = SaveMenu(DISPLAYSURF, email)
    SettingGame = SettingMenu(WINDOWWIDTH, WINDOWHEIGHT, DISPLAYSURF)
    score_manager = Score(LIVESFONT, PATH)
    return

def MainGame(email):
    global startBG, FPSCLOCK, DISPLAYSURF, BASICFONT, LIVESFONT, LEVEL, BOARDWIDTH, BOARDHEIGHT, BOXSIZEX, BOXSIZEY, XMARGIN, YMARGIN, savemenu, SettingGame, score_manager

    startBG = pygame.image.load('images/image_background/introduction_image.jpg')
    startBG = pygame.transform.scale(startBG, (WINDOWWIDTH, WINDOWHEIGHT))
    while True:
        random.shuffle(listBG)
        random.shuffle(listMusicBG)
        LEVEL = 1

        # Hiển thị màn hình bắt đầu
        global action
        action = showStartScreen(email)
        pygame.event.clear(pygame.MOUSEBUTTONUP)  # Xóa sự kiện chuột sau khi nhận hành động

        # Hiển thị màn hình Option khi người chơi yêu cầu
        if action == "OPTION":
            action = SettingGame.Option()
            pygame.event.clear(pygame.MOUSEBUTTONUP)  # Xóa sự kiện chuột sau khi đóng option
            continue  # Quay lại màn hình Start sau khi chỉnh Option

        # Xử lý hành động từ màn hình chính
        if action == "LOG OUT":
            return "LOG OUT" # Trả về trạng thái LOG OUT cho ứng dụng
        
        elif action == "NEW GAME" :
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
            
        elif action == "LOAD GAME":
            savemenu.page = 1
            savemenu.appear()
            while savemenu.visible:
                for event in pygame.event.get():
                    saved_state = savemenu.load(event)
            if not saved_state:
                pygame.event.clear(pygame.MOUSEBUTTONUP)  # Xóa sự kiện chuột nếu không có trạng thái lưu
                continue  # Nếu không có trạng thái lưu, quay lại màn hình chính
        
        elif action == 'INSTRUCTIONS':
            scroll_offset = -int(200*y_scale)
            back_home = pygame.image.load('./images/image_button/buttonbackhome.png')
            back_home = pygame.transform.scale(back_home, (int(170*x_scale), int(100*y_scale)))
            back_home_rect = pygame.Rect(0,0,int(170*x_scale), int(100*y_scale))
            with open('./saves/instructions.txt', 'r', encoding='utf_8') as file:
                text_lines = file.readlines()
            back_to_home = False
            while not back_to_home:
                max_scroll = max(0, len(text_lines) * int(50*y_scale) - int(600*y_scale))
                for event in pygame.event.get():
                        
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_pos = event.pos
                        if back_home_rect.collidepoint(mouse_pos):
                            back_to_home = True
                            break
                        elif event.button == 4:  # Con lăn lên
                            scroll_offset = max(-int(200*y_scale), scroll_offset - int(50*y_scale))
                        elif event.button == 5:  # Con lăn xuống
                            scroll_offset = min(max_scroll, scroll_offset + int(50*y_scale))
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_UP:
                            scroll_offset = max(-200, scroll_offset - int(50*y_scale))
                        elif event.key == pygame.K_DOWN:
                            scroll_offset = min(max_scroll, scroll_offset + int(50*y_scale))
                        elif event.key == pygame.K_SPACE:
                            scroll_offset = min(max_scroll, scroll_offset + int(500*y_scale))
                if back_to_home:
                    break
                display_text(DISPLAYSURF, pygame.font.Font('./font_pixel.otf', int(50*x_scale)), text_lines, scroll_offset, int(150*y_scale), WINDOWHEIGHT - int(200*y_scale))
                DISPLAYSURF.blit(back_home, (0,0))
                pygame.display.flip()
                pygame.time.Clock().tick(30)  # Giới hạn FPS
            continue
            
        result = 'PLAY_AGAIN'
        # Vòng lặp chơi game
        while result == 'PLAY_AGAIN':
            if not saved_state:
                result = runGame(email, saved_state, new_game_option.level_choose, new_game_option.gen_choose, new_game_option.device_choose, size, listBG[0])
                temp = (new_game_option.level_choose, new_game_option.gen_choose, new_game_option.device_choose, size, listBG[0])
            else:
                result = runGame(email, saved_state, None, None, None, None, None)
                temp = (saved_state["level"], saved_state["gen"], saved_state["device"], tuple(saved_state["size"]), saved_state["bg"])
            if result == "MAIN_MENU":  # Nếu quay về StartScreen
                pygame.event.clear()
                pygame.event.clear(pygame.MOUSEBUTTONUP)
                break
            elif result == 'PLAY_AGAIN':
                saved_state = None
                new_game_option.level_choose, new_game_option.gen_choose, new_game_option.device_choose, size, listBG[0] = temp

            

        # Kiểm tra nếu quay lại màn hình chính
        pygame.event.clear(pygame.MOUSEBUTTONUP)
        if action == "MAIN_MENU":
            pygame.event.clear()
            pygame.time.wait(100)  # Xóa sự kiện chuột khi quay lại màn hình chính
            continue

class RunningBox:
    def __init__(self):
        self.runningbox = pygame.transform.scale(pygame.image.load('images/multiplier/runningbox.png'), (BOXSIZEX + 2, BOXSIZEY + 2))
        self.x = 1
        self.y = 1
        self.mode = 'normal'
    def draw(self):
        left, top = leftTopCoordsOfBox(self.x, self.y)
        runningboxRect = pygame.Rect(left, top, BOXSIZEX + 2, BOXSIZEY + 2)
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
        self.font = pygame.font.Font('font_pixel.otf', int(50*x_scale))
        self.fonts = pygame.font.Font('font_pixel.otf', int(40*x_scale))
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
            if self.size_choose == 3 and (self.row_text == '' or self.col_text == ''):
                return False
            if self.size_choose == 3 and self.row_text != '' and self.col_text != '':
                if (int(self.row_text) * int(self.col_text)) % 2 != 0:
                    return False

        return True

    def appear(self):
        self.visible = True
        self.return_home = False
        self.size_rects = []
        self.gen_rects = []
        self.level_rects = []
        self.device_rects = []
        nen = pygame.image.load('images/new_game/new_game_background.png')
        nen = pygame.transform.scale(nen, (WINDOWWIDTH, WINDOWHEIGHT))
        self.screen.blit(nen, (0, 0))
        size = ('8x8', '9x16', '12x20')
        x, y = int(200*x_scale), int(130*y_scale)
        self.screen.blit(self.font.render('SIZE', True, RED), (x + int(80*x_scale), y))
        for i in range(3):
            y += int(140*y_scale)
            if i == self.size_choose:
                color = BLUE
            else:
                color = BLACK
            pygame.draw.rect(self.screen, color, (x, y, int(300*x_scale), int(120*y_scale)), int(4*x_scale))
            self.size_rects.append(pygame.Rect(x, y, int(300*x_scale), int(120*y_scale)))
            self.screen.blit(self.font.render(size[i], True, BLACK), (x + int(150*x_scale) - self.font.render(size[i], True, BLACK).get_width()/2, y + int(14*y_scale))) 
        x, y = int(800*x_scale), int(130*y_scale)
        self.screen.blit(self.font.render('GEN', True, RED), (x + int(140*x_scale), y))
        for i in range(2):
            y += int(160*y_scale)
            x = int(680*x_scale)
            for j in range(2):
                pygame.draw.rect(self.screen, BLUE if self.gen_choose == 2 * i + j else BLACK, (x, y, int(300*x_scale), int(120*y_scale)), int(4*x_scale))
                self.gen_rects.append(pygame.Rect(x, y, int(300*x_scale), int(120*y_scale)))
                self.screen.blit(self.font.render(f'GEN{i*2 + j + 1}', True, BLACK), (x + int(150*x_scale) - self.font.render(f'GEN{i*2 + j + 1}', True, BLACK).get_width()/2, y + int(14*y_scale)))
                x += int(340*x_scale)
        x, y = int(1550*x_scale), int(130*y_scale)
        self.screen.blit(self.font.render('GAME MODE', True, RED), (x + int(120*x_scale) - self.font.render('GAME MODE', True, RED).get_width()//2, y))
        for i in range(5):
            y += int(110*y_scale)
            color = BLUE if i == self.level_choose else BLACK
            pygame.draw.rect(self.screen, color, (x, y, int(240*x_scale), int(80*y_scale)), int(4*x_scale))
            self.level_rects.append(pygame.Rect(x, y, int(240*x_scale), int(80*y_scale)))
            self.screen.blit(self.font.render(f'{i + 1}', True, BLACK), (x + int(120*x_scale) - self.font.render(f'{i + 1}', True, BLACK).get_width()/2, y - int(4*x_scale)))
        
        self.screen.blit(self.font.render('DEVICE:', True, RED), (int(1460*x_scale), int(770*y_scale)))
        device = ('MOUSE', 'KEYBOARD')
        x, y = int(940*x_scale), int(870*y_scale)
        for i in range(2):
            x += int(310*x_scale)
            color = BLUE if i == self.device_choose else BLACK
            pygame.draw.rect(self.screen, color, (x, y, int(300*x_scale), int(100*y_scale)), int(4*x_scale))
            self.device_rects.append(pygame.Rect(x, y, int(300*x_scale), int(100*y_scale)))
            self.screen.blit(self.font.render(device[i], True, BLACK), (x + int(150*x_scale) - self.font.render(device[i], True, BLACK).get_width()/2, y + int(0*y_scale)))
        x, y = int(140*x_scale), int(770*y_scale)
        
        pygame.draw.rect(self.screen, BLUE if self.size_choose == 3 else BLACK, (x, y, int(400*x_scale), int(200*y_scale)), int(4*x_scale))
        self.screen.blit(self.fonts.render('COL', True, RED), (x + int(20*x_scale), y + int(20*y_scale)))
        pygame.draw.rect(self.screen, BLUE if self.col_active else GRAY, (x + int(120*x_scale), y + int(30*y_scale), int(240*x_scale), int(60*y_scale)), int(4*x_scale))
        self.col_rect = pygame.Rect(x + int(120*x_scale), y + int(30*y_scale), int(240*x_scale), int(60*y_scale))
        self.screen.blit(self.fonts.render('ROW', True, RED), (x + int(20*x_scale), y + int(100*y_scale)))
        pygame.draw.rect(self.screen, BLUE if self.row_active else GRAY, (x + int(120*x_scale), y + int(110*y_scale), int(240*x_scale), int(60*y_scale)), int(4*x_scale))
        self.row_rect = pygame.Rect(x + int(120*x_scale), y + int(110*y_scale), int(240*x_scale), int(60*y_scale))
        self.size_rects.append(pygame.Rect(x, y, int(400*x_scale), int(200*y_scale)))
        self.screen.blit(self.fonts.render(self.col_text, True, BLACK), (x + int(180*x_scale), y + int(26*y_scale)))
        self.screen.blit(self.fonts.render(self.row_text, True, BLACK), (x + int(180*x_scale), y + int(106*y_scale)))
        
        home_button = pygame.image.load('images/new_game/home_button.png')
        home_button = pygame.transform.scale(home_button, (int(100*x_scale), int(100*y_scale)))
        self.home_button_rect = (pygame.Rect(WINDOWWIDTH - int(110*x_scale), int(10*y_scale), int(100*x_scale), int(100*y_scale)),)
        self.screen.blit(home_button, (WINDOWWIDTH - int(110*x_scale), int(10*y_scale), int(100*x_scale), int(100*y_scale)))
        
        pygame.draw.rect(self.screen, GRAY, (WINDOWWIDTH // 2 - int(80*x_scale), WINDOWHEIGHT - int(130*y_scale), int(160*x_scale), int(80*y_scale)), 4)
        self.play_button_rect = (pygame.Rect(WINDOWWIDTH // 2 - int(80*x_scale), WINDOWHEIGHT - int(130*y_scale), int(160*x_scale), int(80*y_scale)),)
        play_word = self.font.render('PLAY', True, RED if self.playable() else GRAY)
        self.screen.blit(play_word, (WINDOWWIDTH // 2 - play_word.get_width()//2, WINDOWHEIGHT - int(135*y_scale)))
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
    with open(f"{PATH}/saves/users.json", "r") as file:
        data = json.load(file)
        for user in data:
            if user["email"] == email:
                username = user["username"]
    cur_rect = None
    pixel_font = pygame.font.Font('font_pixel.otf', int(60 * x_scale))
    startScreenSound.set_volume(SettingGame.volumeSFX)
    if SettingGame.muteSFX:
        startScreenSound.play()
    pygame.event.clear()
    button_folder = 'images/button'
    new_game_button = pygame.image.load(f'{button_folder}/new_game_button.png')
    new_game_button = pygame.transform.scale(new_game_button, (int(400 * x_scale), int(120 * y_scale)))
    load_game_button = pygame.image.load(f'{button_folder}/load_game_button.png')
    load_game_button = pygame.transform.scale(load_game_button, (int(400 * x_scale), int(120 * y_scale)))
    rank_button = pygame.image.load(f'{button_folder}/rank_button.png')
    rank_button = pygame.transform.scale(rank_button, (int(400 * x_scale), int(120 * y_scale)))
    setting_button = pygame.image.load(f'{button_folder}/setting_button.png')
    setting_button = pygame.transform.scale(setting_button, (int(400 * x_scale), int(120 * y_scale)))
    log_out_button = pygame.image.load(f'{button_folder}/log_out_button.png')
    log_out_button = pygame.transform.scale(log_out_button, (int(300 * x_scale), int(120 * y_scale)))
    quit_game_button = pygame.image.load(f'{button_folder}/quit_game_button.png')
    quit_game_button = pygame.transform.scale(quit_game_button, (int(300 * x_scale), int(120 * y_scale)))
    collections_button = pygame.image.load(f'{button_folder}/collections_button.png')
    collections_button = pygame.transform.scale(collections_button, (int(400 * x_scale), int(120 * y_scale)))
    instructions_button = pygame.image.load(f'{button_folder}/instructions_button.png')
    instructions_button = pygame.transform.scale(instructions_button, (int(300 * x_scale), int(120 * y_scale)))
    buttons = [new_game_button, load_game_button, rank_button, setting_button, collections_button, log_out_button, instructions_button, quit_game_button]
    buttons_rect = []
    y = int(30 * y_scale)
    for i in range(4):
        buttons_rect.append((int(358*x_scale), y, buttons[i].get_width(), buttons[i].get_height()))
        y += buttons[i].get_height() + int(40*y_scale)

    # Định vị nút Collections
    buttons_rect.append((int(358*x_scale), WINDOWHEIGHT - int(150*y_scale), collections_button.get_width(), collections_button.get_height()))

    buttons_rect.append((WINDOWWIDTH - (buttons[5].get_width() + int(30*x_scale)), int(180*y_scale), buttons[5].get_width(), buttons[5].get_height()))
    buttons_rect.append((WINDOWWIDTH - (buttons[6].get_width() + int(30*x_scale)), WINDOWHEIGHT - int(350*y_scale), buttons[6].get_width(), buttons[6].get_height()))
    buttons_rect.append((WINDOWWIDTH - (buttons[7].get_width() + int(30*x_scale)), WINDOWHEIGHT - int(150*y_scale), buttons[7].get_width(), buttons[7].get_height()))
    buttons_Rect = tuple(pygame.Rect(i[0], i[1], i[2], i[3]) for i in buttons_rect)
    DISPLAYSURF.blit(startBG, (0, 0))
    for i in range(8):
        DISPLAYSURF.blit(buttons[i], (buttons_rect[i][0], buttons_rect[i][1]))
    DISPLAYSURF.blit(pixel_font.render('Welcome:', True, BLACK), (WINDOWWIDTH - (int(180*x_scale) + pixel_font.render('Welcome:', True, BLACK).get_width()//2), int(y_scale)))
    email_render = pixel_font.render(username, True, RED)
    email_render_x = WINDOWWIDTH - int(180*x_scale)
    if email_render.get_width() // 2 <= int(180*x_scale):
        email_render_x = email_render_x - email_render.get_width() // 2
    else:
        email_render_x = WINDOWWIDTH - email_render.get_width()
    DISPLAYSURF.blit(email_render, (email_render_x, int(70*y_scale)))
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
                    for i in range(8):
                        DISPLAYSURF.blit(buttons[i], (buttons_rect[i][0], buttons_rect[i][1]))
                    DISPLAYSURF.blit(pixel_font.render('Welcome:', True, BLACK), (WINDOWWIDTH - (int(180*x_scale) + pixel_font.render('Welcome:', True, BLACK).get_width()//2), int(y_scale)))
                    DISPLAYSURF.blit(email_render, (email_render_x, int(70*y_scale)))
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
                            RANKSCREEN.main(WINDOWWIDTH, WINDOWHEIGHT, DISPLAYSURF, x_scale, y_scale)
                        elif i == 3:# OPTION
                            return "OPTION"
                        elif i == 4:  # COLLECTIONS
                            showCollectionsMenu()  # Chuyển đến màn hình Collections
                            startScreenSound.set_volume(SettingGame.volumeSFX)
                            if SettingGame.muteSFX:
                                startScreenSound.play()
                            continue  # Sau khi thoát, quay lại vòng lặp menu chính

                        elif i == 5:  # LOG OUT
                            return "LOG OUT"
                        elif i == 6: #instructions
                            return "INSTRUCTIONS"
                        elif i == 7:  # QUIT
                            pygame.quit()
                            sys.exit()

        pygame.display.update()
        FPSCLOCK.tick(FPS)

def display_text(screen, font, text_lines, scroll_offset, y_min, y_max):
    BG = pygame.image.load('./images/button/instruction_back.png')
    BG = pygame.transform.scale(BG, (WINDOWWIDTH, WINDOWHEIGHT))
    screen.blit(BG, (0,0))
    y = -scroll_offset  # Bắt đầu từ vị trí cuộn
    for line in text_lines:
        if len(line)>=1 and y > y_min and y < y_max:  # Chỉ hiển thị các dòng trong khung nhìn
            extra = ''
            if line[:2] == '**':
                COLOR = RED
            elif line[0].isdigit():
                COLOR = BLUE
                extra = ' '*3
            elif line[:4] == '- **':
                COLOR = BLUE
                extra = ' '*3
            else:
                COLOR = BLACK
                extra = ' '*6
            rendered_text = font.render(extra + line.strip(), True, COLOR)
            screen.blit(rendered_text, (int(120*x_scale), y))
        y += int(50*y_scale)  # Khoảng cách giữa các dòng

def load_poke_images(gen_folder):
    """Tải danh sách ảnh từ thư mục tương ứng với Gen."""
    global POKES_DICT, LISTPOKES, NUMPOKES, BOXSIZEX, BOXSIZEY
    path = PATH + f'/images/images_icon/{gen_folder}/'
    if not os.path.exists(path):
        raise FileNotFoundError(f"Folder {path} không tồn tại!")

    LISTPOKES = os.listdir(path)
    NUMPOKES = len(LISTPOKES)
    POKES_DICT = {}

    for i in range(len(LISTPOKES)):
        POKES_DICT[i + 1] = pygame.transform.scale(
            pygame.image.load(path + LISTPOKES[i]),
            (BOXSIZEX, BOXSIZEY)
        )
    print(f"Loaded {NUMPOKES} heroes from {gen_folder}.")

def runGame(email, saved_state, level, gen, device, size, randomBG):
    
    global update_map_name
    update_map_name = None
    clickSound.set_volume(SettingGame.volumeSFX)
    getPointSound.set_volume(SettingGame.volumeSFX)
    wrongSound.set_volume(SettingGame.volumeSFX)
    
    global font
    font = pygame.font.Font('font_pixel.otf', int(30*x_scale))

    # Tải trạng thái hoặc khởi tạo mặc định
    # saved_state = load_game_state(email)
    global mainBoard, LEVEL, LIVES, GAMETIME, TIMEBONUS, STARTTIME, lastTimeGetPoint, hint, mainBoard, firstSelection, clickedBoxes, settings, action, less_time
    
    settings = Settings(DISPLAYSURF)
    
    settings.save_callback = lambda: save_game_state(email, mainBoard, LEVEL, LIVES, GAMETIME, TIMEBONUS, STARTTIME, BG, gen, device, size, name)

    # Button Swap, Hint and add Time
    imageHint = pygame.image.load("images/swap_and_hint/hint.png")
    imageHint = pygame.transform.scale(imageHint, (int(70*x_scale), int(70*y_scale)))
    imageSwap = pygame.image.load("images/swap_and_hint/swap.png")
    imageSwap = pygame.transform.scale(imageSwap, (int(70*x_scale), int(70*y_scale)))
    imageClock = pygame.image.load("images/swap_and_hint/clock.png")
    imageClock = pygame.transform.scale(imageClock, (int(70*x_scale), int(70*y_scale)))
    imageHintRect = imageHint.get_rect(topleft = (int(30*x_scale), int(120*y_scale)))
    imageSwapRect = imageSwap.get_rect(topleft = (int(30*x_scale), int(210*y_scale)))
    imageClockRect = imageClock.get_rect(topleft = (int(30*x_scale), int(300*y_scale)))
    hintPressed = False
    
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
    boxx, boxy = 0, 0
    
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
                    if SettingGame.muteSFX:
                        clickSound.play()
                else:  # Lần click thứ hai
                    path = bfs(mainBoard, firstSelection[1], firstSelection[0], boxy, boxx)
                    if path:  # Nếu tìm được đường nối
                        # Lấy chỉ số Pokémon từ mainBoard tại các ô đã chọn
                        pokemon_index = mainBoard[firstSelection[1]][firstSelection[0]]

                        # Kiểm tra xem cặp này đã có hay chưa và lưu lại
                        if LISTPOKES[pokemon_index - 1] not in unlocked_pokemon:
                            unlocked_pokemon.append(LISTPOKES[pokemon_index - 1])
                            with open(f'{PATH}/saves/save_game/{email}_saved_collection.json', 'w') as file:
                                json.dump(unlocked_pokemon, file)

                            # Thêm thông báo vào hàng đợi
                            message = f"New Pokémon collected!"
                            add_notification(message)

                        if SettingGame.muteSFX:
                            getPointSound.play()
                        mainBoard[firstSelection[1]][firstSelection[0]] = 0
                        mainBoard[boxy][boxx] = 0
                        drawPath(mainBoard, path)
                        TIMEBONUS += 1
                        lastTimeGetPoint = time.time()
                        mainBoard = alterBoardWithLevel(mainBoard, firstSelection[1], firstSelection[0], boxy, boxx, LEVEL)
                        score_manager.increase(10)

                    else:  # Nếu không tìm được đường nối
                        if SettingGame.muteSFX:
                            wrongSound.play()

                    # Reset trạng thái sau lần click thứ hai
                    clickedBoxes = []
                    firstSelection = None
    
    global BOARDHEIGHT, BOARDWIDTH, XMARGIN, YMARGIN, BOXSIZEX, BOXSIZEY
    size = saved_state["size"] if saved_state else size
    BOARDWIDTH, BOARDHEIGHT = size[0] + 2, size[1] + 2
    BOXSIZEX, BOXSIZEY = int(1700*x_scale) // BOARDWIDTH, int(1000*y_scale) // BOARDHEIGHT
    if BOXSIZEX * 1.25 < BOXSIZEY:
        BOXSIZEY = int(BOXSIZEX * 1.25)
    else:
        BOXSIZEX = int(BOXSIZEY // 1.25)
    XMARGIN = (WINDOWWIDTH - (BOXSIZEX * BOARDWIDTH)) // 2
    YMARGIN = (WINDOWHEIGHT - (BOXSIZEY * BOARDHEIGHT)) // 2 + int(40*y_scale)

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
        score = saved_state["score"]
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
        score = 0
    load_poke_images(f'Gen{int(gen) + 1}')
    score_manager.score = score
    global Background
    Background = pygame.image.load(BG)
    Background = pygame.transform.scale(Background, (WINDOWWIDTH, WINDOWHEIGHT))
    clickedBoxes = []
    firstSelection = None
    mousex, mousey = 0, 0
    lastTimeGetPoint = time.time()
    randomMusicBG = listMusicBG[LEVEL - 1]
    pygame.mixer.music.load(randomMusicBG)
    pygame.mixer.music.set_volume(SettingGame.volumeSound)
    pygame.mixer.music.play(-1, 0.0)
    if not SettingGame.muteSound:
        pygame.mixer.music.pause()
    running_box = RunningBox()
    if mainBoard[1][1] == 0:
        running_box.find_nearest(mainBoard)
    while not restart_flag:  # Vòng lặp chính sẽ thoát khi restart_flag được bật
        # Check game
        if isGameComplete(mainBoard):
            restart_flag = not restart_flag
            pygame.mixer.music.stop()
            if name == None:
                if list(size) in ([8,8], [16,9], [20,12]):
                    new_map_name = EnterMapName(WINDOWWIDTH // 2 - int(500*x_scale), WINDOWHEIGHT // 2 - int(250*y_scale), int(1000*x_scale), int(500*y_scale), DISPLAYSURF, email, False)
                    while True:
                        name = new_map_name.appear()
                        if name:
                            break
            return showGameOverScreen(mainBoard, name, email, size, LEVEL, gen, device, score_manager.score)
        # Vẽ hint
        hint = getHint(mainBoard)
        if not hint:
            resetBoard(mainBoard)
            continue
        
        if update_map_name:
            name = update_map_name
            update_map_name = None
        DISPLAYSURF.blit(Background, (0, 0))
        imageLiveGame = pygame.image.load(f"images/swap_and_hint/image_heart/heart_{LIVES}.png")
        imageLiveGame = pygame.transform.scale(imageLiveGame, (int(100*x_scale), int(33*y_scale)))
        DISPLAYSURF.blit(imageLiveGame, (int(20*x_scale), int(70*y_scale)))
        drawBoard(mainBoard)
        drawClickedBox(mainBoard, clickedBoxes)
        drawTimeBar()
        drawInfo(name, device, gen, LEVEL, size)

        # Kiểm tra và vẽ thông báo (nếu có)
        draw_notifications(DISPLAYSURF)

        DISPLAYSURF.blit(imageHint, (int(30*x_scale), int(120*y_scale)))
        DISPLAYSURF.blit(imageSwap, (int(30*x_scale), int(210*y_scale)))
        DISPLAYSURF.blit(imageClock, (int(30*x_scale), int(300*y_scale)))
        
        # Kiểm tra và đặt lại hệ số nhân (nếu cần)
        score_manager.reset_multiplier()
        
        # Vẽ điểm số ở góc phải
        score_manager.draw(DISPLAYSURF)
        # drawLives()
        
        mouseClicked = False
        enterPress = False
        # Vòng lặp sự kiện
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            
            elif event.type == pygame.MOUSEMOTION:
                mousePos = event.pos
                if imageHintRect.collidepoint(mousePos):
                    imageHint.set_alpha(100)
                else:
                    imageHint.set_alpha(255)
                if imageSwapRect.collidepoint(mousePos):
                    imageSwap.set_alpha(100)
                else:
                    imageSwap.set_alpha(255)
                if imageClockRect.collidepoint(mousePos):
                    imageClock.set_alpha(100)
                else:
                    imageClock.set_alpha(255)
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mousePos = event.pos
                if imageHintRect.collidepoint(mousePos):
                    if LIVES > 0:
                        LIVES -= 1
                        hintPressed = True
                    else:
                        restart_flag = not restart_flag
                        pygame.mixer.music.stop()
                        return showGameOverScreen(mainBoard, gamename=name, email=email)
                    
                if imageSwapRect.collidepoint(mousePos):
                    resetBoard(mainBoard)
                    if LIVES > 0:
                        LIVES -= 1
                    else:
                        restart_flag = not restart_flag
                        pygame.mixer.music.stop()
                        return showGameOverScreen(mainBoard, gamename=name, email=email)
                if imageClockRect.collidepoint(mousePos):
                    if time.time() - STARTTIME - 30 - TIMEBONUS> 0:
                        STARTTIME += 30
                    else:
                        STARTTIME += time.time() - STARTTIME
                    if GAMETIME - (time.time() - STARTTIME - TIMEBONUS) < 40:
                        TimeOutSound.stop()
                        TimeOutSound.play()
                    if LIVES > 0:
                        LIVES -= 1
                    else:
                        restart_flag = not restart_flag
                        pygame.mixer.music.stop()
                        return showGameOverScreen(mainBoard, gamename=name, email=email)
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
                elif event.key == pygame.K_h:
                    if LIVES > 0:
                        LIVES -= 1
                        hintPressed = True
                    else:
                        restart_flag = not restart_flag
                        pygame.mixer.music.stop()
                        return showGameOverScreen(mainBoard, gamename=name, email=email)
                elif event.key == pygame.K_r:
                    resetBoard(mainBoard)
                    if LIVES > 0:
                        LIVES -= 1
                    else:
                        restart_flag = not restart_flag
                        pygame.mixer.music.stop()
                        return showGameOverScreen(mainBoard, gamename=name, email=email)
                elif event.key == pygame.K_t:
                    if time.time() - STARTTIME - 30 - TIMEBONUS> 0:
                        STARTTIME += 30
                    else:
                        STARTTIME += time.time() - STARTTIME
                    if GAMETIME - (time.time() - STARTTIME - TIMEBONUS) < 40:
                        TimeOutSound.stop()
                        TimeOutSound.play()
                    if LIVES > 0:
                        LIVES -= 1
                    else:
                        restart_flag = not restart_flag
                        pygame.mixer.music.stop()
                        return showGameOverScreen(mainBoard, gamename=name, email=email)
                    
        print(boxx, boxy)
        # Nếu Settings bị đóng, xóa các sự kiện chuột dư thừa
        if not settings.visible and mouseClicked:
            pygame.event.clear(pygame.MOUSEBUTTONUP)  # Xóa sự kiện chuột dư thừa
        # Vẽ nền và các thành phần chính
        if settings.start_pause:
            STARTTIME += time.time() - settings.start_pause
            lastTimeGetPoint += time.time() - settings.start_pause
            settings.start_pause = None

        # Kiểm tra thời gian hoặc trạng thái game
        if not settings.visible:
            settings.draw()
            ###
            if time.time() - STARTTIME > GAMETIME + TIMEBONUS:
                RingRingSound.play()
                return showGameOverScreen(mainBoard, gamename=name, email=email)
            if GAMETIME - (time.time() - STARTTIME - TIMEBONUS) < 40:
                if less_time == False and not settings.visible:
                    TimeOutSound.play()
                    less_time = True
            else:
                if less_time == True:
                    TimeOutSound.stop()
                    less_time = False
            if time.time() - lastTimeGetPoint >= GETHINTTIME:
                drawHint(hint)
            if device == 0:
                boxx, boxy = getBoxAtPixel(mousex, mousey)
                
            else:
                running_box.draw()
                boxx, boxy = running_box.active()
            if logic_game(boxx, boxy, mouseClicked, enterPress) == 'WIN':
                restart_flag = True
                
        # Vẽ menu Settings nếu mở
        settings.draw()
        if hintPressed:
            drawHint(hint)   
            if time.time() - lastTimeGetPoint >= GETHINTTIME or getHint(mainBoard) != hint:
                hintPressed = False   
        pygame.display.update()
        FPSCLOCK.tick(FPS)

    pygame.mixer.music.stop()
    pygame.event.clear(pygame.MOUSEBUTTONUP)
    pygame.event.clear()
    return "MAIN_MENU" 

#Lưu game và load game
def save_game_state(email, mainBoard, LEVEL, LIVES, GAMETIME, TIMEBONUS, STARTTIME, BG, gen, device, size, map_name):
    """Lưu trạng thái hiện tại của trò chơi vào tệp JSON cho tài khoản cụ thể."""
    if not map_name:
        savemenu.back = 'back'
        savemenu.page = 1
        savemenu.appear()
        while True:
            for event in pygame.event.get():
                savemenu.save_game(event, mainBoard, LEVEL, LIVES, GAMETIME, TIMEBONUS, STARTTIME, BG, gen, device, size, map_name)
            if savemenu.visible == False:
                # settings.appear_again = True
                break
    else:
        temp_image = pygame.image.load('saves/save_game/temporary.png')
        with open(f'saves/save_game/{email}_saved_game.json', 'r', encoding='utf_8') as file:
            games = json.load(file)
            for game in games:
                if games[game]['name'] == map_name:
                    games[game] = {
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
                    "start_time": time.time() - STARTTIME,  # Thời gian đã trôi qua
                    "score": score_manager.score
                }
                    pygame.image.save(temp_image, f'saves/save_game/{email}_saved{int(game)}.png')
        with open(f'saves/save_game/{email}_saved_game.json', "w") as save_file:
            json.dump(games, save_file, indent=4)
        settings.saved = True

def drawInfo(name, device, gen, level, size):
    fonts = pygame.font.Font('font_pixel.otf', int(30*x_scale))
    name_render = pygame.font.Font('font_pixel.otf', int(40*x_scale)).render(name if name else 'NO NAME MAP', True, BLUE if name else RED)
    DISPLAYSURF.blit(name_render, (WINDOWWIDTH//2 - name_render.get_width() // 2, int(60*y_scale)))
    DISPLAYSURF.blit(fonts.render(f'Map size: {size[0]}x{size[1]}', True, RED), (int(20*x_scale), WINDOWHEIGHT - int(50*y_scale)))
    delta_x = fonts.render(f'Map size: {size[0]}x{size[1]}', True, RED).get_width()
    DISPLAYSURF.blit(fonts.render(f"Device: {'MOUSE' if device == 0 else 'KEYBOARD'}", True, RED), (int(40*x_scale) + delta_x, WINDOWHEIGHT - int(50*y_scale)))
    delta_x += fonts.render(f"Device: {'MOUSE' if device == 0 else 'KEYBOARD'}", True, RED).get_width() + int(20*x_scale)
    DISPLAYSURF.blit(fonts.render(f'Gen: {int(gen) + 1}', True, RED), (int(40*x_scale) + delta_x, WINDOWHEIGHT - int(50*y_scale)))
    delta_x += fonts.render(f'Gen: {gen}', True, RED).get_width() + int(20*x_scale)
    DISPLAYSURF.blit(fonts.render(f'Game Mode: {int(level) + 1}', True, RED), (int(40*x_scale) + delta_x, WINDOWHEIGHT - int(50*y_scale)))

def getRandomizedBoard():
    """Để đảm bảo bàn chơi không bị shuffle lại quá nhiều lần, hàm tạo bảng random sẽ ưu tiên vào số lượng Pokemon trùng lặp
    thay vì số lượng loại Pokemon xuất hiện trên bàn chơi."""
    pokes_on_board = (BOARDHEIGHT - 2)*(BOARDWIDTH - 2)
    pokes_index = list(range(1, 37)) #Vì mỗi gen có 36 pokemon
    random.shuffle(pokes_index) #Xáo để tạo sự ngẫu nhiên khi lấy Pokemon
    list_pokemons = []
    repeat = 2
    if pokes_on_board >= 64: #Bảng có từ 64 Pokemon trở lên thì số trùng lặp của mỗi Pokemon là từ 4 trở lên
        for repeat in range(4, pokes_on_board + 1, 2):
            if pokes_on_board // repeat <= 36: #Kiểm soát biến số repeat để số loại Pokemon xuất hiện phải nhỏ hơn hoặc bằng 36
                break
    for i in pokes_index:
        list_pokemons.extend([i] * repeat) #Tạo ListPokemon ngẫu nhiêu lần 1 - Lấy các pokemon ngẫu nhiên
        if len(list_pokemons) >= pokes_on_board:
            break #Dừng sớm để bớt tốn bộ nhớ
    list_pokemons = list_pokemons[:pokes_on_board] #Vì có thể bị dư số lượng Pokemon <= repeat nên sẽ lượt bỏ vài lần trùng lặp của Pokemon cuối
    random.shuffle(list_pokemons) #Tạo list ngẫu nhiên lần 2 - Trộn vị trí

    board = [[0 for _ in range(BOARDWIDTH)] for _ in range(BOARDHEIGHT)]
    # Tạo bảng với viền 0 xung quanh
    k = 0
    for i in range(1, BOARDHEIGHT - 1):
        for j in range(1, BOARDWIDTH - 1):
            board[i][j] = list_pokemons[k]
            k += 1
    return board

def leftTopCoordsOfBox(boxx, boxy):
    left = boxx * BOXSIZEX + XMARGIN
    top = boxy * BOXSIZEY + YMARGIN
    return left, top

def getBoxAtPixel(x, y):
    if x <= XMARGIN or x >= WINDOWWIDTH - XMARGIN or y <= YMARGIN or y >= WINDOWHEIGHT - YMARGIN:
        return 0, 0
    return (x - XMARGIN) // BOXSIZEX, (y - YMARGIN) // BOXSIZEY

def drawBoard(board, clickedBoxes=[]):
    for boxx in range(len(board[0])):
        for boxy in range(len(board)):
            left, top = leftTopCoordsOfBox(boxx, boxy)
            if board[boxy][boxx] != 0:  # Nếu ô không trống
                DISPLAYSURF.blit(POKES_DICT[board[boxy][boxx]], (left, top))
                
                # Áp dụng hiệu ứng nhạt màu nếu ô nằm trong clickedBoxes
                if (boxx, boxy) in clickedBoxes:
                    s = pygame.Surface((BOXSIZEX, BOXSIZEY))
                    s.set_alpha(100)  # Đặt độ trong suốt (0-255)
                    s.fill((255, 255, 255))  # Phủ màu trắng nhạt
                    DISPLAYSURF.blit(s, (left, top))

def drawHighlightBox(board, boxx, boxy):
    # Lấy tọa độ góc trên bên trái của ô
    left, top = leftTopCoordsOfBox(boxx, boxy)
    
    # Vẽ một khung chữ nhật màu đỏ đậm quanh ô (highlight)
    pygame.draw.rect(DISPLAYSURF, HIGHLIGHTCOLOR, 
                     (left - 2, top - 2, BOXSIZEX + 4, BOXSIZEY + 4), 4)  # Độ dày 4 pixel

def drawClickedBox(board, clickedBoxes):
    for boxx, boxy in clickedBoxes:
        left, top = leftTopCoordsOfBox(boxx, boxy)
        boxRect = pygame.Rect(left, top, BOXSIZEX, BOXSIZEY)
        image = POKES_DICT[board[boxy][boxx]].copy()

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
    return tuple([left + BOXSIZEX // 2, top + BOXSIZEY // 2])

def drawPath(board, path):
    for i in range(len(path) - 1):
        startPos = getCenterPos(path[i])
        endPos = getCenterPos(path[i + 1])
        pygame.draw.line(DISPLAYSURF, RED, startPos, endPos, 4)
    pygame.display.update()
    pygame.time.wait(300)

def drawTimeBar():
    TIMEBAR_LENGTH = int(TIMEBAR_LENGTH*x_scale)
    TIMEBAR_WIDTH = int(TIMEBAR_WIDTH*y_scale)
    barPos = (WINDOWWIDTH // 2 - TIMEBAR_LENGTH // 2, int(8*y_scale))
    barSize = (int(TIMEBAR_LENGTH*x_scale), int(TIMEBAR_WIDTH*y_scale))
    progress = 1 - ((time.time() - STARTTIME - TIMEBONUS) / GAMETIME)

    pygame.draw.rect(DISPLAYSURF, borderColor, (barPos, barSize), 1)
    innerPos = (barPos[0] + int(2*x_scale), barPos[1] + int(2*y_scale))
    innerSize = ((barSize[0] - int(4*x_scale)) * progress, barSize[1] - int(4*y_scale))
    pygame.draw.rect(DISPLAYSURF, barColor, (innerPos, innerSize))

def showGameOverScreen(board, gamename = None, email = None, size = None, gamemode = None, gen = None, device = None, score = None):
    TimeOutSound.stop()
    global LIVES, DISPLAYSURF, mainBoard
    LIVES = 3
    mainBoard = getRandomizedBoard()
    result = isGameComplete(board)
    imageBack = pygame.image.load("images/image_button/no.png")
    imageBack = pygame.transform.scale(imageBack, (int(300*x_scale), int(164*y_scale)))
    imageBackRect = imageBack.get_rect(topleft = (int(600*x_scale), int(800*y_scale)))
    imagePlay = pygame.image.load("images/image_button/yes.png")
    imagePlay = pygame.transform.scale(imagePlay, (int(300*x_scale), int(164*y_scale)))
    imagePlayRect = imagePlay.get_rect(topleft = (int(1100*x_scale), int(800*y_scale)))
    running = True
    if email:
        with open(os.path.join("saves/save_game", f"{email}_saved_game.json"), 'r') as save_file:
            saved_game = json.load(save_file)
            for j in saved_game:
                if saved_game[j]['name'] == gamename:
                    i = j
                    break
            try:
                del saved_game[str(i)]
                os.remove(f'saves/save_game/{email}_saved{i}.png')
            except:
                pass
        with open(os.path.join("saves/save_game", f"{email}_saved_game.json"), 'w') as save_file:
            json.dump(saved_game, save_file, indent=4)
    if result:
        if list(size) in ([8,8], [16,9], [20,12]):
            strsize = f'{size[0]}x{size[1]}'
            with open(f"{PATH}/saves/rank.json", 'r') as file:
                data = json.load(file)
            with open(f"{PATH}/saves/users.json", "r") as file:
                user_data = json.load(file)
            for user in user_data:
                if user['email'] == email:
                    username = user['username']
                    break
            if gamename != None:
                cur_game = {
                    'namegame':gamename,
                    'user':username,
                    'size':strsize,
                    'gamemode':str(gamemode + 1),
                    'gen':str(gen + 1),
                    'device': 'Mouse' if device == 0 else 'Keyboard',
                    'score': score
                }
                data.append(cur_game)
                with open(f"{PATH}/saves/rank.json", 'w') as filesave:
                    json.dump(data, filesave, indent=4)
        pygame.mixer.music.load("sound_effect/music_background/win.mp3")
        if SettingGame.muteSFX:
            pygame.mixer.music.play()
        imageWin = pygame.image.load("images/end_game/win.png")
        imageWin = pygame.transform.scale(imageWin, (int(800*x_scale), int(412*y_scale)))
        imagePlayAgain = pygame.image.load("images/end_game/playagain.png")
        imagePlayAgain = pygame.transform.scale(imagePlayAgain, (int(600*x_scale), int(252*y_scale)))
        
        while running:
            DISPLAYSURF.blit(Background, (0, 0))
            DISPLAYSURF.blit(imageWin, (int(600*x_scale), int(60*y_scale)))
            DISPLAYSURF.blit(imagePlayAgain, (int(700*x_scale), int(500*y_scale)))
            DISPLAYSURF.blit(imageBack, (int(600*x_scale), int(800*y_scale)))
            DISPLAYSURF.blit(imagePlay, (int(1100*x_scale), int(800*y_scale)))
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    
                elif event.type == pygame.MOUSEMOTION:
                    mousePos = event.pos
                    if imagePlayRect.collidepoint(mousePos):
                        imagePlay.set_alpha(100)
                    else:
                        imagePlay.set_alpha(255)
                    if imageBackRect.collidepoint(mousePos):
                        imageBack.set_alpha(100)
                    else:
                        imageBack.set_alpha(255) 
                
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mousePos = event.pos
                    if imagePlayRect.collidepoint(mousePos):
                        return "PLAY_AGAIN"
                    if imageBackRect.collidepoint(mousePos):
                        running = False
                        pygame.event.clear()
                        pygame.event.clear(pygame.MOUSEBUTTONUP)
                        return "MAIN_MENU"
                        
            pygame.display.flip()
            
    else:
        pygame.mixer.music.load("sound_effect/music_background/lose.mp3")
        if SettingGame.muteSFX:
            pygame.mixer.music.play()
        imageTryAgain = pygame.image.load("images/end_game/tryagain.png").convert_alpha()
        imageTryAgain = pygame.transform.scale(imageTryAgain, (int(600*x_scale), int(336*y_scale)))
        imageTryAgain.set_colorkey((255, 0, 255))
        imageLose = pygame.image.load("images/end_game/gameover.png")
        imageLose = pygame.transform.scale(imageLose, (int(700*x_scale), int(416*y_scale)))
        
        while running:
            DISPLAYSURF.blit(Background, (0, 0))
            DISPLAYSURF.blit(imageBack, (int(600*x_scale), int(800*y_scale)))
            DISPLAYSURF.blit(imagePlay, (int(1100*x_scale), int(800*y_scale)))
            DISPLAYSURF.blit(imageTryAgain, (int(700*x_scale), int(500*y_scale)))
            DISPLAYSURF.blit(imageLose, (int(650*x_scale), int(60*y_scale)))
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                elif event.type == pygame.MOUSEMOTION:
                    mousePos = event.pos
                    if imagePlayRect.collidepoint(mousePos):
                        imagePlay.set_alpha(100)
                    else:
                        imagePlay.set_alpha(255)
                    if imageBackRect.collidepoint(mousePos):
                        imageBack.set_alpha(100)
                    else:
                        imageBack.set_alpha(255)   
                
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mousePos = event.pos
                    if imagePlayRect.collidepoint(mousePos):
                        return "PLAY_AGAIN"
                    if imageBackRect.collidepoint(mousePos):
                        running = False
                        pygame.event.clear()
                        pygame.event.clear(pygame.MOUSEBUTTONUP)
                        return "MAIN_MENU"
                        
            pygame.display.flip()

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
        pygame.draw.rect(DISPLAYSURF, GREEN, (left, top, BOXSIZEX, BOXSIZEY), 4)

def resetBoard(board):
    pokesOnBoard = []
    repeatedList = set()
    for boxy in range(BOARDHEIGHT):
        for boxx in range(BOARDWIDTH):
            if board[boxy][boxx] != 0:
                pokesOnBoard.append(board[boxy][boxx])
                repeatedList.add(board[boxy][boxx])
    if len(repeatedList) <= 1:
        return board
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

class SaveMenu:
    def __init__(self, screen, email):
        self.visible = False
        self.screen = screen
        self.height = WINDOWHEIGHT
        self.width = WINDOWWIDTH
        delta_w = (WINDOWWIDTH - int(1500*x_scale)) // 4
        delta_h = (WINDOWHEIGHT - int(692*y_scale)) // 3
        
        self.memory_rects = ((delta_w , int(130*x_scale) + delta_h, int(500*x_scale), int(284*y_scale)), (delta_w*2 + int(500*x_scale) , int(130*x_scale) + delta_h, int(500*x_scale), int(284*y_scale)), (delta_w*3 + int(1000*x_scale) , int(130*x_scale) + delta_h, int(500*x_scale), int(284*y_scale)), (delta_w , int(414*y_scale) + delta_h*2, int(500*x_scale), int(284*y_scale)), (delta_w*2 + int(500*x_scale) , int(414*y_scale) + delta_h*2, int(500*x_scale), int(284*y_scale)), (delta_w*3 + int(1000*x_scale), int(414*y_scale) + delta_h*2, int(500*x_scale), int(284*y_scale)))
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
        self.font = pygame.font.Font('font_pixel.otf', int(50*x_scale))
        self.fonts = pygame.font.Font('font_pixel.otf', int(40*x_scale))
        self.next_page = pygame.image.load('images/save_menu/next_page.png')
        self.next_page = pygame.transform.scale(self.next_page, (int(100*x_scale),int(100*y_scale)))
        self.next_page_rect = pygame.Rect(WINDOWWIDTH // 2 + int(120*x_scale), WINDOWHEIGHT - int(110*y_scale), int(100*x_scale),int(100*y_scale))
        self.prev_page = pygame.image.load('images/save_menu/previous_page.png')
        self.prev_page = pygame.transform.scale(self.prev_page, (int(100*x_scale),int(100*y_scale)))
        self.prev_page_rect = pygame.Rect(WINDOWWIDTH // 2 - int(120*x_scale), WINDOWHEIGHT - int(110*y_scale), int(100*x_scale),int(100*y_scale))
        self.is_drawed = False
        self.cur_rect = None
        self.back = 'home'
    def appear(self):
        self.visible = True
        self.BG = pygame.image.load('images/save_menu/savemenu.png')
        self.BG = pygame.transform.scale(self.BG, (WINDOWWIDTH, WINDOWHEIGHT))
        self.screen.blit(self.BG, (0,0))
        with open(os.path.join("saves/save_game", f"{self.email}_saved_game.json"), "r") as save_file:
            saved_game = json.load(save_file)
            self.memories = [None for _ in range(6 * self.maxpage)]
            for i in saved_game:
                self.memories[int(i)] = f'saves/save_game/{self.email}_saved{i}.png'
        for i in range(6):
            x,y,w,h = self.memory_rects[i]
            pygame.draw.rect(self.screen, GRAY, pygame.Rect(x,y,w,h), border_radius=1)
        delete_icon = pygame.image.load('images/save_menu/delete.png')
        delete_icon = pygame.transform.scale(delete_icon, (int(100*x_scale),int(100*y_scale)))
        self.delete_rects = [None for _ in range(6)]
        for i in range(6 * (self.page - 1), 6 * self.page):
            if self.memories[i]:
                image = pygame.image.load(self.memories[i])
                image = pygame.transform.scale(image, (int(500*x_scale) - 2, int(284*y_scale) - 2))
                self.screen.blit(image, (self.memory_rects[i % 6][0] + 1, self.memory_rects[i % 6][1] + 1))
                delete_icon_rect = delete_icon.get_rect()
                delete_icon_rect.topleft = (self.memory_rects[i % 6][0], self.memory_rects[i % 6][1])
                self.screen.blit(delete_icon, delete_icon_rect)
                self.delete_rects[i % 6] = delete_icon_rect
                map_name = self.font.render(saved_game[str(i)]['name'], True, BLACK)
                self.screen.blit(map_name, (self.memory_rects[i % 6][0] + int(250*x_scale) - map_name.get_width()/2, self.memory_rects[i % 6][1] + int(280*y_scale)))
        for i in range(6 * (self.page - 1), 6 * self.page):
            if self.memories[i]:
                color = RED
            else:
                color = BLACK
            number = self.font.render(str(i + 1), True, color)
            self.screen.blit(number, (self.memory_rects[i % 6][0] + int(250*x_scale) - number.get_width()//2, self.memory_rects[i % 6][1] + int(142*y_scale) - number.get_height()//2))
        if self.page > 1:
            self.screen.blit(self.prev_page, tuple(self.prev_page_rect))
        if self.page < self.maxpage:
            self.screen.blit(self.next_page, tuple(self.next_page_rect))
                
        self.out = pygame.Rect(WINDOWWIDTH - int(180*x_scale), WINDOWHEIGHT - int(100*y_scale), int(150*x_scale), int(75*y_scale))
        pygame.draw.rect(self.screen, BLUE, self.out)
        back_word = self.fonts.render('HOME' if self.back == 'home' else 'BACK', True, BLACK)
        self.screen.blit(back_word, (WINDOWWIDTH - int(105*x_scale) - back_word.get_width()//2, WINDOWHEIGHT - int(100*y_scale)))
        pygame.display.flip()
    
    def save_game(self, event, mainBoard, LEVEL, LIVES, GAMETIME, TIMEBONUS, STARTTIME, BG, gen, device, size, map_name):
        self.back = 'back'
        temp_image = pygame.image.load('saves/save_game/temporary.png')
        # Đảm bảo thư mục lưu trữ game tồn tại
        save_folder = "saves/save_game"
        if not os.path.exists(save_folder):
            os.makedirs(save_folder)
        
        delete_icon = pygame.image.load('images/save_menu/delete.png')
        delete_icon = pygame.transform.scale(delete_icon, (int(100*x_scale),int(100*y_scale)))
        if event.type == pygame.MOUSEMOTION:
            self.mouse_on(event)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            for i, box in enumerate(self.memory_boxes):
                if self.delete_rects[i] and self.delete_rects[i].collidepoint(mouse_pos):
                    
                    self.delete(i + (self.page - 1) * 6)
                    
                elif box and box.collidepoint(mouse_pos):
                    enter_map_name = EnterMapName(WINDOWWIDTH // 2 - int(500*x_scale), WINDOWHEIGHT // 2 - int(250*y_scale), int(1000*x_scale), int(500*y_scale), DISPLAYSURF, self.email)
                    map_name = None
                    while not map_name:
                        map_name = enter_map_name.appear()
                        if enter_map_name.visible == False:
                            break
                            
                    if enter_map_name.visible:
                        pygame.image.save(temp_image, f'saves/save_game/{self.email}_saved{i + (self.page - 1) * 6}.png')
                        with open(f'saves/save_game/{self.email}_saved_game.json', 'r', encoding='utf_8') as file:
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
                        "start_time": time.time() - STARTTIME,  # Thời gian đã trôi qua
                        "score": score_manager.score
                    }
                        global update_map_name
                        update_map_name = map_name
                        with open(f'saves/save_game/{self.email}_saved_game.json', "w") as save_file:
                            json.dump(game_state, save_file, indent=4)
                        self.visible = False
                        settings.saved = True
                        settings.processing_click = False
                        break
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
        with open(os.path.join("saves/save_game", f"{self.email}_saved_game.json"), 'r') as save_file:
            saved_game = json.load(save_file)
            del saved_game[str(i)]
        with open(os.path.join("saves/save_game", f"{self.email}_saved_game.json"), 'w') as save_file:
            json.dump(saved_game, save_file, indent=4)
        os.remove(f'saves/save_game/{self.email}_saved{i}.png')
        self.appear()
                    
    def load(self, event):
        self.back = 'home'
        if event.type == pygame.MOUSEMOTION:
            self.mouse_on(event)
        elif event.type == pygame.MOUSEBUTTONUP:
            mouse_pos = event.pos 
            for i, box in enumerate(self.memory_boxes):
                 
                if self.delete_rects[i] and self.delete_rects[i].collidepoint(mouse_pos):
                    self.delete(i + (self.page - 1) * 6)
                    return None
                elif box and box.collidepoint(mouse_pos):
                    save_file_path = os.path.join("saves/save_game", f"{self.email}_saved_game.json")
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
    def __init__(self, x,y,w,h, screen, email, closeable = True):
        self.x, self.y, self.w, self.h = x,y,w,h
        self.Rect = pygame.Rect(x,y,w,h)
        self.screen = screen
        pygame.font.init()
        self.font = pygame.font.Font(None, int(64*x_scale))
        self.visible = True
        self.email = email
        self.closeable = closeable
        
    def appear(self):
        if self.closeable == True:
            enter_map_name = pygame.image.load('images/save_menu/enter_map_name.png')
        else:
            enter_map_name = pygame.image.load('images/save_menu/enter_map_name_2.png')
        enter_map_name = pygame.transform.scale(enter_map_name, (self.w, self.h))
        self.screen.blit(enter_map_name, (self.x, self.y))
        if self.closeable == True:
            close_button = pygame.transform.scale(pygame.image.load('images/save_menu/close_button.png'), (int(100*x_scale), int(100*y_scale)))
            self.screen.blit(close_button, (self.x + int(16*x_scale), self.y + int(16*y_scale)))
            close_button_rect = pygame.Rect(self.x + int(16*x_scale), self.y + int(16*y_scale), int(100*x_scale), int(100*y_scale))
        
        # Ô nhập dữ liệu
        input_box = pygame.Rect(self.x + self.w // 2 - int(300*x_scale), self.y + int(240*y_scale), int(600*x_scale), int(80*y_scale))
        color_inactive = GRAY
        color_active = BLUE
        color = color_inactive
        active = False
        text = ''

        enter_button = pygame.image.load('images/save_menu/enter_button.png')
        enter_button = pygame.transform.scale(enter_button, (int(300*x_scale), int(70*y_scale)))
        self.screen.blit(enter_button, (self.x + self.w // 2 - int(150*x_scale), self.y + int(370*y_scale)))
        enter_rect = pygame.Rect(self.x + self.w // 2 - int(150*x_scale), self.y + int(370*y_scale), int(300*x_scale), int(70*y_scale))
        
        # Vòng lặp chính
        running = True
        error = None
        error_on = False
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    # Kiểm tra nếu nhấp vào ô nhập
                    if input_box.collidepoint(event.pos):
                        active = True
                    else:
                        active = False
                    # Thay đổi màu sắc dựa trên trạng thái
                    color = color_active if active else color_inactive
                    if enter_rect.collidepoint(mouse_pos):
                        with open(os.path.join("saves/save_game", f"{self.email}_saved_game.json"), 'r') as save_file:
                            games = json.load(save_file)
                            for game in games:
                                if games[game]['name'] == text:
                                    error = self.font.render('Map name has been used!', True, RED)
                                    break
                            else:
                                return text
                    if self.closeable == True and close_button_rect.collidepoint(mouse_pos):
                        self.visible = False
                        return None
                if event.type == pygame.KEYDOWN:
                    if active:
                        if event.key == pygame.K_RETURN:
                            with open(os.path.join("saves/save_game", f"{self.email}_saved_game.json"), 'r') as save_file:
                                games = json.load(save_file)
                                for game in games:
                                    if games[game]['name'] == text:
                                        error = self.font.render('Map name has been used!', True, RED)
                                        break
                                else:
                                    return text
                        elif event.key == pygame.K_BACKSPACE:
                            error = None
                            text = text[:-1]
                        elif len(text) < 15:
                            text += event.unicode
                            error = None
            if error != None:
                self.screen.blit(error, (self.x + int(500*x_scale) - error.get_width() // 2, self.y + int(140*y_scale)))
                error_on = True
            elif error_on == True:
                if self.closeable == True:
                    enter_map_name = pygame.image.load('images/save_menu/enter_map_name.png')
                else:
                    enter_map_name = pygame.image.load('images/save_menu/enter_map_name_2.png')
                enter_map_name = pygame.transform.scale(enter_map_name, (self.w, self.h))
                self.screen.blit(enter_map_name, (self.x, self.y))
                if self.closeable == True:
                    self.screen.blit(close_button, (self.x + int(16*x_scale), self.y + int(16*y_scale)))
                self.screen.blit(enter_button, tuple(enter_rect))
                error_on = False
            # Vẽ ô nhập dữ liệu
            pygame.draw.rect(self.screen, WHITE, input_box)
            pygame.draw.rect(self.screen, color, input_box, 2)
            
            # Render văn bản
            txt_surface = self.font.render(text, True, BLACK)
            if txt_surface.get_width() > int(600*x_scale):
                l = int(int(600*x_scale) / txt_surface.get_width() * len(text))
                txt_surface = self.font.render(text[-l:], True, BLACK)
            # Vẽ văn bản
            self.screen.blit(txt_surface, (input_box.x + int(10*x_scale), input_box.y + int(40*y_scale) - txt_surface.get_height()//2))

            # Cập nhật màn hình
            pygame.display.flip()
            
class Settings:
    def __init__(self, screen):
        self.screen = screen
        self.visible = False  # Initially hidden
        self.processing_click = False 
        self.last_close_time = 0
        # Box settings
        self.box_width = 400*x_scale
        self.box_height = 400*y_scale
        self.box_color = (50, 50, 50)  # Màu nền box settings
        self.box_border_color = (255, 255, 255)  # Màu viền box settings
        self.box_rect = pygame.Rect(
            (WINDOWWIDTH - self.box_width) // 2,
            (WINDOWHEIGHT - self.box_height) // 2,
            self.box_width,
            self.box_height,
        )
        self.saved = False

        # Nút Settings chính
        self.settings_button_rect = pygame.Rect(int(10*x_scale), int(10*y_scale), int(130*x_scale), int(40*y_scale))  # Vị trí nút "Settings"

        # Các nút trong box settings (bao gồm nút Close)
        self.button_width = 200*x_scale
        self.button_height = 50*y_scale
        self.buttons = [
            {"text": "Toggle Sound", "action": self.toggle_sound, "rect": None},
            {"text": "Save Game", "action": self.save_game, "rect": None},
            {"text": "Quit Game", "action": self.quit_game, "rect": None},
            {"text": "Main Menu", "action": self.main_menu, "rect": None},
            {"text": "Close", "action": self.toggle_visibility, "rect": None},  # Nút Close
        ]

        self.sound_on = SettingGame.muteSound  # Default sound state
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
        start_y = self.box_rect.y + 40*x_scale  # Khoảng cách từ mép trên box đến nút đầu tiên
        gap = 20*y_scale  # Khoảng cách giữa các nút

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
        SettingGame.muteSound = not SettingGame.muteSound
        if self.sound_on:
            pygame.mixer.music.unpause()  # Unpause music if sound is on
            print("Sound On")
        else:
            pygame.mixer.music.pause()  # Pause music if sound is off
            print("Sound Off")

    def save_game(self):
        if self.saved == False:
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
        fonts = pygame.font.Font('font_pixel.otf', int(20*x_scale))
        if not self.visible:
            self.saved = False
            pygame.draw.rect(self.screen, GREEN, self.settings_button_rect, border_radius=int(5*x_scale))
            text = fonts.render("Settings", True, BLACK)
            self.screen.blit(text, (self.settings_button_rect.x + self.settings_button_rect.w / 2 - text.get_width() / 2, self.settings_button_rect.y))
        else:
            # Vẽ box settings
            if not self.start_pause:
                self.start_pause = time.time()
            global less_time
            less_time = False
            TimeOutSound.stop()
            # if not self.appear_again:
            crop_image = DISPLAYSURF.subsurface((XMARGIN + BOXSIZEX, YMARGIN + BOXSIZEY, BOXSIZEX * (BOARDWIDTH - 2), BOXSIZEY * (BOARDHEIGHT - 2)))
            pygame.image.save(crop_image, 'saves/save_game/temporary.png')
            pygame.draw.rect(self.screen, self.box_color, self.box_rect, border_radius=3)
            pygame.draw.rect(self.screen, self.box_border_color, self.box_rect, width=2, border_radius=3)

            # Vẽ các nút bên trong box settings
            for i, button in enumerate(self.buttons):
                if i == 1 and self.saved == True:
                    pygame.draw.rect(self.screen, GRAY, button["rect"], border_radius=3)
                    text = fonts.render('SAVED', True, WHITE)
                    w = text.get_width()
                    self.screen.blit(text, (button["rect"].x + button["rect"].w / 2 - w / 2, button["rect"].y + int(7*y_scale)))
                else:
                    pygame.draw.rect(self.screen, BLUE, button["rect"], border_radius=3)
                    text = fonts.render(button["text"], True, WHITE)
                    w = text.get_width()
                    self.screen.blit(text, (button["rect"].x + button["rect"].w / 2 - w / 2, button["rect"].y + int(7*y_scale)))

class Collections:
    def __init__(self, screen, unlocked_pokemons):
        self.screen = screen

        self.unlocked_pokemons = set()
        self.current_page = 1  # Trang hiện tại (bắt đầu từ 1)
        self.pokemon_per_page = 15  # Số Pokémon hiển thị mỗi trang

        self.font = pygame.font.Font('font_pixel.otf', int(75*x_scale))  # Font chữ
        self.gen_rects = []  # Lưu danh sách các nút Gen (vùng chữ nhật)

        # Nút Back (ảnh)
        self.back_button_image = pygame.image.load('images/image_button/back.png')
        self.back_button_image = pygame.transform.scale(self.back_button_image, (int(250*x_scale), int(100*y_scale)))  # Kích thước mới
        self.back_button_rect = self.back_button_image.get_rect(topright=(WINDOWWIDTH - int(30*x_scale), int(30*y_scale)))  # Vị trí nút Back

        # Nút Next Page (ảnh)
        self.next_page_image = pygame.image.load('images/save_menu/next_page.png')
        self.next_page_image = pygame.transform.scale(self.next_page_image, (int(100*x_scale), int(100*y_scale)))  # Kích thước mới
        self.next_page_rect = self.next_page_image.get_rect(midbottom=(WINDOWWIDTH // 2 + int(85*x_scale), WINDOWHEIGHT - int(15*y_scale)))

        # Nút Previous Page (ảnh)
        self.prev_page_image = pygame.image.load('images/save_menu/previous_page.png')
        self.prev_page_image = pygame.transform.scale(self.prev_page_image, (int(100*x_scale), int(100*y_scale)))  # Kích thước mới
        self.prev_page_rect = self.prev_page_image.get_rect(midbottom=(WINDOWWIDTH // 2 - int(85*x_scale), WINDOWHEIGHT - int(15*y_scale)))

    def draw_collections_menu(self):
        self.current_page = 1
        """Hiển thị menu chọn Gen với căn chỉnh đều và chữ nằm giữa khung."""
        self.screen.fill((245, 245, 220))  # Màu nền be

        # Tiêu đề
        title = self.font.render("Select Generation", True, RED)
        self.screen.blit(title, (WINDOWWIDTH // 2 - title.get_width() // 2, int(90*y_scale)))  # Tiêu đề nằm giữa màn hình

        # Số lượng nút Gen
        num_buttons = 4  # Tổng số nút Gen
        num_cols = 2  # Số cột
        num_rows = 2  # Số hàng

        # Tìm kích thước chữ lớn nhất để căn chỉnh khung nút
        max_text_width = 0
        max_text_height = 0
        for i in range(num_buttons):
            gen_text = self.font.render(f"GEN {i + 1}", True, BLACK)
            max_text_width = max(max_text_width, gen_text.get_width())
            max_text_height = max(max_text_height, gen_text.get_height())

        # Kích thước nút dựa trên kích thước chữ + padding
        button_width = max_text_width + int(40*x_scale)  # Padding ngang 40px
        button_height = max_text_height + int(30*y_scale)  # Padding dọc 30px

        # Tính toán khoảng cách giữa các nút
        button_spacing_x = int(50*x_scale)  # Khoảng cách ngang giữa các nút
        button_spacing_y = int(40*y_scale)  # Khoảng cách dọc giữa các nút

        # Tổng chiều rộng và chiều cao của khu vực chứa nút
        total_width = num_cols * button_width + (num_cols - 1) * button_spacing_x
        total_height = num_rows * button_height + (num_rows - 1) * button_spacing_y

        # Vị trí bắt đầu để căn giữa toàn bộ cụm nút
        x_start = (WINDOWWIDTH - total_width) // 2
        y_start = (WINDOWHEIGHT - total_height) // 2

        # Xóa danh sách nút cũ
        self.gen_rects.clear()

        # Vẽ các nút Gen
        for row in range(num_rows):
            for col in range(num_cols):
                index = row * num_cols + col
                if index >= num_buttons:
                    break

                # Tính toán vị trí của từng nút
                x = x_start + col * (button_width + button_spacing_x)
                y = y_start + row * (button_height + button_spacing_y)

                # Kiểm tra nút đã mở khóa hay chưa
                color = BLUE if index + 1 in self.unlocked_pokemons else BLACK

                # Vẽ khung nút
                pygame.draw.rect(self.screen, color, (x, y, button_width, button_height), 2)
                self.gen_rects.append(pygame.Rect(x, y, button_width, button_height))  # Lưu vùng chữ nhật của nút

                # Vẽ chữ "GEN X" vào giữa nút
                gen_text = self.font.render(f"GEN {index + 1}", True, BLACK)
                text_x = x + (button_width - gen_text.get_width()) // 2
                text_y = y + (button_height - gen_text.get_height()) // 2
                self.screen.blit(gen_text, (text_x, text_y))

        # Vẽ nút Back
        self.screen.blit(self.back_button_image, self.back_button_rect.topleft)

        pygame.display.flip()  # Cập nhật màn hình

    def handle_menu_event(self):
        """Xử lý sự kiện trong menu chọn Gen."""
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Kiểm tra nút Back
                if self.back_button_rect.collidepoint(event.pos):
                    return "BACK"

                # Kiểm tra các nút Gen
                for i, rect in enumerate(self.gen_rects):  # Kiểm tra từng nút Gen
                    if rect.collidepoint(event.pos):
                        return i + 1  # Trả về Gen được chọn (1, 2, 3, hoặc 4)

            elif event.type == pygame.QUIT:  # Thoát game
                pygame.quit()
                sys.exit()

        return None  # Không có sự kiện nào được xử lý

    def handle_pokemon_event(self, pokemon_list, pokemon_rects):
        """Xử lý sự kiện khi chọn Pokémon."""
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Kiểm tra nút Back
                if self.back_button_rect.collidepoint(event.pos):
                    return "BACK"

                # Kiểm tra các nút Pokémon
                for i, rect in enumerate(pokemon_rects):
                    if rect.collidepoint(event.pos):
                        if pokemon_list[i] not in self.unlocked_pokemons:
                            print("Pokémon này chưa được mở khóa!")  # Thông báo
                            return None  # Không cho phép chọn
                        return pokemon_list[i]  # Trả về tên Pokémon được chọn

            elif event.type == pygame.QUIT:  # Thoát game
                pygame.quit()
                sys.exit()

        return None

    def draw_pokemon_details(self, pokemon_name):
        """Hiển thị thông tin chi tiết của một Pokémon với phông chữ pixel tùy chỉnh và hỗ trợ xuống dòng."""
        import os
        import random

        # Thêm hình nền ngẫu nhiên
        background_folder = "images/image_background_in4"  # Thư mục chứa hình nền
        try:
            background_files = os.listdir(background_folder)
            background_files = [f for f in background_files if f.lower().endswith((".png", ".jpg", ".jpeg"))]
            if background_files:
                background_path = os.path.join(background_folder, random.choice(background_files))
                background_img = pygame.image.load(background_path)
                background_img = pygame.transform.scale(background_img, (WINDOWWIDTH, WINDOWHEIGHT))
                self.screen.blit(background_img, (0, 0))
            else:
                print(f"Thư mục {background_folder} không chứa file ảnh nào.")
        except FileNotFoundError:
            print(f"Không tìm thấy thư mục {background_folder}.")

        # Xác định Gen của Pokémon
        gen = None
        for i in range(1, 5):
            try:
                with open(f'images/pokemon_in4/gen{i}.json', 'r', encoding='utf_8') as file:
                    pokemon_data = json.load(file)
                    if pokemon_name in pokemon_data:
                        gen = i
                        pokemon_info = pokemon_data[pokemon_name]
                        break
            except FileNotFoundError:
                continue

        if not gen:
            print(f"Không tìm thấy thông tin cho Pokémon {pokemon_name}")
            return

        # Hiển thị hình ảnh Pokémon
        image_path = f'images/image_pokemon/gen{gen}/{pokemon_name}'
        try:
            img = pygame.image.load(image_path)

            # Lấy kích thước gốc của ảnh
            original_width, original_height = img.get_size()

            # Tính tỷ lệ để giữ nguyên tỷ lệ gốc và vừa với không gian hiển thị
            max_width, max_height = int(650*x_scale), int(650*y_scale)  # Kích thước tối đa cho hình ảnh
            scale = min(max_width / original_width, max_height / original_height)
            new_width = int(original_width * scale)
            new_height = int(original_height * scale)

            # Scale ảnh với kích thước đã tính
            img = pygame.transform.scale(img, (new_width, new_height))

            # Căn giữa ảnh
            x_centered = WINDOWWIDTH // 2 - new_width // 2
            y_position = int(80*y_scale)  # Vị trí phía trên dành cho hình ảnh
            self.screen.blit(img, (x_centered, y_position))  # Vẽ ảnh trên màn hình
        except FileNotFoundError:
            print(f"Không tìm thấy hình ảnh {image_path}")
            return

        # Sử dụng phông chữ pixel tùy chỉnh
        self.fonts = pygame.font.Font('font_pixel.otf', 50)  # Kích thước font phù hợp với màn hình
        text_x = int(60*x_scale)  # Văn bản cách lề trái
        y_offset = int(700*y_scale)  # Dòng chữ đầu tiên phía dưới hình ảnh
        max_line_width = WINDOWWIDTH - text_x - int(60*x_scale)  # Giới hạn chiều rộng dòng chữ

        # Hiển thị thông tin chi tiết
        for key, value in pokemon_info.items():
            if key.lower() == "description":
                full_text = f"Description: {value}"
                description_lines = self.split_text(full_text, max_line_width)
                for line in description_lines:
                    text_surface = self.fonts.render(line, True, BLACK)
                    self.screen.blit(text_surface, (text_x, y_offset))
                    y_offset += int(60*y_scale)
            else:
                text = f"{key.capitalize()}: {value}"
                text_surface = self.fonts.render(text, True, BLACK)
                self.screen.blit(text_surface, (text_x, y_offset))
                y_offset += int(70*y_scale)

        # Hiển thị nút Back
        self.screen.blit(self.back_button_image, self.back_button_rect.topleft)
        pygame.display.flip()

        # Xử lý sự kiện
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.back_button_rect.collidepoint(event.pos):
                        running = False  # Quay lại màn hình trước
                elif event.type == pygame.QUIT:
                    pygame.quit()

    def split_text(self, text, max_width):
        """Chia đoạn văn bản thành các dòng ngắn dựa trên chiều rộng tối đa."""
        words = text.split(" ")
        lines = []
        current_line = ""

        for word in words:
            test_line = f"{current_line} {word}".strip()
            text_width, _ = self.fonts.size(test_line)  # Tính chiều rộng của dòng chữ
            if text_width <= max_width:
                current_line = test_line
            else:
                lines.append(current_line)  # Thêm dòng hoàn chỉnh vào danh sách
                current_line = word  # Bắt đầu dòng mới với từ hiện tại

        if current_line:
            lines.append(current_line)  # Thêm dòng cuối cùng

        return lines

    def drawCollectionsScreen(self, gen, unlocked_pokemon):
        """Vẽ màn hình hiển thị danh sách Pokémon theo Gen và trang hiện tại."""
        self.screen.fill((245, 245, 220))  # Màu nền
        title = self.font.render(f"Pokémon in Gen {gen} - Page {self.current_page}", True, BLACK)
        self.screen.blit(title, (WINDOWWIDTH // 2 - title.get_width() // 2, int(70*y_scale)))  # Tiêu đề

        # Vẽ danh sách Pokémon
        pokemon_list = os.listdir(f'images/images_icon/Gen{gen}/')
        start_index = (self.current_page - 1) * self.pokemon_per_page
        end_index = start_index + self.pokemon_per_page
        displayed_pokemon = pokemon_list[start_index:end_index]

        pokemon_rects = []

        # Thiết lập kích thước Pokémon và lưới hiển thị
        pokemon_size = int(170*x_scale)  # Kích thước mới của Pokémon
        margin = int(80*x_scale)  # Khoảng cách giữa các Pokémon (dãn ra thêm)
        cols = 5  # Số Pokémon mỗi hàng
        rows = (len(displayed_pokemon) + cols - 1) // cols  # Số hàng cần thiết

        # Tính toán vị trí bắt đầu để căn giữa màn hình
        total_width = cols * pokemon_size + (cols - 1) * margin
        total_height = rows * pokemon_size + (rows - 1) * margin
        x_start = (WINDOWWIDTH - total_width) // 2
        y_start = (WINDOWHEIGHT - total_height) // 2 + int(50*y_scale)

        x, y = x_start, y_start

        for i, pokemon in enumerate(displayed_pokemon):
            img = pygame.image.load(f'images/images_icon/Gen{gen}/{pokemon}')
            img = pygame.transform.scale(img, (pokemon_size, pokemon_size))

            if pokemon not in unlocked_pokemon:
                # Tạo hiệu ứng tối màu cho Pokémon bị khóa
                dark_overlay = pygame.Surface(img.get_size(), pygame.SRCALPHA)
                dark_overlay.fill((0, 0, 0, 150))  # Lớp phủ màu đen với độ trong suốt
                img.blit(dark_overlay, (0, 0))  # Phủ lớp tối lên ảnh

            self.screen.blit(img, (x, y))
            pokemon_rects.append(pygame.Rect(x, y, pokemon_size, pokemon_size))

            x += pokemon_size + margin
            if (i + 1) % cols == 0:  # Xuống dòng sau mỗi `cols` Pokémon
                x = x_start
                y += pokemon_size + margin

        # Vẽ nút Back và các nút chuyển trang
        self.screen.blit(self.back_button_image, self.back_button_rect.topleft)
        if start_index > 0:  # Nút Previous Page
            self.screen.blit(self.prev_page_image, self.prev_page_rect.topleft)
        if end_index < len(pokemon_list):  # Nút Next Page
            self.screen.blit(self.next_page_image, self.next_page_rect.topleft)

        pygame.display.flip()  # Cập nhật màn hình
        return pokemon_list, pokemon_rects

def extract_gen_from_name(pokemon_name):
    match = re.search(r'gen(\d+)_', pokemon_name, re.IGNORECASE)
    if match:
        return int(match.group(1))
    print(f"Không thể xác định Gen từ tên Pokémon: {pokemon_name}")
    return None

def showCollectionsMenu():
    global unlocked_pokemon
    collections = Collections(DISPLAYSURF, unlocked_pokemon)  # Khởi tạo menu Collections
    running = True

    while running:
        collections.draw_collections_menu()  # Vẽ menu Collections
        gen_selected = collections.handle_menu_event()  # Kiểm tra sự kiện từ người dùng

        if gen_selected == "BACK":  # Nếu nhấn nút Back
            running = False  # Thoát vòng lặp và quay lại menu chính
            return

        if gen_selected:  # Nếu chọn một Gen
            showCollectionsScreen(gen_selected, collections, unlocked_pokemon)  # Truyền Gen được chọn vào màn hình hiển thị Pokémon
            continue

        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Thoát game
                pygame.quit()
                sys.exit()

def showCollectionsScreen(gen, collections, unlocked_pokemon):
    """Hiển thị màn hình danh sách Pokémon và xử lý sự kiện."""
    running = True
    while running:
        # Vẽ màn hình và lấy danh sách Pokémon hiển thị, cùng các vùng nhấp chuột
        pokemon_list, pokemon_rects = collections.drawCollectionsScreen(gen, unlocked_pokemon)

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Kiểm tra nếu nhấn nút Back
                if collections.back_button_rect.collidepoint(event.pos):
                    running = False  # Thoát khỏi vòng lặp để quay lại menu Collections

                # Xử lý nút chuyển trang
                elif collections.prev_page_rect.collidepoint(event.pos) and collections.current_page > 1:
                    collections.current_page -= 1  # Lùi về trang trước
                elif collections.next_page_rect.collidepoint(
                        event.pos) and collections.current_page * collections.pokemon_per_page < len(
                        os.listdir(f'images/images_icon/Gen{gen}/')):
                    collections.current_page += 1  # Tới trang sau

                # Kiểm tra nếu nhấn vào một Pokémon
                else:
                    for i, rect in enumerate(pokemon_rects):
                        if rect.collidepoint(event.pos):
                            selected_pokemon = pokemon_list[
                                i + (collections.current_page - 1) * collections.pokemon_per_page]

                            # Kiểm tra trạng thái mở khóa
                            if selected_pokemon not in unlocked_pokemon:
                                print(f"Pokémon '{selected_pokemon}' chưa được mở khóa!")  # In tên Pokémon chưa mở khóa
                                break  # Bỏ qua hành động nếu Pokémon bị khóa

                            # Hiển thị chi tiết Pokémon nếu được mở khóa
                            collections.draw_pokemon_details(selected_pokemon)
                            break

            elif event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


def split_text(text, font, max_width):
    words = text.split(' ')
    lines = []
    current_line = words[0]

    for word in words[1:]:
        if font.size(current_line + ' ' + word)[0] <= max_width:
            current_line += ' ' + word
        else:
            lines.append(current_line)
            current_line = word
    lines.append(current_line)
    return lines
