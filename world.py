import pygame
import threading
import time
import sys
from components import *

class World:
    def __init__(self, screen, width, tile_size, height, player_img, path):
        # informatio about the screen and the game
        self.tile_size = tile_size
        self.width = width
        self.height = height
        self.screen = screen
        self.player_img = player_img
        self.path = path

        # this is the world map
        self.world_data = [
	'                                                                  ',
	'                                                                  ',
	'              X E  C  X                    C                      ',
	'        X     XXXXXXXXXs                   XX   X                 ',
	'  XXX      XX          X                      E XX                ',
	' XX XX    C                             XXXX XXXXX              G ',
	'          XE    E  X  X        E   X                              ',
	'     C  XXXXXXC XXXXC X  XX XXXXXXXX  XX      C       E        XXX',
	' P   XX  X XX X  X XXXE    CX XX  XX  XXX  XXXXXXXXs  XXXXXX      ',
	'XXXXXXX  X  X X  X  XXXXXXXXX XX  XX  XXX  XX XX XXXXXXX  X       ',
]
        # world information
        self.world_shift = 0
        self.current_x = 0
        self.gravity = 0.7
        self.money = 0
        self.hits_allowed = True
        self.timer = None

        # player information
        self.life = 5
        self.fell = False
        self.reached_goal = False

        # font and setup the world
        self.font = pygame.font.SysFont("impact", 70)
        self.message_color = pygame.Color("darkorange")
        self.setup(self.world_data)
    
    def timer_function(self):
        self.hits_allowed = True

    
    # generate the world
    def setup(self, layout):
        # group each sprite based on its type
        self.tiles = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.coins = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()
        self.goal = pygame.sprite.GroupSingle()

        for r in range(len(layout)):
            row = layout[r]
            for c in range(len(row)):
                x = c * self.tile_size
                y = r * self.tile_size
                cell = row[c]

                # tile
                if cell == "X":
                    tile = Tile((x,y), self.tile_size, self.path)
                    self.tiles.add(tile)
                
                # player
                elif cell == "P":
                    player = Player((x,y), self.tile_size, self.player_img)
                    self.starting_location = (x,y)
                    self.player.add(player)

                # enemy
                elif cell == "E":
                    enemy = Enemy((x,y), self.tile_size, self.path)
                    self.enemies.add(enemy)
                
                # goal
                elif cell == "G":
                    goal = Goal((x,y), self.tile_size, self.path)
                    self.goal.add(goal)
                
                # coin
                elif cell == "C":
                    coin = Coin((x,y), self.tile_size, self.path)
                    self.coins.add(coin)
    
    # shift the world when the player goes to the right or left
    def shift(self):
        player = self.player.sprite
        player_x = player.rect.centerx
        direction_x = player.direction.x

        # shift to right if player goes to left
        if player_x < self.width // 3 and direction_x < 0:
            self.world_shift = 6
            player.speed = 0
        
        # shift to left if player goes to right
        elif player_x > self.width - (self.width//3) and direction_x > 0:
            self.world_shift = -6
            player.speed = 0
        else:
            self.world_shift = 0
            player.speed = 6
    
    # apply gravity on player whne jumping
    def apply_gravity(self):
        player = self.player.sprite
        player.direction.y += self.gravity
        player.rect.y += player.direction.y

        # check if the player fell from the map
        if player.rect.y >= self.height + self.tile_size:
            self.fell = True
        
    
    # check for collisions when player moves horizontally
    def horizontal_movement_collision(self):
        player = self.player.sprite
        player.rect.x += player.direction.x * player.speed

        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                # player moved to the left and collided with tile
                if player.direction.x < 0:
                    player.rect.left = sprite.rect.right
                
                # player moved to the right and collided with tile
                elif player.direction.x > 0:
                    player.rect.right = sprite.rect.left
    
    # enemmies keep moving left and right till they reach a tile, then change direction
    def move_enemy(self):
        # do for all enemies
        for e in self.enemies:
            e.rect.x += e.direction * e.speed

            # do for all tiles
            for sprite in self.tiles.sprites():
                if sprite.rect.colliderect(e.rect):
                    # change from left to right
                    if e.direction < 0:
                        e.rect.left = sprite.rect.right
                        e.direction = 1

                    # change from right to left
                    elif e.direction > 0:
                        e.rect.right = sprite.rect.left
                        e.direction = -1
    
    # player moving vertically
    def vertical(self):
        player = self.player.sprite
        self.apply_gravity()

        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                # player goes down till hits the ground
                if player.direction.y > 0:
                    player.rect.bottom = sprite.rect.top
                    player.direction.y = 0
                    player.on_ground = True
                    player.jumping = False

                # player jumps till jump done or collided
                elif player.direction.y < 0:
                    player.rect.top = sprite.rect.bottom
                    player.direction.y = 0
    
    # handles the enemy  hits
    def handle_enemies(self):
        player = self.player.sprite
        for enemy in self.enemies:
            if self.hits_allowed and enemy.rect.colliderect(player.rect):
                # 1 second interval between each hit
                if self.timer:
                    self.timer.cancel()
                self.timer = threading.Timer(1, self.timer_function)
                self.hits_allowed = False
                self.life -= 1
                self.timer.start()
    
    # handle collecting coins
    def handle_coins(self):
        player = self.player.sprite
        for coin in self.coins:
            if player.rect.colliderect(coin.rect):
                # coins disappear when collected
                coin.kill()
                self.money += 1
    
    # handle reaching goal
    def handle_goal(self):
        player = self.player.sprite
        door = self.goal.sprite
        if player.rect.colliderect(door.rect):
            self.reached_goal = True
    
    # checks if game is done
    # if wins adds to the coins
    # if loses, makes coins = 0
    def game_state(self):
        # player dies
        if self.life == 0 or self.fell:
            self.money = 0
            self.show_message("You Lose :(")
            return (True, "lose")
        
        # player reached goal and wins
        elif self.reached_goal == True:
            self.show_message("You win!!!")
            return (True, "win", self.money)
        
        return (False,-1)

    # shows how many lives left on the top left corner
    def show_life(self):
        life_size = 30
        img_loc = self.path + "\pictures\heart.png"
        path = r'{}'.format(img_loc)
        heart = pygame.image.load(path).convert_alpha()
        heart = pygame.transform.scale(heart, (life_size, life_size))
        indent = 0
        for i in range(self.life):
            indent += life_size
            self.screen.blit(heart, (indent, life_size))
    
    # shows how many coins collected
    def show_money(self):
        money_size = 30
        img_loc = self.path + "\pictures\coin.png"
        path = r'{}'.format(img_loc)
        coin = pygame.image.load(path).convert_alpha()
        coin = pygame.transform.scale(coin, (money_size, money_size))
        indent = 0
        for i in range(self.money):
            indent += money_size
            self.screen.blit(coin, (indent, 2*money_size))

    # shows if win or lose
    def show_message(self, msg):
        message = self.font.render(msg, True, self.message_color)
        self.screen.blit(message, (self.width//3, self.height//10 + 20))

    # updates in each frame
    def update(self, keys):
        # updates tiles
        self.tiles.update(self.world_shift)
        self.tiles.draw(self.screen)

        # updates enemies
        self.enemies.update(self.world_shift)
        self.move_enemy()
        self.enemies.draw(self.screen)

        # shift world
        self.shift()

        # update player
        self.horizontal_movement_collision()
        self.vertical()
        self.handle_enemies()
        self.handle_coins()
        self.handle_goal()
        self.player.update(keys)
        
        # updates coins
        self.coins.update(self.world_shift)
        self.coins.draw(self.screen)

        # update goal
        self.goal.update(self.world_shift)
        self.goal.draw(self.screen)

        # shows lives and coins
        self.show_life()
        self.show_money()
        self.player.draw(self.screen)

