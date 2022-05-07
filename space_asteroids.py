import pygame, random
import os
import sys
import warnings
import pandas as pd


dir = 'C:\\Game\\Assets' #change this to your desktop 
#https://stackoverflow.com/questions/50725706/pygame-collision-between-2-objects-in-the-same-group
#https://stackoverflow.com/questions/16161169/pygame-stop-movement-on-collision-detection

#Initialize pygame
pygame.init()

class Game():
    level_key = 1 #Variable to capture level parameter
    """A class to help control and update gameplay"""
    def __init__(self, player, asteroid_group, player_bullet_group,my_coin_group):
        """Initialze the game"""
        
        #Set game values
        self.round_number = 1 
        self.round_time = 60
        self.Starting_round_time = 60
        self.score = 0
        self.asteroid_iterator = 0 
        self.frame_count = 0
        self.player = player #initiliase the objects from passed in objects as above
        self.asteroid_group = asteroid_group #initiliase the objects from passed in objects as above
        self.player_bullet_group = player_bullet_group #initiliase the objects from passed in objects as above
        self.my_coin_group = my_coin_group #initiliase the objects from passed in objects as above

        #Set sounds
        self.coin_sound = pygame.mixer.Sound(dir + "\\sounds\\CoinCollect.mp3")
        self.coin_sound.set_volume(2)
        
        self.explosion = pygame.mixer.Sound(dir + "\\sounds\\explosion.wav")
        self.explosion.set_volume(0.25)
        
        # self.collision = pygame.mixer.Sound(dir + "\\sounds\\collision.wav")
        # self.collision.set_volume(0.2)
        
        pygame.mixer.music.load(dir + "\\Sounds\\Alone Against Enemy.ogg")
        pygame.mixer.music.set_volume(0.3)
    
    def update(self):
        """Update the game"""
        #Update the round time every second
        self.asteroid_iterator += 1
        self.frame_count +=1
        self.level_key = 'L' + str(self.round_number)
        
        if self.asteroid_iterator == game_dict[round][2]: #Game level parameter asteroids 
            self.asteroid_iterator = 0 #set asteroid iterator back to 0
            self.add_asteroid() #add asteroid every half second (30),
        
        if self.frame_count ==60: #every second
            self.round_time-=1 #move round time down by 1
            self.frame_count = 0 #restart framecount
            
        self.check_collisions() #run the check_collisions function
        self.check_round_completion() #every loop run the round_completion
        self.check_game_over() #every second check to see if the game over condition is met
        
        return(self.level_key)
        
    
    def check_round_completion(self):
        """Check if the player passed round time"""
        if self.round_time <= 0: #when round time gets to zero
            self.start_new_round() #run start new round function
            
    def start_new_round(self):
        """Start a new level"""
        if self.round_number <5:
            self.round_number += 1 #increment the round number
        else:
            self.round_number = 5
        self.player.player_bullet +=1 #increment number of bullets
    
        #Reset round values
        self.round_time = self.Starting_round_time #reset round time

        self.player.reset() #reset the player
        self.pause_game("Entering Level " + str(self.round_number), "Press 'Enter' to continue...")
    
    def check_collisions(self):
        """Check for collisions between player and asteroid"""
        invisible = self.player.invisible
        #Check for collision between a player and asteroid
        collided_asteroid = pygame.sprite.spritecollideany(self.player, self.asteroid_group) #Simple test if a sprite intersects anything in a group.
       
        #We collided with an asteroid
        if collided_asteroid and invisible == False: #if we collided with asteroid and we are not invisible
            # Collided with asteroid
            self.player.player_loss.play() #player die sound
            self.player.lives -= 1 #Player loses one life
            self.player.invisible = True #make us invisible
            collided_asteroid.kill()
            if self.round_number >=1: #too many asteroids kill them all
                self.asteroid_group.empty() #empty all the sprite groups
                                    
        #If asteroid hits itself 
        for asteroid in self.asteroid_group:
            sprite_collide = pygame.sprite.spritecollide(asteroid, self.asteroid_group, False,pygame.sprite.collide_mask)
            if len(sprite_collide) > 1:
                #print('first asteroid collide right')
                #sprite_collide[0].rect.right = sprite_collide[1].rect.left
                asteroid.dx = asteroid.dx*-1
                # sprite_collide[0].velocity+=game_dict[round][1]*.30 #1 #1.75
                sprite_collide[0].velocity+=1 #1.75 
                
                while(asteroid.velocity>=4): #slow down 
                        asteroid.velocity-=0.5 
                    
                # while(asteroid.velocity>=game_dict[round][1]): #slow down #ACCESS DICTIONARY UPPER VALUE RANGE on index 0
                #     asteroid.velocity-=(game_dict[round][1]*0.5)
        
        #See if any bullet in the player bullet group hit an asteroid in the asteroid group
        bullet_collide = pygame.sprite.groupcollide(self.player_bullet_group, self.asteroid_group, True, True)
        if bullet_collide: #true kill group A, true kill group B
            for bullet in bullet_collide:
                if bullet.rect.y>0: #only hit asteroids in screen
                    Coin = Coins(bullet.rect.centerx, bullet.rect.top) #pass position of bullet collision to asteroid to Coins Class to generate a coin
                    self.my_coin_group.add(Coin) #add new coin to coin group
                    self.explosion.play() #play explosion sound
                
        #Check for collision between player and coin
        collided_coin = pygame.sprite.spritecollideany(self.player, self.my_coin_group) #Simple test if a sprite intersects anything in a group.
        if collided_coin:
            self.coin_sound.play() #play the coin sound
            collided_coin.kill()
            self.score += 10 #increment score
            
                    
    def draw(self):
        """Draw the game HUD"""
        #Set colors
        PINK = (255, 200, 255)
        PURPLE = (128, 0, 128)
    
        #Set text
        score_text = HUD_font.render("Score: " + str(self.score), False, PURPLE)
        score_rect = score_text.get_rect()
        score_rect.topleft = (50, WINDOW_HEIGHT - 30)
        
        round_text = HUD_font.render("Round: " + str(self.round_number), False, PURPLE)
        round_rect = round_text.get_rect()
        round_rect.topleft = (170, WINDOW_HEIGHT - 30)
        
        health_text = HUD_font.render("Health: " + str(self.player.lives), False, PURPLE)
        health_rect = score_text.get_rect()
        health_rect.topleft = (WINDOW_WIDTH-260, WINDOW_HEIGHT - 30)
        
        time_text = HUD_font.render("Time: " + str(self.round_time), False, PURPLE)
        time_rect = score_text.get_rect()
        time_rect.topleft = (WINDOW_WIDTH-135, WINDOW_HEIGHT - 30)

        title_text = title_font.render("Space Asteroids", True, PINK)
        title_rect = title_text.get_rect()
        title_rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT - 25)

        #Draw the HUD
        display_surface.blit(score_text, score_rect)
        display_surface.blit(health_text, health_rect)
        display_surface.blit(title_text, title_rect)
        display_surface.blit(round_text, round_rect)
        display_surface.blit(time_text, time_rect)
    
    def add_asteroid(self):
        """Add an asteroid to the game"""
          
        for i in range(self.round_number):
            asteroid = Asteroid(self.round_number) #create a new asteroid by running asteroid class and saving asteroid to a variable (use to add that to asteroid class)
            self.asteroid_group.add(asteroid) #add the above asteroid variable to the asteroid group
            #print("There are {} asteroids.".format(len(self.asteroid_group)))
            
    def check_game_over(self):
        """Check to see if the player lost the game"""
        if self.player.lives <= 0: #you have died no health
            pygame.mixer.music.stop()
            outcome = self.pause_game("Game Over! Final Score: " + str(self.score), "Press 'Enter' to play again...")
            if outcome == 'Play':
                self.reset_game() #reset the game
            else:
                warnings.filterwarnings("ignore")
                sys.exit()
            
    def pause_game(self, main_text, sub_text):
        """Pause the game"""
        
        self.player_bullet_group.empty() #empty all the sprite groups
        self.asteroid_group.empty() #empty all the sprite groups
        self.my_coin_group.empty() #empty all the sprite groups
        
        global running #we need to make running a global variable so we can influence the running variable in the game loop

        pygame.mixer.music.pause() #pause the music
        self.player.Thrusters.stop() #stop thruster sound

        #Set colors
        PINK = (255, 150, 255)
        WHITE = (255, 255, 255)
        BLACK = (0, 0, 0)

        #Create main pause text
        main_text = Game_Over_Font.render(main_text, True, PINK)
        main_rect = main_text.get_rect()
        main_rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2)

        #Create sub pause text
        sub_text = Game_Over_Font.render(sub_text, True, WHITE)
        sub_rect = sub_text.get_rect()
        sub_rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2 + 84)

        #Display the pause text
        display_surface.fill(BLACK)
        display_surface.blit(main_text, main_rect)
        display_surface.blit(sub_text, sub_rect)
        pygame.display.update()

        #Pause the game until user hits enter or quits
        is_paused = True
        while is_paused:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    #User wants to continue
                    if event.key == pygame.K_RETURN:
                        is_paused = False #set boolean to false
                        pygame.mixer.music.unpause() #unpause the game
                        return 'Play'
                #User wants to quit
                if event.type == pygame.QUIT:
                    is_paused = False
                    running = False
                    pygame.mixer.music.stop()
                    pygame.quit()
                    return 'Quit'
                
    def high_score(self, main_text, sub_text):
        """Pause the game"""
        
        self.player_bullet_group.empty() #empty all the sprite groups
        self.asteroid_group.empty() #empty all the sprite groups
        self.my_coin_group.empty() #empty all the sprite groups
        
        global running #we need to make running a global variable so we can influence the running variable in the game loop

        pygame.mixer.music.pause() #pause the music
        self.player.Thrusters.stop() #stop thruster sound

        #Set colors
        PINK = (255, 150, 255)
        WHITE = (255, 255, 255)
        BLACK = (0, 0, 0)

        #Create main pause text
        main_text = Game_Over_Font.render(main_text, True, PINK)
        main_rect = main_text.get_rect()
        main_rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2)

        #Create sub pause text
        sub_text = Game_Over_Font.render(sub_text, True, WHITE)
        sub_rect = sub_text.get_rect()
        sub_rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2 + 84)

        #Display the pause text
        display_surface.fill(BLACK)
        display_surface.blit(main_text, main_rect)
        display_surface.blit(sub_text, sub_rect)
        pygame.display.update()

        #Pause the game until user hits enter or quits
        is_paused = True
        while is_paused:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    #User wants to continue
                    if event.key == pygame.K_RETURN:
                        is_paused = False #set boolean to false
                        pygame.mixer.music.unpause() #unpause the game
                        return 'Play'
                #User wants to quit
                if event.type == pygame.QUIT:
                    is_paused = False
                    running = False
                    pygame.mixer.music.stop()
                    pygame.quit()
                    return 'Quit'
                    
    def reset_game(self):
        """Reset the game"""
        #Reset game values
        self.score = 0
        self.round_number = 1 #start from the beginning
        self.round_time = self.Starting_round_time

        #Reset the player
        self.player.lives = self.player.Starting_lives #Set the player health to the starting value
        self.player.reset()  #Set the player health to the starting value
        self.player.player_bullet = 2 #reset bullets to 2

        #Empty sprite groups
        self.player_bullet_group.empty() #empty all the sprite groups
        self.asteroid_group.empty() #empty all the sprite groups
        self.my_coin_group.empty() #empty all the sprite groups

        pygame.mixer.music.play(-1, 0.0) #start the music again

