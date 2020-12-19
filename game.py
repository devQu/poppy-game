import pygame, os, math
from player import Player
from enemy import Enemy

pygame.init()

pygame.display.set_caption("Hourahhh!!!")

GAME_FONT = pygame.freetype.Font("fonts/DiaryOfAn8BitMage-lYDD.ttf", 14)
AVATAR_FONT = pygame.freetype.Font("fonts/DiaryOfAn8BitMage-lYDD.ttf", 12)

width = 800
height = 600
hw, hh = width / 2, height / 2
str_count_enemies = "Hamsters morts: "
str_count_lives = "Lives: "
menu_img = pygame.transform.scale((pygame.image.load(os.path.join("images", "retour.png"))), (360, 40))
game_over = False
lives = 3
game_run = False

win = pygame.display.set_mode((width, height))

bg = pygame.image.load(os.path.join("images", "grass_back.png")).convert_alpha()
sk = pygame.image.load(os.path.join("images", "sky.png")).convert_alpha()
nuages = pygame.image.load(os.path.join("images", "nuages.png")).convert_alpha()

pygame.mixer.music.load(os.path.join("sounds", "theme.mp3"))
pygame.mixer.music.set_volume(0.2)
pygame.mixer.music.play(-1)

pl = Player()

list_enemies = [[True, [1930, 0]], [False, [1930, 1]], [True, [1930, 2]], [True, [1930, 3]], [False, [3760, 1]], [False, [4210, 1]], [True, [3815, 2]], [True, [4130, 2]], [False, [3980, 3]], [True, [3760, 0]], [True, [4210, 0]]]
enemies = []
for item in list_enemies:
    enemies.append(Enemy(item[1][0], item[1][1], item[0]))

# --- Girl sprites
imgs_girl = []
img_girl = None
for i in range(7):
    numimg = str(i + 1) + ".png"
    imgs_girl.append(pygame.transform.scale((pygame.image.load(os.path.join("images", numimg))).convert_alpha(), (96, 96)))
img_girl = pygame.transform.scale((pygame.image.load(os.path.join("images", "1.png"))).convert_alpha(), (96, 96))
# --- Poppy avatar 
avatar = pygame.transform.scale((pygame.image.load(os.path.join("images", "avatar.png"))).convert_alpha(), (40, 40))

clock = pygame.time.Clock()

run = True

