import pygame
import random
import sys
import os
import json

# 1. Khởi tạo Pygame
pygame.init()

# Tên file lưu điểm kỷ lục trên máy tính
SCORE_FILE = "highscore.json"

# Hàm tải điểm kỷ lục từ file (để khi tắt mở lại game vẫn còn)
def load_high_score():
    if os.path.exists(SCORE_FILE):
        try:
            with open(SCORE_FILE, "r") as f:
                data = json.load(f)
                return data.get("high_score", 0)
        except:
            return 0
    return 0

# Hàm lưu điểm kỷ lục vào file
def save_high_score(hs):
    try:
        with open(SCORE_FILE, "w") as f:
            json.dump({"high_score": hs}, f)
    except:
        pass

# Thiết lập màn hình mặc định ban đầu (Full màn hình)
is_fullscreen = True
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
WIDTH, HEIGHT = screen.get_size()
pygame.display.set_caption("Game Ne Vat Can - Complete Version")

clock = pygame.time.Clock()

# Màu sắc (RGB)
WHITE = (255, 255, 255)
RED = (255, 60, 60)
BLUE = (60, 150, 255)
BLACK = (20, 20, 20)
YELLOW = (255, 215, 0)
GREEN = (50, 205, 50)

# Cấu hình Font chữ
font_large = pygame.font.SysFont(None, 55)
font_medium = pygame.font.SysFont(None, 34)
font_small = pygame.font.SysFont(None, 24)

# Trạng thái game: "PLAYING" (Đang chơi), "GAME_OVER" (Thua), "WIN" (Thắng)
game_state = "PLAYING"
score = 0
high_score = load_high_score()  # Tải kỷ lục cũ lên khi vừa mở game

# Kích thước nhân vật và vật cản
PLAYER_W, PLAYER_H = 60, 60
OBS_W, OBS_H = 50, 50

player = pygame.Rect(WIDTH // 2 - PLAYER_W // 2, HEIGHT - 100, PLAYER_W, PLAYER_H)
player_speed = 9

obstacle = pygame.Rect(random.randint(0, WIDTH - OBS_W), -100, OBS_W, OBS_H)
obstacle_speed = 6

# Hàm reset lại game khi chơi lại
def reset_game():
    global score, obstacle_speed, player, obstacle
    score = 0
    obstacle_speed = 6
    player.x = WIDTH // 2 - PLAYER_W // 2
    player.y = HEIGHT - 100
    obstacle.x = random.randint(0, WIDTH - OBS_W)
    obstacle.y = -100

# Vòng lặp chính của game
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            
            # Phím F11 để bật/tắt toàn màn hình tùy ý
            elif event.key == pygame.K_F11:
                is_fullscreen = not is_fullscreen
                if is_fullscreen:
                    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                    WIDTH, HEIGHT = screen.get_size()
                else:
                    WIDTH, HEIGHT = 900, 600
                    screen = pygame.display.set_mode((WIDTH, HEIGHT))
                player.y = HEIGHT - 100

            # Nhấn Space, R hoặc Enter để chơi lại khi Thua hoặc Thắng
            if game_state in ["GAME_OVER", "WIN"]:
                if event.key in [pygame.K_SPACE, pygame.K_r, pygame.K_RETURN]:
                    reset_game()
                    game_state = "PLAYING"

        # Hỗ trợ chạm màn hình điện thoại (Android) hoặc click chuột để chơi lại
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if game_state in ["GAME_OVER", "WIN"]:
                reset_game()
                game_state = "PLAYING"

    if game_state == "PLAYING":
        # Điều khiển trên máy tính (Bàn phím)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            player.x -= player_speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            player.x += player_speed

        # Điều khiển bằng Cảm ứng (Android) hoặc chuột
        if pygame.mouse.get_pressed()[0]:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if mouse_x < player.centerx:
                player.x -= player_speed
            else:
                player.x += player_speed

        # Giới hạn khung hình
        if player.left < 0:
            player.left = 0
        if player.right > WIDTH:
            player.right = WIDTH

        # Vật cản rơi xuống
        obstacle.y += obstacle_speed
        if obstacle.y > HEIGHT:
            obstacle.y = -50
            obstacle.x = random.randint(0, WIDTH - OBS_W)
            score += 1
            obstacle_speed += 0.8

            # --- KIỂM TRA ĐIỀU KIỆN THẮNG (ĐẠT 100 ĐIỂM) ---
            if score >= 100:
                if score > high_score:
                    high_score = score
                    save_high_score(high_score)  # Lưu kỷ lục mới vào file
                game_state = "WIN"

        # --- KIỂM TRA VA CHẠM (THUA) ---
        if player.colliderect(obstacle):
            if score > high_score:
                high_score = score
                save_high_score(high_score)  # Lưu kỷ lục mới vào file
            game_state = "GAME_OVER"

        # --- VẼ GIAO DIỆN ĐANG CHƠI ---
        screen.fill(BLACK)

        pygame.draw.rect(screen, BLUE, player, border_radius=10)
        pygame.draw.rect(screen, RED, obstacle, border_radius=10)

        # Hiển thị Điểm và Kỷ lục
        score_surf = font_medium.render(f"Diem: {score}", True, WHITE)
        screen.blit(score_surf, (40, 30))

        high_score_surf = font_medium.render(f"Ky Luc: {high_score}", True, YELLOW)
        screen.blit(high_score_surf, (WIDTH - high_score_surf.get_width() - 40, 30))

    elif game_state == "GAME_OVER":
        # --- GIAO DIỆN KHI THUA ---
        screen.fill(BLACK)

        go_text = font_large.render("GAME OVER", True, RED)
        final_score_text = font_medium.render(f"Diem dat duoc: {score}", True, WHITE)
        best_score_text = font_medium.render(f"Ky luc cao nhat: {high_score}", True, YELLOW)
        restart_text = font_small.render("Nhan SPACE / Cham man hinh de choi lai  |  [F11] Doi man hinh", True, WHITE)

        screen.blit(go_text, (WIDTH // 2 - go_text.get_width() // 2, HEIGHT // 2 - 120))
        screen.blit(final_score_text, (WIDTH // 2 - final_score_text.get_width() // 2, HEIGHT // 2 - 40))
        screen.blit(best_score_text, (WIDTH // 2 - best_score_text.get_width() // 2, HEIGHT // 2 + 10))
        screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 80))

    elif game_state == "WIN":
        # --- GIAO DIỆN KHI ĐẠT 100 ĐIỂM (CHIẾN THẮNG) ---
        screen.fill(BLACK)

        win_text = font_large.render("CHÚC MỪNG BẠN ĐÃ THẮNG!", True, GREEN)
        reward_text = font_medium.render("Liên hệ Pt Humni (Facebook) để nhận quà", True, YELLOW)
        final_score_text = font_medium.render(f"Điểm số xuất sắc: {score}", True, WHITE)
        restart_text = font_small.render("Nhấn SPACE / Chạm màn hình để chơi lại  |  [F11] Đổi màn hình", True, WHITE)

        screen.blit(win_text, (WIDTH // 2 - win_text.get_width() // 2, HEIGHT // 2 - 140))
        screen.blit(reward_text, (WIDTH // 2 - reward_text.get_width() // 2, HEIGHT // 2 - 60))
        screen.blit(final_score_text, (WIDTH // 2 - final_score_text.get_width() // 2, HEIGHT // 2 - 10))
        screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 60))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()