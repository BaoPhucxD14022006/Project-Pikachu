import pygame
import os 
import sys
import json
import pandas as pd
import math
from functools import reduce

current_dir = os.path.dirname(os.path.abspath(__file__))
FONT_PATH = current_dir
current_dir += '/images/RankScreen'

class OptionButton:
    def __init__(self, screen, x, y, w, h, text, x_scale, y_scale):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.x_scale = x_scale
        self.y_scale = y_scale
        self.screen = screen
        self.options = []
        self.text = text
        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)
        self.is_open = False 
        self.result = None
        
    def add_option(self, option):
        if type(option) == str:
            self.options.append(option)
        else:
            self.options += list(option)
        
    def draw(self):
        border_color = (255, 215, 0)  
        border_width = 4  
        
        fill_color = (255, 255, 255)

        pygame.draw.rect(self.screen, border_color, self.rect, width=border_width)

        inner_rect = self.rect.inflate(-border_width, -border_width)  
        pygame.draw.rect(self.screen, fill_color, inner_rect)

        font_path = current_dir + '/font_pixel.otf'
        font = pygame.font.Font(font_path, int(24*self.x_scale))
        content = self.text + ' : ' + self.result if self.result else self.text
        text = font.render(content, True, (0, 0, 0))
        text_rect = text.get_rect(center=self.rect.center)
        self.screen.blit(text, text_rect)

        if self.is_open:
            option_y = self.y + self.h
            for option in self.options:
                option_rect = pygame.Rect(self.x, option_y, self.w, self.h)
                pygame.draw.rect(self.screen, (255, 255, 255), option_rect)
                border = pygame.Surface((self.w, self.h), pygame.SRCALPHA)
                pygame.draw.rect(border, (100, 100, 100, 100), (0,0,self.w, self.h), width=3)
                self.screen.blit(border, (self.x, option_y))
                option_text = font.render(option, True, (0, 0, 0))  
                self.screen.blit(option_text, (int(self.x + self.w/2 - option_text.get_width()/2) , option_y + int(10*self.y_scale))) 
                option_y += self.h 

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            if self.rect.collidepoint(mouse_x, mouse_y):
                self.is_open = not self.is_open
                self.result = None
            elif self.is_open:
                option_y = self.y + self.h
                flag = None
                for option in self.options:
                    option_rect = pygame.Rect(self.x, option_y, self.w, self.h)
                    if option_rect.collidepoint(mouse_x, mouse_y):
                        flag = True
                        self.result = option
                        self.is_open = False
                    option_y += self.h
                if not flag:
                    self.is_open = False
    
class Button:
    def __init__(self, screen, x, y, path, x_scale, y_scale):
        self.path = path
        self.button = pygame.image.load(current_dir + '/' + self.path)
        self.button = pygame.transform.scale(self.button, (int(self.button.get_width()*2*x_scale), int(self.button.get_height()*2*y_scale)))
        self.screen = screen
        self.rect = pygame.Rect(x, y, self.button.get_width(), self.button.get_height())
        
    def draw(self):
        self.screen.blit(self.button, self.rect)
        
