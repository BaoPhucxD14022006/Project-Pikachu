import pygame
import sys

# Khởi tạo Pygame
pygame.init()

# Kích thước màn hình
WINDOWWIDTH, WINDOWHEIGHT = 800, 600
DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
pygame.display.set_caption("Chọn Màn Chơi")

# Màu sắc
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Font chữ
FONT = pygame.font.SysFont('comicsansms', 50)

# Biến trạng thái
current_level = 1  # Màn chơi hiện tại
max_level = 5  # Số lượng màn chơi tối đa


def draw_level_selector(current_level):
    """Vẽ màn hình chọn màn chơi"""
    DISPLAYSURF.fill(BLACK)  # Làm sạch màn hình
    
    # Vẽ nút trái và phải
    left_arrow = FONT.render("<", True, WHITE if current_level > 1 else RED)
    right_arrow = FONT.render(">", True, WHITE if current_level < max_level else RED)
    
    # Vẽ thông tin màn chơi
    level_text = FONT.render(f"Level {current_level}", True, GREEN)
    
    # Lấy vị trí cho các nút và text
    left_arrow_rect = left_arrow.get_rect(center=(WINDOWWIDTH // 4, WINDOWHEIGHT // 2))
    right_arrow_rect = right_arrow.get_rect(center=(3 * WINDOWWIDTH // 4, WINDOWHEIGHT // 2))
    level_text_rect = level_text.get_rect(center=(WINDOWWIDTH // 2, WINDOWHEIGHT // 2))
    
    # Vẽ lên màn hình
    DISPLAYSURF.blit(left_arrow, left_arrow_rect)
    DISPLAYSURF.blit(right_arrow, right_arrow_rect)
    DISPLAYSURF.blit(level_text, level_text_rect)
    
    pygame.display.update()
    
    return left_arrow_rect, right_arrow_rect


def main():
    global current_level

    while True:
        # Vẽ giao diện chọn màn
        left_arrow_rect, right_arrow_rect = draw_level_selector(current_level)
        
        # Xử lý sự kiện
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Xử lý khi nhấn phím
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and current_level > 1:
                    current_level -= 1
                if event.key == pygame.K_RIGHT and current_level < max_level:
                    current_level += 1
                if event.key == pygame.K_RETURN:
                    print(f"Bắt đầu màn {current_level}!")

            # Xử lý khi bấm chuột
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos  # Lấy vị trí chuột
                if left_arrow_rect.collidepoint(mouse_pos) and current_level > 1:
                    current_level -= 1
                if right_arrow_rect.collidepoint(mouse_pos) and current_level < max_level:
                    current_level += 1
                if pygame.Rect(WINDOWWIDTH // 2 - 100, WINDOWHEIGHT // 2 - 50, 200, 100).collidepoint(mouse_pos):
                    print(f"Bắt đầu màn {current_level}!")

        pygame.time.Clock().tick(30)


if __name__ == "__main__":
    main()
