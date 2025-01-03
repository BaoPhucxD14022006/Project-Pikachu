import pygame
import sys

# Khởi tạo pygame
pygame.init()

# Đặt kích thước màn hình
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 200
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pagination Example")

# Định nghĩa màu sắc
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BUTTON_COLOR = (100, 150, 255)
TEXT_COLOR = (0, 0, 0)

# Font chữ
font = pygame.font.SysFont(None, 40)

# Class Pagination
class Pagination:
    def __init__(self, total_pages):
        self.current_page = 1
        self.total_pages = total_pages

    def next_page(self):
        if self.current_page < self.total_pages:
            self.current_page += 1

    def prev_page(self):
        if self.current_page > 1:
            self.current_page -= 1

    def draw(self, screen):
        prev_button = pygame.Rect(50, 120, 40, 40)
        pygame.draw.polygon(screen, BUTTON_COLOR, [(prev_button.centerx, prev_button.top), 
                                                  (prev_button.left, prev_button.centery), 
                                                  (prev_button.centerx, prev_button.bottom)])
    
        next_button = pygame.Rect(270, 120, 40, 40)
        pygame.draw.polygon(screen, BUTTON_COLOR, [(next_button.centerx, next_button.top), 
                                                  (next_button.right, next_button.centery), 
                                                  (next_button.centerx, next_button.bottom)])
        
        # Vẽ số trang hiện tại
        page_text = font.render(f"{self.current_page} of {self.total_pages}", True, TEXT_COLOR)
        screen.blit(page_text, (150, 120))

# Khởi tạo Pagination với 10 trang
pagination = Pagination(total_pages=10)

# Vòng lặp chính
running = True
clock = pygame.time.Clock()

while running:
    # Kiểm tra các sự kiện
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            # Kiểm tra nếu click vào mũi tên "Lùi"
            if pygame.Rect(50, 120, 40, 40).collidepoint(mouse_pos):
                pagination.prev_page()
            # Kiểm tra nếu click vào mũi tên "Tới"
            elif pygame.Rect(270, 120, 40, 40).collidepoint(mouse_pos):
                pagination.next_page()

    # Làm mới màn hình
    screen.fill(WHITE)

    # Vẽ phân trang
    pagination.draw(screen)

    # Cập nhật màn hình
    pygame.display.flip()

    # Giới hạn tốc độ khung hình
    clock.tick(60)

# Đóng pygame khi thoát
pygame.quit()
sys.exit()