class RankScreen:
    def __init__(self, w, h, screen, x_scale, y_scale):

        self.w_screen = w
        self.h_screen = h
        self.screen = screen
        self.background = pygame.image.load(current_dir + '/rank_background.png')
        self.background = pygame.transform.scale(self.background, (w, h))
        self.running = True
        
        self.filter = {}
        self.option_size = OptionButton(self.screen, x=int(190*x_scale), y=int(340*y_scale), w=int(180*x_scale), h=int(60*y_scale), text='Size', x_scale=x_scale, y_scale=y_scale)
        self.option_size.add_option(['8x8', '9x16', '12x30'])
        self.filter['size'] = self.option_size.result
        self.option_gen = OptionButton(self.screen, x=int(440*x_scale), y=int(340*y_scale), w=int(180*x_scale), h=int(60*y_scale), text='Gen', x_scale=x_scale, y_scale=y_scale)
        self.option_gen.add_option(['1', '2', '3', '4'])
        self.filter['gen'] = self.option_gen.result
        self.option_level = OptionButton(self.screen, x=int(690*x_scale), y=int(340*y_scale), w=int(280*x_scale), h=int(60*y_scale), text='Game Mode', x_scale=x_scale, y_scale=y_scale)
        self.option_level.add_option(['1', '2', '3', '4', '5'])
        self.filter['gamemode'] = self.option_level.result
        self.option_device = OptionButton(self.screen, x=int(1040*x_scale), y=int(340*y_scale), w=int(260*x_scale), h=int(60*y_scale), text='Device', x_scale=x_scale, y_scale=y_scale)
        self.option_device.add_option(['Mouse', 'Keyboard'])
        self.filter['device'] = self.option_device.result
        self.options_button = [self.option_size,
                               self.option_gen,
                               self.option_level,
                               self.option_device]

        self.button_confirm = Button(self.screen, x=int(1390*x_scale), y=int(325*y_scale), path='button_confirm.png', x_scale=x_scale, y_scale=y_scale)
        self.button_home = Button(self.screen, x=int(20*x_scale), y=int(20*y_scale), path='button_home.png', x_scale=x_scale, y_scale=y_scale)
        self.buttons = [self.button_confirm, self.button_home]
        self.table = Table(x_center= w // 2, y_center= h // 2 + int(160*y_scale), filter=self.filter, screen=self.screen, x_scale=x_scale, y_scale=y_scale)
        self.show_table = False
        self.page = Pagination(self.screen, self.table.max_page, (w // 2 - int(70*x_scale), h - int(45*y_scale)), (w // 2 + int(70*x_scale), h - int(45*y_scale)), int(40*x_scale), x_scale)
        
    def update_filter(self):
        self.filter['size'] = self.option_size.result
        self.filter['gen'] = self.option_gen.result
        self.filter['gamemode'] = self.option_level.result
        self.filter['device'] = self.option_device.result
        
    def handle_event(self):
        for event in pygame.event.get():
            for option_button in self.options_button:
                option_button.handle_event(event)
                self.draw()
            self.update_filter()
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEMOTION:
                mouse_pos = pygame.mouse.get_pos()
                for button in self.buttons:
                    if button.rect.collidepoint(mouse_pos):
                        button.button.set_alpha(100)
                    else:
                        button.button.set_alpha(255)
                    self.draw()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if self.button_confirm.rect.collidepoint(mouse_pos):
                    self.update_filter()
                    self.table.filter = self.filter
                    self.table.update_data()
                    self.page.total_pages = self.table.max_page
                    self.page.current_page = 1
                    self.show_table = True
                    self.draw()
                if self.show_table:
                    if reduce(lambda x,y : x or y, [option_button.is_open for option_button in self.options_button]):
                        self.show_table = False
                if self.page.rect_prev.collidepoint(mouse_pos):
                    self.page.prev_page()
                    self.draw()
                if self.page.rect_next.collidepoint(mouse_pos):
                    self.page.next_page()
                    self.draw()
                if self.button_home.rect.collidepoint(mouse_pos):
                    self.running = False
                    print("HOME")
                    
    
    def run(self):
        self.draw()
        while self.running:
            self.handle_event()
            pygame.display.flip()
            
    
    def draw(self):
        self.screen.blit(self.background, (0, 0)) 
        for option_button in self.options_button:
            option_button.draw()
        for button in self.buttons:
            button.draw()
        if self.show_table:
            self.table.draw(page=self.page.current_page)
            self.page.draw()
            
            
class Table:
    def __init__(self, x_center, y_center, filter, screen, x_scale, y_scale):
        self.x_center = x_center
        self.y_center = y_center
        self.x_scale = x_scale
        self.y_scale = y_scale
        self.filter = filter
        self.screen = screen
        self.h_row = int(55*y_scale)
        self.max_row = 10
        self.data, self.max_page = self.get_data()
        
    def check_game(self, game):
        for key in self.filter:
            if self.filter[key] is not None:
                if game[key] != self.filter[key]:
                    return False
        return True

    def get_data(self):
        with open(FONT_PATH + '/saves/' + 'rank.json', 'r') as file:
            data = json.load(file)
        data_dic = {}
        data_dic['namegame'] = []
        data_dic['user'] = []
        for key in self.filter:
            if self.filter[key] is None:
                data_dic[key] = []
        data_dic['score'] = []
        for namegame in data:
            if self.check_game(namegame):
                data_dic['namegame'].append(namegame['namegame'])
                data_dic['user'].append(namegame['user'])
                data_dic['score'].append(namegame['score'])
                for key in self.filter:
                    if self.filter[key] is None:
                        data_dic[key].append(namegame[key])
        df = pd.DataFrame(data_dic)
        df = df.sort_values(by='score', ascending=False)
        df = df.reset_index(drop=True)
        df.at[0, 'rank'] = 1
        for i in range(1, len(df)):
            if df.iloc[i]['score'] == df.iloc[i - 1]['score']:
                df.at[i, 'rank'] = df.at[i - 1, 'rank']
            else:
                df.at[i, 'rank'] = i + 1
        df['rank'] = df['rank'].astype(int)
        df['number'] = range(1, len(df) + 1)
        cols = ['number'] + [col for col in df.columns if col != 'number']
        df = df[cols]
        max_page = math.ceil(len(df) / self.max_row)
        return df, max_page

    def update_data(self):
        self.data, self.max_page = self.get_data()

    def draw(self, page=1):
        font_path = FONT_PATH + '/font_pixel.otf'
        font = pygame.font.Font(font_path, int(30*self.x_scale))
        df = self.data[(page-1)*self.max_row:]
        if len(df) > self.max_row:
            df = df[:self.max_row]
        df = df.reset_index(drop=True)
        if not df.isna().any().any():
            column_names = df.columns.tolist()
            column_widths = self.calculate_column_widths(df)
            w_table = sum(column_widths)
            x_cell = self.x_center - w_table//2
            y_cell = self.y_center - self.max_row // 2 * self.h_row
            for i, col in enumerate(column_names):
                text_surface = font.render(col.title(), True, (0, 0, 0)) 
                text_rect = text_surface.get_rect(center=(x_cell + column_widths[i] / 2, y_cell + self.h_row / 2))
                self.screen.blit(text_surface, text_rect)
                x_cell += column_widths[i]
                
            x_cell = self.x_center - w_table//2
            y_cell = self.y_center - self.max_row // 2 * self.h_row + self.h_row
            for i in range(min(self.max_row, len(df))):
                for j, col in enumerate(df.columns):
                        text_surface = font.render(str(df.at[i, col]), True, (0, 0, 0))
                        text_rect = text_surface.get_rect(center=(x_cell + column_widths[j] / 2, y_cell + self.h_row / 2))
                        self.screen.blit(text_surface, text_rect)
                        x_cell += column_widths[j]
                x_cell = self.x_center - w_table//2
                y_cell += self.h_row
        else:
            text_surface = font.render(str('No matching results'), True, (0, 0, 0))
            text_rect = text_surface.get_rect(center=(self.x_center, self.y_center))
            self.screen.blit(text_surface, text_rect)      

    def calculate_column_widths(self, df):
        column_widths = []
        for col in df.columns:
            max_len = max(df[col].apply(lambda x: len(str(x))).max(), len(col))  
            max_len = max(max_len, len(col))
            column_widths.append(max_len * int(30*self.x_scale))  
        column_widths = [w + int(5*self.x_scale) for w in column_widths]
        return column_widths
    
class Pagination:
    def __init__(self, screen, total_pages, prev_button_pos, next_button_pos, size, x_scale):
        self.current_page = 1
        self.total_pages = total_pages
        self.prev_button_pos = prev_button_pos
        self.rect_prev = pygame.Rect(prev_button_pos[0], prev_button_pos[1], size, size)
        self.next_button_pos = next_button_pos
        self.rect_next = pygame.Rect(next_button_pos[0], next_button_pos[1], size, size)
        self.size = size
        self.color = (0, 0, 255)
        self.text_color = (0, 0, 0)
        font_path = FONT_PATH + '/font_pixel.otf'
        self.font = pygame.font.Font(font_path, int(30*x_scale))
        self.screen = screen

    def next_page(self):
        if self.current_page < self.total_pages:
            self.current_page += 1

    def prev_page(self):
        if self.current_page > 1:
            self.current_page -= 1

    def draw(self):
        prev_button = pygame.Rect(self.prev_button_pos[0], self.prev_button_pos[1], self.size, self.size)
        pygame.draw.polygon(self.screen, self.color, [(prev_button.centerx, prev_button.top), 
                                                  (prev_button.left, prev_button.centery), 
                                                  (prev_button.centerx, prev_button.bottom)])
        next_button = pygame.Rect(self.next_button_pos[0], self.next_button_pos[1], self.size, self.size)
        pygame.draw.polygon(self.screen, self.color, [(next_button.centerx, next_button.top), 
                                                  (next_button.right, next_button.centery), 
                                                  (next_button.centerx, next_button.bottom)])
        text = f"{self.current_page} of {self.total_pages}"
        text_surface = self.font.render(text, True, self.text_color)
        text_rect = text_surface.get_rect(center=((self.next_button_pos[0] - self.prev_button_pos[0] - self.size)//2 + self.prev_button_pos[0] + self.size,
                                self.next_button_pos[1] + self.size//2))
        self.screen.blit(text_surface, text_rect )
def main(w, h, screen, x_scale, y_scale):
    pygame.init()
    rank = RankScreen(w, h, screen, x_scale, y_scale)
    rank.run()