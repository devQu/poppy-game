import pygame, os, math
#from player import Player

class Enemy():

    def __init__(self, x, y, if_left):
    
        self.killed = False # --- For kill enemy item
        self.fell_down = False
        self.imgs_mouses = []
        self.imgs_mouses_died = []
        self.imgs_mouses_attack = []
        self.img_mouse_died = None
        self.x = x
        
        if y == 0: # --- For install enemy in a platform --- 4 levels
            self.y = 428
        elif y == 1:
            self.y = 340
        elif y == 2:
            self.y = 253
        elif y == 3:
            self.y = 174
        elif y == 4:
            self.y = 98
            
        self.layer = y
        
        self.animation_count = 0
        self.step = 1 # --- Speed of walking
        self.left = if_left
        self.dis = 200 # --- Walking radius
        self.radius_attack = 250 # --- Attack radius
        self.attack = False # --- For activate attack regime
        self.player_hit = False # --- If enemy deals damage

        self.left_edge = self.x - self.dis
        self.right_edge = self.x + self.dis
        
        self.flip_action = False
        self.push = 0
        
        if self.left:
            self.flip_action = True
            
        for i in range(6):
            number = "h" + str(i + 1) + ".png"
            self.imgs_mouses.append(pygame.transform.scale((pygame.image.load(os.path.join("images", number))).convert_alpha(), (60, 60)))
        for i in range(6):
            number = "h_die" + str(i + 1) + ".png"
            self.imgs_mouses_died.append(pygame.transform.scale((pygame.image.load(os.path.join("images", number))).convert_alpha(), (80, 60)))
        for i in range(6):
            number = "h_attack" + str(i + 1) + ".png"
            self.imgs_mouses_attack.append(pygame.transform.scale((pygame.image.load(os.path.join("images", number))).convert_alpha(), (60, 60)))
        self.img_mouse_died = pygame.transform.scale((pygame.image.load(os.path.join("images", "h_die6.png"))).convert_alpha(), (80, 60))
        
    def move(self, win, width_window, pl_x, pl_layer_now, pl_health, pl_jump):
    
        self.push = pl_x - width_window / 2
        danger_dis = self.x - pl_x
        self.player_hit = False
    
        if math.fabs(danger_dis) < self.radius_attack and self.layer == pl_layer_now:
            self.attack = True
        else:
            self.attack = False
        
        if not self.killed:
        
            if not self.attack:

                self.img = self.imgs_mouses[self.animation_count // 3]
                self.animation_count += 1
                self.step = 1
                
                if self.left:
                    if self.x > self.left_edge:
                        self.x -= self.step
                    else:
                        self.left = False
                        self.flip_action = True
                else:
                    if self.x < self.right_edge:
                        self.x += self.step
                    else:
                        self.left = True
                        self.flip_action = True
                

                if self.animation_count >= len(self.imgs_mouses) * 3:
                    self.animation_count = 0
                    
            else:
                
                if math.fabs(danger_dis) < 35:
                    self.img = self.imgs_mouses_attack[self.animation_count // 3]
                    self.animation_count += 1
                    self.step = 0
                    self.player_hit = False
                    if self.animation_count >= len(self.imgs_mouses_attack) * 3:
                        self.animation_count = 0
                        if not pl_jump:
                            self.player_hit = True
                        else:
                            self.player_hit = False
                            
                        
                else:
                    self.img = self.imgs_mouses[self.animation_count // 3]
                    self.animation_count += 1
                    self.step = 3
                    
                    if danger_dis > 0:
                        if not self.left:
                            self.left = True
                            self.flip_action = True
                        self.x -= self.step
                    elif danger_dis <= 0:
                        if self.left:
                            self.left = False
                            self.flip_action = True
                        self.x += self.step

                    if self.animation_count >= len(self.imgs_mouses) * 3:
                        self.animation_count = 0
                    
            #self.img = pygame.transform.flip(self.img, True, False)
            if self.flip_action:
                for i, image in enumerate(self.imgs_mouses):
                    self.imgs_mouses[i] = pygame.transform.flip(image, True, False)
                for i, image in enumerate(self.imgs_mouses_attack):
                    self.imgs_mouses_attack[i] = pygame.transform.flip(image, True, False)
                self.flip_action = False

            win.blit(self.img, (self.x - self.push, self.y))
        
        else:
            if not self.fell_down:
                self.img = self.imgs_mouses_died[self.animation_count // 3]
                self.animation_count += 1
                
                if self.animation_count >= len(self.imgs_mouses_died) * 3:
                    self.animation_count = 0
                    self.fell_down = True
            else:
                self.img = self.img_mouse_died
                
            win.blit(self.img, (self.x - self.push, self.y + 10))
            