class Background():
      def __init__(self):
            self.bgimage = BCK
            
            self.rectBGimg = self.bgimage.get_rect()
            self.bgY1 = 0
            self.bgX1 = 0
             
            self.bgY2 = -self.rectBGimg.height 
            self.bgX2 = 0                   
            
      def update(self):
        self.movingUpSpeed = game_dict[round][3] #Game parameter for background speed
        self.bgY1 += self.movingUpSpeed
        self.bgY2 += self.movingUpSpeed

        if self.bgY1 >= self.rectBGimg.height:
            self.bgY1 = 0
        if self.bgY2 >= 0:
            self.bgY2 = -self.rectBGimg.height

      def render(self):
         display_surface.blit(self.bgimage, (self.bgX1, self.bgY1))
         display_surface.blit(self.bgimage, (self.bgX2, self.bgY2)) 
    
class Player(pygame.sprite.Sprite): #This is a child class - inheriting from sprites in Pygame.
    """A class to model a spaceship the user can control"""
    itera = 0 #Capture an iterator to use in the PlayerFlame
    def __init__(self, bullet_group):
        """Initialize the player"""
        super().__init__() #initiliase our super class because it’s a sub class we call super() (inheriting SPRITE CLASS)
       
        self.lives = 3 #number of lives
        self.Starting_lives = 3 #starting lives
        self.velocity = 5 #velocity of the ship
        self.iter = 0 #flame iterable
        self.invisible = False
        self.frame_count = 0 #invisible iterator
        self.blinks = 0 #blink iterator
        self.frames_counter = 0 
        self.player_bullet = 2
        
        self.player_loss = pygame.mixer.Sound(dir + "\\sounds\\Loss3.wav")
        self.player_loss.set_volume(0.5)

        self.bullet_group = bullet_group #passed bullet group initiliase in player class

        self.shoot_sound = pygame.mixer.Sound(dir + "\\sounds\\tir.mp3") #shoot sound
        self.shoot_sound.set_volume(0.35)
                                                   
        #Moving the ship straight
        self.move_straight_sprites = move_straight_sprites
        
        #Placing Ship
        self.current_sprite = 0
        self.image = self.move_straight_sprites
        self.rect = self.image.get_rect()
        self.rect.centerx = WINDOW_WIDTH//2 #place the image middle of screen
        self.rect.bottom = WINDOW_HEIGHT-60 #place bottom of screen
        
        #Moving the ship animations
        self.move_right_sprites = move_right_sprites
        self.move_left_sprites = move_left_sprites
        
        #Load sounds
        # self.channel1 = pygame.mixer.Channel(0)
        self.Thrusters = pygame.mixer.Sound(dir + "/sounds/Thrust2.wav")
        self.Thrusters.set_volume(0.5)
        
    def update(self):
        """Update the player (move player)"""

        self.image.set_alpha(1000) #visible 
        if self.invisible:
            self.frame_count += 1 #iterate once invisible
            self.blinks+=1 #iterate blinks
            if self.blinks <= 2:
                self.image.set_alpha(0) #invisible 
                
            elif self.blinks >2 and self.blinks<=3:
                self.image.set_alpha(1000) #visible 
                self.blinks=0                
            
            if self.frame_count >= 90 and self.invisible: #invisibility check 
                self.invisible = False #reset invisible flag to true after 1.5 seconds
                self.frame_count = 0  #reset iterator        
        
        keys = pygame.key.get_pressed() #get the list of pressed keys

        #Move the player within the bounds of the screen
        if keys[pygame.K_LEFT] and self.rect.left > 5 and self.invisible == False:
            self.rect.x -= self.velocity
            self.animate(self.move_left_sprites, 1,self.invisible) #when we move left call the animate function passing in the left_sprites list and speed we move the animation
        
        elif not keys[pygame.K_LEFT] and self.invisible == False: 
            self.MoveStraight(move_straight_sprites,self.invisible)
        
        if keys[pygame.K_RIGHT] and self.rect.right < (WINDOW_WIDTH*.99) and self.invisible == False:
            self.rect.x += self.velocity
            self.animate(self.move_right_sprites, 1,self.invisible) #when we move right call the animate function passing in the right sprite list and speed we move the animation
        
        if keys[pygame.K_UP] and self.rect.top > 5 and self.invisible == False:
            self.rect.y -= self.velocity
            PlayerFlame(self.rect.centerx, self.rect.bottom,self.iter) #pass center position of our ship x, bottom of the ship y, flame group and move_straight_flames to the PlayerFlame class
            
        if keys[pygame.K_DOWN] and self.rect.bottom<WINDOW_HEIGHT-50 and self.invisible == False:
            self.rect.y += self.velocity
        
        if not keys[pygame.K_UP] or self.rect.top <= 5: #turn off thrusters when not key up
            pygame.mixer.fadeout(1000)
            self.Thrusters.stop()
            pygame.mixer.fadeout(400)
        
        if self.invisible: #if we are invisible since we got hit by asteroid
            self.stop_sound() #stop the thruster sound
            self.MoveStraight(move_straight_sprites,self.invisible) #ensure our move sprite is straight
            original_x = self.rect.centerx
            original_y = self.rect.bottom
            #logic to glide back to starting position
            if original_x > WINDOW_WIDTH//2 and self.frames_counter<=60:
                self.frames_counter += 1
                self.rect.centerx = self.rect.centerx - (original_x - WINDOW_WIDTH//2)/20
                self.frames_counter = 0
            if original_x < WINDOW_WIDTH//2 and self.frames_counter<=60:
                self.frames_counter += 1
                self.rect.centerx = self.rect.centerx - (original_x - WINDOW_WIDTH//2)/20
                self.frames_counter = 0
            if original_y < WINDOW_HEIGHT and self.frames_counter<=60:
                self.frames_counter += 1
                self.rect.bottom = self.rect.bottom - (original_y - WINDOW_HEIGHT+30)/20
                self.frames_counter = 0

            
    def fire(self):
        """Fire a bullet"""
       #Restrict the number of bullets on screen at a time
        if len(self.bullet_group) < self.player_bullet and self.invisible ==False:
            self.shoot_sound.play()
            PlayerBullet(self.rect.centerx, self.rect.top, self.bullet_group) #pass center position of our ship x, top of the ship y, bullet group to the PlayerBullet class           
            
    def animate(self, sprite_list, speed, invisible):
        """Animate the player's actions"""

        if self.current_sprite < len(sprite_list) -1:
            self.current_sprite =1
        
        self.image = sprite_list[int(self.current_sprite)]
        
    def MoveStraight(self, sprite_list, invisible):
        """Animate the player's actions"""

        self.image = move_straight_sprites
    
    def play_sound(self):
        if self.invisible == False:
            self.Thrusters.play() #play the ship sound
            
    def stop_sound(self):
        if self.invisible == True:
            self.Thrusters.stop() #stop the ship sound
            
    def reset(self):
        """Reset the player's position"""
        self.rect.centerx = WINDOW_WIDTH//2 #place the image middle of screen
        self.rect.bottom = WINDOW_HEIGHT-60 #place bottom of screen
        
class Coins(pygame.sprite.Sprite): #This is a child class - inheriting from sprites object in Pygame.
    def __init__(self, x, y):
        """Initialize the coins"""
        super().__init__() #initiliase our super class because it’s a sub class we call super() (inheriting SPRITE CLASS)
        self.x = x
        self.y = y
        self.iterate = 0 #iterable to animate
        self.image = CoinsList[0] 
        self.rect = self.image.get_rect() #rectangle of the image
        self.rect.centerx = self.x   #position the coin x axis
        self.rect.centery = self.y  #position the coin y axis
        self.frames = 0 #iterator for frame count
        self.coin_loss = pygame.mixer.Sound(dir + "\\sounds\\Loss.wav")
        self.coin_loss.set_volume(0.4)

    def update(self):
        """Update the coin"""
        self.animate(CoinsList, 0.10)
        self.frames+=1
        if self.frames == 150: #2.5 seconds
            self.coin_loss.play() #you loser :)
            self.kill() #kill the coin after x time
            self.frames = 0 #reset the iterator            
        
    def animate(self, sprite_list, speed):
        """Animate the asteroid actions"""
        self.iterate+=speed 
        if self.iterate >= len(sprite_list)-1: #call the iterable from the PLAYER CLASS!
            self.iterate = 0
           
        self.image = sprite_list[int(self.iterate)] #cycle through for animating

class PlayerFlame():  
    """A class to model the flame behind the ship """
    def __init__(self, x, y,iter):
        """Initialize the flame"""
        self.x =x
        self.y =y
        Player.itera +=0.25 #call the iterable from the PLAYER CLASS!
        self.render()
        
    def render(self):
         if Player.itera >=6: #call the iterable from the PLAYER CLASS!
             Player.itera = 0
         self.image = pygame.transform.flip(move_straight_flames[int(Player.itera)],False,True)
         self.rect = self.image.get_rect() #rectangle of the image
         self.rect.centerx = self.x - 10  #position the flame x axis
         self.rect.centery = self.y - 10  #position the flame y axis
         display_surface.blit(self.image, (self.rect.centerx, self.rect.centery))

class Asteroid(pygame.sprite.Sprite): #This is a child class - inheriting from sprites object in Pygame.
    """A class to create enemy asteroid objects"""
    def __init__(self,round_number): 
        #print("This is {} variables.".format(round_number))
        
        """Initialize the asteroid"""
        super().__init__() #initiliase our super class because it’s a sub class we call super() (inheriting SPRITE CLASS)
                      
        #Asteroid
        self.current_sprite = 0
        self.image = moving_asteroids[self.current_sprite] #starting image 
        self.rect = self.image.get_rect()
        self.rect.topleft = (random.randint(0, WINDOW_WIDTH), 1) #Randomly place the asteroid
        self.dx = random.choice([-1, 1])
        self.dy = 1 #asteroid always moves down
        self.velocity = random.randint(game_dict[round][0],game_dict[round][1])

        #mask the asteroid
        self.mask = pygame.mask.from_surface(self.image)
        
                
    def update(self):
        """Update the asteroid"""
        self.animate(moving_asteroids, .5) #run the animate function of asteroid class feeding in the asteroid sprite list (moving_asteroids)
        self.move() #run the move asteroid function

        mask_outline = self.mask.outline()
        pygame.draw.lines(self.image, (255, 0, 255), True, mask_outline,width=1)
        
    def move(self):
        """Move the asteroid"""
        #print(self.asteroid_level)
        self.rect.x += self.dx*self.velocity #x coords move by dx multiplied by velocity
        self.rect.y += self.dy*self.velocity #y coords move by dy multiplied by velocity
        #print(self.rect.x)
       
        if self.rect.x > WINDOW_WIDTH or self.rect.x<=0: #if asteroid moves off screen
            self.kill() #kill the asteroid (destroy it from the list)
        
        if self.rect.y >= WINDOW_HEIGHT: #if asteroid moves off screen
            self.kill() #kill the asteroid (destroy it from the list)
    
    def animate(self, sprite_list, speed):
        """Animate the asteroid actions"""
        if self.current_sprite < len(sprite_list) -1:
            self.current_sprite += speed
        else:
            self.current_sprite = 0 #animation has ended and we start sprite list at index 0 again
           
        self.image = sprite_list[int(self.current_sprite)] #which sprite to load
        self.mask = pygame.mask.from_surface(self.image) #mask around asteroid animation
        
class PlayerBullet(pygame.sprite.Sprite):  #This is a child class - inheriting from sprites in Pygame.
    """A class to model a bullet fired by the player"""

    def __init__(self, x, y, bullet_group):
        """Initialize the bullet"""
        super().__init__() #initiliase our super class because it’s a sub class we call super() (inheriting SPRITE CLASS)
        self.image = pygame.transform.rotate(pygame.image.load(dir + "\\Images\\Weapons\\image39.png").convert_alpha(),90) #player shoots a laser
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect() #rectangle of the image
        self.rect.centerx = x  #position the bullet x axis
        self.rect.centery = y  #position the bullet y axis
        
        self.velocity = 7 #the speed of the bullet
        bullet_group.add(self) #add this version of the bullet to the group

    def update(self):
        """Update the bullet"""
        self.rect.y -= self.velocity #move the bullet up minusing the velocity
        
        #If the bullet is off the screen, kill it
        if self.rect.bottom < 0:
            self.kill() #remove the sprite from the sprite group
            
#Set display surface
WINDOW_WIDTH = 1100
WINDOW_HEIGHT = 820
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Asteroids")

#LOAD SOUNDS
# pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=4096)


data = {'Name':['Tom', 'Brad', 'Kyle', 'Jerry'],
        'Score':[19, 20, 21, 22]        }

high_score = pd.DataFrame(data)

#Game Parameters
game_dict = {'L1': [2, 4, 30, 2, 2], #asteroid velocity x,asteroid velocity y, no. asteroids, speed background, no. bullets
             'L2': [2, 5, 20, 4, 2],
             'L3': [3, 5, 20, 6, 3],
             'L4': [3, 5, 10, 8, 4],
             'L5': [3, 6, 10, 10, 6],}


#Set fonts
title_font = pygame.font.Font(dir + "\\Fonts\\Quilts.ttf", 48)
HUD_font = pygame.font.Font(dir + "\\Fonts\\Aloevera.ttf", 20)
Game_Over_Font = pygame.font.Font(dir + "\\Fonts\\Aloevera.ttf", 48)

#LOAD SPRITE LIST
move_straight_sprites = [] #player move straight sprite
move_straight_sprites = pygame.transform.scale(pygame.image.load(dir + "\\Images\\ship\\ship0.png").convert_alpha(), (68, 62)) #player move forward sprite

#Background sprite
BCK = pygame.transform.scale(pygame.image.load(dir + "\\Images\\Background\\bg_space_seamless.png").convert(), (WINDOW_WIDTH,WINDOW_HEIGHT)) #background image

move_right_sprites = [] #player move right sprite
move_right_sprites.append(pygame.transform.scale(pygame.image.load(dir + "\\Images\\ship\\ship0.png").convert_alpha(), (68, 62)))
move_right_sprites.append(pygame.transform.scale(pygame.image.load(dir + "\\Images\\ship\\ship5.png").convert_alpha(), (68, 62)))

move_left_sprites = [] #player move left sprite
for sprite in move_right_sprites:
    move_left_sprites.append(pygame.transform.flip(sprite, True, False)) #flip the right sprite to fill the left sprites list

moving_asteroids =[] #Asteroid Sprite List
for image in os.listdir(dir+'\\Images\\Asteroid\\'):
            moving_asteroids.append(pygame.transform.scale(pygame.image.load(dir +'\\Images\\Asteroid\\' + image).convert_alpha(), (65, 65)))

move_straight_flames = [] #Flame Sprite List
for image in os.listdir(dir+'\\Images\\flames\\'):
            move_straight_flames.append(pygame.transform.scale(pygame.image.load(dir +'\\Images\\flames\\' + image).convert_alpha(), (17, 28)))

CoinsList = [] #coins list
for image in os.listdir(dir+'\\Images\\Coins\\'):
            CoinsList.append(pygame.transform.scale(pygame.image.load(dir +'\\Images\\Coins\\' + image).convert_alpha(), (30, 30)))

#Set FPS and clock
FPS = 60
clock = pygame.time.Clock()

"""SPRITE GROUPS"""
#Create sprite groups
my_player_bullet_group = pygame.sprite.Group()
my_asteroid_group = pygame.sprite.Group()
back_ground = Background()
my_coin_group = pygame.sprite.Group()

#Create a player group and Player object
my_player_group = pygame.sprite.Group()
my_player = Player(my_player_bullet_group) #Create a player to the player Class, we also need to pass the player bullets group
my_player_group.add(my_player) #Add my player object to the group

#Create a Game object
my_game = Game(my_player, my_asteroid_group, my_player_bullet_group,my_coin_group)
#my_game.start_new_round() #run start_new_round method which creates lots of new asteroids
pygame.mixer.music.play(-1, 0.0)

round ='L1' #initial round value required for game parameters 
running = True

while running:
    #Check to see if the user wants to quit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN: #if we press a key
            #Player wants to move forward
            if event.key == pygame.K_UP:
                my_player.play_sound() #run thruster sound
            #Player wants to fire
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    my_player.fire()
                           
    #Blit the background
    back_ground.update()
    back_ground.render()
    
    #Update the player to the screen
    my_player_group.update()
    my_player_group.draw(display_surface)
    
    #Update bullets to the screen
    my_player_bullet_group.update()
    my_player_bullet_group.draw(display_surface)
    
    #Update Coins to the screen
    my_coin_group.update()
    my_coin_group.draw(display_surface)
    
    #Update and draw the game
    round = my_game.update()
    my_game.draw() #draw method for game class
    
    # Update Asteroids to Screen
    my_asteroid_group.update()
    my_asteroid_group.draw(display_surface)
    
    #Update the display and tick clock
    pygame.display.update()
    clock.tick(FPS)
    
#End the game 
pygame.quit()