while run:

    clock.tick(60)
    pos = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                pass
        if event.type == pygame.MOUSEBUTTONDOWN and game_over: # --- Player is killed
            if pos[0] in range(int(width / 2 + 10), int(width / 2 + 60))and pos[1] in range(int(height / 2 + 75), int(height / 2 + 95)):
                pl.x -= 300
                pl.y = pl.platforms[0]
                pl.health = 1
                pl.layer_now = 0
                game_over = False
        if event.type == pygame.MOUSEBUTTONDOWN and lives == 0: # --- Player is completely killed 
            if pos[0] in range(int(width / 2 + 10), int(width / 2 + 60))and pos[1] in range(int(height / 2 + 75), int(height / 2 + 95)):
                pl.x = 50
                pl.y = pl.platforms[0]
                pl.index_dialog = 0
                pl.health = 1
                pl.layer_now = 0
                pl.kill_count = 0
                for enemy in enemies:
                    enemy.killed = False
                lives = 3
        if event.type == pygame.MOUSEBUTTONDOWN and not game_run: # --- Start button is activated
            if pos[0] in range(int(width / 2 + 30), int(width / 2 + 120))and pos[1] in range(int(height / 2 + 90), int(height / 2 + 115)):
                game_run = True
                
    # Draw blue background
    win.blit(sk, (0,0))
    # Draw transparent nuages
    win.blit(nuages, (-1 * (round(pl.x * 0.2) % width), 0))
    win.blit(nuages, (-1 * (round(pl.x * 0.2) % width) + width, 0))
    # Draw grass, ground, locations
    if pl.x >= width / 2 and pl.x < bg.get_width() - width / 2:
        win.blit(bg, (-1 * (pl.x - width / 2), 0))
    elif pl.x >= bg.get_width() - width / 2:
        win.blit(bg, (-1 * (bg.get_width() - width), 0))
    else:
        win.blit(bg, (0, 0))
    # --- Draw avatar and info --- right-top corner ---
    win.blit(avatar, (705,30))
    AVATAR_FONT.render_to(win, (665, 75), str_count_enemies + str(pl.kill_count), (0, 0, 0))
    AVATAR_FONT.render_to(win, (700, 90), str_count_lives + str(lives), (139, 0, 0))
    pygame.draw.rect(win, (255, 0, 0), (705, 15, 40, 7), 0)
    pygame.draw.rect(win, (0, 255, 0), (705, 15, 40 * pl.health, 7), 0)

    #pygame.draw.circle(win, (255,0,0), (pl.x, 100), 10, 0)
    if game_run:
        if lives > 0:
            if pl.health > 0:
                pl.set_text(GAME_FONT, win, pl.kill_count)
                pl.move(win, width, enemies)        
                #pygame.draw.rect(win, (220, 220, 220), (pl.player_x, pl.y, 10, 10), 0)
                for enemy in enemies:
                    enemy.move(win, width, pl.x, pl.layer_now, pl.health, pl.jump)
            else: # --- Player is killed
                if not game_over:
                    lives -= 1
                game_over = True
                pygame.draw.rect(win, (255, 255, 255), (width / 2 - 60, height / 2, 190, 110), 0)
                pygame.draw.rect(win, (220, 220, 220), (width / 2 + 10, height / 2 + 75, 50, 20), 0)
                GAME_FONT.render_to(win, (width / 2 - 45, height / 2 + 20), "Poppy est malade ...", (0, 0, 0))
                GAME_FONT.render_to(win, (width / 2 - 45, height / 2 + 45), "Il faut le soigner !", (0, 0, 0))
                GAME_FONT.render_to(win, (width / 2 + 25, height / 2 + 80), "OK", (0, 0, 0))
        else: # --- Player is completely killed 
            pygame.draw.rect(win, (255, 255, 255), (width / 2 - 60, height / 2, 190, 110), 0)
            pygame.draw.rect(win, (220, 220, 220), (width / 2 + 10, height / 2 + 75, 50, 20), 0)
            GAME_FONT.render_to(win, (width / 2 - 45, height / 2 + 20), "Tu es perdu ...", (0, 0, 0))
            GAME_FONT.render_to(win, (width / 2 - 45, height / 2 + 45), "Cliquez pour revenir", (0, 0, 0))
            GAME_FONT.render_to(win, (width / 2 + 25, height / 2 + 80), "OK", (0, 0, 0))
    else: # --- Draw start window
        pygame.draw.rect(win, (255, 255, 255), (width / 2 - 150, height / 2 - 230, 450, 370), 0)
        pygame.draw.rect(win, (220, 220, 220), (width / 2 + 30, height / 2 + 90, 90, 25), 0)
        win.blit(menu_img, (width / 2 - 100, height / 2 - 200))
        GAME_FONT.render_to(win, (width / 2 - 12, height / 2 - 120), "Les boutons du clavier", (139, 0, 0))
        GAME_FONT.render_to(win, (width / 2 - 12, height / 2 - 100), "pour contrôler Poppy:", (139, 0, 0))
        GAME_FONT.render_to(win, (width / 2 - 22, height / 2 - 60), "E - Lancer une bulle magic", (0, 0, 0))
        GAME_FONT.render_to(win, (width / 2 - 22, height / 2 - 30), "SPACE - Sauter", (0, 0, 0))
        GAME_FONT.render_to(win, (width / 2 - 22, height / 2 + 0), "PgLeft - Aller à gauche", (0, 0, 0))
        GAME_FONT.render_to(win, (width / 2 - 22, height / 2 + 30), "PgRight - Aller à droite", (0, 0, 0))
        GAME_FONT.render_to(win, (width / 2 - 12, height / 2 + 60), "Cliquez sur ce bouton", (34, 139, 34))
        GAME_FONT.render_to(win, (width / 2 + 52, height / 2 + 98), "Allez!", (0, 0, 0))
        
    pygame.display.update()
            
    #keys = pygame.key.get_pressed()
    
pygame.quit()