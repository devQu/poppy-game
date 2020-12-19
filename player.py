import pygame, os, math, pygame.freetype
from enemy import Enemy

class Player():

    def __init__(self):
        self.img = None
        self.imgs_run = []
        self.imgs_stay = None
        self.imgs_spark = []
        self.imgs_balls = []
        self.img_ball = None
        self.ball_step = 0
        self.y_ball_fly = 440
        self.pew = False
        self.push = 0
        self.x = 50
        self.y = 404
        self.player_x = self.x
        self.animation_count = 0
        self.animation_ball_count = 0
        self.step = 5
        self.ifright = True
        self.if_ball_right = True
        self.jump = False # -- if Player is jumping now
        self.fall = False # -- if Player is falling now
        self.jump_k = 5 # -- koefficient of jump height 
        self.jump_up = False # -- if jump in place
        self.dialog_text = [[100, 350, "Qu'est-ce qui s'est passé ici ??"],
                            [350, 550, "Oh, la la ..."],
                            [850, 950, "Wow ... C'est bien de la magie !"],
                            [1050, 1150, "C'est incroyable ! Je l'ai dans les mains .../Poppy est devenu un vrai sorcier !"]]
        self.level_text = ["Oh ... C'était dur./Quelle est la prochaine étape ?", "Bientôt je pourrais aller /à la maison ..."]
        self.int_temp = [] # --- Interval for view level_text
        self.check_text = False # --- For calculate and write text area
        self.check_text_dem = True # --- For display phrase in check_text while Player in int_temp
        self.index_dialog = 0 # --- Index of current phrase of dialog_text
        self.index_level_text = 0 # --- Index of current phrase of level_text
        self.index_break = 0
        self.letter = 0 # --- Position of letter for draw dialog text
        self.line_break = False # --- For break line of dialog text
        self.stop = False # --- For stop Player
        self.x_temp = self.x
        self.layers = [(1, (1590, 2185)), (2, (1590, 2185)), (3, (1590, 2185)), (1, (3385, 4525)), (2, (3530, 4400)), (3, (3675, 4250)), (4, (3770, 4160))]
        self.platforms = [404, 317, 230, 149]
        self.layer_now = 0 # --- Current height level of the Player
        self.kill_count = 0 # --- Quantity of enemies killed

        self.jump_sound = pygame.mixer.Sound(os.path.join("sounds", "jump.wav"))
        self.jump_sound.set_volume(0.1)
        self.poppy_sound = pygame.mixer.Sound(os.path.join("sounds", "poppy.wav"))
        self.poppy_sound.set_volume(0.9)
        
        self.health = 1
        
        # Images
        for i in range(12):
            number = str(i) + ".png"
            self.imgs_run.append(pygame.transform.scale((pygame.image.load(os.path.join("images", number))).convert_alpha(), (96, 96)))

        self.imgs_stay = pygame.transform.scale((pygame.image.load(os.path.join("images", "0.png"))).convert_alpha(), (96, 96))
    
        for i in range(8):
            number = "spark" + str(i + 1) + ".png"
            self.imgs_spark.append(pygame.transform.scale((pygame.image.load(os.path.join("images", number))).convert_alpha(), (60, 60)))
        for i in range(7):
            number = "ball" + str(i + 1) + ".png"
            self.imgs_balls.append(pygame.transform.scale((pygame.image.load(os.path.join("images", number))).convert_alpha(), (20, 20)))
    
    def set_text(self, font, win, killed): 

        # --- For diapason text --- dialog_text
        if self.x >= self.dialog_text[self.index_dialog][0] and self.x <= self.dialog_text[self.index_dialog][1]:
            # --- Draw text
            if self.line_break:
                font.render_to(win, (self.player_x - 50, self.y - 5), self.dialog_text[self.index_dialog][2][self.index_break + 1:self.letter], (255, 255, 255))
            else:
                self.index_break = self.letter
            font.render_to(win, (self.player_x - 50, self.y - 20), self.dialog_text[self.index_dialog][2][0:self.index_break], (255, 255, 255))
            
            if self.letter < len(self.dialog_text[self.index_dialog][2]):
                # --- If the text contains the symbol
                if self.dialog_text[self.index_dialog][2][self.letter] == "/":
                    self.index_break = self.dialog_text[self.index_dialog][2].index("/")
                    self.line_break = True
                self.letter += 1
                self.stop = True
            else:
                self.stop = False
        if self.x > self.dialog_text[self.index_dialog][1]: # --- If Player crossed the border
            self.letter = 0 # --- Reset number of letter of current phrase
            if self.index_dialog < len(self.dialog_text) - 1:
                self.index_dialog += 1 # --- Activate the next phrase
                
        # --- Full shit hindu code !!!
        # --- For event text --- level_text        
        if killed == 4 and self.check_text_dem or killed == 11 and self.check_text_dem:
            if not self.check_text:
                self.int_temp.extend((self.x - 150, self.x + 150))
                self.check_text = True
            if "/" in self.level_text[self.index_level_text]:
                slash = self.level_text[self.index_level_text].index("/")
                if self.x in range(self.int_temp[0], self.int_temp[1]):
                    font.render_to(win, (self.player_x - 50, self.y - 20), self.level_text[self.index_level_text][0: slash], (255, 255, 255))
                    font.render_to(win, (self.player_x - 50, self.y - 5), self.level_text[self.index_level_text][slash + 1: ], (255, 255, 255))
                else:
                    self.index_level_text += 1
                    self.check_text_dem = False
            else:
                if self.x in range(self.int_temp[0], self.int_temp[1]):
                    font.render_to(win, (self.player_x - 50, self.y - 20), self.level_text[self.index_level_text], (255, 255, 255))
                else:
                    self.index_level_text += 1
                    self.check_text_dem = False
        if killed == 5 or killed == 12:
            self.check_text_dem = True
            self.check_text = False
            self.int_temp = []
        
        
    # --- Move player in left and right
    def move(self, win, width_window, enemies):

        window = win
        now_key = pygame.key.get_pressed()
        self.magic_ball(window, width_window, now_key, enemies) # --- Magic ball action !!!

        if not self.jump:
            if now_key[pygame.K_LEFT] and self.x > self.step:
            
                if now_key[pygame.K_SPACE]:
                    self.jump_sound.play()
                    self.jump = True
                    
                self.falling()
            
                if self.ifright:
                    self.flip()
                if not self.stop: # --- If text in the screen
                    self.img = self.imgs_run[self.animation_count // 2]
                    self.animation_count += 1
                    self.x -= self.step

                    if self.animation_count >= len(self.imgs_run) * 2:
                        self.animation_count = 0
                    
                self.draw(window, now_key, width_window)
                
            elif now_key[pygame.K_RIGHT] and self.x < 8000 - 96 - self.step :
            
                if now_key[pygame.K_SPACE]:
                    self.jump_sound.play()
                    self.jump = True
            
                self.falling()
            
                if not self.ifright:
                    self.flip()
                if not self.stop: # --- If text in the screen
                    self.img = self.imgs_run[self.animation_count // 2]
                    self.animation_count += 1
                    self.x += self.step

                    if self.animation_count >= len(self.imgs_run) * 2:
                        self.animation_count = 0
                    
                self.draw(window, now_key, width_window)
                
            elif now_key[pygame.K_SPACE]:
                self.jump_sound.play()
                self.jump = True
                self.jump_up = True
                
            else:
                self.draw(window, now_key, width_window)
        else:
            up_down = 1
            if self.jump_k >= -5:
                if self.jump_k < 0: # --- for move down
                    up_down = -1
                if self.ifright and not self.jump_up: # --- if moving right
                    self.x += self.step - 1
                elif not self.ifright and not self.jump_up:
                    self.x -= self.step - 1                 
                # Verified if a lavel
                for i, item in enumerate(self.layers):
                    if self.x in range(item[1][0], item[1][1]):
                        if self.layer_now == 0 and item[0] == 1:
                            if up_down == -1 and self.y == 311.25:
                                self.y = 317
                                self.layer_now = 1
                                self.jump = False
                                self.jump_k = 5
                                self.jump_up = False
                        elif self.layer_now == 1 and item[0] == 2:
                            if up_down == -1 and self.y == 222:
                                self.y = 230
                                self.layer_now = 2
                                self.jump = False
                                self.jump_k = 5
                                self.jump_up = False
                        elif self.layer_now == 2 and item[0] == 3:
                            if up_down == -1 and self.y == 133.75:
                                self.y = 149
                                self.layer_now = 3
                                self.jump = False
                                self.jump_k = 5
                                self.jump_up = False
                        elif self.layer_now == 3 and item[0] == 4:
                            if up_down == -1 and self.y == 52.75:
                                self.y = 78
                                self.layer_now = 4
                                self.jump = False
                                self.jump_k = 5
                                self.jump_up = False
                    else:
                        self.layer_now == 0
                    
                if self.jump:        
                    self.y -= (self.jump_k ** 2) * up_down 
                    self.jump_k -= 0.5
            else:
                self.jump = False
                self.jump_k = 5
                self.jump_up = False
                self.falling()
                
            self.draw(window, now_key, width_window)           
    
    # --- Draw Player
    def draw(self, win, key, W):
        
        if self.x < W / 2:
            self.player_x = self.x
        elif self.x >= 8000 - W / 2:
            self.player_x = W / 2 + W / 2 - (8000 - self.x)
        else:
            self.player_x = W / 2
        
        if key[pygame.K_RIGHT] or key[pygame.K_LEFT]:
            win.blit(self.img, (self.player_x, self.y))
        else:
            win.blit(self.imgs_stay, (self.player_x, self.y))
    
    # --- Flip player
    def flip(self):
        
        self.imgs_stay = pygame.transform.flip(self.imgs_stay, True, False)
        for i, img in enumerate(self.imgs_run):
            self.imgs_run[i] = pygame.transform.flip(img, True, False)
            
        self.ifright = False if self.ifright else True
        
    # --- Falling on the ground
    def falling(self):

        if self.layer_now > 0:
            done = False
            
            for item in self.layers:
                if self.layer_now == item[0]:
                    if self.x in range(item[1][0], item[1][1]):
                        done = True
                        break
                    else: 
                        done = False
            if not done:
                self.y = self.platforms[self.layer_now - 1]
                self.layer_now -= 1

    # --- Magic ball's processing
    def magic_ball(self, win, width_window, key, enemies):

        y_ball = 440
        x_ball = 1000 - self.push
        ball_left = 60 if self.ifright else 15 # --- If Player flip
        if self.x >= width_window / 2:
            self.push = self.x - width_window / 2
        if self.x >= 1000:
            self.imgs_spark = self.imgs_balls.copy()
            #y_ball = self.y + 60
            
            if key[pygame.K_e]:
                self.pew = True
                self.if_ball_right = True if self.ifright else False
                self.y_ball_fly = self.y + 60
            if self.pew: # --- If Player shoots a ball
                if self.if_ball_right:
                    self.ball_step += 10 # --- Speed of ball
                else:
                    self.ball_step -= 10
                x_ball = self.x + ball_left + self.ball_step - self.push # --- X + displacement + step - (X - W/2)
                y_ball = self.y_ball_fly

                if x_ball > width_window or x_ball <= 0: # --- Return ball to Player
                    self.pew = False
                    self.ball_step = 0
                    x_ball = self.player_x + ball_left + self.ball_step
            else:
                x_ball = self.player_x + ball_left + self.ball_step
                y_ball = self.y + 60
                
            for enemy in enemies:
                if enemy.player_hit: # --- If enemy item hits Player 
                    if self.health > 0:
                        self.health = round((lambda x: x - 0.2)(self.health), 1)
                        
                if math.fabs(enemy.x - self.push - x_ball) <= 5 and enemy.layer == self.layer_now and self.pew and not enemy.killed: # --- Delete Enemy if a ball collide him
                    self.poppy_sound.play()
                    enemy.killed = True
                    self.kill_count += 1
                    enemy.animation_count = 0
                    self.pew = False
                    self.ball_step = 0
                    x_ball = self.player_x + ball_left + self.ball_step
            
        self.img_ball = self.imgs_spark[self.animation_ball_count // 3]
        self.animation_ball_count += 1

        if self.animation_ball_count >= len(self.imgs_spark) * 2:
            self.animation_ball_count = 0

        win.blit(self.img_ball, (x_ball, y_ball))




