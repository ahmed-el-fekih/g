import pygame

class Tile(pygame.sprite.Sprite):
    # pos is position of the tile, size is the size of the tile
    def __init__(self, pos, size, path) -> None:
        # initialize sprite
        super().__init__()

        # get location from path
        img_path = path + r"\pictures\tile.png"
        img_path  = r"{}".format(img_path)

        # load and scale image
        self.image = pygame.image.load(img_path)
        self.image = pygame.transform.scale(self.image, (size, size))
        self.rect = self.image.get_rect(topleft=pos)
    
    # method to be used when the world is scrolled
    def update(self, x_shift):
        self.rect.x += x_shift


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, size, img_path):
        super().__init__()
        # convert alpha is for improving game performance
        self.image = pygame.image.load(img_path).convert_alpha()
        self.image = pygame.transform.scale(self.image,(size,size))
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(topleft = pos)

        # player movement
        self.direction = pygame.math.Vector2(0,0) # this is an x, y list that represents the player movment
        self.speed = 6
        self.jump_move = -13 # how much the character jumps
        self.jumping = False

        # player status
        self.life = 5
        self.game_over = False
        self.win = False
        self.status = "idle"
        self.on_ground = False
        self.on_ceiling = False
        self.on_left = False
        self.on_right = False

    # changes direction based on pressed keys
    def update_helper(self, keys):
        # checks horizontal movement
        if keys[pygame.K_LEFT]:
            self.direction.x = -1
        
        elif keys[pygame.K_RIGHT]:
            self.direction.x = 1
        
        else:
            self.direction.x = 0
        
        # checks vertical movement
        if keys[pygame.K_SPACE] and not self.jumping:
            self.direction.y = self.jump_move
            self.jumping = True
    
    # update the direction
    def update(self, keys):
        if self.life > 0 and not self.game_over:
            self.update_helper(keys)
        
        elif self.game_over and self.win:
            self.direction.x = 0
        
        else:
            self.direction.x = 0

class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos, size, path):
        super().__init__()

        # get location from path
        img_path = path + "\pictures\evil.png"
        img_path  = r"{}".format(img_path)

        # convert alpha is for improving game performance
        self.image = pygame.image.load(img_path).convert_alpha()
        self.image = pygame.transform.scale(self.image,(size,size))
        self.rect = self.image.get_rect(topleft = pos)
        self.speed = 3

        # direction that the enemy moves in, starts with positive
        self.direction = 1
    
    # update enemies when world shifts
    def update(self, shift):
        self.rect.x += shift

class Coin(pygame.sprite.Sprite):
    def __init__(self, pos, size, path) -> None:
        # initialize sprite
        super().__init__()

        # get location from path
        img_path = path + "\pictures\coin.png"
        img_path  = r"{}".format(img_path)

        # load and scale image
        self.image = pygame.image.load(img_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (size, size-10))
        self.rect = self.image.get_rect(topleft=pos)
    
    # method to be used when the world is scrolled
    def update(self, x_shift):
        self.rect.x += x_shift

class Goal(pygame.sprite.Sprite):
    def __init__(self, pos, size, path) -> None:
        # initialize sprite
        super().__init__()

        # get location from path
        img_path = path + "\pictures\door.png"
        img_path  = r"{}".format(img_path)

        # load and scale image
        self.image = pygame.image.load(img_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (size, size*2))
        self.rect = self.image.get_rect(topleft=pos)
    
    def update(self, x_shift):
        self.rect.x += x_shift