import pygame
from components import Tile, Player

class World:
    def __init__(self, screen, width, tile_size):
        self.tile_size = tile_size
        self.width = width
        self.screen = screen

        self.world_data = [
	'                                                                  ',
	'                                                                  ',
	'                E  E                       C                      ',
	'        X     XXXXXXXXXs                   XX   X                 ',
	' EXXXE     XX         XX                XXXX EE XX                ',
	' XX XX    C                                  XXXXX                ',
	'          XE    E           E  E   X                            G ',
	'     C  XXXXXX  XXXXE    XXXXXXXXXXX  XX      C       EE E     XXX',
	' P   XX  X XX X  X XXXE     X XX  XX  XXX  XXXXXXXXs  XXXXXX      ',
	'XXXXXXX  X  X X  X  XXXXXXXXX XX  XX  XXX  XX XX XXXXXXX  X       ',
]
        self.world_shift = 0
        self.current_x = 0
        self.gravity = 0.7
        self.game = None

        self.setup(self.world_data)

    
    # generate the world
    def setup(self, layout):
        self.tiles = pygame.sprite.Group()
        self.traps = pygame.sprite.Group()
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
                    tile = Tile((x,y), self.tile_size)
                    self.tiles.add(tile)
                
                # player
                elif cell == "P":
                    player = Player((x,y), self.tile_size)
                    self.player.add(player)

                # # enemy/trap
                # elif cell == "E":
                #     enemy = Enemy((x,y))
                
                # # goal
                # elif cell == "G":
                
                # # coin
                # elif cell == "C":
    
    def apply_gravity(self):
        player = self.player.sprite
        player.direction.y += self.gravity
        player.rect.y += player.direction.y
    
    def horizontal_movement_collision(self):
        player = self.player.sprite
        player.rect.x += player.direction.x * player.speed

        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.x < 0:
                    player.rect.left = sprite.rect.right
                    # player.on_left = True
                    # self.current_x = player.rec

                
                elif player.direction.x > 0:
                    player.rect.right = sprite.rect.left
    
    def vertical(self):
        player = self.player.sprite
        self.apply_gravity()

        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.y > 0:
                    player.rect.bottom = sprite.rect.top
                    player.direction.y = 0
                    player.on_ground = True

                elif player.direction.y < 0:
                    player.rect.top = sprite.rect.bottom
                    player.direction.y = 0
        
    def update(self, keys):
        self.tiles.update(0)
        self.tiles.draw(self.screen)

        # for player
        self.horizontal_movement_collision()
        self.vertical()
        self.player.update(keys)
        self.player.draw(self.screen)
